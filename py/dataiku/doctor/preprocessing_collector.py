#!/usr/bin/env python
# encoding: utf-8

"""
Perform the initial feature analysis that will drive the actual preprocessor for prediction

Takes the preprocessing params and the train dataframe and outputs the feature analysis data.
"""


import logging
import json
from .utils import coerce_dataframe
import constants
from collections import Counter

NULL_CAT = 'NULL_Value'


class PreprocessingDataCollector(object):

    def __init__(self, train_df, preprocessing_params):
        self.df = train_df
        self.preprocessing_params = preprocessing_params
        logging.info("PREPROCE DATA COLL %s" % json.dumps(preprocessing_params))
        self.ret = {}

    def build(self):
        coerce_dataframe(self.df, self.preprocessing_params['per_feature'])
        self.ret["per_feature"] = {}
        # The feature_order array is used to ensure that we will always use
        # the same ordering accross the bench and all recipes using this
        # modeling project, to have consistent matrices between train and score
        self.ret["feature_order"] = []
        for vname in self.preprocessing_params["per_feature"].keys():
            self.ret["feature_order"].append(vname)
            per_feature_params = self.preprocessing_params["per_feature"][vname]
            if vname in self.df:
                self.ret["per_feature"][vname] = self.get_feature_analysis_data(vname, per_feature_params)
        # make sure that we end up with unicode string,
        # exactly as when we will reload these results from the disk.
        return json.loads(json.dumps(self.ret))

    def get_feature_analysis_data(self, name, params):
        """Analyzes a single feature (preprocessing params -> feature analysis data)
        params is the preprocessing params for this feature.
            It must contain:
            - name, type, role (role_reason)
            - missing_handling, missing_impute_with, category_handling, rescaling
            """
        output = {"stats": {}}
        logging.info("Looking at %s..." % name)
        series = self.df[name]
        
        # First collect basic stats
        if self.feature_needs_analysis(params):
            if params["type"] == 'NUMERIC':
                output['stats'] = {
                    'min': series.min(),
                    'average': series.mean(),
                    'median': series.median(),
                    'max': series.max(),
                    'p99': series.quantile(0.99),
                    'std': series.std()
                }

                #If we are imputing missings, get the actual value to impute with
                if params["missing_handling"] == "IMPUTE":
                    if params["missing_impute_with"] == "MEAN":
                        output["missing_impute_with_value"] = output["stats"]["average"]
                    elif params["missing_impute_with"] == "MEDIAN":
                        output["missing_impute_with_value"] = output["stats"]["median"]
            elif params["type"] == "CATEGORY":
                value_counts = series.value_counts()
                if len(value_counts) >= 0:
                    output['stats'].update({
                        'mostFrequentValue': value_counts.index[0],
                        'leastFrequentValue': value_counts.index[-1]
                    })
                else:
                    output['stats'].update({
                        'mostFrequentValue': NULL_CAT,
                        'leastFrequentValue': NULL_CAT
                    })
                missing_handling = params["missing_handling"]
                #If we are imputing missings, get the actual value to impute with
                if missing_handling == "IMPUTE":
                    if params["missing_impute_with"] == "MODE":
                        output["missing_impute_with_value"] = output["stats"]["mostFrequentValue"]
                    elif params["missing_impute_with"] == "CREATE_CATEGORY":
                        # Need to fixup the stats
                        nulls = series.isnull().sum()
                        output["stats"]["mostFrequentValue"] = value_counts.index[0] if value_counts.ix[0] >= nulls else NULL_CAT
                        output["stats"]["leastFrequentValue"] = value_counts.index[-1] if value_counts.ix[-1] <= nulls else NULL_CAT
                        output["missing_impute_with_value"] = NULL_CAT

                # If we are dummifying, get the "known" values in the train set and save them
                if missing_handling != "FLAG":
                    c = series.nunique()
                    output["category_cardinality_in_train"] = c
                    if params["category_handling"] == "DUMMIFY":
                        #  handle max_nb_categories
                        try:
                            nb_categories = int(params["max_nb_categories"])
                        except:
                            nb_categories = 50
                        if params["missing_handling"] == "IMPUTE" and params["missing_impute_with"] == "CREATE_CATEGORY":
                            series = series.fillna(NULL_CAT)
                        most_frequent_categories = Counter(series)
                        if len(most_frequent_categories) == 2:
                            # if we have only 2 categories, it makes sense to go with the nb categories -1 solution
                            nb_categories = 1
                        output[constants.CATEGORY_POSSIBLE_VALUES] = [
                            k for (k, v) in most_frequent_categories.most_common(nb_categories)
                        ]
                        output[constants.CATEGORY_NEED_OTHERS] = (len(most_frequent_categories) > nb_categories) and (len(most_frequent_categories) > 50)
            elif params["type"] == "TEXT":
                output["missing_impute_with_value"] = ""
        return output


class PredictionPreprocessingDataCollector(PreprocessingDataCollector):
    def __init__(self, train_df, preprocessing_params):
        PreprocessingDataCollector.__init__(self, train_df, preprocessing_params)

    def feature_needs_analysis(self, params):
        """params is the params object from preprocessing params"""
        return params["role"] == "INPUT"


class ClusteringPreprocessingDataCollector(PreprocessingDataCollector):
    def __init__(self, train_df, preprocessing_params):
        PreprocessingDataCollector.__init__(self, train_df, preprocessing_params)

    def feature_needs_analysis(self, params):
        """params is the params object from preprocessing params"""
        return params["role"] in ("INPUT", "PROFILING")
