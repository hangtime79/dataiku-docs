(ml)=

```{eval-rst}
..
  this code samples has been verified on DSS: 13.2.0
  Date of check: 24/09/2024
  
  this code samples has been verified on DSS: 14.2.0
  Date of check: 15/09/2025
```

# Visual Machine learning

Through the public API, the Python client allows you to automate all the aspects of the lifecycle of machine learning models.

- Creating a visual analysis and ML task
- Tuning settings
- Training models
- Inspecting model details and results
- Deploying saved models to Flow and retraining them

## Concepts

In DSS, you train models as part of a *visual analysis*. A visual analysis is made of a preparation script, and one or several *ML Tasks*.

A ML Task is an individual section in which you train models. A ML Task is either a prediction of a single target variable, or a clustering.

The ML API allows you to manipulate ML Tasks, and use them to train models, inspect their details, and deploy them to the Flow.

Once deployed to the Flow, the *Saved model* can be retrained by the usual build mechanism of DSS.

A ML Task has settings, which control:

- Which features are active
- The preprocessing settings for each features
- Which algorithms are active
- The hyperparameter settings (including grid searched hyperparameters) for each algorithm
- The settings of the grid search
- Train/Test splitting settings
- Feature selection and generation settings

## Usage samples

### The whole cycle

This examples create a prediction task, enables an algorithm, trains it, inspects models, and deploys one of the model to Flow

```python
# client is a DSS API client

p = client.get_project("MYPROJECT")

# Create a new ML Task to predict the variable "target" from "trainset"
mltask = p.create_prediction_ml_task(
    input_dataset="trainset",
    target_variable="target",
    ml_backend_type='PY_MEMORY', # ML backend to use
    guess_policy='DEFAULT' # Template to use for setting default parameters
)

# Wait for the ML task to be ready
mltask.wait_guess_complete()

# Obtain settings, enable GBT, save settings
settings = mltask.get_settings()
settings.set_algorithm_enabled("GBT_CLASSIFICATION", True)
settings.save()

# Start train and wait for it to be complete
mltask.start_train()
mltask.wait_train_complete()

# Get the identifiers of the trained models
# There will be 3 of them because Logistic regression and Random forest were default enabled
ids = mltask.get_trained_models_ids()

for id in ids:
    details = mltask.get_trained_model_details(id)
    algorithm = details.get_modeling_settings()["algorithm"]
    auc = details.get_performance_metrics().get("auc", None)

    print("Algorithm=%s AUC=%s" % (algorithm, auc))

# Let's deploy the first model
model_to_deploy = ids[0]

ret = mltask.deploy_to_flow(model_to_deploy, "my_model", "trainset")

print("Deployed to saved model id = %s train recipe = %s" % (ret["savedModelId"], ret["trainRecipeName"]))
```

The methods for creating prediction and clustering ML tasks are defined at {meth}`~dataikuapi.dss.project.DSSProject.create_prediction_ml_task` and {meth}`~dataikuapi.dss.project.DSSProject.create_clustering_ml_task`.

### Obtaining a handle to an existing ML Task

When you create these ML tasks, the returned {class}`dataikuapi.dss.ml.DSSMLTask` object will contain two fields `analysis_id` and `mltask_id` that can later be used to retrieve the same {class}`~dataikuapi.dss.ml.DSSMLTask` object

```python
# client is a DSS API client

p = client.get_project("MYPROJECT")
mltask = p.get_ml_task(analysis_id, mltask_id)
```

### Tuning feature preprocessing

#### Enabling and disabling features

```python
# mltask is a DSSMLTask object

settings = mltask.get_settings()

settings.reject_feature("name_of_not_useful_feature")
settings.use_feature("name_of_useful_feature")

settings.save()
```

#### Changing advanced parameters for a feature

```python
# mltask is a DSSMLTask object

settings = mltask.get_settings()

# Use impact coding rather than dummy-coding
fs = settings.get_feature_preprocessing("myfeature")
fs["category_handling"] = "IMPACT"

# Impute missing with most frequent value
fs["missing_handling"] = "IMPUTE"
fs["missing_impute_with"] = "MODE"

settings.save()
```

### Tuning algorithms

#### Global parameters for hyperparameter search

This sample shows how to modify the parameters of the search to be performed on the hyperparameters.

