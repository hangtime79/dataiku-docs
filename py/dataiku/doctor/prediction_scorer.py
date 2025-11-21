#!/usr/bin/env python
# encoding: utf-8
"""
prediction_scorer : Takes a trained modeler, validation dataframe and outputs appropriate scoring data
"""

import logging

import numpy as np
import pandas as pd

from math import sqrt
from .utils.metrics import mroc_auc_score, log_loss
from sklearn.metrics import roc_curve, average_precision_score,\
                            accuracy_score, precision_score, f1_score,\
                            recall_score, matthews_corrcoef, hamming_loss,\
                            explained_variance_score, mean_absolute_error, mean_squared_error,\
                            r2_score, confusion_matrix
from utils.lift_curve import LiftBuilder
import dataiku.core.pandasutils as pdu
from collections import defaultdict, Counter


class PredictionModelScorer(object):
    def __init__(self, modeling_params, clf, valid):
        self.modeling_params = modeling_params
        self.clf = clf
        self.valid = valid
        self.ret = {"metrics": {}}

    def get_variables_importance(self):
        variables_imp = []
        if hasattr(self.clf, 'feature_importances_'):
            features = self.valid_X.columns
            for v, i in zip(features, self.clf.feature_importances_):
                imp = {'variable': v, 'importance': i}
                variables_imp.append(imp)
        return variables_imp
        
    def get_model_coefficients(self):
        model_coefficients = []
        if self.modeling_params['algorithm'] in {'LOGISTIC_REGRESSION', 'SGD_CLASSIFICATION', 'LEASTSQUARE_REGRESSION', 'RIDGE_REGRESSION', 'LASSO_REGRESSION'}:
            features = self.valid_X.columns
            if self.modeling_params['algorithm'] in {'LOGISTIC_REGRESSION', 'SGD_CLASSIFICATION'}:
                for v, i in zip(features, self.clf.coef_[0]):
                    coeff = {'variable': v, 'coefficient': i}
                    model_coefficients.append(coeff)
                if self.clf.intercept_ is not None:
                    intercept = self.clf.intercept_[0]
                    interc = {'variable': '__intercept__', 'coefficient': intercept}
                    model_coefficients.append(interc)
            elif self.modeling_params['algorithm'] in {'LEASTSQUARE_REGRESSION', 'RIDGE_REGRESSION', 'LASSO_REGRESSION'}:
                for v, i in zip(features, self.clf.coef_):
                    coeff = {'variable': v, 'coefficient': i}
                    model_coefficients.append(coeff)
                if self.clf.intercept_ is not None:
                    intercept = self.clf.intercept_
                    interc = {'variable': '__intercept__', 'coefficient': intercept}
                    model_coefficients.append(interc)
        return model_coefficients

    def add_metric(self, measure, value, description=""):
        self.ret["metrics"][measure] = {'measure': measure, 'value': value, 'description': description}


def trim_curve(curve, distance_threshold=0.05):
    """ Given a list of P_k=(x,y) curve points, remove points until there is no segemnt P_k , P_k+1
        that are smaller than distance_threshold. """
    yield curve[0]
    distance = 0
    for ((x_prev, y_prev), (x_next, y_next)) in zip(curve, curve[1:]):
        dx = x_next - x_prev
        dy = y_next - y_prev
        distance += sqrt(dx ** 2 + dy ** 2)
        if distance >= distance_threshold:
            yield x_next, y_next
            distance = 0
    if distance > 0:
        yield curve[-1]


