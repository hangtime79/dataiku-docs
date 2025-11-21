""" Feature-wise preprocessing pipeline.

Picks each feature independantly and preprocess it into
one (eg. Impact coded column) or more columns (eg. Dummifed columns).
"""
from collections import OrderedDict
import pandas as pd
from .. import constants
import logging
import numpy as np
from dataiku.doctor.utils import datetime_to_epoch
from sklearn.feature_extraction.text import HashingVectorizer
import scipy


def is_series_like(series):
    return isinstance(series, pd.Series) or isinstance(series, np.ndarray) or isinstance(series, scipy.sparse.csr.csr_matrix)


class DataFrameBuilder(object):
    """ A dataframe builder just receives columns
    to ultimately create a dataframe, respecting the
    insertion order.
    """

    __slots__ = ('prefix', 'columns',)

    def __init__(self, prefix=""):
        """ constructor

        prefix -- Prefixes the name of the column of
                  the resulting dataframe.
        """
        # TODO put the prefix in to_dataframe
        self.columns = OrderedDict()
        self.prefix = prefix

    def add_column(self, column_name, column_values):
        assert column_name not in self.columns
        assert is_series_like(column_values)
        self.columns[column_name] = column_values

    def to_dataframe(self,):
        df = pd.DataFrame(self.columns)
        df.columns = [
            self.prefix + ":" + col if col is not None else self.prefix
            for col in df.columns
        ]
        return df.dropna()


class FeaturePreprocessingPipeline(object):

    """ Processing of a single feature. """

    __slots__ = ('column_name', 'preprocessing_steps',)

    def __init__(self, column_name, preprocessing_steps,):
        self.column_name = column_name
        self.preprocessing_steps = preprocessing_steps

    def fit(self, serie, target=None):
        self.fit_and_process(serie, target)

    def __str__(self):
        s = "\n"
        for step in self.preprocessing_steps:
            s += "   - " + str(step) + "\n"
        return s

    def fit_and_process(self, series, target=None):
        df_builder = DataFrameBuilder(prefix=self.column_name)
        for step in self.preprocessing_steps:
            logging.info("   " + str(step))
            series = step.fit_and_process(series, df_builder=df_builder, target=target)
            assert is_series_like(series), "Processor " + str(step) + " did not return a series-like object."
        return df_builder.to_dataframe()

    def process(self, series):
        try:
            df_builder = DataFrameBuilder(prefix=self.column_name)
            for step in self.preprocessing_steps:
                series = step.process(series, df_builder)
                assert is_series_like(series), str(step) + " did not return a series-like object." + str(series)
            return df_builder.to_dataframe()
        except Exception as e:
            logging.error("!Error while preprocessing feature %s " % self.column_name)
            logging.error("--------------------")
            logging.error(str(self))
            raise e

    @staticmethod
    def from_params(column_name, column_params, column_collector, modeling_project):
        role = column_params["role"]
        if role == "PROFILING":
            return FeaturePreprocessingPipeline._from_params_profiling(column_name,
                                                                       column_params,
                                                                       column_collector,
                                                                       modeling_project)
        elif role == "INPUT":
            return FeaturePreprocessingPipeline._from_params_input(column_name,
                                                                   column_params,
                                                                   column_collector,
                                                                   modeling_project)
        else:
            return None
    
    @staticmethod
    def _from_params_profiling(column_name, column_params, column_collector, modeling_project):
        # Coerce the type to either double or unicode
        # depending on how we decide to the detected type of the column.
        column_type = column_params["type"]
        coerce_type = {
            constants.NUMERIC: "double",
            constants.CATEGORY: "unicode",
            constants.TEXT : "unicode"
        }[column_type]
        preprocessors = [TypeCoercion(coerce_type)]
        if column_type == constants.CATEGORY:
            preprocessors.append(DummifyProcessor(column_collector[constants.CATEGORY_POSSIBLE_VALUES], add_other=True))
        elif column_type == constants.NUMERIC:
            preprocessors.append(EmitSerie())
            ## Ignoring others
        return FeaturePreprocessingPipeline(column_name, preprocessors)

    @staticmethod
    def _from_params_input(column_name, column_params, column_collector, modeling_project):
        # Coerce the type to either double or unicode
        # depending on how we decide to the detected type of the column.
        column_type = column_params["type"]
        coerce_type = {
            constants.NUMERIC: "double",
            constants.CATEGORY: "unicode",
            constants.TEXT: "unicode"
        }[column_type]
        preprocessors = [TypeCoercion(coerce_type)]
        missing_handling_method = column_params[constants.MISSING_HANDLING]
        # Process missing values.
        if missing_handling_method == constants.IMPUTE:
            preprocessors.append(ImputeMissingValue(column_collector))
        elif missing_handling_method == constants.FLAG:
            preprocessors.append(FlagMissingValue())
            return FeaturePreprocessingPipeline(column_name, preprocessors)
        else:
            # actually dropping the row will be done
            # at the end of processing.
            assert missing_handling_method == constants.DROP_ROW

        if column_type == constants.CATEGORY:
            method = column_params[constants.CATEGORY_HANDLING]
            if method == constants.DUMMIFY:
                preprocessors.append(DummifyProcessor(column_collector[constants.CATEGORY_POSSIBLE_VALUES], column_collector[constants.CATEGORY_NEED_OTHERS]))
            elif method == constants.IMPACT:
                impact_coder = modeling_project.get_impact_coder(column_name)
                preprocessors.append(ImpactCoding(impact_coder))
            else:
                raise ValueError("Category handling method %s is unknown" % method)
        elif column_type == constants.TEXT:
            #method = column_params[constants.TEXT_HANDLING]
            #if method == constants.TERM_HASH:
            preprocessors.append(HashTermCoding(column_name, 50))
            #else:
            #    raise ValueError("Text handling method %s is unknown" % method)
        else:
            assert column_type == constants.NUMERIC
            if column_params[constants.RESCALING]:
                # TODO Do we really want to use the collector for this?
                rescaling_method = column_params[constants.RESCALING_METHOD]
                if rescaling_method == constants.MINMAX:
                    min_value = column_collector["stats"]["min"]
                    max_value = column_collector["stats"]["max"]
                    preprocessors.append(RescalingProcessor.from_minmax(min_value, max_value))
                else:
                    avg_value = column_collector["stats"]["average"]
                    std_value = column_collector["stats"]["std"]
                    preprocessors.append(RescalingProcessor.from_avgstd(avg_value, std_value))
            preprocessors.append(EmitSerie())
        return FeaturePreprocessingPipeline(column_name, preprocessors)


