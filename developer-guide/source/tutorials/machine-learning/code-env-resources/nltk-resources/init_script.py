## Base imports
import os
from dataiku.code_env_resources import clear_all_env_vars
from dataiku.code_env_resources import set_env_path

# Clears all environment variables defined by previously run script
clear_all_env_vars()

## NLTK
# Set NLTK data directory
set_env_path("NLTK_DATA", "nltk_data")

# Import NLTK
import nltk

# Download model: automatically managed by NLTK, does not download
# anything if model is already in NLTK_DATA.
nltk.download('punkt', download_dir=os.environ["NLTK_DATA"])
