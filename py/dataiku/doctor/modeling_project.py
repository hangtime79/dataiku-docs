from os import path as osp
import re
import cPickle as pickle
import pandas as pd
import numpy as np
import logging

from dataiku.core import dkujson as json
from .preprocessing import ContinuousImpactCoding, CategoricalImpactCoding
import constants
from .utils import strip_accents
from .utils import ProgressListener
from .preprocessing import PCA
from .preprocessing import FeaturePreprocessingPipeline, EmitSerie, ExtractColumn
from .preprocessing import PCAStep, FeaturesPreprocessingStep, OutlierDetection,\
    SelectColumns, DoNothing, DropNARows, PreprocessingPipeline, RemapValue


def load_relfilepath(basepath, relative_filepath):
    """ Returns None if the file does not exists """
    filepath = osp.join(basepath, relative_filepath)
    if osp.exists(filepath):
        return json.load_from_filepath(filepath)
    else:
        return None


def extract_input_columns(preprocessing_params, with_target=False, with_profiling=True):
    role_filter = {"INPUT"}
    if with_profiling:
        role_filter.add("PROFILING")
    if with_target:
        role_filter.add("TARGET")
    return [
        column_name
        for column_name, column_params in preprocessing_params["per_feature"].items()
        if column_params["role"] in role_filter
    ]


class ModelingProject(object):

    __slots__ = ('folder_path',
                 'core_params',
                 'preprocessing_params',
                 'collector_data',
                 '__resources',
                 '__model')

    def __init__(self,
                 folder_path,
                 core_params=None,
                 preprocessing_params=None,
                 collector_data=None,
                 modeling_params=None):
        self.folder_path = folder_path
        self.core_params = core_params
        self.preprocessing_params = preprocessing_params
        self.collector_data = collector_data
        self._impact_coders = None
        self.__resources = {}
        self.__model = None  # model cache

    @property
    def sampling(self,):
        default_sampling = {"samplingMethod": "FULL"}
        return self.core_params.get("sampling", default_sampling)
    
    def _resource_filepath(self, resource_name):
        return osp.join(self.folder_path, resource_name + ".pkl")

    def get_resource(self, resource_name,):
        """ Resources are just dictionaries pickled in a .pkl
        named after their resource name. """
        if resource_name in self.__resources:
            return self.__resources[resource_name]
        filepath = self._resource_filepath(resource_name)
        if osp.exists(filepath):
            with open(filepath, 'rb') as resource_file:
                self.__resources[resource_name] = pickle.load(resource_file)
        else:
            self.__resources[resource_name] = {}
        return self.__resources[resource_name]

    def _save_resource(self, resource_name):
        assert resource_name in self.__resources
        resource = self.__resources[resource_name]
        if len(resource):
            # we only save non-empty resources
            with open(self._resource_filepath(resource_name), "wb") as resource_file:
                pickle.dump(resource, resource_file, 2)

    def open(self, relative_filepath, *args, **kargs):
        """ open a file relatively to self.folder_path"""
        filepath = osp.join(self.folder_path, relative_filepath)
        return open(filepath, *args, **kargs)

    def input_columns(self, with_target=True, with_profiling=True):
        """ Return the list of input features.

        Can help limit RAM usage, by giving that
        to get_dataframe.

        (includes profiling columns)
        """
        return extract_input_columns(self.preprocessing_params, with_target, with_profiling)

    @property
    def impact_coders(self,):
        return self.get_resource('impact')

    @property
    def pca(self,):
        return self.get_resource('pca')
    
    def _create_impact_coder(self, feature_name):
        raise NotImplementedError()

    def get_core_model(self,):
        if self.__model is None:
            with self.open(self.CORE_MODEL_FILE, "rb") as f:
                self.__model = pickle.load(f)
        return self.__model

    def get_impact_coder(self, feature_name,):
        if feature_name not in self.impact_coders:
            self.impact_coders[feature_name] = self._create_impact_coder(feature_name)
        return self.impact_coders[feature_name]

    @property
    def prediction_type(self,):
        return self.core_params[constants.PREDICTION_TYPE]

    def _load_file(self, relative_filepath):
        return load_relfilepath(self.folder_path, relative_filepath)

    def _save_file(self, relative_filepath, obj):
        json.dump(self.open(relative_filepath, 'w'), obj)

    def load(self,):
        self.core_params = self._load_file("core_params.json")
        self.preprocessing_params = self._load_file("preprocessing_params.json")
        self.collector_data = self._load_file("collector_data.json")
        self.modeling_params = self._load_file("modeling_params.json")

    @staticmethod
    def load_from_folder(folder_path, model_type=None):
        if model_type is None:
            core_params = load_relfilepath(folder_path, "core_params.json")
            model_type = core_params[constants.PREDICTION_TYPE]
        modeling_project = MODELING_PROJECT_TYPE_MAP[model_type](folder_path)
        modeling_project.load()
        return modeling_project

    def save(self,):
        self._save_file("core_params.json", self.core_params)
        self._save_file("preprocessing_params.json", self.preprocessing_params)
        self._save_file("collector_data.json", self.collector_data)
        for resource_name in self.__resources.keys():
            self._save_resource(resource_name)

    def build_feature_preprocessing_step(self, output_name=None, with_target=False, verbose=True):
        feature_preprocessors = []
        column_collectors = self.collector_data["per_feature"]
        FEATURE_FILTER = {"INPUT", "PROFILING"}
        if with_target:
            FEATURE_FILTER.add("TARGET")
        if not "feature_order" in self.collector_data:
            logging.warn("Emulating feature order ! Please retrain this model")
            self.collector_data["feature_order"] = self.preprocessing_params["per_feature"].keys()
        for column_name in self.collector_data["feature_order"]:
            column_param = self.preprocessing_params["per_feature"][column_name]
            role = column_param["role"]
            if role in FEATURE_FILTER:
                column_collector = column_collectors[column_name]
                feature_preprocessor = FeaturePreprocessingPipeline.from_params(
                    column_name,
                    column_param,
                    column_collector,
                    self,)
                if feature_preprocessor is not None:
                    feature_preprocessors.append(feature_preprocessor)
        if with_target:
            target_preprocessors = [RemapValue(self.target_map), EmitSerie()]
            feature_preprocessors.append(FeaturePreprocessingPipeline(self.target_variable, target_preprocessors))
        return FeaturesPreprocessingStep(
            feature_preprocessors,
            target_name=self.target_variable,
            output_name=output_name,
            verbose=verbose)

    def steps(self, verbose=True, **kwargs):
        raise NotImplementedError()

    def build_preprocessing_pipeline(self, *args, **kwargs):
        return PreprocessingPipeline(steps=list(self.steps(*args, **kwargs)))

    @property
    def target_variable(self,):
        return self.core_params.get(constants.TARGET_VARIABLE, None)


