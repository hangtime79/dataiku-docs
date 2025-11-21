# Experiment tracking with LightGBM

In this tutorial you will train a model using the [LightGBM](https://lightgbm.readthedocs.io/) framework and use the experiment tracking capabilities of Dataiku to log training runs (parameters, performance).

## Prerequisites

- [Dataiku 11.0.0 or higher](https://doc.dataiku.com/dss/latest/release_notes/11.0.html#mlops-experiment-tracking)
- Access to a Project with a Dataset that contains the [UCI Bank Marketing data](https://archive.ics.uci.edu/static/public/222/bank+marketing.zip)
- A code environment containing the `mlflow` and `lightgbm` packages

## Performing the experiment

The following code snippet provides a reusable example to train a simple gradient boosting model with these main steps:

**(1)** Specify the categorical and numeric features and the target variable.

**(2)** Using the categorical and continuous variables spcecified, set up a preprocessing [`Pipeline`](https://scikit-learn.org/stable/modules/compose.html#pipeline) with two transformation steps. First, define a transformer to one-hot-encode categorical variables and then impute any missing values in continuous variables and rescale them in the other.

**(3)** Define a dictionary containing the search space for hyperparameter tuning. Then lay out a cross-validation strategy to train a classifier and evaluate the model. Log the parameters and resulting metrics as well as the models using Experiment Tracking feature, while looping over combinations of hyperparameters. The model artifact logged for the run is also a Pipeline called `clf_pipeline` that encapsulates the preprocessing and the model itself.

```{literalinclude} code.py
```
