import dataiku

def extract_packages_list_from_pyenv(env_name):
    """
    Extracts python package list (requested) from an environment.
    Returns a list of python packages.
    """   
    client = dataiku.api_client()
    pyenv = client.get_code_env(env_lang="PYTHON", env_name=env_name)
    pyenv_settings = pyenv.get_settings()
    
    packages = pyenv_settings.settings["specPackageList"]
    packages_list = packages.split("\n")
    
    return packages_list

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

def s3_path_from_dataset(dataset_name):
    """
    Retrieves full S3 path (i.e. s3:// + bucket name + path in bucjet) for dataset.
    Assumues dataset is stored on S3 connection.
    
    TODO: actually check this, and don't just fail.
    """
    ds = dataiku.Dataset(dataset_name) # resolved path and connection name via internal API
    ds_path = ds.get_location_info()["info"]["path"]
    
    return ds_path
