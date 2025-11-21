Exporting models
#################

DSS provides multiple capabilities for exporting models.

.. contents::
        :local:

Deploy the model on Dataiku API nodes for real-time scoring
============================================================

See :doc:`/apinode/index`, and its subsections :doc:`/apinode/endpoint-std` and :doc:`/apinode/endpoint-mlflow`.


.. _Python Export:

Export to Python
=================

For use cases where the API node may not be feasible (such as edge deployment, or very-low-latency deployment), it is possible to export the model to a zip file that can then be used to score the model in any Python code, fully outside of DSS.

This scoring uses the `dataiku-scoring` open source Python package.

Note that this feature is not available in all Dataiku licenses. You may need to reach out to your Dataiku Account Manager or Customer Success Manager.

* Go to the trained model you wish to export (either a model trained in the Lab or a version of a saved model deployed in the Flow)
* Click the `Actions` button on the top-right corner and select `Export model as ...`
* Select `Python` to download the export file

.. _python export requirements:

Requirements
------------

The model needs to be compatible with either :doc:`Local (Optimized) scoring <scoring-engines>` or be an :doc:`MLflow imported model <../mlops/mlflow-models/importing>` to be compatible with Python export.

The `dataiku-scoring` package is available on Pypi. It is compatible with Python 3.6 and above, and depends on NumPy.

To ensure to install the correct version, you can unzip the exported model file and run:

.. code-block:: bash

    pip install -r requirements.txt

You can optionally use Pandas for easier interaction with the model. All Pandas versions above 0.23 are supported.

.. _python export input data:

Usage
-----

The package exposes the ``load_model`` function, which allows you to load the model’s zip file as a python object. The loaded model will have a ``predict`` method and a ``predict_proba`` method for classification problems. Here are the signatures of these methods:


.. code-block:: python

    predict(
      data: [pandas.DataFrame, numpy.ndarray, List[Dict | List]]
    ) -> numpy.array

    # Only exists for classification problems
    predict_proba(
      data: [pandas.DataFrame, numpy.ndarray, List[Dict | List]]
    ) -> numpy.darray


Example
-------

We train a model in DSS on the `iris dataset <https://scikit-learn.org/stable/auto_examples/datasets/plot_iris_dataset.html>`_  and download it using Python export. The iris dataset is a multiclass classification problem where the output classes are “Setosa,” “Virginica,” and “Versicolor.” Here is an example of using the downloaded zip file together with `dataiku-scoring` to score the first two rows of the iris dataset.

.. code:: python

    import dataikuscoring

    model = dataikuscoring.load_model("path/to/model.zip")

    data = [
        {'sepal.length': 5.1, 'sepal.width': 3.5, 'petal.length': 1.4, 'petal.width': 0.2},
        {'sepal.length': 4.9, 'sepal.width': 3.0, 'petal.length': 1.4, 'petal.width': 0.2}
    ]

    model.predict(data)  # returns array(['Setosa', 'Setosa'], dtype=object)

Provided you have pandas in your environment, you can also directly use a pandas.DataFrame:

.. code:: python

    import pandas as pd

    df = pd.DataFrame(data)
    model.predict(df)

Or a List of List / NumPy array:

.. code:: python

    data = [[5.1, 3.5, 1.4, 0.2], [4.9, 3.0, 1.4, 0.2]]
    model.predict(data)

    import numpy as np
    model.predict(np.array(data))

.. note::

   A warning is displayed when you use a List of List or a NumPy array as input to the ``model.predict`` method. In these cases, the column names are not provided, so features are implicitly assumed to be in the same order as in the training dataset in DSS.


Since the iris dataset is a classification problem, we can also output probabilities:

.. code:: python

    model.predict_proba(data)

will output::

    {'Virginica' : array([0.15511770783800324, 0.1360890057639774], dtype=object),
     'Versicolor': array([0.06850569755129679, 0.13872351067755467], dtype=object),
     'Setosa' : array([0.7763765946107, 0.725187483558468]}, dtype=object)}


Limitations
-----------