class PredictionProject(ModelingProject):

    CORE_MODEL_FILE = "clf.pkl"

    def _create_impact_coder(self, feature_name):
        raise NotImplementedError()

    def steps(self, with_target=False, verbose=True):
        yield self.build_feature_preprocessing_step(with_target=with_target, verbose=verbose)
        yield DropNARows()
        if with_target:
            yield ExtractColumn(
                column_name=self.target_variable,
                output_name="target")
        if self.preprocessing_params["reduce"]["enabled"]:
            kept_variance = self.preprocessing_params['reduce'].get('kept_variance', 0.9)
            if 'END_PCA' not in self.pca:
                self.pca['END_PCA'] = PCA(kept_variance=kept_variance, normalize=True)
            yield PCAStep(pca=self.pca['END_PCA'], output_name='TRAIN')
        else:
            yield DoNothing(output_name="TRAIN")

    def predict(self, df, listener=None, verbose=True):
        if listener is None:
            listener = ProgressListener()
        df = df.copy(deep=True)
        if self.target_variable in df:
            del df[self.target_variable]

        with listener.push_state("Preprocessing"):
            pipeline = self.build_preprocessing_pipeline(verbose=verbose)
            transformed = pipeline.process(df, retain={"TRAIN"})

        df = transformed["TRAIN"]
        
        # TODO PUT That in the pipeline?
        with listener.push_state("Loading model"):
            core_model = self.get_core_model()

        return self.Result(
            target_name=self.target_variable,
            target_map=self.target_map,
            core_model=core_model,
            transformed=transformed)


class PredictionResult(object):

    __slots__ = ('target_name', 'inverse_map', 'core_model', 'transformed',)

    def __init__(self, target_name, target_map, core_model, transformed):
        self.target_name = target_name
        self.inverse_map = {
            mapped_value: original_value
            for (original_value, mapped_value) in target_map.iteritems()
        }
        self.core_model = core_model
        self.transformed = transformed

    @property
    def prediction_column_name(self,):
        return "predicted_%s" % self.target_name

    def postprocess_prediction(self, predictions):
        return predictions

    @property
    def predictions(self,):
        features = self.transformed["TRAIN"]
        predictions = self.core_model.predict(features)
        predictions_remapped = self.postprocess_prediction(predictions)
        predictions = pd.DataFrame({
            self.prediction_column_name: predictions_remapped,
            'original_index': features.index
        })
        predictions = predictions.set_index('original_index')
        predictions.index.name = None
        return predictions


