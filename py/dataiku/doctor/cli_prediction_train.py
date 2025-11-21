# encoding: utf-8

"""
Execute a prediction training recipe.
Must be called in a Flow environment
"""

import sys
import logging
from dataiku import Dataset
from dataiku.doctor.utils import ProgressListener
from dataiku.doctor.entrypoints import prediction_train_and_score, prediction_preprocessonly
from dataiku.doctor import ModelingProject

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')


def main(model_folder, input_dataset, output_model_folder):
    modeling_project = ModelingProject.load_from_folder(model_folder)
    listener = ProgressListener()
    df = Dataset(input_dataset).get_dataframe(sampling = modeling_project.sampling,
                                              columns=modeling_project.input_columns(with_target=True))
    logging.info("Loaded input dataset. Shape %s,%s" % df.shape)
    assert modeling_project.modeling_params is not None
    (train, valid) = prediction_preprocessonly(modeling_project.core_params,
                                               modeling_project.preprocessing_params,
                                               output_model_folder,
                                               listener,
                                               df,
                                               with_target=True)
    target_map = modeling_project.preprocessing_params.get("target_remapping", {}).get("pd")
    prediction_train_and_score(train,
                               valid,
                               modeling_project.core_params,
                               modeling_project.modeling_params,
                               output_model_folder,
                               listener,
                               target_map)
    # Model is saved in prediction_preprocessing.
    # ... and yes it sucks!
    print output_model_folder


def usage():
    print """
    python cli_prediction_train.py <model_folder> <input_dataset> <output_model_folder>
    """


if __name__ == "__main__":
    try:
        (model_folder, input_dataset, output_model_folder) = sys.argv[1:]
        sys.exit()
    except:
        print help(sys.modules[__name__])
    main(model_folder, input_dataset, output_model_folder)
