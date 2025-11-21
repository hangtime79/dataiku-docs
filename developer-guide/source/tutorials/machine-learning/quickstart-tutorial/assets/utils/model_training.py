"""model_training.py

This file contains ML modeling functions to grid search best hyper parameters of a Scikit-Learn model and cross evaluate a model.
"""

import numpy as np
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import cross_validate

def find_best_parameters(X, y, estimator, params, cv=5):
    """
    Performs a grid search on the sklearn estimator over a set of hyper parameters and return the best hyper parameters.
    
    :param pd.DataFrame X: The data to fit
    :param pd.Series y: the target variable to predict
    :param sklearn-estimator estimator: The scikit-learn model used to fit the data
    :param dict params: the set of hyper parameters to search on
    :param int cv: the number of folds to use for cross validation, default is 5
    
    :returns: the best hyper parameters
    :rtype: dict
    """
    grid = GridSearchCV(estimator, params, cv=cv)
    grid.fit(X, y)
    return grid.best_params_

def cross_validate_scores(X, y, estimator, cv=5, scoring=['accuracy']):
    """
    Performs a cross evaluation of the scikit learn model over n folds.
    
    :param pd.DataFrame X: The data to fit
    :param pd.Series y: the target variable to predict
    :param sklearn-estimator estimator: The scikit-learn model used to fit the data
    :param int cv: the number of folds to use for cross validation
    :param list scoring: the list of performance metrics to use to evaluate the model
    
    :returns: the average result for each performance metrics over the n folds
    :rtype: dict
    """
    cross_val = cross_validate(estimator, X, y, cv=cv, scoring=scoring)
    metrics_result = {}
    for metric in scoring:
        metrics_result[metric] = np.mean(cross_val['test_'+metric])
    return metrics_result