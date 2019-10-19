import math; import numpy as np; import pandas as pd; from ast import literal_eval; p=print; import timeit
pd.set_option('display.width',200000);import timer
myTimer = timer.timer()


dfmf = pd.read_csv("matches.csv").loc[:,:]

noProcesses = 7

# calculates the round win percentage for each team against all COs, then appends the difference to matchesfeat.csv

def findcorw(tid, co1):
    temp = dfmf[dfmf['mid'].isin(co1)]
    # team 1 is tid
    temp1 = temp[temp['t1id'] == tid]
    # team 2 is tid
    temp2 = temp[temp['t2id'] == tid]
    if not temp2.empty:
        temp2['rw'] = temp2['rw'].apply(lambda x: 1 - x)

    return (temp1['rw'].sum() + temp2['rw'].sum()) / (temp1.shape[0] + temp2.shape[0])


def wrapper(l):
    if l[2] != l[2]: #easy way to check for nan
        return np.nan
    t1id = l[0]; t2id = l[1]; co1 = eval(l[2]); co2 = eval(l[3])
    t1rw = findcorw(t1id, co1)
    t2rw = findcorw(t2id, co2)
    ret = np.round(t1rw - t2rw, 3)
    return ret

import multiprocessing

l = []
for i in dfmf.itertuples():
    # make this independent of column position
    # plus one because itertuples includes index
    t1idindex = list(dfmf.columns).index('t1id') + 1
    t2idindex = list(dfmf.columns).index('t2id') + 1
    co1index = list(dfmf.columns).index('co1') + 1
    co2index = list(dfmf.columns).index('co2') + 1
    l.append([i[t1idindex],i[t2idindex],i[co1index],i[co2index]])

if __name__ == '__main__':
    pool = multiprocessing.Pool(processes = noProcesses)
    results = pool.map(wrapper, l)
    dfmf['corw'] = results
    dfmf.to_csv("matches.csv", index=False)
    myTimer.stop()