import draw
import obtain
import sys

# cmdline, eg
# python intraday.py tsla 300 10
if len(sys.argv) == 4:
    symbol = sys.argv[1]
    print symbol
    seconds = float(sys.argv[2])
    days = float(sys.argv[3])
    data = obtain.getIntradayCsv(symbol, seconds, days)
    print 'data acquired'
    cooked = obtain.prepareData(data)
    print 'data adjusted'
    fname = '%s-%ss-%sd' % (symbol, int(seconds), int(days))
    draw.drawBarImage(fname,cooked)
    # draw.drawDotImage(fname,cooked)
    print 'image rendered'