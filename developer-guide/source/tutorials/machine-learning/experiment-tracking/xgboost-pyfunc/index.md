# Experiment Tracking with the PythonModel module

The MLflow library provides many functions to log/save and load different flavors of ML models. For example, to log a scikit-learn model, you can simply invoke the `mlflow.sklearn.log_model(your_scikit_model)` method.

To log more exotic ML libraries or custom models, MLflow offers the possibility to wrap them in a python class inheriting the [`mlflow.pyfunc.PythonModel`](https://www.mlflow.org/docs/2.17.2/python_api/mlflow.pyfunc.html#mlflow.pyfunc.PythonModel) module.

This wrapper is particularly convenient when a model consisting of multiple frameworks needs to be logged as a single MLflow-compliant object. The most common use-case for this is when one needs a given framework to pre-process the data and another one for the ML algorithm itself. In Dataiku, models logged to and subsequently deployed from the [Experiment Tracking interface](https://doc.dataiku.com/dss/latest/mlops/experiment-tracking/viewing.html) need to be single objects capable of handling both the data pre-processing and scoring part.

In this tutorial, you will build an example that wraps an [XGBoost Classifier](https://xgboost.readthedocs.io/en/stable/python/python_api.html#xgboost.XGBClassifier) with a [scikit-learn preprocessing](https://scikit-learn.org/stable/modules/preprocessing.html#preprocessing) layer and saves them in the MLflow format ready to be visualized in the Experiment Tracking interface and ultimately deployed. This tutorial is based on an [example provided in the MLFlow documentation](https://www.mlflow.org/docs/2.17.2/models.html#example-saving-an-xgboost-model-in-mlflow-format). 

## Prerequisites

* A Python code environment containing the following libraries (see supported versions [here](https://doc.dataiku.com/dss/latest/mlops/mlflow-models/limitations.html)) :
    * [mlflow](https://www.mlflow.org/docs/2.17.2/getting-started/intro-quickstart/index.html))
    * [scikit-learn](https://scikit-learn.org/stable/install.html#installation-instructions)
    * [xgboost](https://xgboost.readthedocs.io/en/stable/install.html#python)
* A Dataiku project with a managed folder in it. 

## Wrapping an XGBoost classifier alongside a scikit-learn pre-processing layer

The following class inherits the [`mlflow.pyfunc.PythonModel`](https://www.mlflow.org/docs/2.17.2/python_api/mlflow.pyfunc.html#mlflow.pyfunc.PythonModel) and contains two crucial methods: 


```py
class XGBWrapper(mlflow.pyfunc.PythonModel):
    def load_context(self, context):
        from cloudpickle import load
        self.model = load(open(context.artifacts["xgb_model"], 'rb'))
        self.preprocessor = load(open(context.artifacts["preprocessor"], 'rb'))

    def predict(self, context, model_input):
        model_input = model_input[['sepal length (cm)', 'sepal width (cm)',
                                   'petal length (cm)', 'petal width (cm)']]
        model_input = self.preprocessor.transform(model_input)
        return self.model.predict_proba(model_input)
```
1. 
    The `load_context()` method will be run at load time and allows to load all the artifacts needed in the `predict()` method. The `context` parameter is a [`PythonModelContext`](https://www.mlflow.org/docs/2.17.2/python_api/mlflow.pyfunc.html#mlflow.pyfunc.PythonModelContext) instance that is created implicitly at model log or save time. This parameter contains an `artifacts` dictionary whose values are paths to the serialized objects. For example:

    ```py
    artifacts = {
        "xgb_model": "path/to/xgb_model.plk", 
        "preprocessor": "path/to/preprocessor.pkl"
    }
    ```

Where the `xgb_model.plk` and `preprocessor.pkl` would be a fitted XGBoost model and a scikit-learn preprocessor. Those would be serialized using `cloudpickle` and saved to some local directory.

2. 
    The `predict()` method of the `XGBWrapper` class is used to predict whatever data is passed through the `model_input` parameter. That parameter is expected to be a `pandas.DataFrame`. In the case of a classification problem, we recommend this `predict()` method to return the model's `predict_proba()` so as to output the different class probabilities along with the class prediction. An added benefit to returning `predict_proba()` is being able to visualize all the classifier insights once the model is deployed in the flow.
    
    Note that the `predict()` method can also take the same `context` parameter as that found in the `load_context()` method. Yet, it is more efficient to load artifacts only once using the `load_context()` method.


## Full example
In this example, you will be using the [Iris dataset](https://archive.ics.uci.edu/ml/datasets/iris) available through the scikit-learn datasets module.


### 1. Preparing the experiment

Start by setting the following variables, handles and function for the experiment:

```py
import dataiku 
from datetime import datetime

# Replace these constants with your own values
PREDICTION_TYPE = "MULTICLASS"
EXPERIMENT_FOLDER_ID = ""          # Replace with your Managed Folder id 
EXPERIMENT_NAME = ""               # Replace with your experiment name
MLFLOW_CODE_ENV_NAME = ""          # Replace with your code environment name

def now_str():
    return datetime.now().strftime("%Y%m%d%H%M%S")

# Get the current project handle
client = dataiku.api_client()
project = client.get_default_project()

# Create a mlflow_extension object to easily log information about our models
mlflow_extension = project.get_mlflow_extension()

# Get a handle on a Managed Folder to store the experiments.
mf = project.get_managed_folder(EXPERIMENT_FOLDER_ID)
```

### 2. Loading the data

In a Dataiku project, create a Python notebook and set its kernel to the code environment listed in the above prerequisites.

Run the following code:

```py
import dataiku
import pandas as pd
from sklearn import datasets
from sklearn.model_selection import train_test_split


iris = datasets.load_iris()

features = iris.feature_names
target = 'species'
df = pd.DataFrame(iris.data, columns=features)
mapping = {k:v for k,v in enumerate(iris.target_names)}
df[target] = [mapping.get(val) for val in iris.target]

df_train, df_test = train_test_split(df,test_size=0.2, random_state=42)

X_train = df_train.drop(target, axis=1)
y_train = df_train[target]

X_test = df_test.drop(target, axis=1)
y_test = df_test[target]
```



### 3. Preprocessing the data

In this step: 
* Specify the target and the features. 
* Set up a [scikit-learn Pipeline](https://scikit-learn.org/stable/modules/generated/sklearn.pipeline.Pipeline.html) to impute potential missing values and rescale continuous variables.

```py
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from cloudpickle import dump, load


preprocessor = Pipeline([
    ('imp', SimpleImputer(strategy='median')),
    ('sts', StandardScaler()),
])

X_train = preprocessor.fit_transform(X_train)
X_test = preprocessor.transform(X_test)

artifacts = {
    "xgb_model": "xgb_model.plk", 
    "preprocessor": "preprocessor.pkl"
}

# pickle and save the preprocessor
dump(preprocessor, open(artifacts.get("preprocessor"), 'wb'))
```

### 4. Training and logging the model 

Finally, train the xgboost classifier. Log the hyperparameters, performance metrics and the classifier itself into your Experiment run. 
```py
import xgboost as xgb
from sklearn.metrics import precision_score

hparams = {
    "max_depth": 5,
    "n_estimators": 50
}

with project.setup_mlflow(mf) as mlflow:
    experiment_id = mlflow.create_experiment(f'{EXPERIMENT_NAME}_{now_str()}')
    
    class XGBWrapper(mlflow.pyfunc.PythonModel):
        def load_context(self, context):
            from cloudpickle import load
            self.model = load(open(context.artifacts["xgb_model"], 'rb'))
            self.preprocessor = load(open(context.artifacts["preprocessor"], 'rb'))

        def predict(self, context, model_input):
            model_input = model_input[['sepal length (cm)', 'sepal width (cm)',
                                       'petal length (cm)', 'petal width (cm)']]
        
            model_input = self.preprocessor.transform(model_input)
            return self.model.predict_proba(model_input)

    with mlflow.start_run(experiment_id=experiment_id) as run:
        print(f'Starting run {run.info.run_id} ...\n{hparams}')

        model = xgb.XGBClassifier(**hparams)
        model.fit(X_train, y_train)

        # pickle and save the model
        dump(model, open(artifacts.get("xgb_model"), 'wb'))

        preds = model.predict(X_test)
        precision = precision_score(y_test, preds, average=None)

        run_metrics = {f'precision_{k}':v for k,v in zip(model.classes_, precision)}

        # Save the MLflow Model, hyper params and metrics
        mlflow_pyfunc_model_path = f"xgb_mlflow_pyfunc-{run.info.run_id}"
        mlflow.pyfunc.log_model(
            artifact_path=mlflow_pyfunc_model_path, python_model=XGBWrapper(),
            artifacts=artifacts)

        mlflow.log_params(hparams)
        mlflow.log_metrics(run_metrics)

        mlflow_extension.set_run_inference_info(run_id=run._info.run_id, 
                                                prediction_type='MULTICLASS',
                                                classes=list(model.classes_),
                                                code_env_name=MLFLOW_CODE_ENV_NAME)  
        print(f'Run {run.info.run_id} done\n{"-"*40}')
```

You're done! You can now go to the [Experiment Tracking interface](https://doc.dataiku.com/dss/latest/mlops/experiment-tracking/viewing.html) to check the performance of your model. You can also either deploy the model from that interface or using the [dataiku API](https://doc.dataiku.com/dss/latest/mlops/mlflow-models/importing.html#importing-mlflow-models). For either deployment, you will need an evaluation dataset that has the same schema as that of your training dataset (although the order of the columns is does not matter).


## Conclusion
In this tutorial, you learned how to wrap two frameworks under a single MLFlow-compliant object and log it along with key metadata.
Having to use multiple frameworks is frequent in many areas of ML. For example: 

* In Natural Language Processing (NLP) one may want to pre-process the data using a pre-trained embedding layer (say [`spaCy`](https://spacy.io/)) before scoring them using a [`PyTorch`](https://pytorch.org/) classifier.

* In the field of Computer Vision, the [`Pillow`](https://pillow.readthedocs.io/en/stable/) library can be used to decode image bytes from base64 encoding before being scored using [`Keras`](https://keras.io/) or some other library.




