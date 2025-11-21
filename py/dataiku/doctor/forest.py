from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import RandomForestClassifier
from sklearn import cross_validation
from sklearn.metrics import f1_score
import pandas as pd
import multiprocessing
import logging


class IML(object):
    def model(self, params):
        return None

    def merge(self, clf2):
        return None

    def should_continue(self, Ytest, Y1, Y2):
        return False

    def __init__(self,  **params):
        self.params = params
        self.clf = None

    def fit(self, X, Y, sample_weight=None):
        if sample_weight is not None:
            Xt, Xtest, Yt, Ytest, sample_weightt, sample_weightest = cross_validation.train_test_split(X, Y, sample_weight, test_size=0.1, random_state=0)
        else:
            Xt, Xtest, Yt, Ytest  = cross_validation.train_test_split(X, Y, test_size=0.2, random_state=0)
            sample_weightt = None
            sample_weighttest = None

        self.clf = self.model(self.params)
        self.clf.fit(Xt, Yt, sample_weightt)
        Y1 = self.clf.predict(Xtest)
        should_stop_count = 0
        for i in xrange(0,1000):
            logging.info("IML training iteration %d (should_stop=%d)" % (i, should_stop_count))
            clf2 = self.model(self.params)
            clf2.fit(Xt, Yt, sample_weightt)
            self.merge(clf2)
            Y2 = self.clf.predict(Xtest)
            if not self.should_continue(Ytest, Y1, Y2):
                should_stop_count = should_stop_count + 1
            else:
                should_stop_count = 0
            if i > 3 and should_stop_count > 3:
                break
            Y1 = Y2

    def predict(self, X):
        return self.clf.predict(X)

    def predict_proba(self, X):
        return self.clf.predict_proba(X)

    def score(self, X, Y, sample_weight=None):
        return self.clf.score(X, Y) ## Sample Weight in 0.15

    @property
    def estimators_(self):
        return self.clf.estimators_

    @property
    def classes_(self):
        return self.clf.classes_

    @property
    def feature_importances_(self):
        return self.clf.feature_importances_

class RegressionIML(IML):
    def should_continue(self, Ytest, Y1, Y2):
        df = pd.DataFrame({"Ytest": Ytest, "Y1": Y1, "Y2": Y2})
        s1 = df[['Ytest', 'Y1']].corr()['Ytest'][1]
        s2 = df[['Ytest', 'Y2']].corr()['Ytest'][1]
        t =  (s2 / s1) > 1.01
        self.last_increase = (s2/s1)
        logging.info("IML run done, improved by %f", self.last_increase)
        return (s2 / s1) > 1.01

class ClassificationIML(IML):
    def should_continue(self, Ytest, Y1, Y2):
        s1 = f1_score(Ytest, Y1, average='weighted')
        s2 = f1_score(Ytest, Y2, average='weighted')
        self.last_increase = s2/s1
        logging.info("IML run done, improved by %f", self.last_increase)
        return self.last_increase > 1.01

class RandomForestRegressorIML(RegressionIML):
    """Random Forest with autostop of growing the forest"""
    i = 0
    def model(self, params):
        self.i = self.i + 1
        return RandomForestRegressor(**dict(params, random_state=params.get('random_state', 1234) + self.i, n_estimators=max(multiprocessing.cpu_count() -1, 1)))

    def merge(self, clf2):
        for e in clf2.estimators_:
            self.clf.estimators_.append(e)
            self.clf.n_estimators =self.clf.n_estimators + 1
        logging.info("Merg done, now have %d trees in forest", self.clf.n_estimators)

class RandomForestClassifierIML(ClassificationIML):
    """Random Forest with autostop of growing the forest"""
    i = 0
    def model(self, params):
        self.i = self.i + 1
        return RandomForestClassifier(**dict(params, random_state=params.get('random_state', 1234) + self.i, n_estimators=max(multiprocessing.cpu_count() -1, 1)))

    def merge(self, clf2):
        for e in clf2.estimators_:
            self.clf.estimators_.append(e)
            self.clf.n_estimators =self.clf.n_estimators + 1
        logging.info("Merg done, now have %d trees in forest", self.clf.n_estimators)


if __name__ == "__main__":
    import sklearn.datasets
    clf = RandomForestRegressorIML()
    for d in [sklearn.datasets.load_boston(), sklearn.datasets.load_diabetes()]:
        clf.fit(d.data, d.target)
        print "Auto score", clf.score(d.data, d.target)
        print "Last increatese", clf.last_increase
        print len(clf.estimators_)
    clf = RandomForestClassifierIML()
    for d in [sklearn.datasets.load_digits(9), sklearn.datasets.load_iris()]:
        clf.fit(d.data, d.target)
        print "Auto score", clf.score(d.data, d.target)
        print "Last increase", clf.last_increase
        print len(clf.estimators_)

