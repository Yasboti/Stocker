# import all the things
from datetime import date, timedelta
import numpy as np
from numpy import *
from scipy.signal import argrelextrema
from matplotlib import gridspec
import datetime
import sqlite3
import pandas as pd


# produces a DataFrame with daily counts of max/min extrema
def accumulateFrame(symbols, order, mindate, maxdate):
    connection = sqlite3.connect('../data/historical.sl')
    c = connection.cursor()
    df = pd.DataFrame(columns=['ts','min','max']).set_index('ts')
    for symbol in symbols:
        query = "SELECT ts,close,high,low FROM eod WHERE symbol = '" + symbol + "' AND ts BETWEEN " + str(mindate) + " AND " + str(maxdate) + " ORDER BY ts;"
        c.execute(query)
        data = c.fetchall()
        dates = array([datetime.datetime.fromordinal(q[0]) for q in data])
        closes = array([q[1] for q in data])
        highs = array([q[2] for q in data])
        lows = array([q[3] for q in data])
        # compute extrema
        if len(lows) > 0:
            cmin = argrelextrema(data=lows, comparator=np.less, order=order)
            # create frame for minima indexed by date
            if(len(cmin[0]) > 0):
                mins = np.vstack((dates[cmin], np.negative(np.ones(cmin[0].size)), np.zeros(cmin[0].size))).transpose()
                df1 = pd.DataFrame(mins, columns=['ts','min','max']).set_index('ts')
                df = df.add(df1, fill_value=0)
        if len(highs) > 0:
            cmax = argrelextrema(data=highs, comparator=np.greater, order=order)
            # create frame for maxima indexed by date
            if(len(cmax[0]) > 0):
                maxes = np.vstack((dates[cmax], np.zeros(cmax[0].size), np.ones(cmax[0].size))).transpose()
                df2 = pd.DataFrame(maxes, columns=['ts','min','max']).set_index('ts')
                df = df.add(df2, fill_value=0)
    return df

def figure(stub, df, size):
    plot = df.plot(kind='line', figsize=size, legend=False)
    plot.set_autoscaley_on(False)
    plot.set_ylim([-1000,1000])
    fig = plot.get_figure()
    fig.savefig("../media/" + stub + ".png")




# retrieve symbol list
symbols = []
markets = ['amex','nasdaq','nyse','otcbb']
single = 'otcbb'
markets = [single]
for m in markets:
    fname = '../data/symbols-' + m + '-unique.txt'
    with open(fname, 'r') as f:
        symbols += f.read().splitlines()   

mindate = datetime.date(2014,6,11)
maxdate = datetime.date(2014,12,12)
order = 32

print len(symbols), 'data streams'

for days in range(0, 501):
    mind = mindate - timedelta(days)
    maxd = maxdate - timedelta(days)
    df = accumulateFrame(symbols, order, mind.toordinal(), maxd.toordinal())
    print 'producing plot for', mind, maxd
    figure("stacked-{0}-{1}-{2}-{3}d".format(single,mind,maxd,order), df, (12,6))
