######################## Base imports #################################
import logging
import os
import shutil

from dataiku.code_env_resources import clear_all_env_vars
from dataiku.code_env_resources import grant_permissions
from dataiku.code_env_resources import set_env_path
from dataiku.code_env_resources import set_env_var
from dataiku.code_env_resources import update_models_meta

# Set-up logging
logging.basicConfig()
logger = logging.getLogger("code_env_resources")
logger.setLevel(logging.INFO)

# Clear all environment variables defined by a previously run script
clear_all_env_vars()

# Optionally restrict the GPUs this code environment can use (it can use all by default)
# set_env_var("CUDA_VISIBLE_DEVICES", "") # Hide all GPUs
# set_env_var("CUDA_VISIBLE_DEVICES", "0") # Allow only cuda:0
# set_env_var("CUDA_VISIBLE_DEVICES", "0,1") # Allow only cuda:0 & cuda:1

######################## Sentence Transformers #################################
# Set sentence_transformers cache directory
set_env_path("SENTENCE_TRANSFORMERS_HOME", "sentence_transformers")

import sentence_transformers

# Download pretrained models
MODELS_REPO_AND_REVISION = [
    ("DataikuNLP/average_word_embeddings_glove.6B.300d", "52d892b217016f53b6c717839bf62c746a658933"), 
    # Add other models you wish to download and make available as shown below (removing the # to uncomment):
    # ("bert-base-uncased", "b96743c503420c0858ad23fca994e670844c6c05"),
]

sentence_transformers_cache_dir = os.getenv("SENTENCE_TRANSFORMERS_HOME")
for (model_repo, revision) in MODELS_REPO_AND_REVISION:
    logger.info("Loading pretrained SentenceTransformer model: {}".format(model_repo))
    model_path = os.path.join(sentence_transformers_cache_dir, model_repo.replace("/", "_"))


    # This also skips same models with a different revision
    if not os.path.exists(model_path):
        model_path_tmp = sentence_transformers.util.snapshot_download(
            repo_id=model_repo,
            revision=revision,
            cache_dir=sentence_transformers_cache_dir,
            library_name="sentence-transformers",
            library_version=sentence_transformers.__version__,
            ignore_files=["flax_model.msgpack", "rust_model.ot", "tf_model.h5",],
        )
        os.rename(model_path_tmp, model_path)
    else:
        logger.info("Model already downloaded, skipping")
# Add text embedding models to the code-envs models meta-data
# (ensure that they are properly displayed in the feature handling)
update_models_meta()
# Grant everyone read access to pretrained models in sentence_transformers/ folder
# (by default, sentence transformers makes them only readable by the owner)
grant_permissions(sentence_transformers_cache_dir)