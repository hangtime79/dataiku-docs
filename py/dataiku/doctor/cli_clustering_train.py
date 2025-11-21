# encoding: utf-8

"""
Execute a clustering training recipe.
Must be called in a Flow environment
"""

from dataiku import Dataset
from dataiku.doctor.utils import ProgressListener, magic_main
from dataiku.doctor import ModelingProject
from dataiku.core import dkujson as json
from .entrypoints import clustering_train_and_score, clustering_preprocess
from dataiku.core.dataset import FULL_SAMPLING
from os import path as osp
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')


def main(model_folder, input_dataset, output_model_folder):
    modeling_project = ModelingProject.load_from_folder(model_folder, model_type="clustering")
    sampling = modeling_project.core_params.get("sampling", FULL_SAMPLING)
    input_df = Dataset(input_dataset).get_dataframe(columns=modeling_project.input_columns(), sampling=sampling)
    listener = ProgressListener()
    
    # collector = ClusteringPreprocessingDataCollector(input_df, modeling_project.preprocessing_params)
    
    # TODO: UGLY as HELL
    # modeling_project.collector_data = collector.build()
    # pipeline = modeling_project.build_preprocessing_pipeline()
    # train_df = pipeline.fit_and_process(input_df)["TRAIN"]
    # (cluster_model, cluster_ids) = ClusteringTrainer(modeling_project.modeling_params, train_df).execute()

    preprocess_output = clustering_preprocess(
        modeling_project.core_params,
        modeling_project.preprocessing_params,
        output_model_folder,
        listener,
        input_df)

    result = clustering_train_and_score(
        preprocess_output,
        modeling_project.core_params,
        modeling_project.preprocessing_params,
        modeling_project.modeling_params,
        output_model_folder,
        listener)

    result_filepath = osp.join(output_model_folder, "results.json")
    json.dump_to_filepath(result_filepath, result)


if __name__ == "__main__":
    magic_main(main)
