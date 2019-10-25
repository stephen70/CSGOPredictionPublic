import math; import numpy as np; import time; import pandas as pd
p=print;pd.options.mode.chained_assignment = None;pd.set_option('display.width', 1000); import timer

# Description: finds and appends a list of common opponents using matchesNoCO.csv, and adds the round win percentage
# interval: maximum amount of days between t1 playing t3 and t2 playing t3
# span: maximum amount of days old a match can be while being eligible for use as a CO match
# minMaps: minimum amount of maps each team has to have played against a CO. Does not mean maps for each CO
# minCOs: minimum number of different COs teams must have

myTimer = timer.timer()

interval = 60; span = 120; minMaps = 5; minCOs = 2

noProcesses = 7

dfm = pd.read_csv("matchesNoCO.csv").loc[:,:]

def findCommonOpponents(t1id, t2id, day):
    t1id = int(t1id); t2id = int(t2id); day = int(day)

    # drop matches which occurred span days before the match, or after the match
    df = dfm.drop(dfm.loc[(dfm['days'] > day + span)].index) # create a copy of dfm so dfm is unchanged
    df = df.reset_index(drop=True)
    df = df.drop(df.loc[df['days'] < (day + 1)].index) # day + 1 to remove the current day. removing via df['days'] == day simply didn't work.
    df = df.reset_index(drop=True)

    # df1: matches with team 1, df2: matches with team 2
    df1 = df.loc[(df["t1id"] == t1id) | (df["t2id"] == t1id), ("t1id", "t2id", "days", "mid")]
    df2 = df.loc[(df["t1id"] == t2id) | (df["t2id"] == t2id), ("t1id", "t2id", "days", "mid")]

    # if no matches found for either team within span, stop immediately and return None
    if df1.shape[0] == 0 or df2.shape[0] == 0:
        return []

    # find the other team IDs from t1 and t2's matches
    df1["otherID"] = np.where(df1['t1id'] == t1id, df1['t2id'], df1['t1id'])
    df1.drop(columns=['t1id', 't2id'], inplace=True)
    # drop if the other team is actually t1 or t2
    df1.drop(df1[(df1['otherID'] == t2id)].index, inplace=True)

    df2["otherID"] = np.where(df2['t1id'] == t2id, df2['t2id'], df2['t1id'])
    df2.drop(columns=['t1id', 't2id'], inplace=True)
    df2.drop(df2[(df2['otherID'] == t1id)].index, inplace=True)

    # creates dataframe with 3 columns, the day Team 1 played the CO, the CO ID, and the day Team 2 played CO
    dfco = pd.merge(df1, df2, on='otherID', sort=False)

    # both teams must have played CO no more than interval days after eachother
    dfco.query('-@interval < days_x - days_y < @interval', inplace=True)

    # if no common opponents, drop the match
    if dfco.shape[0] == 0:
        return []

    co1 = dfco["mid_x"].drop_duplicates().tolist()
    co2 = dfco["mid_y"].drop_duplicates().tolist()

    COs = dfco["otherID"].drop_duplicates().tolist()

    # check each team has played more than minMaps with COs
    df1 = df1[df1['otherID'].isin(COs)]
    df2 = df2[df2['otherID'].isin(COs)]
    # if not at least minMaps, drop the match
    if (df1.shape[0] < minMaps) | (df2.shape[0] < minMaps) | (len(COs) < minCOs):
        return []

    return [co1, co2]

def wrapper(list):
    ret = findCommonOpponents(list[0],list[1],list[2])
    return ret

import multiprocessing

l = []
for i in dfm.itertuples():
    l.append([i[2],i[8],i[15]])

if __name__ == '__main__':
    pool = multiprocessing.Pool(processes = noProcesses)
    results = pd.DataFrame(pool.map(wrapper, l), columns=['co1','co2'])
    dfm['co1'] = results['co1']
    dfm['co2'] = results['co2']

    dfm.to_csv("matches.csv", index=False)
    dfm.to_csv("..\\..\\FeatureCreation\\1BaseFeatures\\matches.csv", index=False)
    myTimer.stop()