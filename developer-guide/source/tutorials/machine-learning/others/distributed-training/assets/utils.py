import dataiku
from ray.job_submission import JobStatus

import time
import os

def s3_path_from_managed_folder(folder_id):
    """
    Retrieves full S3 path (i.e. bucket name + path in bucjet) for managed folder.
    Assumues managed folder is stored on S3 connection.
    
    TODO: actually check this, and don't just fail.
    """
    mf = dataiku.Folder(folder_id)
    mf_path = mf.get_info()["accessInfo"]["bucket"] + mf.get_info()["accessInfo"]["root"]
    
    return mf_path

def s3_credentials_from_managed_folder(folder_id):
    """
    Retireves S3 credentials (access key, secret key, session token) from managed folder.
    Assumues managed folder is stored on S3 connection, with AssumeRole as auth method.
    
    TODO: actually check this, and don't just fail.
    """
    client = dataiku.api_client()
    project = client.get_default_project()
    
    mf = project.get_managed_folder(folder_id) # connection only available through client
    mf_connection_name = mf.get_settings().settings["params"]["connection"]

    mf_connection = client.get_connection(mf_connection_name)
    mf_connection_info = mf_connection.get_info()
    access_key = mf_connection_info["resolvedAWSCredential"]["accessKey"]
    secret_key = mf_connection_info["resolvedAWSCredential"]["secretKey"]
    session_token = mf_connection_info["resolvedAWSCredential"]["sessionToken"]
    
    return access_key, secret_key, session_token

def s3_path_from_dataset(dataset_name):
    """
    Retrieves full S3 path (i.e. s3:// + bucket name + path in bucjet) for dataset.
    Assumues dataset is stored on S3 connection.
    
    TODO: actually check this, and don't just fail.
    """
    ds = dataiku.Dataset(dataset_name) # resolved path and connection name via internal API
    ds_path = ds.get_location_info()["info"]["path"]
    
    return ds_path

def s3_credentials_from_dataset(dataset_name):
    """
    Retireves S3 credentials (access key, secret key, session token) from S3 dataset.
    Assumues dataset is stored on S3 connection, with AssumeRole as auth method.
    
    TODO: actually check this, and don't just fail.
    """
    client = dataiku.api_client()
    
    ds = dataiku.Dataset(dataset_name) # resolved path and connection name via internal API
    ds_connection_name = ds.get_config()["params"]["connection"]

    ds_connection = client.get_connection(ds_connection_name)
    ds_connection_info = ds_connection.get_info()
    access_key = ds_connection_info["resolvedAWSCredential"]["accessKey"]
    secret_key = ds_connection_info["resolvedAWSCredential"]["secretKey"]
    session_token = ds_connection_info["resolvedAWSCredential"]["sessionToken"]
    
    return access_key, secret_key, session_token

def copy_project_lib_to_tmp(file_dir, file_name, timestamp):
    """
    Makes a copy of a project library file to a temporary location.
    Timestamp ensures file path uniqueness.
    """
    client = dataiku.api_client()
    project = client.get_default_project()
    project_library = project.get_library()

    file_path = file_dir + file_name
    file = project_library.get_file(file_path).read()

    # Stage train script in /tmp
    tmp_file_dir = f"/tmp/ray-{timestamp}/"
    tmp_file_path = tmp_file_dir + file_name

    os.makedirs(os.path.dirname(tmp_file_dir), exist_ok=True)
    with open(tmp_file_path, "w") as f:
        f.write(file)
    
    return tmp_file_dir
    
def extract_packages_list_from_pyenv(env_name):
    """
    Extracts python package list (requested + mandatory) from an environment.
    Returns a list of python packages.
    """   
    client = dataiku.api_client()
    pyenv = client.get_code_env(env_lang="PYTHON", env_name=env_name)
    pyenv_settings = pyenv.get_settings()
    
    packages = pyenv_settings.settings["specPackageList"] + pyenv_settings.settings["mandatoryPackageList"]
    packages_list = packages.split("\n")
    
    return packages_list
    
def wait_until_rayjob_completes(ray_client, job_id, timeout_seconds=3600):
    """
    Polls Ray Job for `timeout_seconds` or until a specofoc status is reached:
    - JobStatus.SUCCEEDED: return
    - JobStatus.STOPPED or JobStatus.FAILED: raise exception
    """
    start = time.time()
    
    while time.time() - start <= timeout_seconds:
        status = ray_client.get_job_status(job_id)
        print(f"Ray Job `{job_id}` status: {status}")
        if (status == JobStatus.SUCCEEDED) or (status == JobStatus.STOPPED) or (status == JobStatus.FAILED):
            print("Ray training logs: \n", ray_client.get_job_logs(job_id))
            break
        time.sleep(1)
    
    if (status == JobStatus.SUCCEEDED):
        print("Ray Job {job_id} completed successfully.")
        return
    else:
        raise Exception("Ray Job {job_id} failed, see logs above.")
        
        
    
    