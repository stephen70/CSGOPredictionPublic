import math;
import numpy as np;

import pandas as pd;
from ast import literal_eval;

# 17 minutes

p = print;pd.set_option('display.width',20000)
import matplotlib.pyplot as plt

# to be rewritten


fileLoc = "..\\Generated\\initial.csv"

# finds percentage of T rounds won * percentage of CT rounds won
timeSpan = 60

mdf = pd.read_csv(fileLoc, engine='c', usecols=['Days', 'T1ID', 'T2ID', 'W/L', 'MatchID'], dtype={
    'Days': np.int16, 'T1ID': np.int16, 'T2ID': np.int16, 'W/L': np.float, 'MatchID': np.int32})

mse = pd.read_csv("..\\Database\\matchResultsEssential.csv", engine='c',
                  usecols=['Team 1 Half 1 Score', 'Team 1 Half 2 Score', 'Team 2 Half 1 Score', 'Team 2 Half 2 Score',
                           'Match ID', 'Team 1 Start Side', 'Team 1 ID', 'Team 2 ID','Team 1 Score','Team 2 Score'], dtype={'Team 1 ID': np.int32, 'Team 1 Start Side':str,  'Team 1 Half 1 Score': np.int16,  'Team 1 Half 2 Score': np.int16,
                            'Team 2 ID': np.int16,  'Team 2 Half 1 Score': np.int32,  'Team 2 Half 2 Score': np.int16,  'Match ID':np.int32})
import statistics as stat
def find(id, day):
    try:
        df = mdf.drop(mdf.loc[mdf['Days'] > day + timeSpan].index)
        df.drop(df.loc[df['Days'] <= day].index, inplace=True)
        Tpercent = []
        CTpercent = []
        df1 = df.loc[df['T1ID'] == id]

        # 3: t1h1, 4: t1h2, 6: t2h1, 7: t2h2
        for i in df1.itertuples():
            mid = i[5]
            df11 = mse.loc[mse['Match ID'] == mid]
            for j in df11.itertuples():
                if j[2] == "CT":
                    CTpercent.append(j[4] / 15.0)
                    Tpercent.append(float(j[5]) / (j[5] + j[9]))
                else:
                    Tpercent.append(j[4] / 15.0)
                    CTpercent.append(float(j[5]) / (j[5] + j[9]))

        df2 = df.loc[df['T2ID'] == id]
        for i in df2.itertuples():
            mid = i[5]
            df22 = mse.loc[mse['Match ID'] == mid]
            for j in df22.itertuples():
                if j[2] == "T":
                    CTpercent.append(j[8] / 15.0)
                    Tpercent.append(float(j[9]) / (j[5] + j[9]))
                else:
                    Tpercent.append(j[8] / 15.0)
                    CTpercent.append(float(j[9]) / (j[5] + j[9]))
        if len(CTpercent) == 0:
            return [0, 0, 0, 0]
        comp = stat.pstdev([CTpercent[i] * Tpercent[i] for i in np.arange(len(CTpercent))])
        return [comp]
    except Exception:
        return 0

def wrapper(list):
    l = find(list[0], list[2])
    k = find(list[1], list[2])
    if l == 0 or k == 0:
        return None
    ret = [l[i] - k[i] for i in range(1)]
    return ret

dfread = pd.read_csv("..\\Generated\\middle.csv", engine='c', converters={"COs": literal_eval}, dtype={
    'Days': np.int16, 'Map': np.int8, 'T1ID': np.int16, 'T1SS': np.bool_, 'T2ID': np.int16, 'W/L': np.float,
    'MatchID': np.int32, 'U': np.float16})

import multiprocessing

l = []
for i in dfread.itertuples():
    l.append([i[3],i[4],i[1]])

if __name__ == '__main__':
    pool = multiprocessing.Pool(processes = 7)
    results = pool.map(wrapper, l)
    df = pd.DataFrame(results, columns=['a'])
    dfread['CompSTD'] = df['a']
    dfread[['CompSTD']].to_csv("..\\Generated\\All RoundStats STD.csv", index=False, header=None)