The Python export feature does not support preparation scripts. In your Lab analysis where you trained your model, if the Script tab has steps, those steps are not included in the exported model. If your model has a preparation script, you must prepare the data yourself before scoring with the loaded python model. The expected input of the model is the output of your preparation script.


.. _MLflow export:

Export as a MLflow model
=========================

MLflow is an open-source platform to manage machine learning models lifecycle. If your machine learning deployment pipelines already uses MLflow, you may want to use the MLflow export to benefit of DSS Visual ML tool.

You can export a zip file containing a MLflow model representing the trained in the DSS Visual ML tool. This can be used in any MLflow-compatible scoring system that supports the "python_function" flavor of MLflow

Note that this feature is not available in all Dataiku licenses. You may need to reach out to your Dataiku Account Manager or Customer Success Manager.


.. warning::

    You will need to install the `dataiku-scoring` python package (see :ref:`python export requirements`) in any python environment where you want to load and use the MLflow export of your model.

.. note::

    The `dataiku-scoring` package defines a specific `dss` flavor for MLflow that enables using a model designed and exported with DSS with MLflow. You can find the documentation `here <https://www.mlflow.org/docs/2.17.2/models.html#storage-format>`_ if you are unfamiliar with MLflow `flavors`.

.. warning::

    **Tier 2 support**: MLflow export is covered by :doc:`Tier 2 support </troubleshooting/support-tiers>`

* Go to the model you wish to export (either a model trained in the Lab or a version of a saved model deployed in the Flow)
* Click the `Actions` button on the top-right corner and select `Export model as ...`
* Select `MLFlow` to download the zip file
* Unzip the zip file to use it with MLflow

Alternatively, you can export using the :doc:`API <devguide:api-reference/python/ml>` with the following method :meth:`dataikuapi.dss.ml.DSSTrainedPredictionModelDetails.get_scoring_mlflow`.


Requirements
------------

The model needs to be compatible with either :doc:`Local (Optimized) scoring <scoring-engines>` or be an :doc:`MLflow imported model <../mlops/mlflow-models/importing>` to be compatible with Python export.

Like all MLflow models, the Dataiku-exported MLflow model contains its requirements.

You will need MLflow in version 2.17.2 at least.

Usage
-----

To load and use your model you can use the generic MLflow `python_function` flavor following:

.. code:: python

    import mlflow

    model = mlflow.pyfunc.load_model("path/to/model_unzipped")

    model.predict(input_data)

The model accepts the same input data as the one described in the Python export in :ref:`python export input data`.

For a more extensive description on how to use an MLflow model you can refer to the official MLflow `documentation <https://www.mlflow.org/docs/2.17.2/models.html#how-to-load-and-score-python-function-models>`_.

If your model is a classification model, you can access the probabilities using ``model._model_impl.dss_model.predict_proba``


"dss" MLflow flavor
---------------------

`MLflow flavors <https://www.mlflow.org/docs/2.17.2/models.html#built-in-model-flavors>`_ are adapters designed for using various machine learning frameworks with a unified API.

In addition to the `python_function` flavor, MLflow models exported from Dataiku contain a `dss` flavor which is a simple wrapper on top of the `dataiku-scoring` package described in :ref:`Python Export`, which allows you to use the `dataiku-scoring` API more directly.

The following describes the DSS flavor in the same way as other flavors in the official MLflow documentation.

The ``dataikuscoring.mlflow`` module defines the DSS flavor for MLflow. The `dss` model flavor enables logging DSS models in MLflow format via the ``dataikuscoring.mlflow.save_model()`` and ``dataikuscoring.mlflow.log_model()`` methods. These methods also add the standard MLflow `python_function` flavor to the MLflow Models that they produce, allowing the models to be interpreted as generic Python function for inference via ``mlflow.pyfunc.load_model()``. This loaded PyFunc model can only score DataFrame input. You can also use the ``dataikuscoring.mlflow.load_model()`` method to load MLflow Models with the DSS Default format. You obtain a model similar to what is described in :ref:`Python Export`.

