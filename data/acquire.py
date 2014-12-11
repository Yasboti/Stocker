import csv
import datetime 
from matplotlib.finance import quotes_historical_yahoo_ochl

# retrieve symbol list
with open('other-symbols.txt', 'r') as f:
    symbols = f.read().splitlines()

# set date range
date1 = datetime.date(2000, 1, 1)
date2 = datetime.date(2014, 12, 31)


# retrieve all data
for symbol in symbols:
    try:
        data = quotes_historical_yahoo_ochl(symbol, date1, date2)
        if None != data and len(data) > 30:
            print symbol, len(data)
            with open(symbol + '.csv', 'w') as f:
                writer = csv.writer(f)
                writer.writerows(data)
    except:
        True