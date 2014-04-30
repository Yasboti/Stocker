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

def importAll(rc):
   symbols = rc.smembers('symbols')
   print len(symbols), 'known symbols'
   while(len(symbols) > 0):
      s = symbols.pop()
      print s,
      munge(s, rc)
      print '%s rows added' % rc.zcard(s)


# store last 15 days of intraday data for symbol
def updateIntraday(symbol):
   rc = redis.StrictRedis(host='localhost', port=6379, db=0)
   print symbol
   data = obtain.getIntradayCsv(symbol, 15)
   print len(data), 'rows obtained'
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
      key = '%s.intraday.%s' % (symbol, c)
      print 'storing', key
      print len(ts), len(columns[c])
      for i, timestamp in enumerate(ts):
         val = columns[c][i]
         val = int(val) if 'volume' == c else float(val)
         rc.zadd(key, int(timestamp), val)