.. note::

    When exporting a Model using the MLflow format in DSS, the resulting zip file contains a zipped version of the output of the ``dataikuscoring.mlflow.save_model()`` method.

You can load your model using the `dss` flavor by doing ``model = dataikuscoring.mlflow.load_model("path/to/model_unzipped")``. The loaded model is equivalent to the one loaded with the default Python export format and described in :ref:`python export input data`.

Logging the model to an MLflow backend
--------------------------------------

The model exported in MLflow format can later be imported into an `MLflow Model registry backend <https://www.mlflow.org/docs/2.17.2/model-registry.html>`_ or an `MLflow Tracking backend <https://www.mlflow.org/docs/2.17.2/tracking.html>`_.

The following example demonstrates how to import a model in a local MLflow backend using a local SQLite database and a DSS model exported in MLflow format:

.. code:: python

    import dataikuscoring.mlflow
    import mlflow

    model = mlflow.pyfunc.load_model("path/to/model_unzipped")
    # alternatively:
    # model = dataikuscoring.mlflow.load_model("path/to/model_unzipped")

    mlflow.set_tracking_uri("sqlite:///mlflow.db")
    mlflow.set_registry_uri("sqlite:///mlflow.db")
    with mlflow.start_run() as run:
        dataikuscoring.mlflow.log_model(model, artifact_path)

You can then run ``mlflow ui --port 5001 --backend-store-uri sqlite:///mlflow.db`` in a shell to access the run and the model it contains, and deploy it to the model registry.

The model was loaded using MLflow, but its original flavor is the `dss` flavor. Therefore, we need to use the original `dss` flavor when logging the model to the backend.


Limitations
-----------

The MLflow export feature does not support preparation scripts. In your Lab analysis, where you trained your model, if the Script tab has steps, those steps are not included in the exported model. If your model has a preparation script, you must prepare the data yourself before scoring with the loaded python model. The expected input of the model is the output of your preparation script.



Export to a Databricks Registry
===============================

This export feature takes the MLflow export a step further, by pushing the model to a Databricks Registry. Both the legacy Workspace Model Registry and the Unity Catalog are supported.

It requires a valid connection to your Databricks workspace. This is done by an administrator in the Administration > Connections, by creating a connection of type "Databricks Model Depl.".

Note that this feature is not available in all Dataiku licenses. You may need to reach out to your Dataiku Account Manager or Customer Success Manager.


.. warning::

    **Tier 2 support**: Export to a Databricks Registry is covered by :doc:`Tier 2 support </troubleshooting/support-tiers>`

* Go to the model you wish to export (either a model trained in the Lab or a version of a saved model deployed in the Flow)
* Click the `Actions` button on the top-right corner and select `Export model as ...`
* Select `Databricks`
* Select a *Databricks Model Deployment Infrastructure* connection
* Check `Use Unity Catalog` to export to this registry. Else, the model will be pushed to the Workspace Model Registry.
* Enter an `Experiment Name` or click on `Get Experiments` and pick an existing one.
* Enter the name of the `Registered Model` to which a the exported model will be added as a version, on click on `Get Models` and pick an existing one.


.. note::
    Like all MLflow models, the Dataiku-exported MLflow model contains its requirements.

    * In the case of a model **trained in Dataiku**, those requirements will most noticeably include the `dataiku-scoring` library.
    * In the case of a model **imported from an MLflow model**, the original model will be exported. **The requirements from the imported model will be used**, not the requirements of the code env

Requirements
------------

The model needs to be compatible with either :doc:`Local (Optimized) scoring <scoring-engines>` or be an :doc:`MLflow imported model <../mlops/mlflow-models/importing>`.


Limitations
-----------

The MLflow export feature does not support preparation scripts. In your Lab analysis, where you trained your model, if the Script tab has steps, those steps are not included in the exported model. If your model has a preparation script, you must prepare the data yourself before scoring with the loaded python model. The expected input of the model is the output of your preparation script.



Export a Java class/JAR for a model
===================================


.. note::

   Starting with DSS 13, JAR export requires Java 11 or newer.


