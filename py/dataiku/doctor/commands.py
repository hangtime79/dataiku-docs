""" Commands available from the doctor main kernel server.

To add a command, simple add a method.
Method starting by a _ are not exposed.

Arguments with default values are supported.
*args ,**kargs are not supported.

If one of your json parameter is a global in python, you
can suffix your parameter by an _ (e.g. input_)
"""

import sys
import inspect
import logging
from os import path as osp

from dataiku.core import dkujson as json
from dataiku import Dataset
from .entrypoints import prediction_preprocessonly, prediction_train_and_score
from .entrypoints import clustering_preprocess, clustering_train_and_score
from .utils import dataframe_cache
from .guesser import clustering_param_guesser, prediction_param_guesser
from .utils import ProgressListener, unix_time_millis
import constants
from .notebook_builder import PredictionNotebookBuilder, ClusteringNotebookBuilder
import pandas as pd
from dataiku.core.dataset import FULL_SAMPLING
from dataiku.doctor import modeling_project

preprocessing_listener = ProgressListener()
global_modeling_sets = []


def _to_progress(preprocessing_listener, modeling_listener):
    ret = json.loads(json.dumps(preprocessing_listener.to_jsonifiable()))
    if modeling_listener is not None:
        ret["stack"].extend(modeling_listener.stack)
        ret["top_level_todo"].extend(modeling_listener.top_level_todo)
        ret["top_level_done"].extend(modeling_listener.top_level_done)
    return ret


def _get_summarized_metrics(results):
    return {
        k: {
            "measure": v['measure'],
            "value": v['value']
        }
        for (k, v) in results['metrics'].iteritems()
        if 'metrics' in results
    }


def _list_commands():
    current_module = sys.modules[__name__]
    return [
        (func_name, func)
        for (func_name, func) in current_module.__dict__.iteritems()
        if not func_name.startswith("_") and inspect.isfunction(func) and inspect.getmodule(func) == current_module
    ]


def get_category_variable_distribution(input_params, variable):
    dataset = Dataset(input_params["dataset"], project_key=input_params["datasetProjectKey"])
    df = dataframe_cache.get_dataframe(dataset, limit=100000)
    counts = df[variable].value_counts().reset_index()[0:20]
    counts.columns = ['label', 'value']
    return json.loads(counts.to_json(orient="records"))


def heatmap(folder):
    return json.load(open(osp.join(folder, "heatmap.json"), "r"))


def facts(folder):
    return json.load(open(osp.join(folder, "facts.json"), "r"))


def get_scatterplot_points(folder, variable1, variable2):
    df = pd.read_pickle(osp.join(folder, "scatter_sample.pkl"))
    df = df[~df[variable1].isnull()]
    if (variable1 != variable2):
        df = df[['cluster_labels', variable1, variable2]]
        df = df[~df[variable2].isnull()]
    else:
        df = df[['cluster_labels', variable1]]
        df[variable1 + "_bis"] = df[variable1]
    outliers_color = len(df["cluster_labels"].unique()) - 1
    df = df[~df["cluster_labels"].isnull()]
    df['color'] = df['cluster_labels'].map(lambda x: int(str(x)[-1]) if x != constants.CLUSTER_OUTLIERS else outliers_color)
    df = df[~df["cluster_labels"].isnull()]
    return [
        {
            'cluster': cluster,
            'x': x,
            'y': y,
            'c': c
        }
        for (_, cluster, x, y, c) in df.itertuples()
    ]


def clustering_get_scatterplot(folder, variable1, variable2):
    scatter_points = get_scatterplot_points(folder, variable1, variable2)
    return {"points": scatter_points}


def guess_prediction_params(input_, target_variable, prediction_type):
    # We must clear the cache because a previous guess might have casted
    # the target and lost some data. We want guess to always use the pristine data
    # See #3361
    dataframe_cache.clear_cache()
    dataset = Dataset(input_["dataset"], project_key=input_["datasetProjectKey"])
    df = dataframe_cache.get_dataframe(dataset, sampling="head", limit=100000)
    return prediction_param_guesser(df, target_variable, prediction_type)


def guess_clustering_params(input_,):
    dataframe_cache.clear_cache()
    dataset = Dataset(input_["dataset"], project_key=input_["datasetProjectKey"])
    df = dataframe_cache.get_dataframe(dataset, sampling="head", limit=100000)
    return clustering_param_guesser(df)

# TODO : merge pred&clust notebook funcs


def create_prediction_notebook(bench_params,
                               core_params,
                               preprocessing_params,
                               modeling_params,):
    return PredictionNotebookBuilder(bench_params,
                                     core_params,
                                     preprocessing_params,
                                     modeling_params).create_notebook()


def create_clustering_notebook(bench_params,
                               core_params,
                               preprocessing_params,
                               modeling_params,):
    return ClusteringNotebookBuilder(bench_params,
                                     core_params,
                                     preprocessing_params,
                                     modeling_params).create_notebook()


