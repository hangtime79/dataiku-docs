"""
Execute clustering on a dataset (training+scoring)
Must be called in a Flow environment
"""

import logging
import pandas as pd
import numpy as np
from dataiku import Dataset
from .modeling_project import ModelingProject
from dataiku.doctor.utils import magic_main
from preprocessing_collector import ClusteringPreprocessingDataCollector
from model_from_params import clustering_model_from_params
from dataiku.core.dataset import FULL_SAMPLING


logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')


def main(model_folder, input_dataset, output_dataset):
    modeling_project = ModelingProject.load_from_folder(model_folder, model_type="clustering")
    sampling = modeling_project.core_params.get("sampling", FULL_SAMPLING)
    input_df = Dataset(input_dataset).get_dataframe(sampling=sampling)
    if "cluster_labels" in input_df.columns:
        raise ValueError("Input dataset %s already contains a column named cluster_labels." % input_dataset)
    collector = ClusteringPreprocessingDataCollector(input_df, modeling_project.preprocessing_params)
    # TODO: UGLY as HELL
    modeling_project.collector_data = collector.build()
    pipeline = modeling_project.build_preprocessing_pipeline()
    train_df = pipeline.fit_and_process(input_df, retain=("TRAIN",))["TRAIN"]
    cluster_model = clustering_model_from_params(modeling_project.modeling_params)
    cluster_ids = cluster_model.fit_predict(np.array(train_df)).astype(int)
    cluster_labels = pd.Series(data=cluster_ids,
                               index=train_df.index,
                               name="cluster_labels").map(lambda i: "cluster_%i" % i)
    results = input_df.join(cluster_labels, how='left')
    Dataset(output_dataset).write_with_schema(results)

if __name__ == "__main__":
    magic_main(main)