```python
# mltask is a DSSMLTask object

settings = mltask.get_settings()

hp_search_settings = settings.get_hyperparameter_search_settings()

# Set the search strategy either to "GRID", "RANDOM" or "BAYESIAN"
hp_search_settings.strategy = "RANDOM"

# Alternatively use a setter, either set_grid_search
# set_random_search or set_bayesian_search
hp_search_settings.set_random_search(seed=1234)

# Set the validation mode either to "KFOLD", "SHUFFLE" (or accordingly their
# "TIME_SERIES"-prefixed counterpart) or "CUSTOM"
hp_search_settings.validation_mode = "KFOLD"

# Alternatively use a setter, either set_kfold_validation, set_single_split_validation
# or set_custom_validation
hp_search_settings.set_kfold_validation(n_folds=5, stratified=True)

# Save the settings
settings.save()
```

#### Algorithm specific hyperparameter search

This sample shows how to modify the settings of the Random Forest Classification algorithm, where two kinds of hyperparameters (multi-valued numerical and single-valued) are introduced.

```python
# mltask is a DSSMLTask object

settings = mltask.get_settings()

rf_settings = settings.get_algorithm_settings("RANDOM_FOREST_CLASSIFICATION")


# rf_settings is an object representing the settings for this algorithm.
# The 'enabled' attribute indicates whether this algorithm will be trained.
# Other attributes are the various hyperparameters of the algorithm.

# The precise hyperparameters for each algorithm are not all documented, so let's
# print the dictionary keys to see available hyperparameters.
# Alternatively, tab completion will provide relevant hints to available hyperparameters.
print(rf_settings.keys())

# Let's first have a look at rf_settings.n_estimators which is a multi-valued hyperparameter
# represented as a NumericalHyperparameterSettings object
print(rf_settings.n_estimators)

# Set multiple explicit values for "n_estimators" to be explored during the search
rf_settings.n_estimators.definition_mode = "EXPLICIT"
rf_settings.n_estimators.values = [100, 200]
# Alternatively use the set_values setter
rf_settings.n_estimators.set_explicit_values([100, 200])

# Set a range of values for "n_estimators" to be explored during the search
rf_settings.n_estimators.definition_mode = "RANGE"
rf_settings.n_estimators.range.min = 10
rf_settings.n_estimators.range.max = 100
rf_settings.n_estimators.range.nb_values = 5  # Only relevant for grid-search
# Alternatively, use the set_range setter
rf_settings.n_estimators.set_range(min=10, max=100, nb_values=5)

# Let's now have a look at rf_settings.selection_mode which is a single-valued hyperparameter
# represented as a SingleCategoryHyperparameterSettings object.
# The object stores the valid options for this hyperparameter.
print(rf_settings.selection_mode)

# Features selection mode is not multi-valued so it's not actually searched during the
# hyperparameter search
rf_settings.selection_mode = "sqrt"

# Save the settings
settings.save()
```

The next sample shows how to modify the settings of the Logistic Regression classification algorithm, where a new kind of hyperparameter (multi-valued categorical) is introduced.

```python
# mltask is a DSSMLTask object

settings = mltask.get_settings()

logit_settings = settings.get_algorithm_settings("LOGISTIC_REGRESSION")

# Let's have a look at logit_settings.penalty which is a multi-valued categorical
# hyperparameter represented as a CategoricalHyperparameterSettings object
print(logit_settings.penalty)

# List currently enabled values
print(logit_settings.penalty.get_values())

# List all possible values
print(logit_settings.penalty.get_all_possible_values())

# Set the values for the "penalty" hyperparameter to be explored during the search
logit_settings.penalty = ["l1", "l2"]
# Alternatively use the set_values setter
logit_settings.penalty.set_values(["l1", "l2"])

# Save the settings
settings.save()
```

### Exporting a model documentation

This sample shows how to generate and download a model documentation from a template.

