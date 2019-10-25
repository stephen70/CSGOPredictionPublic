import math; import numpy as np;  import pandas as pd; from ast import literal_eval; p=print; import timer
pd.set_option('display.width',20000)
myTimer = timer.timer()
# to be rewritten

lastMatchSpan = 90
noProcesses = 7

df = pd.read_csv("matches.csv").loc[:,:]

def findTimeSinceLastMatch(tid, day):
    temp = df.loc[df['days'] < day + lastMatchSpan]
    temp = temp.loc[temp['days'] > day]

    temp = temp.loc[(temp['t1id'] == tid) | (temp['t2id'] == tid)]

    if temp.shape[0] == 0:
        return 90

    temp = temp.tail(1)

    return int(temp['days']) - day


def wrapper(list):
    ret1 = findTimeSinceLastMatch(list[0],list[2])
    ret2 = findTimeSinceLastMatch(list[1],list[2])
    return ret2 - ret1

import multiprocessing

l = []
for i in df.itertuples():
    # make this independent of column position
    # plus one because itertuples includes index
    t1idindex = list(df.columns).index('t1id') + 1
    t2idindex = list(df.columns).index('t2id') + 1
    daysindex = list(df.columns).index('days') + 1
    l.append([i[t1idindex],i[t2idindex],i[daysindex]])

if __name__ == '__main__':
    pool = multiprocessing.Pool(processes = noProcesses)
    results = pool.map(wrapper, l)
    df['lm'] = results
    df.to_csv("matches.csv", index=False)
    myTimer.stop()