class FeaturePreprocessingStep(object):

    __slots__ = tuple()

    def fit(self, serie, target):
        """
        Fit a preprocessing step.

        Some preprocessing actually need to be
        fitted. For instance impact coding, and PCA
        requires respectively to learn an impact coding map
        and a projection basis.
        """
        pass

    def fit_and_process(self, serie, df_builder, target=None):
        self.fit(serie, target)
        return self.process(serie, df_builder)

    def _process(self, serie, df_builder):
        """ returns a modified serie, pass
        to the next preprocessing step, and may
        emit output columns."""
        raise Exception("Not implemented")

    def __str__(self,):
        return self.__class__.__name__


class TypeCoercion(FeaturePreprocessingStep):

    __slots__ = ('coerce_type',)

    def __init__(self, coerce_type):
        self.coerce_type = coerce_type

    def __str__(self,):
        return "TypeCoercion(%s)" % str(self.coerce_type)

    def process(self, serie, df_builder):
        # if its a datetime, casting it to float
        # requires to compute the number of seconds
        # to EPOCH.
        if self.coerce_type == np.dtype(float) and serie.dtype == np.dtype('<M8[ns]'):
            return datetime_to_epoch(serie)
        else:
            return serie.astype(self.coerce_type)


class RemapValue(FeaturePreprocessingStep):

    __slots__ = ('values_map',)

    def __init__(self, values_map):
        self.values_map = {
            k.encode("utf-8"): v
            for k, v in values_map.items()
        }

    def process(self, serie, df_builder):
        if self.values_map:
            return serie.astype(str).map(self.values_map)
        else:
            return serie


class ImputeMissingValue(FeaturePreprocessingStep):

    __slots__ = ('impute_with_value',)

    def __init__(self, collector_data):
        impute_value = collector_data["missing_impute_with_value"]
        if isinstance(impute_value, unicode):
            self.impute_with_value = impute_value.encode("utf-8")
        else:
            self.impute_with_value = impute_value

    def process(self, serie, df_builder):
        return serie.fillna(self.impute_with_value)


class EmitSerie(FeaturePreprocessingStep):
    def process(self, series, df_builder):
        assert is_series_like(series)
        df_builder.add_column(None, series)
        return series


class ImpactCoding(FeaturePreprocessingStep):

    __slots__ = ('impact_coder',)

    def __init__(self, impact_coder):
        self.impact_coder = impact_coder

    def fit(self, serie, target=None):
        self.impact_coder.fit(serie, target)

    def process(self, serie, df_builder):
        df = self.impact_coder.transform(serie)
        for (column_name, serie) in df.iterkv():
            df_builder.add_column(column_name, serie)
        return serie


