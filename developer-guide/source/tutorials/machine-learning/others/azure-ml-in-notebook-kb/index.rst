How to use Azure AutoML from a Dataiku Notebook
***********************************************

.. meta::
    :tag: Azure
    :tag: ML
    :tag: notebooks
    :tag: Python
    :tag: code

Azure Machine Learning can be used for any kind of machine learning, from classical ML to deep learning, supervised, and unsupervised learning. Whether you prefer to write Python or R code or zero-code/low-code options such as the designer, you can build, train, and track highly accurate machine learning and deep-learning models in an Azure Machine Learning Workspace. Users can apply automated ML when they want Azure Machine Learning to train and tune a model for them using a specified target metric.

It is currently possible to leverage Azure's AutoML capabilities from within a Dataiku python notebook.  The following details the necessary configuration for Azure and Dataiku to make this integration possible, as well as a code example of how to create and deploy an Azure AutoML job from Dataiku.

Configuration
==================

Azure side
------------

- Create a machine learning workspace.
- Create a storage account:

    - Choose the new “StorageV2”
    - Once created, go to the storage page -> Containers -> Create a container (mine is container-of-dku). This will be the container used by Dataiku.

Dataiku side
------------

- Create the new connection to the storage that we just created:

    - Access Key can be found on the portal UI when going to your storage page -> Access Key.
    - Path restrictions -> Container -> container-of-dku
    - Advanced -> HDFS interface -> ABFS

- Create a python3 (mandatory) code-env with these requirements (according to here):

    - matplotlib
    - numpy
    - cython
    - urllib3
    - scipy
    - scikit-learn
    - tensorflow
    - xgboost
    - azureml-sdk
    - azureml-widgets
    - azureml-explain-model
    - pandas-ml
    - azureml-defaults
    - azureml-dataprep[pandas]
    - azureml-train-automl
    - azureml-train
    - azureml-widgets
    - azureml-pipeline
    - azureml-contrib-interpret
    - pytorch-transformers==1.0.0
    - spacy==2.1.8
    - onnxruntime==1.0.0
    - :samp:`https://aka.ms/automl-resources/packages/en_core_web_sm-2.1.0.tar.gz`

- The AutoML API we will use requires that the files are uncompressed csv, and they must have the columns name. This is not the default behavior when Dataiku creates a managed azure dataset, so there are some format config we need to modify manually.

    - To do that, go to azure dataset on the flow you intend to use as the input for your model. Then select Settings -> Previews and input the following values:
            
        - File compression: None
        - Choose Parse next line as column headers
    
    - Return to the parent recipe of the dataset and rerun it

- To check before starting, go to your storage page -> Containers -> YOUR_CONTAINER -> dataiku -> YOUR_PROJECT -> YOUR_DATASET. Inside that folder you should see that your files are in the format “out-sX.csv”. Download the first file and check that it contains the column names.

Train an AutoML model
=========================

- Create a Python Code recipe with the desired training data, stored in Azure, as your recipe input 
- Open up your recipe in a notebook and set the code-env to the previously created AzureML environment

Connect to the workspace
-------------------------------

.. code-block:: python

    from azureml.core import Workspace 
    # THIS INFORMATION CAN BE FOUND ON THE AZURE WORKSPACE UI
    config = {
        "subscription_id": "XXXXXXXXXXX",
        "resource_group": "resource-of-dku",
        "workspace_name": "playground-of-dku"
    }
    subscription_id = config.get('subscription_id')
    resource_group = config.get('resource_group')
    workspace_name = config.get('workspace_name')

    ws = Workspace(subscription_id = subscription_id, resource_group = resource_group, workspace_name = workspace_name)

 
Create an Experiment
--------------------------

.. code-block:: python

    from azureml.core.experiment import Experiment
    experiment_name = 'automl-experiment-of-dku' 

    experiment = Experiment(ws, experiment_name)

 
Create a Compute Cluster
--------------------------

.. code-block:: python

    from azureml.core.compute import AmlCompute
    from azureml.core.compute import ComputeTarget

    # Choose a name for your cluster. 
    amlcompute_cluster_name = "cluster-of-dku"
    found = False
    # Check if this compute target already exists in the workspace.
    cts = ws.compute_targets
    if amlcompute_cluster_name in cts and cts[amlcompute_cluster_name].type == 'AmlCompute':
        found = True
        print('Found existing compute target.')
        compute_target = cts[amlcompute_cluster_name]

    if not found:
        print('Creating a new compute target...')
        provisioning_config = AmlCompute.provisioning_configuration(vm_size = "Standard_D4_v2",  max_nodes = 10)
        compute_target = ComputeTarget.create(ws, amlcompute_cluster_name, provisioning_config)

    print('Checking cluster status...')
    compute_target.wait_for_completion(show_output = True, min_node_count = None, timeout_in_minutes = 20)


