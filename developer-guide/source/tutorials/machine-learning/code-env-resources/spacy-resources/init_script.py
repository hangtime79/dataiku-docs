## Base imports
from dataiku.code_env_resources import clear_all_env_vars

# Clears all environment variables defined by previously run script
clear_all_env_vars()

## SpaCy
# Import SpaCy
import spacy

# Download model: automatically managed by spacy, installs the model
# spacy pipeline as a Python package.
spacy.cli.download("en_core_web_sm")
