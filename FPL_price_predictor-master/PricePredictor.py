import pickle

import pandas as pd
import numpy as np
from sklearn import svm, tree
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score


class PricePredictor:
    def __init__(self):
        # features are 'selected', 'transfers_balance', 'transfers_in', 'transfers_out', 'ict_index', 'value'
        self.train_data = pd.read_csv(r'train_data.csv')
        self.test_data = pd.read_csv(r'train_data.csv')
        self.train_label = np.array(self.train_data.pop('label'))
        self.test_label = np.array(self.test_data.pop('label'))
        self.test_data.pop('Unnamed: 0')
        self.test_data.pop('transfers_balance')
        self.train_data.pop('Unnamed: 0')
        self.train_data.pop('transfers_balance')
        self.train_data = np.array(self.train_data)
        self.test_data = np.array(self.test_data)
        # scaling data
        scalar = StandardScaler()
        self.test_data = scalar.fit_transform(self.test_data)
        self.train_data = scalar.fit_transform(self.train_data)
        del scalar

    def fit_svm(self):
        clf = svm.SVC()
        clf.fit(self.train_data, self.train_label)
        filename = 'svm_model.sav'
        pickle.dump(clf, open(filename, 'wb'))

    def predict_DTC(self):
        clf = tree.DecisionTreeClassifier(max_depth=20)
        clf.fit(self.train_data, self.train_label)
        predictions = clf.predict(self.test_data)
        print(accuracy_score(self.test_label, predictions) * 100)

    def predict_svm(self):
        clf = pickle.load(open('svm_model.sav', 'rb'))
        predictions = clf.predict(self.test_data)
        print(accuracy_score(self.test_label, predictions) * 100)

    # TODO save and load decision tree