For use cases where the API node may not be feasible (such as edge deployment, or very-low-latency deployment), it is possible to export the model to a JAR file that can then be used to score the model in any Java code, fully outside of DSS.

Note that this feature is not available in all Dataiku licenses. You may need to reach out to your Dataiku Account Manager or Customer Success Manager.

The model needs to be compatible with :doc:`Local (Optimized) scoring <scoring-engines>` to be compatible with Java export.

* Go to the trained model you wish to export (either a model trained in the Lab or
  a version of a saved model deployed in the Flow)
* Click the `Actions` button on the top-right corner and select `Export model as ...`
* Select `Java`, indicate the full-qualified class name you want for your model

Add that JAR to the classpath of your Java application.

If you have several models you wish to use on the same JVM, you can export the "thin" JAR for each model, which only contains the class and resources for the model, and not the scoring libraries. In that case, you also need to download the scoring libraries (from the same dropdown menu) and add both JARs to the classpath.

Usage
-----

If you specified the name ``com.mycompany.myproject.MyModel`` at export time, you can use it like this once you've added the JAR to the classpath:

.. code:: java

    import com.mycompany.myproject.MyModel;
    import com.dataiku.scoring.*;

    // ...
    MyModel model = new MyModel();
    Observation.Builder obsBuilder = model.observationBuilder();
    Observation obs = obsBuilder
        .with("myCategoricalFeature", "Some string value")
        .with("myNumericFeature", 42.0d)
        // other .with("featureName", <string or double value>)
        .build();
    if (obs.hasError()) {
        System.err.println("Can't build observation: " + obs.getErrorMessage());
        // maybe throw here
    }

    // For a classification model
    Try<ClassificationResult> prediction = model.predict(obs);
    if (prediction.isError()) {
        System.err.println("Can't make a prediction: " + prediction.getMessage());
        // maybe throw here
    } else {
        ClassificationResult result = prediction.get();
        // predictedClass is one of model.getClassLabels()
        String predictedClass = result.getPrediction();
         // probabilities has the same indices as model.getClassLabels()
         // i.e. 0 to (model.getNumClasses() - 1)
        double[] probabilities = result.getProbabilities();
        // Use result here
    }

    // For a regression model
    Try<RegressionResult> prediction = model.predict(obs);
    if (prediction.isError()) {
        System.err.println("Can't make a prediction: " + prediction.getMessage());
        // maybe throw here
    } else {
        RegressionResult result = prediction.get();
        double predictedValue = result.getPrediction();
        // Use result here
    }

You can find the javadoc for the ``com.dataiku.scoring`` package here: |scoring_api_doc_url|.

If you want to debug your model, you can run the "fat" jar version with ``-jar``:

.. code:: bash

    java -jar /path/to/dataiku-model-my-model-assembly.jar

... or the "thin" jar version, specifying you model class as the Main class to run:

.. code:: bash

    java -cp /path/to/dataiku-model-my-model.jar:/path/to/dataiku-scoring-libs_DSS_VERSION.jar \
        com.mycompany.myproject.MyModel

This command will take JSON objects with feature values on standard input (one per line),
and return predictions as JSON objects on standard output (one per line as well).
For instance with a classification model trained on the classical Titanic dataset:

