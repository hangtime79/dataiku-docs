from dataiku.core.dkujson import dump_to_filepath
from os import path as osp
import constants

from preprocessing_collector import PredictionPreprocessingDataCollector, ClusteringPreprocessingDataCollector
from model_from_params import classification_model_from_params, regression_model_from_params, clustering_model_from_params
from prediction_scorer import ClassificationModelScorer, RegressionModelScorer
from clustering_scorer import ClusteringModelScorer
from modeling_project import ClusteringProject, MODELING_PROJECT_TYPE_MAP
import deduplicator
import dataiku.core.pandasutils as pdu
import cPickle as pickle
from .utils import coerce_dataframe
import inspect
import numpy as np
import pandas as pd


def prediction_preprocessonly(
        core_params,
        preprocessing_params,
        run_folder,
        listener,
        df,
        with_target=False):
    with listener.push_state(constants.STATE_DEDUPLICATING):
        df = deduplicator.perform_dedup(df, preprocessing_params)

    with listener.push_state("Splitting for cross-validation"):
        train, valid = pdu.split_train_valid(df, prop=core_params["crossval"]["samprate"], seed=1337)

    with listener.push_state("Collecting preprocessing data"):
        collector = PredictionPreprocessingDataCollector(train, preprocessing_params)
        collector_data = collector.build()

    # Validation needs the same kind of type management as train !
    coerce_dataframe(valid, preprocessing_params['per_feature'])

    project_type = core_params[constants.PREDICTION_TYPE]  # regression | multiclass | classification
    modeling_project = MODELING_PROJECT_TYPE_MAP[project_type](
        folder_path=run_folder,
        core_params=core_params,
        preprocessing_params=preprocessing_params,
        collector_data=collector_data)
    pipeline = modeling_project.build_preprocessing_pipeline(with_target=with_target)
    with listener.push_state("Preprocessing train set"):
        transformed_train = pipeline.fit_and_process(train)
        modeling_project.save()

    with listener.push_state("Preprocessing validation set"):
        transformed_valid = pipeline.process(valid)

    return (transformed_train, transformed_valid)


def prediction_train_and_score(transformed_train,
                               transformed_valid,
                               core_params,
                               modeling_params,
                               run_folder,
                               listener,
                               target_map):
    """Trains one model and saves results to run_folder"""
    prediction_type = core_params["prediction_type"]

    train_X = transformed_train["TRAIN"]
    train_y = transformed_train["target"]

    if prediction_type in ("classification", "multiclass"):
        # TODO make it work for clustering as well
        with listener.push_state(constants.STATE_FITTING):
            model = classification_model_from_params(modeling_params)
            kwargs = {}
            if "sample_weight" in inspect.getargspec(model.fit).args:
                # Compute instance weight
                unique_values = np.unique(train_y)
                d = {
                    y: float(len(train_y)) / np.sum(train_y == y)
                    for y in unique_values
                }
                kwargs["sample_weight"] = np.array(pd.Series(train_y).map(d))
            model.fit(train_X, train_y, **kwargs)
            if hasattr(model, 'best_estimator_') and model.best_estimator_:
                model = model.best_estimator_
        with listener.push_state(constants.STATE_SAVING):
            with open(osp.join(run_folder, "clf.pkl"), "w") as f:
                pickle.dump(model, f, 2)
        with listener.push_state(constants.STATE_SCORING):
            results = ClassificationModelScorer(modeling_params, model, transformed_valid, target_map=target_map).score()
    elif prediction_type == "regression":
        with listener.push_state(constants.STATE_FITTING):
            model = regression_model_from_params(modeling_params)
            model.fit(train_X, train_y)
            if hasattr(model, 'best_estimator_') and model.best_estimator_:
                model = model.best_estimator_
        with listener.push_state(constants.STATE_SAVING):
            with open(osp.join(run_folder, "clf.pkl"), "w") as f:
                pickle.dump(model, f, 2)
        with listener.push_state(constants.STATE_SCORING):
            results = RegressionModelScorer(modeling_params, model, transformed_valid).score()
    else:
        raise ValueError("Prediction type %s is not valid" % prediction_type)
    (nb_records, nb_features) = train_X.shape
    results.update({
        "train_nb_records": nb_records,
        "train_nb_features": nb_features
    })
    dump_to_filepath(osp.join(run_folder, "results.json"), results)
    return results


def clustering_preprocess(core_params, preprocessing_params, run_folder, listener, df):
    """Performs preprocessing for a clustering. Returns tuple (train_df, trainnoacp_df, outliers_df)"""
    with listener.push_state(constants.STATE_DEDUPLICATING):
        df = deduplicator.perform_dedup(df, preprocessing_params)

    with listener.push_state("Collecting preprocessing data"):
        collector = ClusteringPreprocessingDataCollector(df, preprocessing_params)
        collector_data = collector.build()
        dump_to_filepath(osp.join(run_folder, "collector_data.json"), collector_data)

    modeling_project = ClusteringProject(
        folder_path=run_folder,
        core_params=core_params,
        preprocessing_params=preprocessing_params,
        collector_data=collector_data)

    pipeline = modeling_project.build_preprocessing_pipeline()
    with listener.push_state("Preprocessing train set"):
        results = pipeline.fit_and_process(df)
        # TODO move that somewhere else
        modeling_project.save()
    return results


def clustering_train_and_score(preprocessing_results,
                               core_params,
                               preprocessing_params,
                               modeling_params,
                               run_folder,
                               listener):
    """Trains one model and saves results to run_folder"""

    with listener.push_state(constants.STATE_FITTING):
        train = preprocessing_results["TRAIN"]
        cluster_model = clustering_model_from_params(modeling_params)
        cluster_labels_arr = cluster_model.fit_predict(np.array(train)).astype(int)
        cluster_labels = pd.Series(cluster_labels_arr, index=train.index, name='cluster_labels')
    with listener.push_state(constants.STATE_SAVING):
        with open(osp.join(run_folder, "clusterer.pkl"), "w") as f:
            pickle.dump(cluster_model, f, 2)
    with listener.push_state(constants.STATE_SCORING):
        results = ClusteringModelScorer(
            cluster_model,
            preprocessing_results,
            cluster_labels,
            preprocessing_params,
            run_folder).score()
        dump_to_filepath(osp.join(run_folder, "results.json"), results)
        return results