class FlagMissingValue(FeaturePreprocessingStep):

    def process(self, serie, df_builder):
        df_builder.add_column("not_missing", serie.notnull().astype(float))
        return serie


class RescalingProcessor(FeaturePreprocessingStep):

    __slots__ = ('do_fit', 'shift', 'inv_scale',)

    @staticmethod
    def from_minmax(min_value, max_value):
        return RescalingProcessor(shift=min_value, scale=(max_value - min_value))

    @staticmethod
    def from_avgstd(mean, standard_deviation):
        return RescalingProcessor(shift=mean, scale=standard_deviation)

    def __init__(self, shift=None, scale=None):
        if shift is scale is None:
            self.do_fit = True
        else:
            assert shift is not None and scale is not None
            self.do_fit = False
            self.shift = shift
            self.set_scale(scale)

    def set_scale(self, scale):
        if scale == 0.:
            # if there is not variance, just return a null-series
            self.inv_scale = 0.
        else:
            self.inv_scale = 1. / scale

    def fit(self, serie, target=None):
        if self.do_fit:
            self.shift = serie.mean()
            self.set_scale(serie.std())

    def process(self, serie, df_builder):
        return (serie - self.shift) * self.inv_scale

class FastSparseDummifyProcessor(FeaturePreprocessingStep):
    import scipy

    # Fast method to get the most common entries
    # %time common = df["fiBaseModel"].value_counts()[0:200].reset_index()["index"].values

    def __init__(self, values):
        self.values = [val.encode("utf-8") for val in values]

    def process(self, serie, df_builder):
        pass
        # Construct mapping tbale 
        #xmap = {}
        #for i in xrange(0, len(common)):
        #    xmap[common[i]] = i

        # Create an array of column index
        #%time labels_restricted= df["fiBaseModel"].map(xmap).fillna(len(common)).astype(np.int16)

        # NB: There is faster but we can't select
        # pd.factorize or manually with pandas.hashtable.PyObjectHAshTable + ObjectVector

        # Dense method:
        # np.eye + np.take
        # np.eye(len(common+1)).take(labels_restricted, axis=0)

        # Sparse method: This is the native CSR format.
        #%%time
        #from scipy import sparse
        #eye = np.eye(len(common) + 1, dtype=np.uint8)
        #matrixes = []
        #
        #nb_rows = len(labels_restricted)
        #
        #data = np.ones(nb_rows)
        #indptr = [y for y in xrange(nb_rows)]
        #
        #mat = scipy.sparse.csr_matrix((data, labels_restricted.values, indptr))

class DummifyProcessor(FeaturePreprocessingStep):

    __slots__ = ('values', 'add_other')

    def __init__(self, values, add_other):
        """
        Dummifies column.
        Create as many columns as there are values.

        If add_other is set to True, add an extra column
        to tell whether the value encounterred was not in
        "values".
        """
        self.values = [val.encode("utf-8") for val in values]
        self.add_other = add_other

    def dummy_column_name(self, value):
        return u"dummy:" + value.decode("utf-8")

    def process(self, serie, df_builder):
        mask = None
        for val in self.values:
            column_name = self.dummy_column_name(val)
            m = (serie == val)
            if mask is None:
                mask = m
            else:
                mask = mask | m
            df_builder.add_column(column_name, m.astype(float))
        if self.add_other:
            df_builder.add_column("Others", (~mask).astype(float))
        return serie

class HashTermCoding(FeaturePreprocessingStep):
    """
    Using the scikit feature text extraction with the hashing trick.
    http://scikit-learn.org/stable/modules/feature_extraction.html#vectorizing-a-large-text-corpus-with-the-hashing-trick
    """
    __slots__ = ('column_name', 'n_hash', 'n_features',  'pca')

    def __init__(self, column_name, n_features=10, n_hash=100000):
        self.n_features = n_features
        self.n_hash = n_hash
        self.column_name = column_name
        from sklearn import decomposition
        self.pca = decomposition.TruncatedSVD(n_components=self.n_features)

    def fit(self, serie, target=None):
        hv = HashingVectorizer(n_features=self.n_hash)
        self.pca.fit(hv.transform(serie[0:10000]))

    def process(self, serie, df_builder):
        hv = HashingVectorizer(n_features=self.n_hash)
        sparse = hv.transform(serie)
        transformed = self.pca.transform(sparse)
        for i in xrange(0, self.n_features):
            df_builder.add_column(":text:"+str(i), transformed[:,i])
        return serie