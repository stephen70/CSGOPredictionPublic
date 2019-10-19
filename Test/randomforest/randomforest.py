from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np
import pickle
from keras.models import Sequential
from keras.layers import Dense, Activation, Flatten
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score
from sklearn.metrics import accuracy_score
from keras.callbacks import ModelCheckpoint
from sklearn.metrics import accuracy_score
from sklearn.model_selection import RandomizedSearchCV
from sklearn.ensemble import RandomForestRegressor
import random; import collections
import sklearn
from sklearn.utils import shuffle
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import roc_auc_score, roc_curve;import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
df = pd.read_csv('..\\..\\Generated\\final.csv', usecols= ['H2H', 'CO', 'Fat', 'LM', 'RoD', 'T%', 'CT%', 'Comp', 'CompSTD','RaD', 'W/L'])



n_folds = 10
iters = 50


temproclist = []
roclist = []
paramlist = []
def create_model(parameters):
    model = RandomForestClassifier(**parameters)
    return model

def fit_and_evaluate(t_x, val_x, t_y, val_y, parameters):
    model = create_model(parameters)
    t_x = StandardScaler().fit_transform(t_x)
    val_x = StandardScaler().fit_transform(val_x)

    #PCA
    # pca = PCA(n_components=10)
    # t_x = pca.fit_transform(t_x)
    # val_x = pca.fit_transform(val_x)
    #
    # t_x = pd.DataFrame(data=t_x)
    # val_x = pd.DataFrame(data=val_x)
    # t_x.reset_index(drop=True, inplace=True)
    # val_x.reset_index(drop=True, inplace=True)

    model.fit(t_x, t_y)
    RF_predictions = model.predict(val_x)
    score = accuracy_score(val_y, RF_predictions)
    fpr, tpr, threshold = roc_curve(val_y, RF_predictions)
    roc_auc = sklearn.metrics.auc(fpr, tpr)
    modellist.append(model)
    return [score, roc_auc]


for i in np.arange(iters):
    parameters = {'n_estimators': random.choice([int(x) for x in np.linspace(start = 200, stop = 3000, num = 10)]),
                  'max_features': random.choice(['auto', 'sqrt']),
                  'max_depth': random.choice([int(x) for x in np.linspace(10, 510, num = 11)]),
                  'min_samples_split': random.choice([2, 5, 10, 20, 30, 40, 50]),
                  'min_samples_leaf': random.choice([4, 8, 16, 32, 64, 128]),
                  'bootstrap': random.choice([True, False])}

    for j in range(n_folds):
        t_x, val_x, t_y, val_y = train_test_split(train_x, train_y, test_size=0.25, random_state=np.random.randint(1, 1000, 1)[0], shuffle=False)
        # t_x, t_y = balancewinloss(t_x, t_y )
        # val_x, val_y = balancewinloss(val_x, val_y)
        results = fit_and_evaluate(t_x, val_x, t_y, val_y, parameters)
        temproclist.append(results[1])

    print("Param: " + str(parameters), " Avg score: " + str(sum(temproclist) / len(temproclist)))
    temproclist = []

# {'n_estimators': 1266, 'max_features': 'sqrt', 'max_depth': 10, 'min_samples_split': 40, 'min_samples_leaf': 2, 'bootstrap': False}
# 0.591254752851711

train_x = StandardScaler().fit_transform(train_x)
test_x = StandardScaler().fit_transform(test_x)

# print("Test dataset:")
# for model in modellist:
#     RF_predictions = model.predict(test_x)
#     score = accuracy_score(test_y, RF_predictions)
#     fpr, tpr, threshold = roc_curve(test_y, RF_predictions)
#     roc_auc = sklearn.metrics.auc(fpr, tpr)
#     print("%:" + str(100 * score)," AUC:" + str(roc_auc))


# paramlist = []
# for i in np.arange(30):
#     parameters = {'n_estimators': random.choice([int(x) for x in np.linspace(start = 200, stop = 5000, num = 10)]),
#                   'max_features': random.choice(['auto', 'sqrt']),
#                   'max_depth': random.choice([int(x) for x in np.linspace(10, 510, num = 11)]),
#                   'min_samples_split': random.choice([2, 5, 10, 20, 30, 40, 50]),
#                   'min_samples_leaf': random.choice([1, 2, 4, 8, 16, 32, 64]),
#                   'bootstrap': random.choice([True, False])}
#
#     model = RandomForestClassifier(**parameters)
#     model.fit(x_train, y_train)
#     RF_predictions = model.predict(x_test)
#     score = accuracy_score(y_test, RF_predictions)
#     print(score)
#     paramlist.append(parameters)

#{'n_estimators': 1266, 'max_features': 'sqrt', 'max_depth': 10, 'min_samples_split': 40, 'min_samples_leaf': 2, 'bootstrap': False}
#0.591254752851711
#
# for i in paramlist:
#     print(str(i) + "\n")


# model = RandomForestClassifier(**parameters)
# model.fit(x_train, y_train)
# RF_predictions = model.predict(x_test)
# score = accuracy_score(y_test, RF_predictions)
# print(score)
# pickle.dump(model, open('model.sav', 'wb'))

#It is also important that any preparation of the data prior to fitting the model occur on the CV-assigned training dataset within the loop rather than on the broader data set. This also applies to any tuning of hyperparameters. A failure to perform these operations within the loop may result in data leakage and an optimistic estimate of the model skill.

# print(X[20:40])
# print(model.predict_proba(X[20:40]))
# print(model.predict(X[20:40]))
# print(Y[20:40])
