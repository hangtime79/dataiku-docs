import dataiku
from dku_ray.utils import (
    s3_path_from_managed_folder,
    s3_credentials_from_managed_folder,
    s3_path_from_dataset, 
    s3_credentials_from_dataset, 
    copy_project_lib_to_tmp,
    extract_packages_list_from_pyenv,
    wait_until_rayjob_completes
)

import time
import os

from ray.job_submission import JobSubmissionClient

# Dataiku client
client = dataiku.api_client()
project = client.get_default_project()

# Script params: YOU NEED TO ADAPT THIS PART
train_dataset_name = "avocado_transactions_train"
target_column_name = "type" # includes the 
managed_folder_id = "CcLoevDh"

ray_cluster_endpoint = "http://10.0.1.190:8265"


train_script_filename = "xgboost_train.py" # name of file in Project Library
train_script_dir = "/python/dku_ray/" # in project libs

ray_env_name = "py310_ray" # dataiku code environment name
num_ray_workers = 3 # num workers and cpus per worker should be sized approriately, 
                    # based on the size of the Ray Cluster deployed 
cpus_per_ray_worker = 10

timestamp = int(time.time()*100000) # unix timestamp in seconds

# Train script
## Copy train script to temporary location (as impersonated users can't traverse project libs)
tmp_train_script_dir = copy_project_lib_to_tmp(train_script_dir, train_script_filename, timestamp)

# Inputs & outputs
## (a) Retrieve S3 input dataset path and credentials
##     Note: connection should be S3 and use AssumeRole; dataset file format should be parquet
ds_path = s3_path_from_dataset(train_dataset_name)
ds_access_key, ds_secret_key, ds_session_token = s3_credentials_from_dataset(train_dataset_name)

## (b) Retrieve output S3 managed folder path and credentials
##     Note: connection should be S3 and use AssumeRole
storage_path = s3_path_from_managed_folder(managed_folder_id)
storage_access_key, storage_secret_key, storage_session_token = s3_credentials_from_managed_folder(managed_folder_id)

# Submit to remote cluster

# Useful links:
#   Ray Jobs SDK: https://docs.ray.io/en/latest/cluster/running-applications/job-submission/sdk.html
#   Runtime env spec: https://docs.ray.io/en/latest/ray-core/api/runtime-env.html
ray_client = JobSubmissionClient(ray_cluster_endpoint)

entrypoint = f"python {train_script_filename} --run-name=\"xgboost-train-{timestamp}\" " + \
    f"--data-s3-path=\"{ds_path}\" --data-label-column=\"{target_column_name}\" " + \
    f"--data-s3-access-key={ds_access_key} --data-s3-secret-key={ds_secret_key} --data-s3-session-token={ds_session_token} " + \
    f"--storage-s3-path=\"{storage_path}\" " + \
    f"--storage-s3-access-key={storage_access_key} --storage-s3-secret-key={storage_secret_key} --storage-s3-session-token={storage_session_token} " + \
    f"--num-workers={num_ray_workers} --cpus-per-worker={cpus_per_ray_worker}"

# Extract python package list from env
python_packages_list = extract_packages_list_from_pyenv(ray_env_name)
    
job_id = ray_client.submit_job(
    entrypoint=entrypoint,
    runtime_env={
        "working_dir": tmp_train_script_dir,
        "pip": python_packages_list
    }
)

# Wait until job fails or succeeds
wait_until_rayjob_completes(ray_client, job_id)