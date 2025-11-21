(model-evaluation-stores)=

```{eval-rst}
..
  this code samples has been verified on DSS: 14.2.0-alpha3
  Date of check: 15/09/2025

  this code samples has been verified on DSS: 13.2.0
  Date of check: 04/10/2024
```

# Model Evaluation Stores

Through the public API, the Python client allows you to perform evaluation of models. Those models are typically models trained in the Lab, and then deployed to the Flow as Saved Models (see {doc}`ml` for additional information). They can also be external models.

## Concepts

### With a DSS model

In DSS, you can evaluate a **version** of a Saved Model using an Evaluation Recipe. 
An Evaluation Recipe takes as input a Saved Model and a Dataset on which to perform this evaluation.
An Evaluation Recipe can have three outputs:

- an **output** dataset,
- a **metrics** dataset, or
- a **Model Evaluation Store** (MES).

By default, the **active** version of the Saved Model is evaluated.
This can be configured in the Evaluation Recipe.

If a MES is configured as an output, a **Model Evaluation** (ME) will be written in the MES each time the MES is built (or each time the Evaluation Recipe is run).

A Model Evaluation is a container for metrics of the evaluation of the Saved Model Version on the Evaluation Dataset. Those metrics include:

- all available **performance** metrics,
- the **Data Drift** metric.

The Data Drift metric is the accuracy of a model trained to recognize lines:

- from the evaluation dataset
- from the **train time test dataset** of the configured version of the Saved Model.

The higher this metric, the better the model can separate lines from the evaluation dataset from those from the train time test dataset. And so, the more data from the evaluation dataset is different from train time data.

Detailed information and other tools, including a binomial test, univariate data drift, and feature drift importance, are available in the **Input Data Drift** tab of a Model Evaluation. Note that this tool is interactive and that displayed results are not persisted.

### With an external model

In DSS, you can also evaluate an **external model** using a **Standalone Evaluation Recipe (SER)**.
A Standalone Evaluation Recipe takes as input a labeled dataset containing labels, predictions, and (optionally) weights. A SER takes a single output: a Model Evaluation Store.

As the Evaluation Recipe, the Standalone Evaluation Recipe will output a Model Evaluation to the configured Model Evaluation Store each time it runs. In this case, however, the Data Drift can not be computed as there is no notion of reference data.

### How evaluation is performed

The Evaluation Recipe and its counterpart for external models, the Standalone Evaluation Recipe, perform the evaluation on a sample of the Evaluation Dataset. The sampling parameters are defined in the recipe. Note that the sample will contain at most 20,000 lines.

Performance metrics are then computed on this sample.

Data drift can be computed in three ways:

- at evaluation time, between the evaluation dataset and the train time test dataset;
- using the API, between the samples of a Model Evaluation, a Saved Model Version (sample of train time test dataset) or a Lab Model (sample of train time test dataset);
- interactively, in the "Input data drift" tab of a Model Evaluation.

In all cases, to compute the Data Drift, the sample of the Model Evaluation and a sample of the reference data are concatenated. In order to balance the data, those samples are truncated to the length of the smallest one. If the size of the reference sample if higher than the size of the ME sample, the reference sample will be truncated.

So:

- at evaluation time, we shall take as input the sample of the Model Evaluation (whose length is at most 20,000 lines) and a sample of the train time test dataset;

- interactively, the sample of the reference model evaluation and:

  - if the other compared item is an ME, its sample;
  - if the other compared item is a Lab Model or an SMV, a sample of its train time test dataset.

### Limitations

Model Evaluation Stores cannot be used with:

- clustering models,
- ensembling models,
- partitioned models.

Compatible prediction models have to be Python models.

## Usage samples

### Create a Model Evaluation Store

```python
# client is a DSS API client

project = client.get_project("MYPROJECT")

mes_id = project.create_model_evaluation_store("My Mes Name")
```

Note that the display name of a Model Evaluation Store (in the above sample `My Mes Name`) is distinct from its unique id.

### Retrieve a Model Evaluation Store

```python
# client is a DSS API client

project = client.get_project("MYPROJECT")

mes_id = project.get_model_evaluation_store("mes_id")
```

### List Model Evaluation Stores

```python
# client is a DSS API client

project = client.get_project("MYPROJECT")

stores = project.list_model_evaluation_stores()
```

### Create an Evaluation Recipe

See {py:class}`dataikuapi.dss.recipe.EvaluationRecipeCreator`

### Build a Model Evaluation Store and retrieve the performance and data drift metrics of the just computed ME

```python
# client is a DSS API client

project = client.get_project("MYPROJECT")

mes = project.get_model_evaluation_store("M3s_1d")

mes.build()

me = mes.get_latest_model_evaluation()

full_info = me.get_full_info()

metrics = full_info.metrics
```

### List Model Evaluations from a store

```python
# client is a DSS API client

project = client.get_project("MYPROJECT")

mes = project.get_model_evaluation_store("M3s_1d")

me_list = mes.list_model_evaluations()
```

### Retrieve an array of creation date / accuracy from a store

```python
project = client.get_project("MYPROJECT")

mes = project.get_model_evaluation_store("M3s_1d")

me_list = mes.list_model_evaluations()
payload = er_settings.obj_payload

# Change the settings

payload['dontComputePerformance'] = True
payload['outputProbabilities'] = False
res = []

for me in me_list:
    full_info = me.get_full_info()
    creation_date = full_info.creation_date
    accuracy = full_info.metrics["accuracy"]
    res.append([creation_date,accuracy])
```

### Retrieve an array of label value / precision from a store

