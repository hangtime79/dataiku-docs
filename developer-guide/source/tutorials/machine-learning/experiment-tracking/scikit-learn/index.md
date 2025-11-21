# Experiment tracking with scikit-learn

In this tutorial you will train a model using the [scikit-learn](https://scikit-learn.org/stable/) framework and use the experiment tracking capabilities of Dataiku to log training runs (parameters, performance).**Solution**

## Prerequisites

* [Dataiku >= 11.0.0](https://doc.dataiku.com/dss/latest/release_notes/11.0.html#mlops-experiment-tracking).
* Access to a Project with a Dataset that contains the [UCI Bank Marketing data](https://archive.ics.uci.edu/static/public/222/bank+marketing.zip).
* A code environment containing the `mlflow` and `scikit-learn` packages.

## Performing the experiment

The following code snippet provides a reusable example to train a simple random forest classifier with these main steps:

**(1)** Select the feature and target variables.

**(2)** Build the preprocessing pipeline for categorical and numerical features.

**(3)** Define the hyperparameters to run the training on, namely the numbers of decision trees in the random forest, the maximum depth of each tree and the minimum number of samples required to be at a leaf node.

**(4)** Perform the experiment run, log the hyperparameters, performance metrics (here we use the F1 and the ROC AUC) and the trained model.

```{literalinclude} code.py
```

After these steps you should have your experiment run's data available both in the [Dataiku UI](https://doc.dataiku.com/dss/latest/mlops/experiment-tracking/viewing.html) and programmatically via the {py:class}`dataikuapi.dss.mlflow.DSSMLflowExtension` class of the Python API client.
