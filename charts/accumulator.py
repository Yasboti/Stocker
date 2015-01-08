import csv
import os
import redis
import time
import obtain

'''
Consumes eod csv files and imports them into redis sorted sets

redis key schema: one sset per stock, score is epoch timestamp

   symbol:timestamp

associated value is in the form of dohlcv list: eg:

   2013-02-01,31.50,31.74,30.47,31.01,66789100

since set elements have to be unique, we must guarantee there
are no duplicates -> including the timestamp guarantees it

'''

# accepts symbol string and redis connection
# expects input files in 'inpupt/' subdir
def munge(symbol, rc):
   symbol = symbol.upper()
   fname = 'input/%s-2004-2014.csv' % symbol
   print fname
   with open(fname, 'r') as fh:
      reader = csv.reader(fh)
      reader.next() # skip headers
      for row in reader:
         if(len(row) < 7): #break on empty rows (eof)
            break
         # convert string date to epoch (scores are numeric)
         ts = int(time.mktime(time.strptime(row[0],'%Y-%m-%d')))
         data = ', '.join([str(x) for x in row]) # make string
         rc.zadd(symbol, ts, data) # add to main sset


# gets a list of all symbols associated with source csv files
# expects the 'input' subdir of current dir to exist
def storeAllSymbols(rc):
   fnames = os.listdir('input')
   symbols = [f.split('-')[0] for f in fnames]
   print len(symbols), 'symbols found'
   rc.sadd('symbols', *symbols)

# create a list from symbols.txt
def storeSymbols():
   rc = redis.StrictRedis(host='localhost', port=6379, db=0)
   symbols = []
   with open('symbols.txt') as f:
      symbols = f.read().splitlines()
      print len(symbols), 'symbols found'
   for s in reversed(symbols):
      rc.lpush('symbols', s)
   print 'done'

def importAll(rc):
   symbols = rc.smembers('symbols')
   print len(symbols), 'known symbols'
   while(len(symbols) > 0):
      s = symbols.pop()
      print s,
      munge(s, rc)
      print '%s rows added' % rc.zcard(s)


# store last N days of intraday data for symbol
# (does not overwrite existing data eg zero volumes)
def updateIntraday(rc, symbol, days):
   data = obtain.getIntradayCsv(symbol, days)
   print '%s: %s rows obtained' % (symbol, len(data))
   if 0 == len(data): return 0
   ts, o, h, l, c, v = zip(*data)
   columns = {
      'open': o,
      'high': h,
      'low': l,
      'close': c,
      'volume': v
   }
   # store each column as a separate ordered (by ts) set
   for c in columns.keys():
      p = rc.pipeline()
      key = '%s.intraday.%s' % (symbol, c)
      for i, timestamp in enumerate(ts):
         val = columns[c][i]
         val = int(val) if 'volume' == c else float(val)
         p.zadd(key, val, int(timestamp))
      p.execute()
   return len(data)

# update intraday data for all known symbols
def getAllIntraday(days):
   rc = redis.StrictRedis(host='localhost', port=6379, db=0)
   name = rc.get('updateList')
   if 'symbols' == name:
      name = 'symbols.update'
      rc.sort('symbols', store = name, alpha = True)
      rc.set('updateList', name)
   while rc.llen(name) > 0:
      # no data? most likely bad symbol, remove it
      symbol = rc.lpop(name)
      updateIntraday(rc, symbol, days)
      time.sleep(2) # delay to prevent captcha ban
      # NOTE this is not a reliable way of doing that
      # remove symbol if no data in at least two trading days
      # if days > 1 and 0 == updateIntraday(rc, symbol, days):
      #    print 'removing', symbol, ' - no data was returned'
      #    rc.lrem('symbols', 1, symbol)
   rc.set('updateList', 'symbols')

