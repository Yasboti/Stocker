import csv
from datetime import date, timedelta
from matplotlib.finance import quotes_historical_yahoo_ochl

# retrieve symbol list
with open('other-symbols.txt', 'r') as f:
    symbols = f.read().splitlines()
with open('other-symbols.txt', 'r') as f:
    symbols += f.read().splitlines()

print len(symbols), 'symbols listed'

# set date range
# date1 = date(2000, 1, 1)
# date2 = date(2014, 12, 31)
date2 = date.today()
date1 = date2 - timedelta(days=5)

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