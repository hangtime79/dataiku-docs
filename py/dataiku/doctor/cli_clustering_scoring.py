# encoding: utf-8

"""
Execute a clustering scoring recipe.
Must be called in a Flow environment
"""

import os.path as osp
import logging
import pandas as pd
from dataiku import Dataset
from dataiku.core import dkujson as json
from dataiku.doctor.utils import magic_main
from .modeling_project import ModelingProject
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')


def iter_output_df(modeling_project, input_dataset):
    user_meta_path = osp.join(modeling_project.folder_path, "user_meta.json")

    cluster_name_map = None
    if osp.exists(user_meta_path):
        user_meta = json.load_from_filepath(user_meta_path)
        if "clusterMetas" in user_meta:
            cluster_name_map = {}
            print user_meta["clusterMetas"]
            for (cluster_id, cluster_data) in user_meta["clusterMetas"].items():
                cluster_name_map[cluster_id] = cluster_data["name"]

    def map_fun(i):
        if cluster_name_map is not None:
            return cluster_name_map["cluster_%i" % i]
        else:
            return "cluster_%i" %i

    pipeline = modeling_project.build_preprocessing_pipeline(verbose=False)
    core_model = modeling_project.get_core_model()
    for input_df in input_dataset.iter_dataframes(chunksize=100000,):
        if "cluster_labels" in input_df.columns:
            raise ValueError("Input dataset %s already contains a column named cluster_labels." % input_dataset)
        train_df = pipeline.process(input_df, retain=("TRAIN",))["TRAIN"]
        cluster_ids = core_model.predict(train_df)
        cluster_labels = pd.Series(data=cluster_ids,
                                   index=train_df.index,
                                   name="cluster_labels").map(map_fun)
        yield input_df.join(cluster_labels, how='left')


def main(model_folder, input_dataset_name, output_dataset_name):
    """
    Given a clustering model and an input dataset,
    computes the closest cluster, append it as a new column,
    and output the result dataset in output_dataset.
    """
    input_dataset = Dataset(input_dataset_name)

    modeling_project = ModelingProject.load_from_folder(model_folder, model_type="clustering")

    output_dataframes = iter_output_df(modeling_project, input_dataset)
    first_output_dataframe = output_dataframes.next()

    output_dataset = Dataset(output_dataset_name)
    output_dataset.write_schema_from_dataframe(first_output_dataframe)

    nb_lines_written = first_output_dataframe.shape[0]
    print "lines written :  %i" % nb_lines_written
    with output_dataset.get_writer() as writer:
        writer.write_dataframe(first_output_dataframe)
        for output_df in output_dataframes:
            writer.write_dataframe(output_df)
            nb_lines_written += output_df.shape[0]
            print "lines written :  %i" % nb_lines_written

if __name__ == "__main__":
    magic_main(main)
