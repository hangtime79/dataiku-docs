Step 3: Create a Dataiku Saved Model using the best-performing model
====================================================================

Dataiku offers pre-built capabilities to evaluate, deploy & monitor
Machine Learning models. Our Python model needs to be stored as a
Dataiku Saved Model to benefit these capabilities. In this notebook, we
will collect the best model optimizing the accuracy metric from our
previous experiment, and deploy it in the Flow as a Dataiku Saved Model.

*Tip:* Creating a Dataiku Saved Model will allow you to benefit from a
set of pre-built evaluation interfaces along with deployment and
monitoring capabilities.

0. Import packages
------------------

**Make sure you’re using the correct code environment** (see
prerequisites)

To be sure, go to **Kernel > Change kernel** and choose the
``py_quickstart``

.. code:: ipython3

    %pylab inline


.. parsed-literal::

    Populating the interactive namespace from numpy and matplotlib


.. code:: ipython3

    import warnings
    warnings.filterwarnings('ignore')

.. code:: ipython3

    import dataiku
    from dataiku import pandasutils as pdu
    import pandas as pd
    import mlflow
    from dataikuapi.dss.ml import DSSPredictionMLTaskSettings

.. code:: ipython3

    client = dataiku.api_client()
    client._session.verify = False

1. Get access to the ML experiment information
----------------------------------------------

In this section, we use the Dataiku Python API to access to the managed
folder where the results of our experiments are stored.

.. code:: ipython3

    # Set parameters
    experiment_name = "Binary Heart Disease Classification"
    experiments_managed_folder_name = "Binary classif experiments"
    
    # Get various handles
    project = client.get_default_project()
    mlflow_extension = project.get_mlflow_extension()
    experiments_managed_folder_id = dataiku.Folder(experiments_managed_folder_name).get_id()
    experiments_managed_folder = project.get_managed_folder(experiments_managed_folder_id)

2. Select the experiment with the best accuracy
-----------------------------------------------

Now, let’s retrieve the run that generated the best model optimizing the
accuracy from our Machine Learning experiments.

.. code:: ipython3

    optimized_metric = "accuracy" # You can switch this parameter to another performance metric
    
    with project.setup_mlflow(managed_folder=experiments_managed_folder) as mlflow:
        experiment = mlflow.set_experiment(experiment_name)
        best_run = mlflow.search_runs(experiment_ids=[experiment.experiment_id], 
                                      order_by=[f"metrics.{optimized_metric} DESC"], 
                                      max_results=1, 
                                      output_format="list")[0]


.. parsed-literal::

    invalid escape sequence '\w'


3. Create or get a Dataiku Saved Model using the API
----------------------------------------------------

In this section, we use the Dataiku Python API to create (or get if it
already exists) the Dataiku Saved Model that will be used to deploy our
Python model in the Flow.

.. code:: ipython3

    # Get or create SavedModel
    sm_name = "heart-disease-clf"
    sm_id = None
    for sm in project.list_saved_models():
        if sm_name != sm["name"]:
            continue
        else:
            sm_id = sm["id"]
            print("Found SavedModel {} with id {}".format(sm_name, sm_id))
            break
    if sm_id:
        sm = project.get_saved_model(sm_id)
    else:
        sm = project.create_mlflow_pyfunc_model(name=sm_name,
                                                prediction_type=DSSPredictionMLTaskSettings.PredictionTypes.BINARY)
        sm_id = sm.id
        print("SavedModel not found, created new one with id {}".format(sm_id))


.. parsed-literal::

    SavedModel not found, created new one with id 9BZVrx8D


4. Import the new mlflow model into a Saved Model version
---------------------------------------------------------

Finally, let’s import the model from our best run as a new version of
the Dataiku Saved Model and make sure it automatically computes
performance metrics & charts based on the train set.

.. code:: ipython3

    # Set version ID (a Saved Model can have multiple versions).
    
    if len(sm.list_versions()) == 0:
        version_id = "V1"
    else:
        max_version_num = max([int(v['id'][1:]) for v in sm.list_versions()])
        version_id = f"V{max_version_num+1}"
    
    # Create version in SavedModel
    sm_version = sm.import_mlflow_version_from_managed_folder(version_id=version_id,
                                                             managed_folder=experiments_managed_folder,
                                                             path=best_run.info.artifact_uri.split(experiments_managed_folder_id)[1]+'/model')
    
    # Evaluate the version using the previously created Dataset
    sm_version.set_core_metadata(target_column_name="HeartDisease",
                                 class_labels=[0, 1],
                                 get_features_from_dataset="heart_measures_train")
    
    sm_version.evaluate("heart_measures_train")

5. Next: use this notebook to create a new step in the pipeline
---------------------------------------------------------------

5.1 Create a new step in the flow
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Now that our notebook is up and running, we can use it to create the
second step of our pipeline in the Flow:

-  Click on the **+ Create Recipe** button at the top right of the
   screen.

-  Select the **Python recipe** option.

-  Add two **inputs**: the ``heart_measures_train`` dataset and the
   ``Binary classif experiments`` folder.

-  Add the ``heart-disease-clf`` Saved Model as the **output**: **Add**
   > **Use existing** (option at the bottom).

-  Click on the **Create the recipe** button.

-  Run the recipe.

You can explore all the built-in evaluation metrics & charts of your
Python model by clicking on the Saved Model in the Flow.

5.2 Evaluate the model on the test dataset
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Now that the model has been deployed on the Flow, we can evaluate it on
our test dataset:

-  Select the ``heart-disease-clf`` Saved Model.

-  On the action panel, select the **Evaluate** recipe.

-  On the settings tab, select the ``heart_measures_test`` as the input
   dataset.

-  For the output, let’s create the ‘Output dataset’ (let’s call it
   ``heart_measures_test_prediction``), the ‘Metrics’ dataset (let’s
   call it ``evaluation_metrics``) and the ‘Evaluation Store’ (let’s
   name it ``eval_heart_prediction``)

-  Click on the **Create recipe** button.

-  Run the recipe.

Success! Our model is now deployed on the Flow, it can be used for
inference on new datasets and be deployed for production.