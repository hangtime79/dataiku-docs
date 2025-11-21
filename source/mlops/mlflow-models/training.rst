Training MLflow models
#######################

Just like any Python packages, you can use MLflow and the related frameworks in any DSS recipe, notebook, scenario, ...

This allows you to train and save a MLflow model directly in DSS, which you can then :doc:`import as a saved model <importing>` in order to leverage visual scoring, evaluation, drift analysis, ...

Dataiku also features an integration of MLflow Experiment Tracking. When leveraging it, trained models are automatically stored in a configurable managed folder (see :doc:`/mlops/experiment-tracking/deploying`).

Training a model
----------------

You can train the MLflow model either outside of DSS, in a :doc:`python recipe </code_recipes/python>`, in a :doc:`python notebook </notebooks/python>`, or using :doc:`/mlops/experiment-tracking/index`...

The list of frameworks supported by MLflow is available in the `MLflow documentation <https://mlflow.org/docs/2.17.2/models.html#built-in-model-flavors>`_. These include the most common libraries such as PyTorch, TensorFlow, Scikit-learn, etc.


Saving the MLflow model
------------------------

You need to export your model in a standard format, provided by MLflow Models, compatible with DSS.

MLflow provides a *save_model* function for each supported `machine learning framework <https://mlflow.org/docs/2.17.2/models.html#built-in-model-flavors>`_.

For instance, saving a Keras model using MLflow in a *model_directory* will look like this:

.. code-block:: python

    ... ommitted Keras model training code

    import mlflow
    mlflow.keras.save_model(model, model_directory)

You can then :doc:`import the exported model in DSS as a Saved Model <importing>`

Python recipe
-------------

The following snippet is a draft of a python recipe:

* taking a train and an evaluation dataset as inputs
* training a model
* saving it in MLflow format
* adding it as a new version to the saved model defined as output

.. code-block:: python

    import os
    import shutil
    import dataiku

    from dataiku import recipe

    client = dataiku.api_client()

    project = client.get_project('PROJECT_ID')

    # get train dataset
    train_dataset = recipe.get_inputs_as_datasets()[0]
    evaluation_dataset = recipe.get_inputs_as_datasets()[1]

    # get output saved model
    sm = project.get_saved_model(recipe.get_output_names()[0])

    # get train dataset as a pandas dataframe
    df = train_dataset.get_dataframe()

    # get the path of a local managed folder where to temporarily save the trained model
    mf = dataiku.Folder("local_managed_folder")
    path = mf.get_path()

    model_subdir = "my_subdir"
    model_dir = os.path.join(path, model_subdir)

    if os.path.exists(model_dir):
        shutil.rmtree(model_dir)

    try:
        # ...train your model...

        # ...save it with package specific MLflow method (here, SKlearn)...
        mlflow.sklearn.save_model(my_model, model_dir)

        # import the model, creating a new version
        mlflow_version = sm.import_mlflow_version_from_managed_folder("version_name", "local_managed_folder", model_subdir, "code-env-with-mlflow-name")
    finally:
        shutil.rmtree(model_dir)

    # setting metadata (target name, classes,...)
    mlflow_version.set_core_metadata(target_column, ["class0", "class1",...] , get_features_from_dataset=evaluation_dataset.name)

    # evaluate the performance of this new version, to populate the performance screens of the saved model version in DSS
    mlflow_version.evaluate(evaluation_dataset.name)

.. note::

    :doc:`/mlops/experiment-tracking/index` features logging of models in a configurable, and not necessarily local, managed folder.

.. note::

    *local_managed_folder* should be a filesystem managed folder, on the DSS host, as we use the :meth:`dataiku.Folder.get_path` method to retrieve
    its path on the local filesystem then compute a directory path where the ML package can save the trained model.

.. note::

    As this recipe uses a local managed folder, it should not be executed in a container.

.. note::

    The 4th parameter of the :meth:`dataikuapi.dss.savedmodel.DSSSavedModel.import_mlflow_version_from_managed_folder` is the name of the code environment to use when scoring the model.
    If not specified, the code environment of the project will be resolved and used.

    This code environment must contain the mlflow package and the packages of the machine learning library of your choice.

.. note::

    A "Run checks" scenario step must be used to run the checks defined for the saved model on the metrics evaluated on the new version.

.. warning::

   Recent versions of MLflow feature an ```mlflow.evaluate``` function. This function is different from :meth:`dataikuapi.dss.savedmodel.MLFlowVersionHandler.evaluate`. Only the later will populate the interpretation screens of a saved model version in DSS.
