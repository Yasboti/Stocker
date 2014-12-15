import csv
from datetime import date, timedelta
from matplotlib.finance import quotes_historical_yahoo_ochl

# retrieve symbol lists
markets = ['amex','nasdaq','nyse','otcbb']
symbols = []
for m in markets:
    fname = 'symbols-' + m + '-unique.txt'
    with open(fname, 'r') as f:
        symbols += f.read().splitlines()

print len(symbols), 'symbols listed'

exit
# set date range
date1 = date(1984, 1, 1)
date2 = date(2014, 12, 31)
# date2 = date.today()
# date1 = date2 - timedelta(days=14)

# retrieve all data
for symbol in symbols:
    try:
        data = quotes_historical_yahoo_ochl(symbol, date1, date2)
        if None != data and len(data) > 0:
            print symbol, len(data)
            with open('csv/' + symbol + '.csv', 'w') as f:
                writer = csv.writer(f)
                writer.writerows(data)
    except:
        True
