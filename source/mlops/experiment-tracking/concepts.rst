Concepts
########

Experiment Tracking in DSS uses the `MLflow Tracking <https://www.mlflow.org/docs/2.17.2/tracking.html>`_ API, and shares most of the concepts.

When running code-based experimentations, you organize your work in *Experiments*.

An *Experiment* contains *Runs*.

A *Run* often corresponds to the training of a model. A run stores *parameters*, *metrics* and *artefacts*. As a user, you store these in a run by calling specific APIs.

For example, you could store the hyperparameters as parameters of the run, resulting performance metrics as metrics of the run, and the resulting model and some generated charts as artefacts of the run.

You may for instance choose to organize your attempts with different algorithms as *Experiments* and have different hyperparameters selections as *Runs*, each run storing the resulting model.

Leveraging the integration of MLflow Tracking, you can track your experiments using the standard MLflow Tracking API, with the following DSS specific benefits:

* All experiments and runs benefit from DSS project-level security
* Run artefacts are stored in a DSS managed folder and can be directly manipulated from there
* If you save a MLflow model as an artefact of a run, you can then directly deploy this model using Dataiku's support for :doc:`/mlops/mlflow-models/index`

DSS experiment tracking makes it easy to manage the security of your experiment data and artefacts. It also allows you to leverage DSS features such as deploying, monitoring and governance.