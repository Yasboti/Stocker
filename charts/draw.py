from PIL import Image, ImageDraw

# render data to image
# (drawn in sequence regardless of timestamp)
def drawBarImage(fname, data):
    bar = 3 # width of each data row as drawn
    width = len(data) * bar
    height = int(width/3)
    im = Image.new('RGBA', (width, height), (255, 255, 255, 255)) 
    draw = ImageDraw.Draw(im)
    lY = 0
    while lY < height:
        draw.line((0, lY, width, lY), fill=(235,245,235))    
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

        # if row[0] - day > 10000:
        #     draw.line((x,0,x,height), fill=(210,210,210))
        day = row[0]

        # drawBar(draw, x, o, c, v, bar)
        drawOHLC(draw, x, o, h, l, c, v, bar)
        idx += 1
        pc = c
    im = im.transpose(Image.FLIP_TOP_BOTTOM)
    im.save('output/%s.png' % fname, 'PNG')
    return im


# render data to image
# (drawn in sequence regardless of timestamp)
def drawDotImage(fname, data):
    bar = 3 # width of each data row as drawn
    width = len(data) * bar
    height = int(width/3)
    im = Image.new('RGBA', (width, height), (0, 0, 0, 255)) 
    draw = ImageDraw.Draw(im)
    lY = 0
    while lY < height:
        draw.line((0, lY, width, lY), fill=(15,5,15))
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
        v = int(235 * row[5]) + 20

        # if row[0] - day > 10000:
        #     draw.line((x,0,x,height), fill=(25,15,25))
        day = row[0]

        drawDot(draw, x, c, v, bar)
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
    d.line((x, y+1, x+step-1, y+1), fill=(v,v,v))
    # d.line((x, y+1, x+step-1, y+1), fill=(v,v,v))

def drawLine(d, px, py, x, y, c):
    d.line((px, py, x, y), fill=(c,c,c))
