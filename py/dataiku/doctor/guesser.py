#!/usr/bin/env python
# encoding: utf-8

"""
Takes a dataframe and a target variable and returns:
 - preprocessing params
 - modeling params
 - basic stats used to compute these (cardinalities, missings)
"""

import logging
import numpy as np
from exception import DoctorException
import dataiku.core.pandasutils as pdu
import math
from dataiku.doctor.utils import datetime_to_epoch


# number limit for a category of the target
# feature to be considered a class.
NB_LIMIT_TARGET_CLASS = 2


def sanity_check(df):
    """ Check that the dataframe is not empty """
    if len(df) == 0:
        raise DoctorException('The input dataset is empty. Have you build it once?')


def handle_types(df, columns=None):
    """Cast inplace columns into float or string as required. """
    for col in df.columns:
        if df[col].dtype == np.dtype(float):
            pass  # OK
        elif df[col].dtype == np.dtype(int):
            df[col] = df[col].astype('double')
        elif df[col].dtype == np.dtype('<M8[ns]'):
            # pandas date, transform it to a float number of second
            # timedelta with EPOCH
            df[col] = datetime_to_epoch(df[col])
        else:
            df[col] = df[col].astype('unicode')
    return df


def at_least_n_cardinality(serie):
    return (serie.value_counts() >= NB_LIMIT_TARGET_CLASS).sum()


def get_feature_stats(df):
    """Basic extraction of variable types, cardinality, missings"""
    logging.info("Getting feature stats")
    stats = pdu.get_stats(df)
    logging.info("Done computing feature stats")
    result_stats = {}
    # TODO cleanup this so that the resulting
    # format is appearant to the reader (without insspecting get_stats)
    for stats_column in stats:
        # Work-around JSON serializability issues
        stats_column['data_type'] = stats_column["data_type"].name
        stats_column['cardinality'] = int(stats_column["cardinality"])
        stats_column['missings'] = int(stats_column["missings"])
        result_stats[stats_column["variable"]] = stats_column
    return result_stats


def guess_prediction_type(variable_type, cardinality, cardinality_more_than):
    """ Looking at the type and cardinality of the variable,
    decide whether we should approach prediciton as
        - binary classification,
        - multiclass classification
        - regression
    """
    if variable_type == "NUMERIC":
        if cardinality >= 10:
            logging.info("PROJTYPE: setting to regression")
            return "regression"
        else:
            logging.info("PROJTYPE: setting to classification despite NUMERIC because cardinality is %i" % cardinality)

    # The other stuff is classification.
    # we still need to know if it is multiclass
    # or binary classification
    # We will reject all classes with less than NB_LIMIT_TARGET_CLASS
    # samples.
    #
    # We therefore use cardinality_more_than
    # rather than the usual cardinality for this task.
    if cardinality_more_than < 2:
        raise ValueError("All the value of the target are equal!")
    elif cardinality_more_than == 2:
        logging.info("PROJTYPE: setting to classification")
        return "classification"
    else:
        return "multiclass"


def guess_missing(variable_type, nmiss, miss_ratio):
    """ returns information on what should be
    done with missing values. """
    if nmiss > 0:
        if miss_ratio > 0.5:
            return {"missing_handling": "FLAG"}
        else:
            if variable_type == "NUMERIC":
                return {
                    "missing_handling": "IMPUTE",
                    "missing_impute_with": "MEDIAN"
                }
            else:
                return {
                    "missing_handling": "IMPUTE",
                    "missing_impute_with": "MODE"
                }
    else:
        # There is no missing on this variable on the guess sample,
        # but we still mark it as impute with median/mode so that
        # if we find later a missing we now how to react
        if variable_type == "NUMERIC":
            return {
                "missing_handling": "IMPUTE",
                "missing_impute_with": "MEDIAN"
            }
        else:
            return {
                "missing_handling": "IMPUTE",
                "missing_impute_with": "MODE"
            }


def default_features_preprocessing(stats, nrows, rescaling_method=None, target_name=None):
    """Autodetect the feature preprocessing, for each of the features."""
    return {
        variable_name: default_feature_preprocessing(variable_name,
                                                     stats[variable_name],
                                                     nrows,
                                                     rescaling_method=rescaling_method,
                                                     target_name=target_name)
        for (variable_name, variable_stats) in stats.items()
    }




