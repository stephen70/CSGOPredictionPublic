import math; import numpy as np; import pandas as pd; from ast import literal_eval; p=print
pd.set_option('display.width',20000)

# calculates number of matches played over last appSpan days. ignores maps played in current match.
# creates app feature, a measure of how often a team plays. if a team is new, this is low and contains information about how new a team are.

df = pd.read_csv("matches.csv").loc[:,:]
df.reset_index(drop=False, inplace=True)
# app decay removed
appSpan = 120

def findapp(t1id, t2id, mid, day, ignoreRounds=True):

    matchindex =  df.loc[df['mid'] == mid].index[0]
    dfrecent = df.loc[df['index'] < matchindex]
    dfrecent = dfrecent.loc[dfrecent['days'] <= day + appSpan]

    # team 1
    df1 = dfrecent.loc[(dfrecent["t1id"] == t1id) | (dfrecent["t2id"] == t1id), :]
    if ignoreRounds:
        t1m = df1.shape[0]
    else:
        t1m = df1['t1s'].sum() + df1['t2s'].sum()
        if t1m != t1m:
            t1m = 0

    # team 2
    df2 = dfrecent.loc[(dfrecent["t1id"] == t2id) | (dfrecent["t2id"] == t2id), :]
    if ignoreRounds:
        t2m = df2.shape[0]
    else:
        t2m = df2['t1s'].sum() + df2['t2s'].sum()
        if t2m != t2m:
            t2m = 0

    ret = t1m - t2m
    return ret

def wrapper(list):
    ret = findapp(list[0],list[1],list[2],list[3], ignoreRounds=True)
    return ret

import multiprocessing

l = []
for i in df.itertuples():
    # make this independent of column position
    # plus one because itertuples includes index
    t1idindex = list(df.columns).index('t1id') + 1
    t2idindex = list(df.columns).index('t2id') + 1
    midindex = list(df.columns).index('mid') + 1
    dayindex = list(df.columns).index('days') + 1
    l.append([i[t1idindex],i[t2idindex],i[midindex],i[dayindex]])

if __name__ == '__main__':
    pool = multiprocessing.Pool(processes = 7)
    df['app'] = pool.map(wrapper, l)
    df.to_csv("matches.csv", index=False)
