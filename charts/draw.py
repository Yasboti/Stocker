import csv
import datetime
import math
import requests


# retrieve data from google
def getCsv(symbol, seconds, days):
    url = 'http://www.google.com/finance/getprices'
    query = '?q=%s&i=%s&p=%sd&f=d,o,h,l,c,v' % (symbol.upper(), seconds, days)
    r = requests.get(url+query)
    print len(r.text)
    reader = csv.reader(r.text.splitlines(),dialect=csv.excel)
    # collect data
    result = []
    header = 0
    for line in reader:
        if header < 7:
            header += 1
        else:
            print line
            if line and 'a' == line[0][0]: # new day timestamp
                dts = float(line[0][1:])
                offset = 0
            else: # within the same day
                offset = float(line[0])
            ts = datetime.datetime.fromtimestamp(dts+(seconds*offset))
            result.append([ts, float(line[1]), float(line[5])]) # only timestamp / close / volume
    return result


# adjust values for display
def prepareData(table):
    pMax = 0
    pMin = float(sys.maxint)
    vMax = 0
    # collect aggregates
    for row in table:
        if vMax < row[2]:
            vMax = row[2]
        if pMax < row[1]:
            pMax = row[1]
        if pMin > row[1]:
            pMin = row[1]
    # scale values
    offset = pMin / (pMax - pMin)
    result = []
    for row in table:
        result.append([row[0], (row[1] - pMin) / (pMax - pMin), math.log(row[2]) / math.log(vMax)])
    return result