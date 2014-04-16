import csv
import datetime
import requests


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