.. code:: bash

    $ echo '{"Sex": "male", "Pclass": 3}' >titanic.txt
    $ echo '{"Sex": "female", "Pclass": 1}' >>titanic.txt
    $ java -jar dataiku-model-survived-on-titanic-assembly.jar <titanic.txt >out.txt
    Nov 26, 2018 3:03:39 PM com.dataiku.scoring.pipelines.Normalization <init>
    INFO: Normalize columns
    Nov 26, 2018 3:03:39 PM com.dataiku.scoring.builders.Build binaryProbabilisticPipeline
    INFO: Loaded model:
    Nov 26, 2018 3:03:39 PM com.dataiku.scoring.builders.Build binaryProbabilisticPipeline
    INFO: com.dataiku.scoring.models.ForestClassifier@3cd1f1c8
    Nov 26, 2018 3:03:39 PM com.dataiku.scoring.builders.Build preprocessingPipeline
    INFO: Loaded preprocessing pipeline:
    Nov 26, 2018 3:03:39 PM com.dataiku.scoring.builders.Build preprocessingPipeline
    INFO: PreprocessingPipeline(
        ImputeWithValue(Pclass -> 2.3099579242636747 ; Parch -> 0.364656381486676 ; SibSp -> 0.5105189340813464 ; Age -> 29.78608695652174 ; Fare -> 32.91587110799433 ; )
        Dummifier(Sex in [female, male, ] ; Embarked in [Q, S, C, ])
        Rescaler(Fare (shift, inv_scale)=(32.91587110799433, 0.01887857758669009) ; Age (shift, inv_scale)=(29.78608695652174, 0.07038582694206309) ; Parch (shift, inv_scale)=(0.364656381486676, 1.2618109015803536) ; Pclass (shift, inv_scale)=(2.3099579242636747, 1.2048162082648861) ; SibSp (shift, inv_scale)=(0.5105189340813464, 0.9172989588087348))
    )

    $cat out.txt
    {"value":{"probabilities":{"died":0.6874695011372898,"survived":0.3125304988627102},"prediction":"died"},"isError":false}
    {"value":{"probabilities":{"died":0.062296226501392105,"survived":0.9377037734986079},"prediction":"survived"},"isError":false}

``com.dataiku.scoring`` uses ``java.util.logging`` for logging. If you wish to forward it to log4j or logback,
you can use a `SLF4J bridge <https://www.slf4j.org>`_.

Binary classifier threshold
---------------------------

By default, the threshold used is the model's threshold (as set automatically or manually before the model was exported).
However, the threshold can easily be overridden:

* From Java code:

.. code:: java

    MyModel model = new MyModel(0.42);  // forces threshold to 0.42

* From model JAR command line:

.. code:: bash

    java -jar /path/to/dataiku-model-my-model-assembly.jar --threshold 0.42


.. _Java Limitations:

Limitations
-----------

The Java export feature does not support preparation scripts. In your Lab analysis where you trained your
model, if the Script tab has steps then those steps are not included in the exported model.
If your model has a preparation script, you will need to prepare the data yourself before scoring with the JAR.
The expected input of the model (the features you add in an ``ObservationBuilder`` to build an ``Observation``)
is the output of your preparation script.


Export a PMML file for a model
===================================

PMML is a XML-based language to define models, and score them using any PMML-compatible scoring system.

You can export a PMML file containing a Dataiku model, which can then be used in any PMML-compatible scoring system.

Note that this feature is not available in all Dataiku licenses. You may need to reach out to your Dataiku Account Manager or Customer Success Manager.

.. warning::

    **Tier 2 support**: PMML export is covered by :doc:`Tier 2 support </troubleshooting/support-tiers>`

If your model is compatible with PMML export (see Limitations below):

* Go to the trained model you wish to export (either a model trained in the Lab or
  a version of a saved model deployed in the Flow)
* Click the `Actions` button on the top-right corner and select `Export model as ...`
* Select PMML


Limitations
-----------

The following preprocessing options are compatible with PMML export:

* Numeric features with regular handling
* Categorical features with impact-coding or Dummy-encoding handling
* "Impute with" and "Treat as regular" options when handling missing values. ("Drop rows" option is not compatible)
* No Vector, Image, Binary or Text features
* No feature generation (numerical derivatives, combination…)
* No dimensionality reduction

The following algorithms are compatible with PMML export:

* Logistic Regression
* Extra trees
* Linear Regression
* Decision Tree
* Random Forest
* Gradient tree boosting, excluding XGBoost

The PMML export feature does not support preparation scripts. In your Lab analysis where you trained your
model, if the Script tab has steps then those steps are not included in the exported model.
If your model has a preparation script, you will need to prepare the data yourself before scoring.
The expected input of the model is the output of your preparation script.

The PMML export outputs probabilities and will use the optimized threshold for binary classification.

The PMML export feature does not support probability calibration.

Computer vision models are not compatible with PMML export.


