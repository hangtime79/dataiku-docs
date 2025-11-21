## Base imports
import os

from dataiku.code_env_resources import clear_all_env_vars
from dataiku.code_env_resources import grant_permissions
from dataiku.code_env_resources import set_env_path
from dataiku.code_env_resources import set_env_var

# Clears all environment variables defined by previously run script
clear_all_env_vars()

## Hugging Face
# Set HuggingFace cache directory
set_env_path("HF_HOME", "huggingface")
set_env_path("TRANSFORMERS_CACHE", "huggingface/transformers")
hf_home_dir = os.getenv("HF_HOME")
transformers_home_dir = os.getenv("TRANSFORMERS_CACHE")

# Import Hugging Face's transformers
import transformers

# Download pre-trained models
model_name = "distilbert-base-uncased"
MODEL_REVISION = "1c4513b2eedbda136f57676a34eea67aba266e5c"
model = transformers.DistilBertModel.from_pretrained(model_name, revision=MODEL_REVISION)
unmasker = transformers.DistilBertForMaskedLM.from_pretrained(model_name, revision=MODEL_REVISION)
tokenizer = transformers.DistilBertTokenizer.from_pretrained(model_name, revision=MODEL_REVISION)

# Grant everyone read access to pre-trained models in the HF_HOME folder
# (by default, only readable by the owner)
grant_permissions(hf_home_dir)
grant_permissions(transformers_home_dir)