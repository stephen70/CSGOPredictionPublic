import numpy as np; import pandas as pd; import matplotlib.pyplot as plt; import stats
from scipy.stats import *; from sklearn.metrics import *;import statsmodels.api as sm
from sklearn.preprocessing import StandardScaler
matches = pd.read_csv("../../FeatureCreation/1BaseFeatures/matches.csv")

# creates feature for differenc ein ranking points at time of match

def addpd(df):
    t1p = int(df['p1'])
    t2p = int(df['p2'])
    df['pd'] = t1p - t2p
    return df

matches = matches.apply(addpd, axis=1)
matches.to_csv("matches.csv", index=False)