import os
import datetime
import csv

# get all .csv files in current dir
dataFiles = []
for root, dirs, files in os.walk('.'):
    for fname in files:
         if fname.endswith('.csv'):
            dataFiles.append(fname)

for fname in dataFiles:
   with open(fname, 'r') as f:
      reader = csv.reader(f)
      data =  list(reader)
      print data[0]
      exit()
      print fname, len(data)