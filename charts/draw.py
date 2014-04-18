import csv
import datetime
import math
import requests
import sys

from PIL import Image, ImageDraw


# get end of day historical data from yahoo
def getDailyCsv(symbol):
    url = 'http://ichart.finance.yahoo.com/table.csv'
    query = '?s=%s&a=00&b=1&c=2013&d=03&e=18&f=2014&g=d&ignore=.csv' % symbol
    r = requests.get(url+query)
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
    return result

# retrieve data from google
# adjust timestamps so that each row has an absolute one
def getIntradayCsv(symbol, seconds, days):
    url = 'http://www.google.com/finance/getprices'
    query = '?q=%s&i=%s&p=%sd&f=d,c,h,l,o,v' % (symbol.upper(), seconds, days)
    r = requests.get(url+query)
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
            # ts = datetime.datetime.fromtimestamp(dts+(seconds*offset))
            ts = dts + (seconds*offset)
            # [ts, c, h, l, o, v]
            result.append([ts, float(line[1]), float(line[2]), float(line[3]), float(line[4]), float(line[5])])
    return result


# adjust values for display
def prepareData(table):
    pMax = 0
    pMin = float(sys.maxint)
    vMax = 0
    # collect aggregates
    for row in table:
        if vMax < row[5]:
            vMax = row[5]
        if pMax < row[1]:
            pMax = row[1]
        if pMin > row[1]:
            pMin = row[1]
    # scale values
    offset = pMin / (pMax - pMin)
    print pMin,pMax,vMax
    result = []
    for row in table:
        # uhh need a better scaling function...
        result.append([
            row[0],                                     # ts
            (row[1] - pMin) / (pMax - pMin),            # close
            (row[2] - pMin) / (pMax - pMin),            # high
            (row[3] - pMin) / (pMax - pMin),            # low
            (row[4] - pMin) / (pMax - pMin),            # open
            # row[5] / vMax # raw volume
            math.pow(row[5],0.75) / math.pow(vMax,0.75) # adjusted volume
            # math.pow(row[5],2) / math.pow(vMax,2) # adjusted volume
        ])
    return result[::-1]
    # return result


# render data to image
# (drawn in sequence regardless of timestamp)
def drawImage(fname, data):
    bar = 3 # width of each data row as drawn
    width = len(data) * bar
    height = int(width/3)
    im = Image.new('RGBA', (width, height), (255, 255, 255, 255)) 
    # im = Image.new('RGBA', (width, height), (0, 0, 0, 255)) 
    draw = ImageDraw.Draw(im)
    lY = 0
    while lY < height:
        draw.line((0, lY, width, lY), fill=(235,245,235))    
        # draw.line((0, lY, width, lY), fill=(15,5,15))
        lY += 35
    idx = 0
    ht = height - 20
    day = 0
    pc = 0
    for row in data:
        x = int(idx * bar)
        c = int(ht * row[1]) + 10
        h = int(ht * row[2]) + 10
        l = int(ht * row[3]) + 10
        o = int(ht * row[4]) + 10
        v = int(240 * (1-row[5]))
        # v = int(235 * row[5]) + 20

        # if row[0] - day > 10000:
        #     draw.line((x,0,x,height), fill=(210,210,210))
            # draw.line((x,0,x,height), fill=(25,15,25))
        day = row[0]

        # drawBar(draw, x, o, c, v, bar)
        drawOHLC(draw, x, o, h, l, c, v, bar)
        # drawDot(draw, x, c, v, bar)
        # drawLine(draw, (idx-1)*bar, pc, x, c, v)
        idx += 1
        pc = c
    im = im.transpose(Image.FLIP_TOP_BOTTOM)
    im.save('output/%s.png' % fname, 'PNG')
    return im

def drawOHLC(d,x,o,h,l,c,v,step):
    d.line((x-1, o, x-1, o), fill=(v,v,v))
    d.line((x+1, c, x+1, c), fill=(v,v,v))
    d.line((x, h, x, l), fill=(v,v,v))

def drawBar(d,x,h,l,v,step):
    d.line((x+1, c, x+1, c), fill=(v,v,v))
    d.line((x, h, x, l), fill=(v,v,v))

def drawDot(d, x, y, v, step):
    d.line((x, y-1, x+step-1, y-1), fill=(v,v,v))
    d.line((x, y, x+step-1, y), fill=(v,v,v))
    # d.line((x, y+1, x+step-1, y+1), fill=(v,v,v))

def drawLine(d, px, py, x, y, c):
    d.line((px, py, x, y), fill=(c,c,c))


# cmdline, eg
# python draw.py tsla 300 10
if len(sys.argv) == 4:
    symbol = sys.argv[1]
    print symbol
    seconds = float(sys.argv[2])
    days = float(sys.argv[3])
    data = getDailyCsv(symbol)
    # data = getIntradayCsv(symbol, seconds, days)
    print 'data acquired'
    cooked = prepareData(data)
    print 'data adjusted'
    fname = '%s-daily' % (symbol)
    # fname = '%s-%ss-%sd' % (symbol, int(seconds), int(days))
    drawImage(fname,cooked)
    print 'image rendered'