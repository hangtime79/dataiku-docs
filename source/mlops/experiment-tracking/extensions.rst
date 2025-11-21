Extensions
##########

Dataiku's experiment tracking features *extensions* to the MLflow Python API.

Some of those extensions are allowing actions that can only be performed through the CLI in standard MLflow.

In order to interact with these extensions, you must first obtain a reference to the :class:`dataikuapi.dss.mlflow.DSSMLflowExtension` through :meth:`dataikuapi.dss.project.DSSProject.get_mlflow_extension`


.. code-block:: python

    import dataiku
    import mlflow

    project = dataiku.api_client().get_default_project()
    mlflow_extension = project.get_mlflow_extension()

You can then use the following methods:

* list models and experiments: :meth:`dataikuapi.dss.mlflow.DSSMLflowExtension.list_models` and :meth:`dataikuapi.dss.mlflow.DSSMLflowExtension.list_experiments`
* rename experiments: :meth:`dataikuapi.dss.mlflow.DSSMLflowExtension.rename_experiment`
* restore experiments and runs: :meth:`dataikuapi.dss.mlflow.DSSMLflowExtension.restore_experiment` and :meth:`dataikuapi.dss.mlflow.DSSMLflowExtension.restore_run`
* clear experiments marked for deletion (*garbage collect*): :meth:`dataikuapi.dss.mlflow.DSSMLflowExtension.garbage_collect`

Others are more DSS specific:

* clean the runtime experiment db for a DSS project: :meth:`dataikuapi.dss.mlflow.DSSMLflowExtension.clean_experiment_tracking_db`
* set the inference info of a run (to make scoring or evaluation of a model easier): :meth:`dataikuapi.dss.mlflow.DSSMLflowExtension.set_run_inference_info`
* create a DSS dataset of the experiment tracking runs of a project: :meth:`dataikuapi.dss.mlflow.DSSMLflowExtension.create_experiment_tracking_dataset`
* deploy a model from a run: :meth:`dataikuapi.dss.mlflow.DSSMLflowExtension.deploy_run_model`
