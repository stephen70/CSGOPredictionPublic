import math;import numpy as np;import multiprocessing;import pandas as pd;from ast import literal_eval; import statistics as stat
p = print;pd.set_option('display.width',20000);import timer


myTimer = timer.timer()

# finds percentage of T rounds won * percentage of CT rounds won over all matches played in the last timeSpan days
timeSpan = 120
noProcesses = 7

mdf = pd.read_csv("matches.csv").loc[:,:]
pdf = pd.read_csv("..\\..\\DataAcquirement\\2Matches\\players.csv")

def findrad(tid, day):
    try:
        temp = mdf.loc[mdf['days'] < day + timeSpan]
        temp = temp.loc[temp['days'] > day]
        radlist = []
        if tid == 6118:
            o = 2
        temp = temp.loc[(temp['t1id'] == tid) | (temp['t2id'] == tid)]
        for match in temp.itertuples():
            mid = match[list(temp.columns).index('mid') + 1]
            rating1 = 0
            rating2 = 0
            count = 0
            temp2 = pdf.loc[pdf['mid'] == mid]
            temp2t1 = temp2.loc[temp2['tid'] == tid]
            temp2t2 = temp2.loc[temp2['tid'] != tid]

            t1avg = temp2t1['rating'].sum() / temp2t1.shape[0]
            t2avg = temp2t2['rating'].sum() / temp2t2.shape[0]

            raddiff = t1avg - t2avg

            if not len(radlist) == 0 and radlist[len(radlist) - 1] == raddiff: # avoids double counting by dropping the result if it is the same as the previous one
                continue

            radlist.append(raddiff)

        radstd = stat.pstdev(radlist)
        ret = [float(sum(radlist)) / len(radlist), radstd]
    except Exception as E:
        print("Exception", E)
        return [np.nan, np.nan]
    return ret


def wrapper(l):
    t1id = l[0]; t2id = l[1]; day = l[2]
    t1rad = findrad(t1id, day)
    t2rad = findrad(t2id, day)
    ret = [np.round(t1rad[0] - t2rad[0], 3), np.round(t1rad[1] - t2rad[1], 3)]
    return ret


l = []
for i in mdf.itertuples():
    # make this independent of column position
    # plus one because itertuples includes index
    t1idindex = list(mdf.columns).index('t1id') + 1
    t2idindex = list(mdf.columns).index('t2id') + 1
    dayindex = list(mdf.columns).index('days') + 1
    l.append([i[t1idindex], i[t2idindex], i[dayindex]])

if __name__ == '__main__':
    pool = multiprocessing.Pool(noProcesses)
    df = pd.DataFrame(pool.map(wrapper, l), columns=['rad','radstd'])
    mdf['rad'] = np.round(df['rad'], 3)
    mdf['radstd'] = np.round(df['radstd'], 3)
    mdf.to_csv("matches.csv", index=False)
    myTimer.stop()