class ClassificationResult(PredictionResult):

    @property
    def probabilities(self,):
        features = self.transformed["TRAIN"]
        probabilities = self.core_model.predict_proba(features)
        class_predictions = []
        for i in xrange(probabilities.shape[1]):
            cleanedup_val = re.sub('[^a-zA-Z0-9]+', '_', strip_accents(self.inverse_map[i]))
            probability_column_name = '%s_proba_%s' % (self.prediction_column_name, cleanedup_val)
            class_predictions.append((probability_column_name, probabilities[:, i]))
        probabilities_df = pd.DataFrame.from_items(class_predictions + [('original_index', features.index)])
        probabilities_df = probabilities_df.set_index('original_index')
        probabilities_df.index.name = None
        return probabilities_df

    def postprocess_prediction(self, predictions):
        predictions_remapped = np.zeros(predictions.shape, dtype="object")
        for (mapped_value, original_value) in self.inverse_map.items():
            predictions_remapped[predictions == mapped_value] = original_value
        return predictions_remapped


class ClassificationProject(PredictionProject):

    Result = ClassificationResult

    def _create_impact_coder(self, feature_name):
        return CategoricalImpactCoding()

    @property
    def target_map(self, with_target=False):
        return self.preprocessing_params["target_remapping"]["pd"]


class RegressionResult(PredictionResult):
    pass


class RegressionProject(PredictionProject):

    Result = RegressionResult

    @property
    def target_map(self, with_target=False):
        return {}

    def _create_impact_coder(self, feature_name):
        feature_params = self.preprocessing_params["per_feature"][feature_name]
        impact_rescale = feature_params.get('rescaling', False)
        impact_scaler = feature_params.get('rescaling_method', None)
        return ContinuousImpactCoding(rescaling=impact_rescale, scaler=impact_scaler)


class ClusteringProject(ModelingProject):

    CORE_MODEL_FILE = "clusterer.pkl"

    def steps(self, verbose=True):
        """
        Build the preprocessing pipeline for clustering projects

        Clustering preprocessing is especially difficult from
        misc reasons, we need to keep track of the dataframe at different
        state of its processing :

        - train
            The model used for clustering performs on
            preprocessed INPUT columns, on which we
            may or may not remove outliers, and may
            or may not apply a PCA.

            * TRAIN

        - profiling
            Columns that are not actually INPUT should still
            be preprocessed (e.g. Dummified) in order to compute
            different statistics on the the different values.
            Such columns have a role called "PROFILING".

            Dataframe preprocessed, (including PROFILING columns)

            * PREPROCESSED

        - feature importance
            Feature importance is done by making a classification on
            the variables.
            In order to have its result human readable, we need
            to do this analysis on prepca values.

            * TRAIN_PREPCA

        - outliers
            The outliers labels is used to make sure we can
            reannotated the initial datasets (for feature importance
            and profiling)

            * OUTLIERS

        """
        yield SelectColumns(patterns=[
            "^" + col + "$"
            for col in self.input_columns(with_target=False, with_profiling=True)
        ], output_name="PROFILING")
        yield self.build_feature_preprocessing_step(verbose=verbose)
        yield DropNARows()

        # select input column
        prefixes_ptn = [input_column + "(?:\:.*)?" for input_column in self.input_columns(with_profiling=False)]
        yield SelectColumns(patterns=prefixes_ptn)

        kept_variance = self.preprocessing_params['reduce'].get('kept_variance')
        if kept_variance == 0.0:
            kept_variance = 0.9
        if self.preprocessing_params["outliers"]["method"] != "none":
            min_n = self.preprocessing_params['outliers']['min_n']
            min_cum_ratio = self.preprocessing_params['outliers']['min_cum_ratio']
            yield OutlierDetection(
                pca_kept_variance=kept_variance,
                min_n=min_n,
                min_cum_ratio=min_cum_ratio,
                outlier_name='OUTLIERS',
                output_name='TRAIN_PREPCA')
        else:
            yield DoNothing(output_name='TRAIN_PREPCA')
        if self.preprocessing_params["reduce"]["enabled"]:
            if 'END_PCA' not in self.pca:
                self.pca['END_PCA'] = PCA(kept_variance=kept_variance, normalize=True)
            yield PCAStep(pca=self.pca['END_PCA'], output_name='TRAIN')
        else:
            yield DoNothing(output_name='TRAIN')


MODELING_PROJECT_TYPE_MAP = {
    "classification": ClassificationProject,
    "multiclass": ClassificationProject,
    "regression": RegressionProject,
    "clustering": ClusteringProject
}
