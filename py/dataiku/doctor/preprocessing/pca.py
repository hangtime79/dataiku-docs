from sklearn import decomposition
import pandas as pd
from dataframe_preprocessing import FeaturesPreprocessingStep
from series_preprocessing import FeaturePreprocessingPipeline, RescalingProcessor, EmitSerie


class PCA(object):
    """ Implements PCA for DataFrames.

    Supports pre-normalization given frozen parameters.
    A normalization step can be included before
    performing the PCA.
    """

    __slots__ = ('input_columns',
                 'output_columns',
                 'n_components',
                 'kept_variance',
                 'pca',
                 'prefix',
                 'stats',
                 'do_normalize')

    def __init__(self, kept_variance, normalize=False, prefix="factor_",):
        assert 0 < kept_variance < 1.0
        self.stats = {}
        self.do_normalize = normalize
        self.prefix = prefix
        self.kept_variance = kept_variance
        self.pca = decomposition.PCA(n_components=kept_variance)
        self.input_columns = None
        self.output_columns = None

    def get_stats(self, df, column_name):
        if column_name not in self.stats:
            series = df[column_name]
            self.stats[column_name] = (series.mean(), series.std())
        return self.stats[column_name]

    def normalize(self, df):
        assert self.input_columns is not None and len(self.input_columns) >= 1
        if self.do_normalize:
            feature_rescalers = []
            for column in self.input_columns:
                column_preprocessors = []
                stats = self.get_stats(df, column)
                if stats is not None:
                    (average, std) = stats
                    column_preprocessors.append(RescalingProcessor.from_avgstd(average, std))
                    column_preprocessors.append(EmitSerie())
                    feature_rescalers.append(FeaturePreprocessingPipeline(column, column_preprocessors))
            assert len(feature_rescalers) >= 1
            return FeaturesPreprocessingStep(feature_rescalers, verbose=False).process(df, {})
        else:
            # yeah, well no we don't normalize actually
            return df.copy()

    def fit_transform(self, df,):
        self.fit(df)
        return self.transform(df)

    def fit(self, df):
        self.input_columns = df.columns
        normalized_df = self.normalize(df)
        self.pca.fit(normalized_df)
        self.n_components = self.pca.components_.shape[0]
        self.output_columns = [
            self.prefix + str(i)
            for i in range(self.n_components)
        ]

    def transform(self, df):
        assert self.input_columns is not None and len(self.input_columns) >= 1
        normalize_df = self.normalize(df)
        projected_data = self.pca.transform(normalize_df)
        return pd.DataFrame(data=projected_data,
                                columns=self.output_columns,
                                index=df.index)
