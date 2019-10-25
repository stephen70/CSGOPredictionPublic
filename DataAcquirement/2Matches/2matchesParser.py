
import csv;import datetime as dt;import math;import numpy as np;import pandas as pd;import timer

# renames columns of the scraped data, converts date into days since match, drops samples with na values, adds ranking points at time of match, and more

pd.set_option('display.width', 10000)
myTimer = timer.timer()

dfm = pd.read_csv('matchResultsUnparsed.csv').loc[:,:]
dfp = pd.read_csv('playerStatsUnparsed.csv')

dfm.drop(['Time'], inplace=True, axis=1)
dfm.reset_index(inplace=True)

# remove matches which have no corresponding player stats
len1 = dfm.shape[0]
for i, row in enumerate(dfm.itertuples()):
    matchID = (row[-1:][0])
    if not (dfp['MatchID'] == matchID).any():
        dfm.drop(i, inplace=True)
print("no. before dropping no player stats", len1, "after", dfm.shape[0])

# add days since match
today_date = dt.date(dt.datetime.now().year, dt.datetime.now().month, dt.datetime.now().day)
def daysSince(dateString):
    dateSplit = dateString.split("/")
    dateSplit[0] = int(dateSplit[0])
    dateSplit[1] = int(dateSplit[1])
    dateSplit[2] = int(dateSplit[2])
    match_date = dt.date(int(dateSplit[2] + 2000), int(dateSplit[0]), int(dateSplit[1]))
    return str((today_date - match_date).days)
dfm['days'] = dfm['Date'].map(lambda string: daysSince(string))

# remove date but add month and year
dfm['Date'] = dfm['Date'].map(lambda string: string.split("/")[0] + "/" + string.split("/")[2])

# add map using 'Cache': 1, 'Cobblestone': 2, 'Dust2': 3, 'Inferno': 4, 'Mirage': 5, 'Nuke': 6, 'Overpass': 7, 'Train': 8, 'Season': 9
maps = {'Cache': 1, 'Cobblestone': 2, 'Dust2': 3, 'Inferno': 4, 'Mirage': 5, 'Nuke': 6, 'Overpass': 7, 'Train': 8, 'Season': 9, 'Default': 10}
dfm['map'] = dfm['Map'].map(lambda x: maps[x])
dfm.drop('Map', inplace=True, axis=1)
dfm = dfm.loc[dfm['map'] != 10]

# drop matches where either team is not ranked at month of match, and append both teams points at month of match
dfranks = pd.read_csv("../1Rankings/ranks.csv",delimiter=";",header=-1)
# define a function which takes in a dataframe and adds on two points columns
# adds NaN if team not found in rankings. then rows with NaN are dropped
def ranks(dfin):
    id1 = dfin['Team 1 ID']
    id2 = dfin['Team 2 ID']
    date = dfin['Date']
    df = dfranks[dfranks.loc[:,0] == date]
    ids = eval(df.loc[:,1].item())
    points = eval(df.loc[:, 2].item())

    try:
        t1index = ids.index(id1)
        points1 = int(points[t1index])
        dfin['p1'] = points1
        t2index = ids.index(id2)
        points2 = int(points[t2index])
        dfin['p2'] = points2
    except ValueError:
        dfin['p1'] = np.nan
        dfin['p2'] = np.nan

    return dfin

dfm = dfm.apply(ranks, axis=1)
dfm.dropna(inplace=True)

print("no. before rank drop", len1, "after", dfm.shape[0])
print("no. at very start", len1, "after", dfm.shape[0])

dfm.reset_index(inplace=True)
dfm.drop(['index'], axis=1, inplace=True)
dfm.rename(columns={'Match ID':'mid','Map':'map','Team':'team','Team 1 ID':'t1id',
                    'Team 1 Start Side':'t1ss','Team 1 Score':'t1s','Team 1 Half 1 Score':'t1h1s',
                    'Team 1 Half 2 Score':'t1h2s','Team 1 Overtime Score':'t1ots',
                    'Team 2 ID':'t2id','Team 2 Start Side':'t2ss','Team 2 Score':'t2s',
                    'Team 2 Half 1 Score':'t2h1s','Team 2 Half 2 Score':'t2h2s',
                    'Team 2 Overtime Score':'t2ots','Date':'date'}, inplace=True)

dfm.drop(dfm.columns[0], inplace=True, axis=1)

# change to correct dtypes
dfm = dfm.astype({'p1': np.int64,'p2': np.int64,'days':np.int64})

def addrw(df):
    t1s = int(df['t1s'])
    t2s = int(df['t2s'])
    df['rw'] = np.round(t1s / (t1s + t2s), 3)
    return df

dfm = dfm.apply(addrw, axis=1)

dfm.to_csv("matchesNoCO.csv", index=False)

myTimer.stop()
