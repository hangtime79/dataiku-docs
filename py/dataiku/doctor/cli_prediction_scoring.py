# encoding: utf-8

"""
Execute a prediction scoring recipe.
Must be called in a Flow environment
"""

import logging
from dataiku import Dataset
from dataiku.doctor.utils import magic_main, ProgressListener
from modeling_project import ModelingProject
from dataiku.core import debugging

debugging.install_handler()

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')


def iter_output_df(modeling_project, input_dataset):
    is_classification = modeling_project.prediction_type in {'classification', 'multiclass'}
    listener = ProgressListener(verbose=False)
    for input_df in input_dataset.iter_dataframes(chunksize=100000,):
        prediction_result = modeling_project.predict(input_df, verbose=False, listener=listener)
        result_dfs = [prediction_result.predictions]
        if is_classification:
            result_dfs.append(prediction_result.probabilities)
        yield input_df.join(result_dfs, how='left')


def main(model_folder, input_dataset_name, output_dataset_name):
    input_dataset = Dataset(input_dataset_name)
    modeling_project = ModelingProject.load_from_folder(model_folder)

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