def train_prediction_models(modeling_sets,
                            preprocessing_set,
                            preprocessing_run_folder,
                            core_params):
    # Fill all the listeners ASAP to have correct progress data
    preprocessing_listener.reset()
    preprocessing_listener.add_future_steps(constants.ALL_PREPROCESSING_STATES)
    for modeling_set in modeling_sets:
        listener = ProgressListener()
        listener.add_future_steps(constants.ALL_PREDICTION_TRAIN_STATES)
        global_modeling_sets.append(modeling_set)
        modeling_set["listener"] = listener

    logging.info("START TRAIN :" + preprocessing_set["description"])
    preprocessing_params = preprocessing_set["preprocessing_params"]

    with preprocessing_listener.push_state(constants.STATE_LOADING_SRC):
        # TODO is attaching a cache to the request handler life time a good idea?
        input_ = core_params["input"]
        sampling = core_params.get("sampling", FULL_SAMPLING)
        dataset = Dataset(input_["dataset"], project_key=input_["datasetProjectKey"])
        input_columns = modeling_project.extract_input_columns(preprocessing_params, with_target=True, with_profiling=False)
        df = dataframe_cache.get_dataframe(dataset,
                                           sampling=sampling,
                                           columns=input_columns)

    (train, valid) = prediction_preprocessonly(
        core_params,
        preprocessing_params,
        preprocessing_run_folder,
        preprocessing_listener,
        df,
        with_target=True)
    for modeling_set in modeling_sets:
        start = unix_time_millis()
        logging.info("--> Training %s " % (json.dumps(modeling_set["modelingParams"])))
        target_map = preprocessing_params.get("target_remapping", {}).get("pd")
        result = prediction_train_and_score(train,
                                            valid,
                                            core_params,
                                            modeling_set["modelingParams"],
                                            modeling_set["run_folder"],
                                            modeling_set["listener"],
                                            target_map)
        end = unix_time_millis()
        ellapsed = end - start
        algorithm = modeling_set["modelingParams"]["algorithm"]
        logging.info("TRAIN DONE: %s (%s) t=%d" % (modeling_set["run_folder"], algorithm, ellapsed))

        # Write the short status and the expanded params
        status = {
            "name": preprocessing_set["description"] + " - " + modeling_set["description"],
            "state": "DONE",
            "startTime": start,
            "endTime": unix_time_millis(),
            "metrics": _get_summarized_metrics(result)
        }
        status_filepath = osp.join(modeling_set["run_folder"], "short_status.json")
        json.dump_to_filepath(status_filepath, status)
        param_filepath = osp.join(modeling_set["run_folder"], "params.json")
        json.dump_to_filepath(param_filepath, modeling_set["modelingParams"])
    return "ok"


def train_clustering_models(core_params,
                            modeling_sets,
                            preprocessing_set,
                            preprocessing_run_folder):
     # Fill all the listeners ASAP to have correct progress data
    preprocessing_listener.reset()
    preprocessing_listener.add_future_steps(constants.ALL_PREPROCESSING_STATES)
    for modeling_set in modeling_sets:
        listener = ProgressListener()
        listener.add_future_steps(constants.ALL_CLUSTERING_TRAIN_STATES)
        modeling_set["listener"] = listener
        global_modeling_sets.append(modeling_set)

    logging.info("START TRAIN :" + preprocessing_set["description"])

    input_params = core_params["input"]
    sampling = core_params.get("sampling", FULL_SAMPLING)
    project_key = input_params["datasetProjectKey"]
    dataset_name = input_params["dataset"]
    preprocessing_params = preprocessing_set["preprocessing_params"]
    input_columns = modeling_project.extract_input_columns(preprocessing_params,
                                                           with_target=False,
                                                           with_profiling=True)
    dataset = Dataset(dataset_name, project_key=project_key)
    with preprocessing_listener.push_state(constants.STATE_LOADING_SRC):
        df = dataframe_cache.get_dataframe(dataset,
                                           columns=input_columns,
                                           sampling=sampling)
    preprocess_output = clustering_preprocess(
        core_params,
        preprocessing_params,
        preprocessing_run_folder,
        preprocessing_listener,
        df)

    assert sorted(preprocess_output.keys())[-3:] == ['PROFILING', 'TRAIN', 'TRAIN_PREPCA']

    for (i, ms) in enumerate(modeling_sets):
        logging.info("--> Training %s " % (json.dumps(ms["modelingParams"])))

        short_status = {
            "description": preprocessing_set["description"] + " - " + ms["description"],
            "startTime": unix_time_millis()
        }
        try:
            result = clustering_train_and_score(
                preprocess_output,
                core_params,
                preprocessing_params,
                ms["modelingParams"],
                ms["run_folder"],
                ms["listener"])
            result_filepath = osp.join(ms["run_folder"], "results.json")
            json.dump_to_filepath(result_filepath, result)
            short_status.update({
                "state": "DONE",
                "evaluationMetric": result.get("main_metric", {}).get("value", 0),
                "metrics": _get_summarized_metrics(result)
            })
        except Exception as e:
            logging.exception("Model processing failed")
            short_status["state"] = "FAILED"
            short_status["errorMessage"] = repr(e)

        short_status["progress"] = _to_progress(preprocessing_listener, ms["listener"])
        short_status["endTime"] = unix_time_millis()
        status_filepath = osp.join(ms["run_folder"], "short_status.json")
        json.dump_to_filepath(status_filepath, short_status)
    return "ok"


def get_current_train_progress(id_):
    logging.info("Getting progress for " + id_)
    ret = json.loads(json.dumps(preprocessing_listener.to_jsonifiable()))
    for modeling_set in global_modeling_sets:
        if modeling_set["modelingRunId"] == id_:
            ret["stack"].extend(modeling_set["listener"].stack)
            ret["top_level_todo"].extend(modeling_set["listener"].top_level_todo)
            ret["top_level_done"].extend(modeling_set["listener"].top_level_done)
            return ret
    logging.warning("Model noty found %s " % id_)
    return ret


def ping():
    return "pong"
