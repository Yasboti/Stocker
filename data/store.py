import os
import datetime
import csv
import sqlite3

# get all .csv files in current dir
dataFiles = []
for root, dirs, files in os.walk('csv'):
   print len(files), 'data files found'
   for fname in files:
      if fname.endswith('.csv'):
         dataFiles.append('csv/'+fname)

connection = sqlite3.connect('historical.sl')
c = connection.cursor()

for fname in dataFiles:
   with open(fname, 'r') as f:
      reader = csv.reader(f)
      symbol = fname[:-4][4:]
      data =  [[symbol] + row for row in list(reader)]
      r = c.executemany('INSERT OR IGNORE INTO eod VALUES (?, ?, ?, ?, ?, ?, ?)', data)
      connection.commit()
