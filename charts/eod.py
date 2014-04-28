import draw
import obtain
import sys

# cmdline, eg
# python eod.py tsla 20140301 20140401
if len(sys.argv) == 4:
    symbol = sys.argv[1]
    print symbol
    start = sys.argv[2]
    end = sys.argv[3]
    data = obtain.getCsv(symbol, start, end)
    print len(data)
    fname = '%s-%s-%s' % (symbol, start, end)
    draw.drawBarImage(fname,data)
    # draw.drawDotImage(fname,cooked)
