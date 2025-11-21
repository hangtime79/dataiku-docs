#import core, os, json

import warnings
warnings.filterwarnings("ignore", message="numpy.dtype size changed")
warnings.filterwarnings("ignore", message="numpy.ufunc size changed")
warnings.filterwarnings("ignore", message="The oldnumeric module")
warnings.filterwarnings("ignore", message="using a non-integer number")

import json
import os
import csv
from core.dataset import Dataset, get_schema_from_df,_dataset_writer_atexit_handler
from core import pandasutils
from core.sql import SQLExecutor


def in_ipython():
    try:
        __IPYTHON__
    except NameError:
        return False
    else:
        return True

try:
    import pandas as pd
    if in_ipython():
        # set display settings.
        pd.set_option('display.max_rows', 210)
        pd.set_option('display.max_columns', 210)
        pd.set_option('display.width', 8000)
except:
    pass

csv.field_size_limit(500 * 1024 * 1024)  # up to 500 MB.

if "DKUFLOW_VARIABLES" in os.environ:
    dku_flow_variables = json.loads(os.environ["DKUFLOW_VARIABLES"])
if "DKU_CUSTOM_VARIABLES" in os.environ:
    dku_custom_variables = json.loads(os.environ["DKU_CUSTOM_VARIABLES"])

__all__ = ["Dataset", "get_schema_from_df", "pandasutils", "dku_flow_variables","_dataset_writer_atexit_handler"]