class ClassificationModelScorer(PredictionModelScorer):

    def __init__(self, modeling_params, clf, valid, target_map=None):
        PredictionModelScorer.__init__(self, modeling_params, clf, valid)
        self.target_map = target_map
        self.multiclass = len(clf.classes_) > 2
        self.inv_map = {
            int(class_id): label
            for label, class_id in self.target_map.items()
        }
        self.classes = [class_label for (_, class_label) in sorted(self.inv_map.items())]

    def binary_roc_curve(self, class_actual, class_predicted):
        class_actual_id = int(self.target_map[class_actual])
        class_predicted_id = int(self.target_map[class_predicted])
        mask = np.in1d(self.valid_Y, np.array([class_actual_id, class_predicted_id]))
        positives = self.valid_Y.values[mask] == class_actual_id
        positives_values = sorted(np.unique(positives))
        if positives_values == [False, True]:
            false_positive_rates, true_positive_rates, thresholds = roc_curve(positives, self.probas[mask, class_actual_id])
            roc_data = zip(false_positive_rates, true_positive_rates)
            return [{"x": x, "y": y} for (x, y) in trim_curve(roc_data)]
        elif positives_values == [False]:
            return [{"x": 0, "y": 0}, {"x": 1, "y": 0}, {"x": 1, "y": 1}]
        else:
            return [{"x": 0, "y": 0}, {"x": 1, "y": 1}, {"x": 1, "y": 1}]

    def score(self):
        self.valid_X = self.valid["TRAIN"]
        self.valid_Y = self.valid["target"].astype(np.int)
        logging.info("Creating predictions on validation set")
        self.prevs = self.clf.predict(self.valid_X).astype(np.int)
        if self.target_map:
            self.mapped_prevs = np.zeros(self.prevs.shape, np.object)
            for k, v in self.target_map.items():
                self.mapped_prevs[self.prevs == v] = k
        else:
            self.mapped_prevs = self.prevs
        logging.info("Creating prediction probabilities on validation set for " + str(self.clf))
        try:
            probas_raw = self.clf.predict_proba(self.valid_X)
            (nb_rows, nb_present_classes) = probas_raw.shape
            self.probas = np.zeros((nb_rows, len(self.target_map)))
            for j in range(nb_present_classes):
                actual_class_id = self.clf.classes_[j]
                self.probas[:, actual_class_id] = probas_raw[:, j]
            self.ret["main_metric"] = {
                    "name": "AUC Score",
                    "value": mroc_auc_score(self.valid_Y, self.probas)
                }
        except:
            self.probas = None


        if hasattr(self.clf, "estimators_"):
            self.ret["n_estimators"] = len(self.clf.estimators_)
        logging.info("Calculated AUC for classification model")
        if not self.multiclass:
            if self.probas is not None:
                self.ret["confusions"] = self.get_confusion_matrix()
                logging.info("Calculated confusion matrix")
        else:
            self.ret["classes"] = self.classes
            self.ret["confusions_multiclass"] = self.get_multiclass_confusion_matrix()
            logging.info("Calculated confusion matrix")

        self.ret["variables_importance"] = self.get_variables_importance()
        logging.info("Calculated variables importance")
        
        self.ret["model_coefficients"] = self.get_model_coefficients()
        logging.info("Calculated model coefficients")

        if self.probas is not None:
            if self.multiclass:
                self.ret["multiclass_roc_curves"] = {
                    class_actual: {
                        class_predicted: self.binary_roc_curve(class_actual, class_predicted)
                        for class_predicted in self.classes
                    }
                    for class_actual in self.classes
                }
            else:
                false_positive_rates, true_positive_rates, thresholds = roc_curve(self.valid_Y, self.probas[:, 1])
                # full roc curve data
                roc_data = zip(false_positive_rates, true_positive_rates)
                # trim the data as we don't need all points for visualization
                self.ret["roc_viz_data"] = [{"x": x, "y": y} for (x, y) in trim_curve(roc_data)]

        # Lift curve
        if self.probas is not None:
            predicted = pd.Series(data=self.probas[:, 1], index=self.valid_X.index, name='predicted')
            results = pd.DataFrame({"__target__": self.valid_Y}).join(predicted)
            lb = LiftBuilder(results, '__target__', 'predicted')
        try:
            self.ret["lift_viz_data"] = lb.build()
        except:
            pass

        if self.probas is not None:
            self.add_metric("ROC - AUC Score", mroc_auc_score(self.valid_Y, self.probas), "From 0.5 (random model) to 1 (perfect model).")
        if not self.multiclass and self.probas is not None:
            self.add_metric('Average Precision Score', average_precision_score(self.valid_Y, self.probas[:, 1]), "Average precision for all classes")
        self.add_metric('Accuracy Score', accuracy_score(self.valid_Y, self.prevs), "Proportion of correct predictions (positive and negative) in the sample")
        self.add_metric('F1 Score', f1_score(self.valid_Y, self.prevs), "Harmonic mean of Precision and Recall")
        self.add_metric('Precision Score', precision_score(self.valid_Y, self.prevs), "Proportion of correct 'positive' predictions in the sample")
        self.add_metric('Recall Score', recall_score(self.valid_Y, self.prevs), "Proportion of catched 'positive' actual records in the predictions")
        #self.add_metric('Hinge Loss', hinge_loss(self.valid_Y, self.prevs))
        if not self.multiclass:
            self.add_metric('Matthews Correlation Coefficient', matthews_corrcoef(self.valid_Y, self.prevs), "The MCC is a correlation coefficient between actual and predicted classifications; +1 is perfect, -1 means no correlation")
        self.add_metric('Hamming Loss', hamming_loss(self.valid_Y, self.prevs), "The Hamming loss is the fraction of labels that are incorrectly predicted. (The lower the better)")
        #self.add_metric('Jaccard Similarity Score', jaccard_similarity_score(self.valid_Y, self.prevs))
        #self.add_metric('Zero One Loss', zero_one_loss(self.valid_Y, self.prevs))
        if self.probas is not None:
            self.add_metric('Log Loss', log_loss(self.valid_Y.values, self.probas), "Error metric that takes into account the predicted probabilities")
        return self.ret

    def get_multiclass_confusion_matrix(self,):
        assert self.prevs.shape == self.valid_Y.shape
        (nb_rows,) = self.prevs.shape
        class_ids = map(int, set(self.valid_Y).union(self.prevs))
        counters = defaultdict(Counter)
        count_actuals = Counter()
        for actual in self.valid_Y:
            count_actuals[actual] += 1
        for (actual, predicted) in zip(self.valid_Y, self.prevs):
            counters[actual][predicted] += 1
        return {
            "nb_rows": nb_rows,
            "counts": {
                self.inv_map[class_actual]: {
                    self.inv_map[class_predicted]: {
                        "actual": self.inv_map[int(class_actual)],
                        "count": counters[class_actual][class_predicted],
                        "ratio": counters[class_actual][class_predicted] / float(count_actuals[class_actual]) if count_actuals[class_actual] > 0.0 else "-", 
                    }
                    for class_predicted in class_ids
                }
                for class_actual in class_ids
            }
        }

    def get_confusion_matrix_given_cut(self, target, predict_proba, cut):
        decision = predict_proba > cut
        conf_matrix = confusion_matrix(decision, target)
        return {
            'cut': cut,
            'tp': conf_matrix[1, 1],
            'tn': conf_matrix[0, 0],
            'fp': conf_matrix[1, 0],
            'fn': conf_matrix[0, 1],
        }

    def get_confusion_matrix(self):
        predict_proba = pd.Series(data=self.probas[:, 1], index=self.valid_X.index, name='predicted')
        return [
            self.get_confusion_matrix_given_cut(self.valid_Y, predict_proba, cut)
            for cut in np.arange(0.05, 1., 0.05)
        ]


