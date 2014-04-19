import csv
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
   with open(fname, 'r') as fh:
      reader = csv.reader(fh)
      reader.next() # skip headers
      for row in reader:
         # convert string date to epoch (scores are numeric)
         ts = int(time.mktime(time.strptime(row[0],'%Y-%m-%d')))
         data = ', '.join([str(x) for x in row]) # make string
         rc.zadd(symbol, ts, data)