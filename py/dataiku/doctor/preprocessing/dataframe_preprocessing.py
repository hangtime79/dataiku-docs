""" Preprocessing takes a dataframe as an input,
and returns a dataframe as an output.

At the end of the pipeline, the matrix underlying the dataframe
should be ready to use for scikit-learn's ML algorithm.

TODO add collector
"""

import logging
import pandas as pd
import re

from sklearn.cluster import KMeans


logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')


class Step(object):

    def __init__(self, output_name=None):
        self.output_name = output_name

    def fit(self, df, target=None, output_name=None):
        pass

    def fit_and_process(self, df, result,):
        self.fit(df,)
        return self.process(df, result)

    def process(self, df, result):
        df = self._process(df)
        if self.output_name is not None:
            result[self.output_name] = df
        return df

    def _process(self, df):
        raise NotImplementedError()

    def __str__(self,):
        return "Step:" + self.__class__.__name__


class DropNARows(Step):
    """ Drop null rows in dataframe """
    def _process(self, df):
        return df.dropna()


class ExtractColumn(Step):

    __slots__ = ('column_name', 'output_name')

    def __init__(self, column_name, output_name):
        self.column_name = column_name
        self.output_name = output_name

    def process(self, df, result):
        result[self.output_name] = df[self.column_name]
        del df[self.column_name]
        return df


class FeaturesPreprocessingStep(Step):
    """ Process each feature independantly with their very own preprocessing pipeline.

    The feature-wise preprocessing pipeline code is in series_preprocessing.py
    """
    __slots__ = ('feature_preprocessors', 'target_name', 'verbose')

    def __init__(self, feature_preprocessors, target_name=None, output_name=None, verbose=True):
        Step.__init__(self, output_name)
        self.feature_preprocessors = feature_preprocessors
        self.target_name = target_name
        self.verbose = verbose

    def fit(self, df,):
        target = None
        if self.target_name is not None:
            target = df[self.target_name]
        for feature_preprocessor in self.feature_preprocessors:
            if self.verbose:
                logging.info("----------------")
                logging.info("Fitting <%s>" % feature_preprocessor.column_name)
            column_serie = df[feature_preprocessor.column_name]
            feature_preprocessor.fit(column_serie, target=target)

    def _process(self, df,):
        dataframes = []
        for feature_preprocessor in self.feature_preprocessors:
            if self.verbose:
                logging.info("----------------")
                logging.info("Processing feature <%s>" % feature_preprocessor.column_name)
                logging.info(str(feature_preprocessor))
            column_serie = df[feature_preprocessor.column_name]
            try:
                processed_dataframe = feature_preprocessor.process(column_serie)
                processed_dataframe.reset_index(drop=True, inplace=True)
                logging.info("Processing feature <%s> dataframe size %s" % (feature_preprocessor.column_name, str(processed_dataframe.shape)))
            except Exception as e:
                print "ERROR while processing %s" % feature_preprocessor.column_name
                raise e
            dataframes.append(processed_dataframe)
        full_df =  pd.concat(dataframes, axis=1)
        logging.info("Processing output a dataframe of shape %s" % str(full_df.shape))
        return full_df


class SelectColumns(Step):

    __slots__ = ('prefix_patterns',)

    def __init__(self, patterns, output_name=None):
        Step.__init__(self, output_name=output_name)
        self.prefix_patterns = map(re.compile, patterns)

    def match(self, column):
        for ptn in self.prefix_patterns:
            if ptn.match(column):
                return True
        return False

    def _process(self, df):
        selected_columns = [
            column
            for column in df.columns
            if self.match(column)
        ]
        return df[selected_columns]


class DoNothing(Step):
    """ Can be useful to fill a result name"""

    def _process(self, df):
        return df


from pca import PCA


class PCAStep(Step):

    __slots__ = ('pca',)

    def __init__(self, pca, output_name=None):  # kept_variance, collector_data=None, normalize=True, ):
        Step.__init__(self, output_name)
        self.pca = pca
        #self.kept_variance = kept_variance
        #self.pca = PCA(kept_variance, collector_data=collector_data, normalize=normalize)

    def normalize(self, df,):
        pass

    def fit(self, df, target=None):
        """ Computes the PCA projection basis on df
        and stores it into the modeling project object.
        """
        logging.info("Starting PCA fit on dataframe of shape %s" % str(df.shape))
        self.pca.fit(df)
        logging.info("PCA fit done")

    def _process(self, df):
        return self.pca.transform(df)


def cubic_root(x):
    return x ** (1. / 3.)


def detect_outliers(df,
                    pca_kept_variance=0.9,
                    min_n=0,
                    min_cum_ratio=0.01):
    """ Removing outliers before learning a model

    It can be benefitial to remove outliers
    before performing cluster analysis.
    This is done using by
        - doing clustering on cubic root of the number
          of lines we have
    """
    pca = PCA(kept_variance=pca_kept_variance,
              normalize=True)
    logging.info("Outliers detection: fitting PCA")
    pca.fit(df)
    logging.info("Outliers detection: performing PCA")
    df_reduced = pca.transform(df)
    n_lines = df_reduced.shape[0]
    n_clusters = max(3, int(cubic_root(n_lines)))
    logging.info("Outliers detection: performing cubic-root kmeans on df %s" % str(df_reduced.shape))
    model = KMeans(n_clusters=n_clusters)
    labels = pd.Series(model.fit_predict(df_reduced.values))
    logging.info("Outliers detection: selecting mini-clusters")
    label_counts = pd.DataFrame(labels.value_counts(ascending=True))
    label_counts.columns = ["count"]
    label_counts["ratio"] = label_counts["count"] / label_counts["count"].sum()
    label_counts["cum_ratio"] = label_counts["ratio"].cumsum()
    label_counts["outlier"] = (label_counts["ratio"] < min_cum_ratio) | (label_counts["count"] < min_n)
    logging.info("Outliers detection: done")
    return labels.map(label_counts["outlier"])


class OutlierDetection(Step):

    __slots__ = ('result',
                 'pca_kept_variance',
                 'min_n',
                 'min_cum_ratio',
                 'outlier_name')

    def __init__(self,
                 pca_kept_variance,
                 min_n,
                 min_cum_ratio,
                 outlier_name='OUTLIERS',
                 output_name=None):
        Step.__init__(self, output_name=output_name)
        self.min_n = min_n
        self.min_cum_ratio = min_cum_ratio
        self.pca_kept_variance = pca_kept_variance
        self.outlier_name = outlier_name

    def process(self, df, result):
        outliers = detect_outliers(df, self.pca_kept_variance, self.min_n, self.min_cum_ratio)
        if self.outlier_name is not None:
            result[self.outlier_name] = outliers
        if outliers.sum() > 0:
            output_df = df[~outliers]
        else:
            output_df = df.copy()
        if self.output_name is not None:
            result[self.output_name] = output_df
        return output_df


class PreprocessingResult(dict):

    def __init__(self, retain=None):
        self.retain = retain

    def __setitem__(self, k, v):
        if self.retain is None or k in self.retain:
            dict.__setitem__(self, k, v)


class PreprocessingPipeline(object):

    __slots__ = ('steps', 'results')

    def __init__(self, steps):
        self.steps = steps
  
    def fit_and_process(self, df, *args, **kwargs):
        result = {}
        cur_df = df
        for step in self.steps:
            cur_df = step.fit_and_process(cur_df, result,)
        return result

    def process(self, df, retain=None):
        result = PreprocessingResult(retain=retain)
        cur_df = df
        for step in self.steps:
            cur_df = step.process(cur_df, result)
        return result
