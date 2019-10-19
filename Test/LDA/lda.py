import numpy as np; import pandas as pd; import matplotlib.pyplot as plt; import stats
from scipy.stats import *; from sklearn.metrics import *;import statsmodels.api as sm
from sklearn.preprocessing import StandardScaler; from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis


df = pd.read_csv("../../FeatureCreation/1BaseFeatures/matches.csv").loc[:,:]
# drop matches with missing features
print(df.shape)
df = df.drop(df.loc[df['corw'] != df['corw']].index)
df = df.drop(df.loc[df['rad'] != df['rad']].index)
df.reset_index(drop=True, inplace=True)
print(df.shape)

# standardization
scaler = StandardScaler()
df['corw'] = scaler.fit_transform(df['corw'].values.reshape(-1, 1))
df['pd'] = scaler.fit_transform(df['pd'].values.reshape(-1, 1))
df['rad'] = scaler.fit_transform(df['rad'].values.reshape(-1, 1))
df['radstd'] = scaler.fit_transform(df['radstd'].values.reshape(-1, 1))
df['app'] = scaler.fit_transform(df['app'].values.reshape(-1, 1))
df['maprw'] = scaler.fit_transform(df['maprw'].values.reshape(-1, 1))

# separate win and loss
dfwin = df.loc[df['rw'] > 0.5]
dfloss = df.loc[df['rw'] < 0.5]
print(dfwin.shape[0],dfloss.shape[0])

# feature to act upon
feat = 'maprw'
print(dfwin[feat].mean(),dfloss[feat].mean(),dfwin[feat].std(),dfloss[feat].std())

# histograms
def showhist():
    bins = np.linspace(-5, 5, 40)
    plt.hist(dfwin[feat], bins, color='blue', alpha=.2,  label='win', edgecolor='black')
    plt.hist(dfloss[feat], bins, color='orange', alpha=.2,  label='loss', edgecolor='black')
    # means
    plt.axvline(linewidth=4, color='blue', x=dfwin[feat].mean(), lw=1)
    plt.axvline(linewidth=4, color='orange', x=dfloss[feat].mean(), lw=1)

    plt.legend()
    plt.show()

# # begin p = 1 linear discriminant analysis
# # convert to binary classes
# df['rw'] = np.round(df['rw'])
# lda = LinearDiscriminantAnalysis()
# lda.fit(df[feat].values.reshape(-1,1), df['rw'].values.reshape(-1,1))
# xytrain = df[[feat,'rw']]
# ypred = pd.DataFrame(lda.predict_proba(df[feat].values.reshape(-1,1)))
# ypred.rename(columns={1:'predrw'}, inplace=True)
# # plot the prediction curve
#
# plt.scatter(xytrain[feat], ypred.loc[:,'predrw'], s=1)
# plt.show()
#
# # calculate classification accuracy
# ypred = np.round(ypred['predrw'])
# ypred.reset_index(inplace=True,drop=True);xytrain.reset_index(inplace=True, drop=True)
# dfacc = pd.concat([xytrain, ypred], axis=1)
#
# dfacc = dfacc.loc[dfacc['rw'] == dfacc['predrw']]
# print("classification acc:",dfacc.shape[0] / ypred.shape[0])


# # begin p > 1 linear discriminant analysis
# feat = ['app','pd','rad','corw','maprw']
# # convert to binary classes
# df['rw'] = np.round(df['rw'])
# lda = LinearDiscriminantAnalysis()
# lda.fit(df[feat], df['rw'].values.reshape(-1,1))
# xytrain = df[feat + ['rw']]
# ypred = pd.DataFrame(lda.predict_proba(df[feat]))
# ypred.rename(columns={1:'predrw'}, inplace=True)
#
# # # plot the prediction curve
# plt.scatter(xytrain['maprw'], ypred.loc[:,'predrw'], s=1)
# plt.show()
#
# # calculate classification accuracy
# ypred = pd.DataFrame(np.round(ypred['predrw']))
# ypred.reset_index(inplace=True,drop=True);xytrain.reset_index(inplace=True, drop=True)
# dfacc = pd.concat([xytrain, ypred], axis=1)
#
# dfacc = dfacc.loc[dfacc['rw'] == dfacc['predrw']]
# print("classification acc:",dfacc.shape[0] / ypred.shape[0])

# # create 2d plot of decision boundary
# ypred = pd.DataFrame(np.round(ypred['predrw']))
# ypred.reset_index(inplace=True,drop=True);xytrain.reset_index(inplace=True, drop=True)
# ypred = pd.concat([xytrain, ypred], axis=1)
# ypredwin = ypred.loc[ypred['predrw'] == 1.0]
# ypredloss = ypred.loc[ypred['predrw'] == 0.0]
# print(ypredwin.shape[0], ypredloss.shape[0])
# plt.scatter(ypredwin[feat[0]], ypredwin[feat[1]], color='blue',label='win')
# plt.scatter(ypredloss[feat[0]], ypredloss[feat[1]], color='orange',label='loss')
# plt.xlabel(feat[0]); plt.ylabel(feat[1])
# plt.legend();plt.show()

# test if win and loss are covariant
# print(dfwin[['corw','pd','rad','rw']].corr(method='spearman'))
# print(dfloss[['corw','pd','rad','rw']].corr(method='spearman'))




# begin quadratic discriminant analysis
# feat = ['pd', 'rad']
# # convert to binary classes
# df['rw'] = np.round(df['rw'])
# qda = QuadraticDiscriminantAnalysis()
# qda.fit(df[feat], df['rw'].values.reshape(-1,1))
# xytrain = df[feat + ['rw']]
# ypred = pd.DataFrame(qda.predict_proba(df[feat]))
# ypred.rename(columns={1:'predrw'}, inplace=True)
# plot the prediction curve
#
# plt.scatter(xytrain[feat], ypred['predrw'], s=1)
# plt.show()

# # calculate classification accuracy
# ypred = pd.DataFrame(np.round(ypred['predrw']))
# ypred.reset_index(inplace=True,drop=True);xytrain.reset_index(inplace=True, drop=True)
# dfacc = pd.concat([xytrain, ypred], axis=1)
#
# dfacc = dfacc.loc[dfacc['rw'] == dfacc['predrw']]
# print("classification acc:",dfacc.shape[0] / ypred.shape[0])
#
# # # create 2d plot of decision boundary
# ypred = pd.DataFrame(np.round(ypred['predrw']))
# ypred.reset_index(inplace=True,drop=True);xytrain.reset_index(inplace=True, drop=True)
# ypred = pd.concat([xytrain, ypred], axis=1)
# ypredwin = ypred.loc[ypred['predrw'] == 1.0]
# ypredloss = ypred.loc[ypred['predrw'] == 0.0]
# print(ypredwin.shape[0], ypredloss.shape[0])
# plt.scatter(ypredwin[feat[0]], ypredwin[feat[1]], color='blue',label='win')
# plt.scatter(ypredloss[feat[0]], ypredloss[feat[1]], color='orange',label='loss')
# plt.xlabel(feat[0]); plt.ylabel(feat[1])
# plt.legend();plt.show()