Creation of the cluster will take some time so a waiting time of a few minutes is normal.

 
Define the datastore for ML purpose
-----------------------------------------

.. code-block:: python

    from azureml.core import Datastore
    import dataiku

    client = dataiku.api_client()

    my_dss_azure_connection_name = 'azure_blob_dku' # CHANGE THIS TO YOUR CONNECTION
    azure_connection = client.get_connection(my_dss_azure_connection_name)
    azure_connection_info = azure_connection.get_info().get('params', {})
    datastore_name='datastore_of_dku' # CHANGE THIS
    container_name = azure_connection_info.get('chcontainer')
    account_name = azure_connection_info.get('storageAccount')
    account_key = azure_connection_info.get('accessKey')
    default_managed_folder = azure_connection_info.get('defaultManagedContainer')

    blob_datastore = Datastore.register_azure_blob_container(workspace=ws, datastore_name=datastore_name, container_name=container_name, account_name=account_name, account_key=account_key)

Represent your azure dataset as a TabularDataset, so that it can be used with the autoML api

.. code-block:: python

    from azureml.core.dataset import Dataset

    dataset = dataiku.Dataset('simple_table_azure') # CHANGE THIS INPUT DATASET NAME
    project_key = dataset.get_config().get('projectKey')
    raw_path = dataset.get_config().get('params').get('path')
    path = raw_path.replace('${projectKey}', project_key)

    my_train_dataset = Dataset.Tabular.from_delimited_files(path=[(blob_datastore, path)], separator='\t')

You can test if the file format has been configured correctly by doing the following:

.. code-block:: python

    my_train_dataset.take(3).to_pandas_dataframe()

It should return a clean dataframe.

If everything looks good, register your TabularDataset, the name and description are not that important, so you can just keep them as in the example if you want.

.. code-block:: python

    my_train_dataset = my_train_dataset.register(workspace=ws, name='simple_blob_train_dataset', description='Simple training data', create_new_version=True)

 
Configure the AutoML task
-------------------------------

.. code-block:: python

    import logging
    from azureml.train.automl import AutoMLConfig
    target_column  = 'Churn' #CHANGE THIS TO THE NAME OF YOUR TARGET COLUMN
    automl_settings = {
        "n_cross_validations": 2,
        "primary_metric": 'average_precision_score_weighted',
        "whitelist_models": ['RandomForest'],
        "enable_early_stopping": True,
        "max_concurrent_iterations": 8, 
        "max_cores_per_iteration": -1,
        "experiment_timeout_hours" : 0.25,
        "iteration_timeout_minutes": 1, 
        "verbosity": logging.INFO,
    }
    automl_config = AutoMLConfig(task = 'classification', debug_log = 'automl_errors.log', compute_target = compute_target, training_data = my_train_dataset, label_column_name = target_column, **automl_settings)

 
Submit the task
-------------------------------

.. code-block:: python

    remote_run = experiment.submit(automl_config, show_output = True)

And that’s it, now just sit back, and wait until the job completes. It will output a summary of its training test and best model.

Deploy the model
=====================

There is no easy way to do this by code, so users will need to create 1) a python scoring file and 2) a yaml configuration file.

Meanwhile, in the UI, it just takes 2 click like specified `here <https://docs.microsoft.com/en-us/azure/machine-learning/tutorial-first-experiment-automated-ml#deploy-the-best-model>`_, so we recommend users to deploy via the UI.

Users can choose to either deploy the model on Azure Kubernetes Service (AKS) or Azure Container Instance (ACI).

To test the endpoint, you can try this code snippet in a notebook:

.. code-block:: python

    # URL for the web service
    scoring_uri = "http://f9ed9cf6-3541-4f8e-aed3-525d8e731a38.eastus2.azurecontainer.io/score"
    # If the service is authenticated, set the key or token
    key = '<your key or token>'

    scoring_data = [[11.01, 717.2, 75.56]]
    data = {"data": scoring_data}
    # Convert to JSON string
    input_data = json.dumps(data)

    # Set the content type
    headers = {'Content-Type': 'application/json'}
    # If authentication is enabled, set the authorization header
    #headers['Authorization'] = f'Bearer {key}'

    # Make the request and display the response
    resp = requests.post(scoring_uri, input_data, headers=headers)