See [Model Document Generator](https://doc.dataiku.com/dss/latest//machine-learning/model-document-generator.html) for more information.

```python
# mltask is a DSSMLTask object

details = mltask.get_trained_model_details(id)

# Launch the model document generation by either
# using the default template for this model by calling without argument
# or specifying a managed folder id and the path to the template to use in that folder
future = details.generate_documentation(FOLDER_ID, "path/my_template.docx")

# Alternatively, use a custom uploaded template file
with open("my_template.docx", "rb") as f:
    future = details.generate_documentation_from_custom_template(f)

# Wait for the generation to finish, retrieve the result and download the generated
# model documentation to the specified file
result = future.wait_for_result()
export_id = result["exportId"]

details.download_documentation_to_file(export_id, "path/my_model_documentation.docx")
```

## Using a model in a Python recipe or notebook

Once a Saved Model has been deployed to the Flow, the normal way to use it is to use scoring recipes.

However, you can also use the {class}`dataiku.Model` class in a Python recipe or notebook to directly score records.

This method has a number of limitations:

* It cannot be used together with containerized execution
* It is not compatible with Partitioned models

`````{tabs}
````{group-tab} Regular

By default, the predictor is full-featured and geared towards scoring dataframes.

`predictor.predict()` lets you score and, if needed, get the explanations associated with each prediction.

```python
  import dataiku

  m = dataiku.Model(my_model_id)
  with m.get_predictor() as predictor:
    scored_df = predictor.predict(my_df_to_score) # faster if you don't need explanations
    scored_explained_df = predictor.predict(my_df_to_score, with_explanations=True, explanation_method="ICE", n_explanations=3)
```
````
````{group-tab} Latency-optimized

Say you want to infer a single record, or a couple of records. If your model is compatible with {ref}`python export <refdoc:Python Export>`, you can use a more lightweight predictor, that is not as full-featured (e.g. cannot compute prediction explanations) but may load faster. If your model is not compatible, it will automatically fallback to the regular predictor.

```python
  import dataiku

  m = dataiku.Model(my_model_id)
  with m.get_predictor(optimize="LATENCY") as predictor:
    predictor.predict(my_df_to_score[:5])
```
````
`````

## Detailed examples

This section contains more advanced examples using ML Tasks and Saved Models.

### Deploy best MLTask model to the Flow 

After training several models in a ML Task you can programmatically deploy the best one by creating a new Saved Model or updating an existing one. In the following example:

* The `deploy_with_best_model()` function creates a new Saved Model with the input MLTask's best model
* The `update_with_best_model()` function updates an existing Saved Model with the MLTask's best model.

Both functions rely on {py:class}`dataikuapi.dss.ml.DSSMLTask` and {py:class}`dataikuapi.dss.savedmodel.DSSSavedModel`.


```{literalinclude} examples/mltasks/deploy-best-to-flow.py
```

### List details of all Saved Models 

You can retrieve, for each Saved Model in a Project, the current model algorithm and performances. In the following example, the `get_project_saved_models()` function outputs a Python dictionary with several details on the current activeversions of all Saved Models in the target Project.

```{literalinclude} examples/savedmodels/explore-project.py
```

### List version details of a given Saved Model

This code snippet allows you to retrieve a summary of all versions of a given Saved Model (algorithm, hyperparameters, performance, features) using {py:class}`dataikuapi.dss.savedmodel.DSSSavedModel`.

```{literalinclude} examples/savedmodels/list-version-details.py
```

### Retrieve linear model coefficients

You can retrieve the list of coefficient names and values from a Saved Model version for compatible algorithms.


```{literalinclude} examples/savedmodels/get-linear-model-coeffs.py
```

### Export model

You can programmatically export the best version of a Saved Model as either a Python function or a MLFlow model. In the following example, the `get_best_classifier_version()` function returns the best version id of the classifier. 

1. Pass that id to the {py:meth}`dataikuapi.dss.savedmodel.DSSSavedModel.get_version_details`  method  to get a {py:class}`dataikuapi.dss.ml.DSSTrainedPredictionModelDetails` handle.

2. Then either use {meth}`~dataikuapi.dss.ml.DSSTrainedPredictionModelDetails.get_scoring_python()` or {meth}`~dataikuapi.dss.ml.DSSTrainedPredictionModelDetails.get_scoring_mlflow()` to download the model archive to a given file name in either Python or MLflow, respectively. 


```{literalinclude} examples/savedmodels/model-export.py
```

### Using a Saved Model in a Python recipe or notebook

Once a model has been trained and deployed as a saved model, you typically use scoring recipes or API node in order to use them. 

You can however also use the saved model directly in a Python recipe or notebook for performing scoring from your own code.

This comes with several limitations:

* It only supports models trained with the in-memory engine. It does not support MLlib models.
* It does not apply the model's preparation script, if any. It expects as input a dataframe equivalent to the output of the model's preparation script.
* It does not support running in containers. Only local execution is supported.

`````{tabs}
````{group-tab} Regular

By default, the predictor is full-featured and geared towards scoring dataframes. 

`predictor.predict()` lets you score and, if needed, get the explanations associated with each prediction.

```python
  import dataiku

  m = dataiku.Model(my_model_id)
  with m.get_predictor() as predictor:
    scored_df = predictor.predict(my_df_to_score) # faster if you don't need explanations
    scored_explained_df = predictor.predict(my_df_to_score, with_explanations=True, explanation_method="ICE", n_explanations=3)
```
````
````{group-tab} Latency-optimized

Say you want to infer a single record, or a couple of records. If your model is compatible with {ref}`python export <refdoc:Python Export>`, you can use a more lightweight predictor, that is not as full-featured (e.g. cannot compute prediction explanations) but may load faster. If your model is not compatible, it will automatically fallback to the regular predictor.

```python
  import dataiku

  m = dataiku.Model(my_model_id)
  with m.get_predictor(optimize="LATENCY") as predictor:
    predictor.predict(my_df_to_score[:5])
```
````
`````

## Reference documentation

### Classes

```{eval-rst}
.. autosummary::
  dataiku.Model
  dataiku.core.saved_model.Predictor
  dataiku.core.saved_model.SavedModelVersionMetrics
  dataikuapi.dss.ml.DSSClusteringMLTaskSettings
  dataikuapi.dss.ml.DSSMLTask
  dataikuapi.dss.ml.DSSMLTaskSettings
  dataikuapi.dss.ml.DSSPredictionMLTaskSettings
  dataikuapi.dss.ml.DSSTimeseriesForecastingMLTaskSettings
  dataikuapi.dss.ml.DSSTrainedClusteringModelDetails
  dataikuapi.dss.ml.DSSTrainedPredictionModelDetails
  dataikuapi.dss.ml.PredictionSplitParamsHandler
  dataikuapi.dss.savedmodel.DSSSavedModel
  dataikuapi.dss.savedmodel.DSSSavedModelSettings
  dataikuapi.dss.savedmodel.ExternalModelVersionHandler
  dataikuapi.dss.savedmodel.MLFlowVersionSettings
```

### Functions
```{eval-rst}
.. autosummary::
    ~dataikuapi.dss.ml.DSSMLTask.deploy_to_flow
    ~dataikuapi.dss.ml.DSSTrainedPredictionModelDetails.download_documentation_to_file
    ~dataikuapi.dss.savedmodel.DSSSavedModel.get_active_version
    ~dataikuapi.dss.ml.DSSMLTaskSettings.get_algorithm_settings
    ~dataikuapi.dss.ml.DSSPredictionMLTaskSettings.get_hyperparameter_search_settings
    ~dataikuapi.dss.ml.DSSMLTaskSettings.get_feature_preprocessing
    ~dataikuapi.dss.ml.DSSTrainedPredictionModelDetails.get_modeling_settings
    ~dataikuapi.dss.ml.DSSTrainedPredictionModelDetails.get_performance_metrics
    ~dataikuapi.dss.ml.DSSTrainedPredictionModelDetails.get_raw_snippet
    ~dataikuapi.dss.project.DSSProject.get_saved_model
    ~dataikuapi.dss.ml.DSSMLTask.get_settings
    ~dataikuapi.dss.ml.DSSMLTask.get_trained_model_details
    ~dataikuapi.dss.ml.DSSMLTask.get_trained_models_ids
    ~dataikuapi.dss.ml.DSSMLTask.get_trained_model_snippet
    ~dataikuapi.dss.savedmodel.DSSSavedModel.get_version_details
    ~dataikuapi.dss.savedmodel.DSSSavedModel.list_versions
    ~dataiku.core.saved_model.Predictor.predict
    ~dataikuapi.dss.ml.DSSMLTaskSettings.reject_feature
    ~dataikuapi.dss.ml.DSSMLTaskSettings.set_algorithm_enabled
    ~dataikuapi.dss.ml.HyperparameterSearchSettings.set_kfold_validation
    ~dataikuapi.dss.ml.HyperparameterSearchSettings.set_random_search
    ~dataikuapi.dss.ml.DSSMLTask.start_train
    ~dataikuapi.dss.ml.HyperparameterSearchSettings.strategy
    ~dataikuapi.dss.ml.DSSMLTaskSettings.use_feature
    ~dataikuapi.dss.ml.HyperparameterSearchSettings.validation_mode
    ~dataikuapi.dss.ml.DSSMLTask.wait_guess_complete
    ~dataikuapi.dss.ml.DSSMLTask.wait_train_complete
```