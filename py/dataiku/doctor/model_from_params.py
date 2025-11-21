#!/usr/bin/env python
# encoding: utf-8
"""
model_trainer : trains the model, using the preprocessed validation set
"""

import numpy as np
import pandas as pd
import logging
from h2o import H2OModel
from forest import RandomForestRegressorIML, RandomForestClassifierIML
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import RidgeCV, LassoLarsIC, LinearRegression

h2o_algo_map = {
    'DEEP_LEARNING_H2O': 'DeepLearning',
    'GBM_H2O': 'GBM',
    'DISTRIBUTED_RF_H2O': 'DRF',
    'GLM_H2O': 'GLM2'
}

h2o_parameters = {
    'DeepLearning': {
        'destination_key': None,
        'source': None,
        'ignored_cols': None,
        'validation': None,
        'classification': None,
        'response': None,
        'expert_mode': None,
        'activation': None,
        'hidden': None,
        'epochs': None,
        'train_samples_per_iteration': None,
        'seed': None,
        'adaptive_rate': None,
        'rho': None,
        'epsilon': None,
        'rate': None,
        'rate_annealing': None,
        'rate_decay': None,
        'momentum_start': None,
        'momentum_ramp': None,
        'momentum_stable': None,
        'nesterov_accelerated_gradient': None,
        'input_dropout_ratio': None,
        'hidden_dropout_ratios': None,
        'l1': None,
        'l2': None,
        'max_w2': None,
        'initial_weight_distribution': None,
        'initial_weight_scale': None,
        'loss': None,
        'score_interval': None,
        'score_training_samples': None,
        'score_validation_samples': None,
        'score_duty_cycle': None,
        'classification_stop': None,
        'regression_stop': None,
        'quiet_mode': None,
        'max_confusion_matrix_size': None,
        'max_hit_ratio_k': None,
        'balance_classes': None,
        'max_after_balance_size': None,
        'score_validation_sampling': None,
        'diagnostics': None,
        'variable_importances': None,
        'fast_mode': None,
        'ignore_const_cols': None,
        'force_load_balance': None,
        'replicate_training_data': None,
        'single_node_mode': None,
        'shuffle_training_data': None,
    },
    'GBM': {
        'destination_key': None,
        'validation': None,
        'response': None,
        'source': None,
        'learn_rate': None,
        'ntrees': None,
        'max_depth': None,
        'min_rows': None,
        'ignored_cols_by_name': None,  # either this or cols..not both
        'cols': None,
        'nbins': None,
        'classification': None,
        'score_each_iteration': None,
        'grid_parallelism': None,
    },
    'DRF': {
        'destination_key': None,
        'source': None,
        # 'model': None,
        'response': None,
        'cols': None,
        'ignored_cols_by_name': None,
        'classification': 1,
        'validation': None,
        'importance': 1,  # enable variable importance by default
        'ntrees': None,
        'max_depth': None,
        'min_rows': None,  # how many rows in leaves for stopping condition
        'nbins': None,
        'mtries': None,
        'sample_rate': None,
        'seed': None,
        'build_tree_per_node': None,
        'score_each_iteration': None,
    },
    'GLM2': {
        'source': None,
        'destination_key': None,
        'response': None,
        # what about cols? doesn't exist?
        # what about ignored_cols_by_name
        'ignored_cols': None,
        'max_iter': None,
        'standardize': None,
        'family': None,
        # 'link': None, # apparently we don't get this for GLM2
        'alphas': 'alpha',
        'lambdas': 'lambda',
        'beta_epsilon': None,  # GLMGrid doesn't use this name
        'tweedie_variance_power': None,
        'n_folds': None,
        # 'weight': None,
        # 'thresholds': None,
        # only GLMGrid has this..we should complain about it on GLM?
        'parallelism': None,
        'beta_eps': None,
        'higher_accuracy': None,
        'use_all_factor_levels': None,
        'lambda_search': None,
    }
}


def classification_model_from_params(modeling_params):
    algorithm = modeling_params['algorithm']
    if algorithm == "SCIKIT_MODEL":
        return scikit_model(modeling_params)
    elif algorithm == "RANDOM_FOREST_CLASSIFICATION":
        if modeling_params["rf_max_tree_depth"] == 0:
            max_tree_depth = None
        else:
            max_tree_depth = modeling_params["rf_max_tree_depth"]
        if modeling_params['rf_estimators'] == 0:
            # automatically stop learning
            return RandomForestClassifierIML(n_jobs=modeling_params['rf_njobs'],
                                             random_state=1337,
                                             max_depth=max_tree_depth,
                                             min_samples_leaf=modeling_params["rf_min_samples_leaf"],
                                             min_samples_split=modeling_params["rf_min_samples_leaf"] * 3)
        else:
            return RandomForestClassifier(
                n_estimators=modeling_params['rf_estimators'],
                n_jobs=modeling_params['rf_njobs'],
                random_state=1337,
                max_depth=max_tree_depth,
                min_samples_leaf=modeling_params["rf_min_samples_leaf"],
                min_samples_split=modeling_params["rf_min_samples_leaf"] * 3,
                verbose=0)
    elif algorithm == "LOGISTIC_REGRESSION":
        return LogisticRegression(penalty=modeling_params['logit_penalty'],
                                  C=modeling_params['C'],
                                  random_state=1337)
    elif algorithm == "SVC_CLASSIFICATION":
        return SVC(C=modeling_params['C'],
                   kernel=str(modeling_params['kernel']),
                   gamma=modeling_params['gamma'],
                   coef0=modeling_params['coef0'],
                   tol=modeling_params['tol'],
                   probability=True,
                   max_iter=modeling_params['max_iter'],
                   verbose=0)
    elif algorithm == "SGD_CLASSIFICATION":
        return SGDClassifier(
            alpha=min(0.0001, modeling_params['alpha']),
            l1_ratio=modeling_params['l1_ratio'],
            loss=str(modeling_params['loss']),
            penalty=modeling_params['penalty'],
            shuffle=True,
            n_iter=modeling_params['max_iter'],
            epsilon=0.01,
            n_jobs=modeling_params['n_jobs'])
    elif "H2O" in algorithm:
        algo = h2o_algo_map[algorithm]
        parameters_allowed = h2o_parameters[algo]
        params = {}
        for k in modeling_params:
            if k in parameters_allowed:
                dest_key = parameters_allowed[k] if parameters_allowed[k] else k
                params[dest_key] = modeling_params[k]
        return H2OModel(
            algo=algo,
            fit_params=params,
            is_classification=True,
            base_url=modeling_params['h2o_url'])
    else:
        raise Exception("Invalid algorithm: %s" % algorithm)


