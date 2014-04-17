import csv
import datetime
import math
import requests
import sys

from PIL import Image, ImageDraw


# retrieve data from google
# adjust timestamps so that each row has an absolute one
def getCsv(symbol, seconds, days):
    url = 'http://www.google.com/finance/getprices'
    query = '?q=%s&i=%s&p=%sd&f=d,o,h,l,c,v' % (symbol.upper(), seconds, days)
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
        # uhh need a better scaling function...
        # result.append([row[0], (row[1] - pMin) / (pMax - pMin), row[2] / vMax])
        # result.append([row[0], (row[1] - pMin) / (pMax - pMin), math.log(row[2]) / math.log(vMax)])
        # result.append([row[0], (row[1] - pMin) / (pMax - pMin), math.sqrt(row[2]) / math.sqrt(vMax)])
        result.append([row[0], (row[1] - pMin) / (pMax - pMin), math.pow(row[2],0.75) / math.pow(vMax,0.75)])
    return result


# render data to image
# (drawn in sequence regardless of timestamp)
def drawImage(fname, data):
    bar = 2 # width of each data row as drawn
    width = len(data) * bar
    height = int(width/3)
    im = Image.new('RGBA', (width, height), (0, 0, 0, 255)) 
    draw = ImageDraw.Draw(im)
    lY = 0
    while lY < height:
        draw.line((0, lY, width, lY), fill=(0,10,5))    
        lY += 35
    idx = 0
    for row in data:
        x = int(idx * bar)
        y = int(height * row[1])
        c = int(255 * row[2])
        drawBar(draw, x, y, c, bar)
        idx += 1
    im.save('output/%s.png' % fname, 'PNG')
    return im

def drawBar(d, x, y, c, step):
    # d.line((x, y-1, x+step-1, y-1), fill=(c,c,c))
    d.line((x, y, x+step-1, y), fill=(c,c,c))
    # d.line((x, y+1, x+step-1, y+1), fill=(c,c,c))

def drawLine(d, px, py, x, y, c):
    d.line((px, py, x, y), fill=(c,c,c))


# cmdline
if len(sys.argv) == 4:
    symbol = sys.argv[1]
    seconds = float(sys.argv[2])
    days = float(sys.argv[3])
    data = getCsv(symbol, seconds, days)
    print 'data acquired'
    cooked = prepareData(data)
    fname = '%s-%ssec-%sdays' % (symbol, int(seconds), int(days))
    drawImage(fname,cooked)
    print 'image rendered'