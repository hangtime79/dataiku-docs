Exposing a MLflow model
#######################


.. Note::
    See :doc:`/apinode/endpoint-std` to learn about exposing a visual model. Exposing a MLflow model relies on the same basis as a virtual model.


Deploying the model
===================


A MLflow model can be deployed using the API, as described in :doc:`/mlops/mlflow-models/importing`. It can also be deployed from an :doc:`/mlops/experiment-tracking/index` run. See :doc:`/mlops/experiment-tracking/deploying` for more information.


Exposing the model
==================

Once deployed, a MLflow model can be exposed nearly like a visual model. Even so, the *MLflow Model output* is to be set in the endpoint settings. It can be either *raw data* or *restructured*. The first outputs directly what the MLflow model outputs while the second makes DSS try to restructure it (disable this in case of compatibility issues).

For example, a *SKLearn binary classification* typically outputs a prediction probability. *Restructure* enriches it to a prediction and probabilities for both label.

See :doc:`/mlops/mlflow-models/using`.

