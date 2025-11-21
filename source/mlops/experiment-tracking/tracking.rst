Tracking experiments in code
#############################

.. contents::
    :local:

Initial setup
==============

Before you can track experiments, you need to create a :doc:`Managed Folder </connecting/managed_folders>` in the project. The managed folder will be used to store artefacts. Take note of the managed folder id (8 alphanum characters, visible in the URL).

Quick start sample
===================

.. code-block:: python

    import dataiku

    project = dataiku.api_client().get_default_project()
    managed_folder = project.get_managed_folder('A_MANAGED_FOLDER_ID')

    with project.setup_mlflow(managed_folder=managed_folder) as mlflow_handle:
        
        # Note: if you don't call this (i.e. when no experiment is specified), the default one is used
        mlflow_handle.set_experiment("My first experiment")

        with mlflow_handle.start_run(run_name="my_run"):
            # ...your MLflow code...
            mlflow_handle.log_param("a", 1)
            mlflow_handle.log_metric("b", 2)

            # This uses the regular MLflow APIs

Tracking API
=============

DSS uses the `MLflow Tracking <https://www.mlflow.org/docs/2.17.2/tracking.html>`_ API. Please refer to the MLflow Tracking documentation.

Autologging
============

MLflow Tracking comes with a very useful feature: autologging, which automatically logs metrics, parameters, and models for common machine-learning packages without the need for explicit log statements.

Leveraging MLflow autologging requires no additional configuration of the DSS integration. Some machine learning packages, such as PyTorch, may however `require additional packages <https://www.mlflow.org/docs/2.17.2/python_api/mlflow.pytorch.html>`_.

In the following sample, we activate MLflow autologging for a SKlearn model. Metrics and artifacts are automatically logged.

.. code-block:: python

    import dataiku
    import mlflow
    import sklearn.linear_model.ElasticNet

    project = dataiku.api_client().get_default_project()
    managed_folder = project.get_managed_folder('A_MANAGED_FOLDER_ID')

    with project.setup_mlflow(managed_folder=managed_folder) as mlflow_handle:
        mlflow_handle.set_experiment("Let's autolog")

        # activate Mflow autologging
        mlflow_handle.sklearn.autolog()

        with mlflow_handle.start_run(run_name="my_run"):
            lr = ElasticNet(alpha=alpha, l1_ratio=l1_ratio, random_state=42)
            lr.fit(train_x, train_y)

Other topics
=============

Logging into another project
------------------------------

You can log experiments into another project than the current one by using:

.. code-block:: python

    project = dataiku.api_client().get_project("MYOTHERPROJECT")

Experiment tracking outside DSS
--------------------------------

MLflow Tracking integration is configured through the ``dataikuapi`` package. See :doc:`devguide:tutorials/devtools/python-client/index` for how to use it from outside of DSS

Usage without context manager
------------------------------

While the usage of the context manager ("with" statement) is recommended, it is not mandatory. You can use this instead:


.. code-block:: python

    import dataiku
    import mlflow

    project = dataiku.api_client().get_default_project()
    managed_folder = project.get_managed_folder('A_MANAGED_FOLDER_ID')

    mlflow_handle = project.setup_mlflow(managed_folder=managed_folder)
        
    mlflow.set_experiment("My first experiment")

    with mlflow.start_run(run_name="my_run"):
        # ...your MLflow code...
        mlflow.log_param("a", 1)
        mlflow.log_metric("b", 2)

    mlflow_handle.clear()

Cautions
---------

If you do not set up the integration before using the MLflow client, or use the client after clearing the integration, it may fall back to its default mode: writing experiment data as the current user, on the filesystem of the host of the DSS server.

Supported versions
--------------------

See :doc:`/mlops/mlflow-models/limitations` for supported MLflow versions.