def default_feature_preprocessing(variable_name,
                                  variable_stats,
                                  nrows,
                                  rescaling_method=None,
                                  target_name=None):
    nmiss = variable_stats['missings']
    miss_ratio = float(nmiss) / nrows
    variable_type = variable_stats["type"]
    category_handling = None
    role_reason = None

    print "HANDLE %s VS %s " % (variable_name, target_name)

    # Rejects
    if variable_name == target_name:
        role = "TARGET"
    elif variable_stats["cardinality"] == 1:
        role = "REJECT"
        role_reason = "ZERO_VARIANCE"
    elif miss_ratio > 0.95:
        role = "REJECT"
        role_reason = "MISSING"
    elif variable_type == "CATEGORY":
        if variable_stats['cardinality'] <= min(0.5 * nrows, 10000):  # Limited as 50 by default anyway
            role = "INPUT"
            category_handling = "DUMMIFY"
        else:
            role = "REJECT"
            role_reason = "CATEGORY_CARDINALITY"
    elif variable_type == "TEXT":
        role = "INPUT"
        variable_type = "TEXT"
    else:
        role = "INPUT"

    res = {
        "name": variable_name,
        "type": variable_type,
        "role": role,
    }
    if rescaling_method is None:
        res["rescaling"] = False
    else:
        res.update({
            "rescaling": True,
            "rescaling_method": rescaling_method
        })
    if role == "INPUT":
        # Missings
        missing_policy = guess_missing(variable_type, nmiss, miss_ratio)
        res.update(missing_policy)
    if role_reason is not None:
        res["role_reason"] = role_reason
    if category_handling is not None:
        res["category_handling"] = category_handling
    if variable_type == "TEXT":
        res['text_handling'] = 'TERM_HASH'
    return res


def remap_target(df, target_variable,):
    freqs = list(df[target_variable].value_counts().iteritems())
    logging.info("Remapping: raw frequencies: %s" % freqs)

    # Force mapping in some cases
    if len(freqs) == 2:
        #values = [term for (term, count) in freqs]
        positive = {"yes", "1", "1.0", "true", "ok"}
        negative = {"no", "0", "0.0", "false", "nok"}

        def sort_key(term_count):
            (term, count) = term_count
            term_lower = str(term).lower()
            return ((term_lower in positive) - (term_lower in negative), -count)
        freqs.sort(key=sort_key)

    full_target_map = []
    pd_target_map = {}
    remapped_i = 0
    for (i, (term, count)) in enumerate(freqs):
        term_str = str(term)
        if term_str != "nan" and count >= NB_LIMIT_TARGET_CLASS:
            pd_target_map[term_str] = remapped_i
            full_target_map.append({
                'target_source_value': term_str,
                'target_mapped_value': remapped_i,
                'target_count': count
            })
            remapped_i += 1
    logging.info("Remapping: output: %s" % pd_target_map)
    if len(full_target_map) > 0:
        return {
            "pd": pd_target_map,
            "full": full_target_map
        }
    else:
        return None


# ---------------------------------------------------
# Prediction

def prediction_param_guesser(df, target_name, prediction_type=None):
    """ Returns an automatically detected prediction config.

    If prediction_type is None, also auto-detect the type of
    the prediction. Forcing prediction is used when the user actually
    use the combobox to, for instance, force a multiclass into a regression
    or the opposite.
    """
    nrows = df.shape[0]
    sanity_check(df)
    target = df[target_name]
    if prediction_type is None or prediction_type == "":
        variable_type = 'NUMERIC' if 'int' in str(target.dtype) or 'float' in str(target.dtype) else 'CATEGORY'
        cardinality = target.nunique()
        cardinality_more_than = at_least_n_cardinality(target)
        prediction_type = guess_prediction_type(variable_type, cardinality, cardinality_more_than)
    else:
        assert prediction_type in ('multiclass', 'classification', 'regression')
    if prediction_type == "regression":
        df[target_name] = target.astype(float)
    else:
        df[target_name] = target.astype(str)
    stats = get_feature_stats(df)
    handle_types(df)
    modeling_params = default_modeling_parameters(prediction_type, nrows, df.shape[1])
    per_feature_preprocessing = default_features_preprocessing(stats, nrows, target_name=target_name)
    preprocessing_params = {
        "per_feature": per_feature_preprocessing,
        "deduplication": {
            "enabled": False,
            "deduplicate_on": stats.keys()[0],
        },
        "reduce": {
            "enable": False,
            "disable": True,
            "kept_variance": 0.95
        }
    }
    if prediction_type in ("classification", "multiclass"):
        preprocessing_params["target_remapping"] = remap_target(df, target_name)
    return {
        "prediction_type": prediction_type,
        "modeling_params": modeling_params,
        "preprocessing_params": preprocessing_params,
        "sample_guess_stats": {
            "nrows": nrows,
            "features": stats
        },
        "crossval": {"samprate": 0.8},
    }


