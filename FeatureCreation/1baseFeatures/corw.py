import math; import numpy as np; import pandas as pd; from ast import literal_eval; p=print; import timeit
pd.set_option('display.width',200000);import timer
myTimer = timer.timer()


dfmf = pd.read_csv("matches.csv").loc[:,:]

noProcesses = 7
# for each team, calculates the average rwp against all COs. then creates corw feature which is the difference in average rwp against COs
# important to average over each CO - otherwise a team playing a lot against a weak CO would gain an advantage

def findcorw(t1id, co1, t2id, co2):
    temp = dfmf[dfmf['mid'].isin(co1 + co2)]

    # convert match IDs to list of CO team IDS
    cos1 = temp['t1id']
    cos1 = cos1.loc[(temp['t1id'] != t1id) & (temp['t1id'] != t2id)]
    cos2 = temp['t2id']
    cos2 = cos2.loc[(temp['t2id'] != t1id) & (temp['t2id'] != t2id)]
    cos = pd.concat([cos1, cos2], axis=0)
    cos = cos.drop_duplicates().tolist()

    corw = np.zeros(len(cos))
    for index, co in enumerate(cos):
        temp11 = temp.loc[(temp['t1id'] == t1id) & (temp['t2id'] == co)]['rw']
        temp12 = temp.loc[(temp['t1id'] == co) & (temp['t2id'] == t1id)]['rw']
        if not temp12.shape[0] == 0:
            temp12 = temp12.apply(lambda x: 1 - x)
        t1rw = (sum(temp11) + sum(temp12)) / (temp11.shape[0] + temp12.shape[0])

        temp21 = temp.loc[(temp['t1id'] == t2id) & (temp['t2id'] == co)]['rw']
        temp22 = temp.loc[(temp['t1id'] == co) & (temp['t2id'] == t2id)]['rw']
        if not temp22.shape[0] == 0:
            temp22 = temp22.apply(lambda x: 1 - x)
        t2rw = (sum(temp21) + sum(temp22)) / (temp21.shape[0] + temp22.shape[0])
        corw[index] = t1rw - t2rw

    return corw.mean()


def wrapper(l):
    if l[2] != l[2]: #easy way to check for nan
        return np.nan
    t1id = l[0]; t2id = l[1]; co1 = eval(l[2]); co2 = eval(l[3])
    ret = findcorw(t1id, co1, t2id, co2)
    ret = np.round(ret, 3)
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