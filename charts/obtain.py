import csv
import math
import requests
import sys

# save to local csv
def saveLocal(symbol, suffix, data):
    fh = open("input/%s-%s.csv" % (symbol, suffix), 'w')
    fh.write(data)
    fh.close()

def getCsv(symbol, start, end):
    symbol = symbol.upper()
    url = "http://localhost:8080/data.yaws?symbol=%s&start=%s&end=%s" % (symbol, start, end)
    r = requests.get(url)
    reader = csv.reader(r.text.splitlines(),dialect=csv.excel)
    result = []
    for line in reader:
        if len(line) == 0:
            break
        result.append([
            line[0],
            float(line[4]), # open and close are switched to match google
            float(line[2]),
            float(line[3]),
            float(line[1]),
            float(line[5])
        ])
    return result

# get end of day historical data from yahoo
def getDailyCsv(symbol):
    url = 'http://ichart.finance.yahoo.com/table.csv'
    # query = '?s=%s&a=01&b=1&c=2003&d=03&e=18&f=2014&g=d&ignore=.csv' % symbol
    query = '?s=%s&a=03&b=1&c=2013&d=03&e=18&f=2014&g=d&ignore=.csv' % symbol
    r = requests.get(url+query)
    saveLocal(symbol, 'eod', r.text)
    result = []
    reader = csv.reader(r.text.splitlines(),dialect=csv.excel)
    header = True
    for line in reader:
        if header:
            header = False
        else:
            result.append([
                line[0],
                float(line[4]), # open and close are switched to match google
                float(line[2]),
                float(line[3]),
                float(line[1]),
                float(line[5])
            ])
    return result[::-1]

# retrieve data from google
# adjust timestamps so that each row has an absolute one
def getIntradayCsv(symbol, days):
    seconds = 60
    url = 'http://www.google.com/finance/getprices'
    query = '?q=%s&i=%s&p=%sd&f=d,c,h,l,o,v' % (symbol.upper(), int(seconds), int(days))
    r = requests.get(url+query)
    saveLocal(symbol, 'intraday', r.text)
    reader = csv.reader(r.text.splitlines(),dialect=csv.excel)
    # collect data
    result = []
    header = 0
    for line in reader:
        if header < 7:
            header += 1
        else:
            if line and 'a' == line[0][0]: # new day timestamp
                dts = float(line[0][1:])
                offset = 0
            else: # within the same day
                offset = float(line[0])
            ts = dts + (seconds*offset)
            # [ts, c, h, l, o, v]
            result.append([ts, float(line[4]), float(line[2]), float(line[3]), float(line[1]), float(line[5])])
    return result


# cmdline
# python draw.py tsla 10
if len(sys.argv) == 3:
    symbol = sys.argv[1]
    print symbol
    days = float(sys.argv[2])
    data = getIntradayCsv(symbol, days)
    print len(data)
    print data[0]
    print data[-1]