def default_modeling_parameters(prediction_type, nrows, ncols):
    njobs = nrows > 100000 and 1 or 2
    if prediction_type == "regression":
        return {
            "random_forest_regression": {
                "enabled": True,
                "n_estimators": [0],
                "max_tree_depth": 20 + int(math.sqrt(ncols)),
                "min_samples_leaf": max(1, int(math.sqrt(nrows) / 10)),
                "n_jobs": njobs
            },
            "ridge_regression": {
                "enabled": True
            },
            "deep_learning_h2o": {
                "enabled": False,
                "hidden": "100,100",
                "epochs": 10,
                "adaptative_rate": True,
                "rho": 0.95,
                "epsilon": 0.000001,
                "rate": 0.00001,
                "rate_annealing": 0,
                "input_dropout_ratio": 0,
                "hidden_dropout_ratios": 0,
                "l1": 0.0,
                "l2": 0.0
            },
            "distributed_rf_h20": {
                "enabled": False,
                "ntrees": 50,
                "max_depth": 5,
                "min_rows": 1,
                "sample_rate": 0.66666,
                "nbins": 20,
                "build_tree_one_node": False
            },
            "gbm_h2o": {
                "enabled": False,
                "learn_rate": 0.1,
                "ntrees": 50,
                "max_depth": 5,
                "min_rows": 10,
                "nbins": 20,
                "family": "AUTO",
                "grid_parallelism": 1
            },
            "glm_h2o": {
                "enabled": False,
                "max_iter": 10000,
                "standardize": True,
                "n_folds": 0,
                "tweedie_variance_power": 0.0,
                "family": "gaussian",
                "alpha": [0.5],
                "lambda": [0.0001],
                "beta_epsilon": 0.0001
            }
        }
    else:
        # for classification
        return {
            "random_forest_classification": {
                "enabled": True,
                "n_estimators": [0],
                "max_tree_depth": 8 + int(math.sqrt(ncols) * 2),
                "min_samples_leaf": nrows > 100000 and 10 or 1,
                "n_jobs": njobs
            },
            "logistic_regression": {
                "enabled": True,
                "l1": True,
                "C": [0.1]
            },
            'svc_classifier': {
                "enabled": (ncols > 100 and nrows < 10000),
                "linear": False,
                "rbf": True,
                "C": [1.0],
                "gamma": [0.],
                'tol': 0.00001,
                'max_iter': -1
            },
            'sgd_classifier': {
                'enabled': False,
                'modified_huber': False,
                'log': True,
                'elasticnet': False,
                'l1': True,
                'l2': False,
                'l1_ratio': 0.15,
                'alpha': 0.0001,
                'n_iter': max(5, 10000000 / nrows)
            },
            "deep_learning_h2o": {
                "enabled": False,
                "hidden": "100,100",
                "epochs": 10,
                "adaptative_rate": True,
                "rho": 0.95,
                "epsilon": 0.000001,
                "rate": 0.00001,
                "rate_annealing": 0,
                "input_dropout_ratio": 0,
                "hidden_dropout_ratios": 0,
                "l1": 0.0,
                "l2": 0.0
            },
            "distributed_rf_h20": {
                "enabled": False,
                "ntrees": 50,
                "max_depth": 5,
                "min_rows": 1,
                "sample_rate": 0.66666,
                "nbins": 20,
                "build_tree_one_node": False
            },
            "gbm_h2o": {
                "enabled": False,
                "learn_rate": 0.1,
                "ntrees": 50,
                "max_depth": 5,
                "min_rows": 10,
                "nbins": 20,
                "family": "AUTO",
                "grid_parallelism": 1
            }
        }


# -------------------------------------------------------
# clustering param guesser


def clustering_param_guesser(df):
    """ Returns an automatically detected prediction config.

    If prediction_type is None, also auto-detect the type of
    the prediction.
    """
    nrows = df.shape[0]
    sanity_check(df)
    handle_types(df)
    stats = get_feature_stats(df)
    modeling_params = {
        "kmeans_clustering": {
            "k": [5],
            "enabled": True
        },
        "mini_batch_kmeans_clustering": {
            "k": [3, 5],
            "enabled": False
        },
        "ward_clustering": {
            "k": [3, 5],
            "enabled": False
        },
        "spectral_clustering": {
            "k": [3, 5],
            "enabled": False,
            "coef0": 1.0,
            "gamma": [1.0],
        },
        "db_scan_clustering": {
            "epsilon": [0.5, 1.0],
            "enabled": False
        }
    }
    per_feature_preprocessing = default_features_preprocessing(stats, nrows, rescaling_method="AVGSTD")
    preprocessing_params = {
        "per_feature": per_feature_preprocessing,
        "deduplication": {
            "enabled": False,
            "deduplicate_on": stats.keys()[0],
        },
        "reduce": {
            "enable": False,
            "disable": True,
            "kept_variance": 0.95
        },
        "outliers": {
            "method": "cluster",
            "min_cum_ratio": 0.01,
            "min_n": int(nrows * 0.01)
        }
    }
    return {
        "modeling_params": modeling_params,
        "preprocessing_params": preprocessing_params,
        "sample_guess_stats": {
            "nrows": nrows,
            "features": stats
        },
        "crossval": {"samprate": 0.8},
    }
