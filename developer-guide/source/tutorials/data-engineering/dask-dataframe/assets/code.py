import dataiku
from dku_dask.utils import (
    extract_packages_list_from_pyenv, 
    s3_credentials_from_dataset,
    s3_path_from_dataset
)

from dask.distributed import Client, PipInstall
import dask.dataframe as dd

# Attach to the Dask cluster
# Note: <Cluster IP> is the Dask cluster endpoint determined during the Dask cluster setup steps.
dask_client = Client("<Dask Endpoint>")

# Install missing packages on the cluster 
# Note: <Dataiku code env name> is the name of the code environment created during the pre-requisites steps.
packages = extract_packages_list_from_pyenv("<Dataiku code env name>")
plugin = PipInstall(packages=packages, restart_workers=True)
dask_client.register_plugin(plugin)

# Retrieve Dataiku dataset as Dask DataFrame
## Get S3 credentials
access_key, secret_key, session_token = s3_credentials_from_dataset("avocado_transactions")
storage_options = {
    "key": access_key,
    "secret": secret_key,
    "token": session_token
}

## Get dataset S3 path
dataset_s3_path = s3_path_from_dataset("avocado_transactions")

## Read dataset as Dask DataFrame
df = dd.read_parquet(dataset_s3_path, aggregate_files=True, storage_options=storage_options)

# Perform a groupy manipulation on the DataFrame
result = df.groupby(["type"]).mean()
result.compute()