The date of creation of a model evaluation might not be the best way to key a metric. In some cases, it might be more interesting to use the labeling system, for instance to tag the version of the evaluation dataset.

If the user created a label `"myCustomLabel:evaluationDataset"`, he may retrieve an array of label value / precision from a store with the following snippet:

```python
project = client.get_project("MYPROJECT")

mes = project.get_model_evaluation_store("M3s_1d")

me_list = mes.list_model_evaluations()

res = []

for me in me_list:
    full_info = me.get_full_info()
    label_value = next(x for x in full_info.user_meta["labels"] if x["key"] == "myCustomLabel:evaluationDataset")
    precision= full_info.metrics["precision"]
    res.append([label_value,precision])
```

### Compute data drift of the evaluation dataset of a Model Evaluation with the train time test dataset of its base DSS model version

```python
project = client.get_project("MYPROJECT")

mes = project.get_model_evaluation_store("M3s_1d")

me1 = mes.get_latest_model_evaluation()

drift = me1.compute_drift()

drift_model_result = drift.drift_model_result
drift_model_accuracy = drift_model_result.drift_model_accuracy
print("Value: {} < {} < {}".format(drift_model_accuracy.lower_confidence_interval,
                                    drift_model_accuracy.value,
                                    drift_model_accuracy.upper_confidence_interval))
print("p-value: {}".format(drift_model_accuracy.pvalue))
```

### Compute data drift, display results and adjust parameters

```python
# me1 and me2 are two compatible model evaluations (having the same prediction type) from any store

# make sure that you import the DataDriftParams and PerColumnDriftParamBuilder before running this code

from dataikuapi.dss.modelevaluationstore import DataDriftParams, PerColumnDriftParamBuilder

drift = me1.compute_drift(me2)

drift_model_result = drift.drift_model_result
drift_model_accuracy = drift_model_result.drift_model_accuracy
print("Value: {} < {} < {}".format(drift_model_accuracy.lower_confidence_interval,
                                    drift_model_accuracy.value,
                                    drift_model_accuracy.upper_confidence_interval))
print("p-value: {}".format(drift_model_accuracy.pvalue))

# Check sample sizes
print("Reference sample size: {}".format(drift_model_result.get_raw()["referenceSampleSize"]))
print("Current sample size: {}".format(drift_model_result.get_raw()["currentSampleSize"]))


# check columns handling
per_col_settings = drift.per_column_settings
for col_settings in per_col_settings:
    print("col {} - default handling {} - actual handling {}".format(col_settings.name, col_settings.default_column_handling, col_settings.actual_column_handling))

# recompute, with Pclass set as CATEGORICAL
drift = me1.compute_data_drift(me2,
                            DataDriftParams.from_params(
                                PerColumnDriftParamBuilder().with_column_drift_param("Pclass", "CATEGORICAL", True).build()
                            )
                            )
...
```

## Reference documentation

There are two main parts related to the handling of metrics and checks in Dataiku's Python APIs:

- {class}`dataiku.core.model_evaluation_store.ModelEvaluationStore` and {class}`dataiku.core.model_evaluation_store.ModelEvaluation` in the `dataiku` package. They were initially designed for usage within DSS.
- {class}`dataikuapi.dss.modelevaluationstore.DSSModelEvaluationStore` and {class}`dataikuapi.dss.modelevaluationstore.DSSModelEvaluation` in the `dataikuapi` package. They were initially designed for usage outside of DSS.

Both set of classes have fairly similar capabilities.

For more details on the two packages, please see {doc}`/getting-started/dataiku-python-apis/index`.

### Classes

```{eval-rst}
.. autosummary::
  dataiku.ModelEvaluationStore
  dataiku.core.model_evaluation_store.ModelEvaluation
  dataikuapi.dss.modelevaluationstore.DSSModelEvaluationStore
  dataikuapi.dss.modelevaluationstore.DSSModelEvaluationStoreSettings
  dataikuapi.dss.modelevaluationstore.DSSModelEvaluation
  dataikuapi.dss.modelevaluationstore.DSSModelEvaluationFullInfo
  dataikuapi.dss.modelevaluationstore.DataDriftParams
  dataikuapi.dss.modelevaluationstore.PerColumnDriftParamBuilder
  dataikuapi.dss.modelevaluationstore.DataDriftResult
  dataikuapi.dss.modelevaluationstore.DriftModelResult
  dataikuapi.dss.modelevaluationstore.UnivariateDriftResult
  dataikuapi.dss.modelevaluationstore.ColumnSettings
  dataikuapi.dss.modelevaluationstore.DriftModelAccuracy
```

### Functions

```{eval-rst}
.. autosummary::
  ~dataikuapi.dss.modelevaluationstore.DSSModelEvaluationStore.build
  ~dataikuapi.dss.modelevaluationstore.DSSModelEvaluation.compute_data_drift
  ~dataikuapi.dss.modelevaluationstore.DSSModelEvaluation.compute_drift
  ~dataikuapi.dss.project.DSSProject.create_model_evaluation_store
  ~dataikuapi.dss.modelevaluationstore.DSSModelEvaluation.get_full_info
  ~dataikuapi.dss.modelevaluationstore.DSSModelEvaluationStore.get_latest_model_evaluation
  ~dataikuapi.dss.project.DSSProject.get_model_evaluation_store
  ~dataikuapi.DSSClient.get_project
  ~dataikuapi.dss.modelevaluationstore.DSSModelEvaluationStore.list_model_evaluations
  ~dataikuapi.dss.project.DSSProject.list_model_evaluation_stores
```