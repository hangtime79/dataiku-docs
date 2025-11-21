# Importing serialized scikit-learn pipelines as Saved Models for MLOps

This tutorial shows how to save a model trained using code into a native Dataiku object for model management. It uses a simple tabular dataset and a scikit-learn pipeline. As long as the intermediate assets are saved, this model development could occur inside or outside Dataiku. Similar pipelines could accommodate other frameworks and data types.

Teams and organizations can have bespoke model pipelines and rules that are not fully integrated with Dataiku. This tutorial shows how to bring models via code into the platform for model lifecycle management as first-class citizens, similar to its [automated machine learning models](https://doc.dataiku.com/dss/latest/machine-learning/auto-ml.html). This last-mile integration is a key feature of Dataiku's MLOps capabilities. It allows for the inspection, evaluation, deployment and governance of models trained using code.

## Prerequisites

* Dataiku >= 12.0
* Access to a project with "write project content" permissions
* A Python code environment with the `scikit-learn`, `mlflow` and `protobuf` (not for Python 3.10+) packages installed

```{note}
This tutorial was tested using `python==3.9`, `scikit-learn==1.0.2`, `mlflow==2.9.2` and `protobuf==3.16.0` but other versions {doc}`could work <refdoc:mlops/mlflow-models/limitations>`.
```

## Overview of the steps

This tutorial covers model development in three simplified steps. Each of the scripts focuses on one of the following:

1. Preparing the data, i.e. all steps *before* model development
2. Creating the model object, i.e. the model development
3. Saving the model as a Dataiku object, i.e. what happens *after*

Here are the steps represented as a Dataiku project flow.

(tutorials_ML_modelimport_scikit_flow)=

!["pickle flow"](./assets/pickle-flow.png){.image-popup}

## Step 1: Pre-modeling tasks

To kick off this process, you'll need two things:

* the *model artifact*, a serialized version of the trained model object
* an *evaluation dataset* that is needed to monitor model performance and provide other metrics

Pipelines running outside Dataiku could produce this model artifact. Here, you'll start from scratch with some data and progress towards that model object within the platform. For simplicity and completeness, you'll generate it from the easily accessible [UCI Bank Marketing dataset](https://archive.ics.uci.edu/dataset/222/bank+marketing).

Create a Python recipe to create the initial dataset (`bank`). The script below prepares the data before model development. It defines the [URL](https://archive.ics.uci.edu/static/public/222/bank+marketing.zip) to download the data archive and stores the relevant CSV as a `pandas` dataframe. Using that dataframe and the Dataiku APIs, this step saves the schema and the file contents to a Dataiku dataset.

(tutorials_machine_learning_modelimport_scikit_step1)=

```{dropdown} [Python script - Step 1](./assets/step1_prep.py)

```{literalinclude} assets/step1_prep.py
:language: python
```

## Step 2: Model development

Next, you will use some standard scikit-learn code to create a model stored in a serialized format as a pickle. First, copy the following code in your [project libraries](https://developer.dataiku.com/latest/getting-started/environment-setup/index.html#building-a-shared-code-base) that you will find at **</> > Libraries**.

```{note}
Code libraries also provide a way to integrate with a larger code base from outside Dataiku that might have modules and scripts required for model development. Read more about the ability to pull from an external code base [here](https://developer.dataiku.com/latest/getting-started/environment-setup/index.html#bringing-an-external-code-base).
```

Under `python/`, create a directory named `model_gen` containing two files:

1. an empty `__init__.py` file
2. a `sk_pipeliner.py` script with code to train a scikit-learn model and save the test set as an evaluation dataset

Copy this code into the second file, i.e. the non-empty Python script:

(tutorials_machine_learning_modelimport_scikit_skfunction)=

```{dropdown} [Python function](./assets/sk_pipeliner.py)

```{literalinclude} assets/sk_pipeliner.py
:language: python

```

Back in the project Flow, create a Python recipe with:

1. a single input: the `bank` dataset created in the last step
2. two outputs: a new dataset called `bank_test`, which will serve as the evaluation dataset, and a new managed folder (`model_folder`) to host the model artifact. *Take note of the folder id and add it to the code below for this step.*

```{note}
Folder ids are a [property](https://developer.dataiku.com/latest/api-reference/python/managed-folders.html#dataikuapi.dss.managedfolder.DSSManagedFolder.id) of a managed folder, uniquely identifying it within a Dataiku project. It can be found on the page URL when the item is opened on the Dataiku UI (`/projects/LLMM_TESTS/managedfolder/[FOLDER_ID]`) and is composed of 8 random characters, e.g. `L3dZ3p1n`.
```

Replace the initial recipe content with code from this script. In conjunction with the function from the project libraries, this Python recipe creates the machine learning pipeline. It invokes the `split_and_train_pipeline` function from `sk_pipeliner` to train a model on the `df` dataframe obtained from the `bank` dataset. The pipeline object is stored as `pipeline.pkl` within a managed folder, which can be located on the Dataiku server, on cloud object storage or elsewhere. Additionally, the function returns a test dataset (`df_test`), which is saved as the `bank_test` dataset. The workflow also ensures that the evaluation dataset has the same schema as the dataset on which model training occurred.

(tutorials_machine_learning_modelimport_scikit_step2pickle)=

```{dropdown} [Python script - Step 2](./assets/step2_pickle.py)

```{literalinclude} assets/step2_pickle.py
:language: python

```

## Step 3: Saving as a Dataiku object

The final step is to convert the model artifact, i.e. the serialized pickle, into a Saved Model, a native Dataiku object. The immediate advantage is that Saved Models possess many post-training features like extensive [model evaluation](https://knowledge.dataiku.com/latest/ml-analytics/model-results/concept-visual-model-summary.html).

This part will create a new Saved Model on the flow from the scikit-learn pipeline. Saved Models can import models trained using code via one of the [MLflow](https://doc.dataiku.com/dss/latest/mlops/mlflow-models/index.html) integrations. So, along the way, you'll transform the scikit pipeline into an MLflow model via the Dataiku APIs.

A new Saved Model is not allowed as the output of a Python recipe, so it needs to be created programmatically first. As such, the following code needs to be run in a Dataiku Python notebook initially. Go to **</> > Notebooks > New notebook > Write your own > Python** and create a new notebook *with the code environment specified in the prerequisites*. Execute all lines to create a model flow item, convert the pickle and load its MLflow equivalent into the Dataiku Saved Model.

(tutorials_machine_learning_modelimport_scikit_step3savedmodel)=

```{dropdown} [Python script - Step 3](./assets/step3_savedmodel.py)
```{literalinclude} assets/step3_savedmodel.py

```

Let's break down some parts of the script to understand the process.

- This code block creates an empty model flow item (`clf`). It checks whether such an object already exists, which will be helpful in subsequent runs. It specifies that the Saved Model holds MLflow models (`create_mlflow_pyfunc_model()`) for binary classification prediction.

```{literalinclude} assets/step3_savedmodel.py
:language: python
:lines: 20-34
```

* The model is then deserialized from the pickle file (`pipeline.pkl`) located in the managed folder.

```{literalinclude} assets/step3_savedmodel.py
:language: python
:lines: 41-43
```

- Then, the deserialized model is logged as an MLflow model via [experiment tracking](https://developer.dataiku.com/latest/concepts-and-examples/experiment-tracking.html)--a dummy run functions as a conversion step.

```{literalinclude} assets/step3_savedmodel.py
:language: python
:lines: 48-56
```

- Finally, comparing the model results with the `evaluation_dataset` *bank_test*,  `mlflow_extension.deploy_run_model()` triggers the evaluation features, unlocking the explainability and interpretability visualizations in the Dataiku UI.

```{literalinclude} assets/step3_savedmodel.py
:language: python
:lines: 58-64

```

## Wrapping up

If you want to add the last script in the flow, use the **Create Recipe** button on the notebook to create a Python recipe with `model_folder` and `bank_test` as inputs and the Dataiku model object (`clf`) as the output. You could use just this step to import pickled models into Dataiku. Of course, there are technical considerations and constraints during such an import. Among others, you'll have to ensure the evaluation dataset has the same schema as the training dataset and the consistency of the Python packages used.
