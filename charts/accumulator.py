import csv
import os
import redis
import time

'''
Consumes eod csv files and imports them into redis sorted sets

redis key schema: one sset per stock, score is epoch timestamp

   symbol:timestamp

associated value is in the form of dohlcv list: eg:

   2013-02-01,31.50,31.74,30.47,31.01,66789100,30.75

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