Export to Jupyter notebook
==========================

.. note::

    This only applies to models trained using the "In-memory (Python)" engine, both for prediction and clustering.
    Not all algorithms are supported by this feature.

Once a model has been trained, you can export it as a Jupyter notebook.

DSS will automatically generate a Jupyter (Python) notebook with code to reproduce a model *similar* to the model that you trained.

To generate a Jupyter notebook:

* Go to the trained model you wish to export
* Click the dropdown icon next to the "Deploy" button
* Select "Export to Jupyter notebook"

.. warning::

    This generated notebook is for educational and explanatory purposes only. In particular, this notebook does not reproduce
    all preprocessing capabilities of DSS, and is only a best-effort approximation of the model trained in DSS.

    To use the exact model trained by DSS, deploy it to the Flow and use the API node, scoring recipes, or any of the export methods described above


Export as a Snowflake function
==============================

Dataiku supports exporting models to Snowflake by leveraging Java User-Defined Functions (Java UDF).

Note that this feature is not available in all Dataiku licenses. You may need to reach out to your Dataiku Account Manager or Customer Success Manager.

The model needs to be compatible with :doc:`Local (Optimized) scoring <scoring-engines>` to be compatible with Snowflake export.

* Go to the saved model version you wish to export (saved model deployed in the Flow)
* Click the `Actions` button on the top-right corner and select `Export model as ...`
* Select `Snowflake`:

  * Select the Snowflake connection where the function will be created.
  * Indicate the name of the Snowflake function (must be unique within connection's schema).


Usage
-----

If you named the function ``mymodel_predict`` at export time, you can use it like this:

* By constructing an object containing the features:

.. code:: sql

  SELECT MYMODEL_PREDICT( OBJECT_CONSTRUCT('Embarked', 1, 'Pclass', 1, 'Sex', 'female','Age', 32)) as OUTPUT;

.. code::

    +----------------------------+
    | OUTPUT                     |
    |----------------------------|
    | {                          |
    |   "isError": false,        |
    |   "value": {               |
    |     "prediction": "1",     |
    |     "probabilities": [     |
    |       0.24289949134462374, |
    |       0.7571005086553763   |
    |     ]                      |
    |   }                        |
    | }                          |
    +----------------------------+

* Or by scoring a full table:

.. code:: sql

    SELECT
        "PassengerId",
        -- features:
        "Embarked",
        "Pclass",
        "Sex",
        "Age",
        -- output:
        "proba_0",
        "proba_1",
        "prediction"
    FROM (
        SELECT
            *,
            RESULT:value:prediction AS "prediction",
            RESULT:value:probabilities[0] AS "proba_0",
            RESULT:value:probabilities[1] AS "proba_1"
        FROM (
            SELECT
                *,
            MYMODEL_PREDICT( OBJECT_CONSTRUCT('Embarked', "Embarked", 'Pclass', "Pclass", 'Sex', "Sex", 'Age', "Age") ) AS "RESULT"
            FROM "KAGGLE_TITANIC_TEST" "data"
        ) "__object"
    );

.. code::

    +-------------+----------+--------+--------+------+---------------------+---------------------+------------+
    | PassengerId | Embarked | Pclass | Sex    | Age  | proba_0             | proba_1             | prediction |
    |-------------+----------+--------+--------+------+---------------------+---------------------+------------|
    | 1           | S        | 200    | male   | 22   | 0.6443216459989076  | 0.35567835400109243 | "0"        |
    | 891         | Q        | 3      | male   | 32   | 0.6059553812552487  | 0.39404461874475133 | "0"        |
    | 890         | C        | 1      | male   | 26   | 0.5074257883223362  | 0.4925742116776638  | "1"        |
    | 889         | S        | 3      | female | NULL | 0.40013285410010047 | 0.5998671458998995  | "1"        |
    +-------------+----------+--------+--------+------+---------------------+---------------------+------------+

Limitations
-----------

Since the Snowflake export is built upon the Java export feature, Java export limitations also apply to Snowflake exports, see :ref:`Java Limitations`.