def scikit_model(modeling_params):
    code = modeling_params['scikit_clf']
    exec(code)
    return clf

def train_classification_model(modeling_params, train):
    train_X = train["TRAIN"]
    train_Y = train["target"]
    clf = classification_model_from_params(modeling_params)
    if modeling_params["algorithm"] in {'RANDOM_FOREST_CLASSIFICATION', 'SVC_CLASSIFICATION', 'SGD_CLASSIFICATION'}:
        # Compute instance weight
        unique_values = np.unique(train_Y)
        d = {}
        for y in unique_values:
            d[y] = float(len(train_Y)) / np.sum(train_Y == y)
        weights = pd.Series(train_Y).map(d)
        clf.fit(train_X, train_Y, sample_weight=np.array(weights))
    else:
        clf.fit(train_X, train_Y)
    return clf


def regression_model_from_params(modeling_params):
    algorithm = modeling_params['algorithm']
    if algorithm == "SCIKIT_MODEL":
        return scikit_model(modeling_params)
    elif algorithm == "RANDOM_FOREST_REGRESSION":
        if modeling_params["rf_max_tree_depth"] == 0:
            max_tree_depth = None
        else:
            max_tree_depth = modeling_params["rf_max_tree_depth"]
        if modeling_params['rf_estimators'] == 0:
            return RandomForestRegressorIML(n_jobs=modeling_params['rf_njobs'],
                                            random_state=1337,
                                            max_depth=max_tree_depth,
                                            min_samples_leaf=modeling_params["rf_min_samples_leaf"],
                                            min_samples_split=modeling_params["rf_min_samples_leaf"] * 3)
        else:
            return RandomForestRegressor(
                n_estimators=modeling_params['rf_estimators'],
                n_jobs=modeling_params['rf_njobs'],
                random_state=1337,
                max_depth=max_tree_depth,
                min_samples_leaf=modeling_params["rf_min_samples_leaf"],
                min_samples_split=modeling_params["rf_min_samples_leaf"] * 3)
    elif algorithm == "RIDGE_REGRESSION":
        return RidgeCV(fit_intercept=True, normalize=True)
    elif algorithm == "LASSO_REGRESSION":
        return LassoLarsIC(fit_intercept=True, normalize=True, copy_X=True)
    elif algorithm == "LEASTSQUARE_REGRESSION":
        return LinearRegression(fit_intercept=True, normalize=True)
    elif "H2O" in algorithm:
        algo = h2o_algo_map[algorithm]
        parameters_allowed = h2o_parameters[algo]
        params = {}
        for k in modeling_params:
            if k in parameters_allowed:
                dest_key = parameters_allowed[k] if parameters_allowed[k] else k
                params[dest_key] = modeling_params[k]
        return H2OModel(algo=algo,
                        fit_params=params,
                        is_classification=False,
                        base_url=modeling_params['h2o_url'])
    else:
        raise Exception("Invalid algorithm: %s" % algorithm)


from sklearn.cluster import KMeans, MiniBatchKMeans, Ward, DBSCAN, SpectralClustering


def clustering_model_from_params(modeling_params):
    algorithm = modeling_params['algorithm']
    k = int(modeling_params.get("k", 0))
    if algorithm == "SCIKIT_MODEL":
        return scikit_model(modeling_params)
    elif algorithm == 'KMEANS':
        logging.info("KMEANS %d %d " % (k, modeling_params["kmeans_njobs"]))
        return KMeans(n_clusters=k, n_jobs=1)
    elif algorithm == 'MiniBatchKMeans':
        return MiniBatchKMeans(n_clusters=k)
    elif algorithm == 'SPECTRAL':
        return SpectralClustering(n_clusters=k,
                                  affinity=modeling_params["affinity"],
                                  coef0=modeling_params.get("coef0"),
                                  gamma=modeling_params.get("gamma"))
    elif algorithm == 'WARD':
        return Ward(n_clusters=k)
    elif algorithm == 'DBSCAN':
        return DBSCAN(eps=float(modeling_params["epsilon"]))
