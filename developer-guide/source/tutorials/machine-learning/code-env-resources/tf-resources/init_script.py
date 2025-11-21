## Base imports
from dataiku.code_env_resources import clear_all_env_vars
from dataiku.code_env_resources import set_env_path
from dataiku.code_env_resources import set_env_var

# Clears all environment variables defined by previously run script
clear_all_env_vars()

## TensorFlow
# Set TensorFlow cache directory
set_env_path("TFHUB_CACHE_DIR", "tensorflow")

# Import TensorFlow Hub
import tensorflow_hub as hub

# Download pretrained model: automatically managed by Tensorflow,
# does not download anything if model is already in TFHUB_CACHE_DIR
model_hub_url = "https://tfhub.dev/google/tf2-preview/mobilenet_v2/classification/4"
hub.KerasLayer(model_hub_url)
