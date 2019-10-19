import csv
import datetime as dt
import math
import numpy as np
import pandas as pd
import timer
pd.set_option('display.width', 10000)
myTimer = timer.timer()

dfp = pd.read_csv('playerStatsUnparsed.csv').loc[:,:]
dfm = pd.read_csv('matchesNoCO.csv')

len1 = dfp.shape[0]

dfp.drop(['Player','Deaths','Rating Type','Kills','ADR','KAST%','Map'], axis=1, inplace=True)
dfp.columns = dfp.columns.str.replace(' ', '')
dfp.dropna(inplace=True)
dfp.drop_duplicates(inplace=True)

# change to correct dtypes
dfp = dfp.astype({'Team': np.int64,'MatchID': np.int64})


print("no. before dropping nans and duplicates", len1, "after", dfp.shape[0])
len1 = dfp.shape[0]

# drop teams not ranked at month of match
matchset = set(dfm['mid'])
for mid in set(dfp['MatchID']):

    dfp.reset_index(inplace=True, drop=True)
    if not mid in matchset:
        dfp = dfp.drop(dfp[dfp.MatchID == mid].index)


print("no. before dropping unranked", len1, "after", dfp.shape[0])

dfp.rename(columns={'MatchID':'mid','Team':'tid','Rating':'rating'},inplace=True)


dfp.to_csv("players.csv", index=False)

myTimer.stop()


