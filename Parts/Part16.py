import pickle
import pandas as pd
from matplotlib import style
import numpy as np
from statistics import mean
from sklearn import svm, preprocessing, model_selection

style.use('fivethirtyeight')
pd.set_option("display.max_columns", 10)

def create_labels(cur_hpi, fut_hpi):
    if fut_hpi > cur_hpi:
        return 1
    else:
        return 0

def moving_average(values):
    ma = mean(values)
    return ma

with open('Pickles/HPI.pickle', 'rb') as pickle_in:
    housing_data = pickle.load(pickle_in)

housing_data = housing_data.pct_change()
housing_data.replace([np.inf, -np.inf], np.nan, inplace=True)
housing_data['US_HPI_future'] = housing_data['US_HPI'].shift(-1)
housing_data.dropna(inplace=True)

# new_column = list(map( function_to_map, parameter1, parameter2, ... ))
housing_data['label'] = list(map(create_labels,housing_data['US_HPI'], housing_data['US_HPI_future']))

housing_data['ma_apply_example'] = housing_data['M30'].rolling(10).apply(moving_average, raw=True)
housing_data.dropna(inplace=True)

X = np.array(housing_data.drop(['label', 'US_HPI_future'], 1))
X = preprocessing.scale(X)

y = np.array(housing_data['label'])

X_train, X_test, y_train, y_test = model_selection.train_test_split(X, y, test_size=0.2)

clf = svm.SVC(kernel='linear')
clf.fit(X_train, y_train)
print(clf.score(X_test, y_test))