def mean_absolute_percentage_error(y_true, y_pred):
    return np.mean(np.abs((y_true - y_pred) / y_true))


class RegressionModelScorer(PredictionModelScorer):
    def __init__(self, modeling_params, clf, valid):
        PredictionModelScorer.__init__(self, modeling_params, clf, valid)

    def score(self):
        self.valid_X = self.valid["TRAIN"]
        self.valid_Y = self.valid["target"]
        
        logging.info("Creating predictions on validation set")
        self.prevs = self.clf.predict(self.valid_X)

        #self.ret["main_metric"] = {"name":"REMOVEME","value":0.0}#self.get_r2()

        self.ret["regression_performance"] = self.get_regression_performance()
        logging.info("Calculated regression performance")

        self.ret["variables_importance"] = self.get_variables_importance()
        logging.info("Calculated variables importance")
        
        self.ret["model_coefficients"] = self.get_model_coefficients()
        logging.info("Calculated model coefficients")

        if hasattr(self.clf, "estimators_"):
            self.ret["n_estimators"] = len(self.clf.estimators_)

        # Scatter plot
        reg = pd.Series(data=self.prevs, index=self.valid_X.index, name='predicted')
        act = pd.Series(data=self.valid_Y, index=self.valid_X.index, name='actual')
        both = pd.concat((act, reg), axis=1)
        nb_records = len(both.index)
        if nb_records < 1000:
            proba = 1
        else:
            proba = 1000.0 / nb_records
        s, m = pdu.split_train_valid(both, prop=proba)
        acc = []
        for record in s.itertuples():
            _acc = {'x': float(record[1]), 'y': float("%.4f" % record[2])}
            acc.append(_acc)
        self.ret["scatter_viz_data"] = acc
        self.add_metric('Explained Variance Score', explained_variance_score(self.valid_Y, self.prevs), "Best possible score is 1.0, lower values are worse")
        self.add_metric('Mean Average Percentage Error (MAPE)', mean_absolute_percentage_error(self.valid_Y, self.prevs), "")
        self.add_metric('Mean Absolute Error (MAE)', mean_absolute_error(self.valid_Y, self.prevs), "Mean absolute error regression loss")
        self.add_metric('Mean Squared Error (MSE)', mean_squared_error(self.valid_Y, self.prevs), "measures the average of the squares of the errors")
        self.add_metric('R2 Score', r2_score(self.valid_Y, self.prevs), "(coefficient of determination) regression score function.")
        self.add_metric('Pearson Correlation', self.get_pearson_correlation(), '')
        return self.ret

    def get_pearson_correlation(self):
        predicted = pd.Series(data=self.prevs, index=self.valid_X.index, name='predicted')
        results = pd.DataFrame({
            "__target__": self.valid_Y,
            "predicted": predicted
        })
        correlation = results[['predicted', '__target__']].corr()
        return correlation['predicted'][1]

    def get_regression_performance(self):
        # Base data
        predicted = pd.Series(data=self.prevs, index=self.valid_X.index, name='predicted')
        results = pd.DataFrame({
            "__target__": self.valid_Y,
            "predicted": predicted
        })
        # Error
        results['__error__'] = results['__target__'] - results['predicted']
        # Winsorize
        q = results['__error__'].quantile(0.98)
        results['__error__'] = results['__error__'].map(lambda x: q if x > q else x)
        # Cut
        results['__error_bin_id__'] = pd.cut(results['__error__'], 10).labels
        results['__error_bin_lb__'] = pd.cut(results['__error__'], 10)
        f = lambda row: '%s %s' % (row['__error_bin_id__'], row['__error_bin_lb__'])
        results['__error_bin__'] = results.apply(f, axis=1)
        # Agregate
        ags = results.groupby('__error_bin__')['__target__'].count().reset_index()
        ags.columns = ['error_bin', 'count']
        return [{
            'error_distribution': ags.to_json(orient='records'),
            'min_error': results['__error__'].min(),
            'p25_error': results['__error__'].quantile(.25),
            'median_error': results['__error__'].median(),
            'average_error': results['__error__'].mean(),
            'std_error': results['__error__'].std(),
            'p75_error': results['__error__'].quantile(.75),
            'p90_error': results['__error__'].quantile(.90),
            'max_error': results['__error__'].max(),
        }]
