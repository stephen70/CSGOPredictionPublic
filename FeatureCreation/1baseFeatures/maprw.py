import math;import numpy as np;import multiprocessing;import pandas as pd;from ast import literal_eval; import statistics as stat
p = print;pd.set_option('display.width',20000);import timer


myTimer = timer.timer()

# finds percentage of rounds won on map in last mapSpan days, returns 0.5 if less than minMaps played on that map
mapSpan = 120
minMaps = 2
noProcesses = 7

df = pd.read_csv("matches.csv").loc[:,:]

def findmaprw(tid, map, day):

    temp = df.loc[df['days'] < day + mapSpan]
    temp = temp.loc[temp['days'] > day]

    temp = temp.loc[(temp['t1id'] == tid) | (temp['t2id'] == tid)]
    temp = temp.loc[temp['map'] == map]

    temp1 = temp.loc[temp['t1id'] == tid]
    temp2 = temp.loc[temp['t2id'] == tid]

    # adjust for empty dfs and nans
    nan1 = temp1['rw'].sum() != temp1['rw'].sum()
    nan2 = temp2['rw'].sum() != temp2['rw'].sum()

    if nan1 and nan2:
        return 0.5

    if nan1:
        temp2['rw'] = temp2['rw'].map(lambda x: 1 - x)
        return  temp2['rw'].sum() / temp2.shape[0]

    if nan2:
        return temp1['rw'].sum() / temp1.shape[0]

    temp2['rw'] = temp2['rw'].map(lambda x: 1 - x)
    return (temp1['rw'].sum() + temp2['rw'].sum()) / (temp1.shape[0] + temp2.shape[0])

def wrapper(l):
    t1id = l[0]; t2id = l[1]; mapplayed = l[2]; day = l[3]
    t1rad = findmaprw(t1id, mapplayed, day)
    t2rad = findmaprw(t2id, mapplayed, day)
    ret = np.round(t1rad - t2rad, 3)
    return ret

l = []
for i in df.itertuples():
    # make this independent of column position
    # plus one because itertuples includes index
    t1idindex = list(df.columns).index('t1id') + 1
    t2idindex = list(df.columns).index('t2id') + 1
    mapindex = list(df.columns).index('map') + 1
    dayindex = list(df.columns).index('days') + 1
    l.append([i[t1idindex], i[t2idindex], i[mapindex], i[dayindex]])

if __name__ == '__main__':
    pool = multiprocessing.Pool(noProcesses)
    dfres = pd.DataFrame(pool.map(wrapper, l), columns=['maprw'])
    df['maprw'] = dfres
    df.to_csv("matches.csv", index=False)
    myTimer.stop()
