import numpy as np; import pandas as pd; import matplotlib.pyplot as plt; import stats
from scipy.stats import *; from sklearn.metrics import *;import statsmodels.api as sm
from sklearn.preprocessing import StandardScaler
matches = pd.read_csv("../../FeatureCreation/1BaseFeatures/matches.csv").loc[:,:]

# drop matches with missing features
print(matches.shape)
matches = matches.drop(matches.loc[matches['corw'] != matches['corw']].index)
matches = matches.drop(matches.loc[matches['rad'] != matches['rad']].index)
matches.reset_index(drop=True, inplace=True)
print(matches.shape)
print(matches.head())

# standardization
scaler = StandardScaler()
matches['corw'] = scaler.fit_transform(matches['corw'].values.reshape(-1, 1))
scaler = StandardScaler()
matches['pd'] = scaler.fit_transform(matches['pd'].values.reshape(-1, 1))
scaler = StandardScaler()
matches['rad'] = scaler.fit_transform(matches['rad'].values.reshape(-1, 1))
scaler = StandardScaler()
matches['radstd'] = scaler.fit_transform(matches['radstd'].values.reshape(-1, 1))
scaler = StandardScaler()
matches['app'] = scaler.fit_transform(matches['app'].values.reshape(-1, 1))
scaler = StandardScaler()
matches['maprw'] = scaler.fit_transform(matches['maprw'].values.reshape(-1, 1))


feature = matches['maprw']
allfeatures = matches[['maprw','rad','corw','app','pd']]

# spearman
print('spearman',feature.corr(matches['rw'], method='spearman'))

# linear regression
x = allfeatures; y = matches['rw']
x = sm.add_constant(x)
model = sm.OLS(y, x)
results = model.fit()
print(results.summary())

# plotting
#plt.hist(feature, bins=20)
print(matches[['rw','corw','pd','rad','radstd','app','maprw']].corr(method='spearman'))
slope, intercept, r_value, p_value, std_err = stats.linregress(feature, matches['rw'])
line = slope * feature + intercept

plt.plot(feature,matches['rw'],'o', feature, line)
plt.scatter(feature, matches['rw'], s=0.1)
plt.show()





