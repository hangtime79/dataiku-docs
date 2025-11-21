# Experiment tracking with Catboost


In this tutorial you will train a model using the [Catboost](https://catboost.ai/) framework and use the experiment tracking abilities of Dataiku to log training runs (parameters, performance).


## Prerequisites
* Access to a Project with a Dataset that contains the [UCI Bank Marketing data](https://archive.ics.uci.edu/static/public/222/bank+marketing.zip)
* A Code Environment containing the `mlflow` and `catboost` packages

## Performing the experiment

The following code snippet provides a reusable example to train a simple gradient boosting model, with these main steps:

**(1)**: Select the features and target variables.

**(2)**: Define the hyperparameters to run the training on. Set the number of boosting rounds to 100, and to check whether overfitting is occuring during cross-validation, set `early_stopping_rounds` to 5. To cap boosting rounds, limit the training to the iteration that has the best score by setting `use_best_model` to `True`.

**(3)**: Perform the experiment run, log the hyperparameters, performance metrics (here we use the AUC) and the trained model.

```{literalinclude} code.py
```


After these steps you should have your Experiment Run's data available both in the [Dataiku UI](https://doc.dataiku.com/dss/latest/mlops/experiment-tracking/viewing.html) and programmatically via the [`DSSMLflowExtension`](https://developer.dataiku.com/latest/api-reference/python/experiment-tracking.html#dataikuapi.dss.mlflow.DSSMLflowExtension)
object of the Python API client.
