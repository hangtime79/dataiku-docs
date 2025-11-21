:tocdepth: 3

Machine learning
#################

For usage information and examples, see :doc:`/concepts-and-examples/ml`

API Reference
=============

Interaction with a ML Task
--------------------------

.. autoclass:: dataikuapi.dss.ml.DSSMLTask
    :members:
    :undoc-members:


Manipulation of settings
------------------------

.. autoclass:: dataikuapi.dss.ml.HyperparameterSearchSettings
    :members:
    :undoc-members:

.. autoclass:: dataikuapi.dss.ml.DSSMLTaskSettings
    :members:
    :undoc-members:

.. autoclass:: dataikuapi.dss.ml.DSSPredictionMLTaskSettings
    :members:
    :undoc-members:
    :inherited-members: DSSMLTaskSettings

.. autoclass:: dataikuapi.dss.ml.DSSClusteringMLTaskSettings
    :members:
    :undoc-members:

.. autoclass:: dataikuapi.dss.ml.DSSTimeseriesForecastingMLTaskSettings
    :members:
    :undoc-members:
    :inherited-members: DSSMLTaskSettings

.. autoclass:: dataikuapi.dss.ml.PredictionSplitParamsHandler
    :members:
    :undoc-members:

Exploration of results
----------------------

.. autoclass:: dataikuapi.dss.ml.DSSTrainedPredictionModelDetails
    :inherited-members:

.. autoclass:: dataikuapi.dss.ml.DSSTrainedClusteringModelDetails
    :inherited-members:

.. autoclass:: dataikuapi.dss.ml.DSSTrainedTimeseriesForecastingModelDetails

Saved models
------------

.. autoclass:: dataikuapi.dss.savedmodel.DSSSavedModel

.. autoclass:: dataikuapi.dss.savedmodel.DSSSavedModelSettings

.. autoclass:: dataiku.core.saved_model.SavedModelVersionMetrics
    :members:

.. autoclass:: dataiku.Model

MLflow models
--------------

.. autoclass:: dataikuapi.dss.savedmodel.ExternalModelVersionHandler

.. autoclass:: dataikuapi.dss.savedmodel.MLFlowVersionSettings

dataiku.Model
--------------

.. autoclass:: dataiku.Model
    :noindex:
    :members:

.. autoclass:: dataiku.core.saved_model.Predictor
    :noindex:
    :members:

Algorithm details
=================

This section documents which algorithms are available, and some of the settings for them.

These algorithm names can be used for :meth:`dataikuapi.dss.ml.DSSMLTaskSettings.get_algorithm_settings` and  :meth:`dataikuapi.dss.ml.DSSMLTaskSettings.set_algorithm_enabled`

.. note::

    This documentation does not cover all settings of all algorithms. To know which settings are
    available for an algorithm, use ``mltask_settings.get_algorithm_settings('ALGORITHM_NAME')``
    and print the returned dictionary.

    Generally speaking, most algorithm settings which are arrays means that this parameter can be
    grid-searched. All values will be tested as part of the hyperparameter optimization.

    For more documentation of settings, please refer to the UI of the visual machine learning, which
    contains detailed documentation for all algorithm parameters

LOGISTIC_REGRESSION
-------------------

* Type: Prediction (binary or multiclass)
* Available on backend: PY_MEMORY
* Main parameters:

.. code-block:: python

    {
        "multi_class": SingleCategoryHyperparameterSettings, # accepted valued: ['multinomial', 'ovr']
        "penalty": CategoricalHyperparameterSettings, # possible values: ["l1", "l2"]
        "C": NumericalHyperparameterSettings, # scaling: "LOGARITHMIC"
        "n_jobs": 2
    }

RANDOM_FOREST_CLASSIFICATION
----------------------------

* Type: Prediction (binary or multiclass)
* Available on backend: PY_MEMORY
* Main parameters:

.. code-block:: python

    {
        "n_estimators": NumericalHyperparameterSettings, # scaling: "LINEAR"
        "min_samples_leaf": NumericalHyperparameterSettings, # scaling: "LINEAR"
        "max_tree_depth": NumericalHyperparameterSettings, # scaling: "LINEAR"
        "max_feature_prop": NumericalHyperparameterSettings, # scaling: "LINEAR"
        "max_features": NumericalHyperparameterSettings, # scaling: "LINEAR"
        "selection_mode": SingleCategoryHyperparameterSettings, # accepted_values=['auto', 'sqrt', 'log2', 'number', 'prop']
        "n_jobs": 4
    }


RANDOM_FOREST_REGRESSION
------------------------

* Type: Prediction (regression)
* Available on backend: PY_MEMORY
* Main parameters: same as RANDOM_FOREST_CLASSIFICATION


EXTRA_TREES
-----------

* Type: Prediction (all kinds)
* Available on backend: PY_MEMORY

RIDGE_REGRESSION
----------------

* Type: Prediction (regression)
* Available on backend: PY_MEMORY

LASSO_REGRESSION
----------------

* Type: Prediction (regression)
* Available on backend: PY_MEMORY

LEASTSQUARE_REGRESSION
----------------------

* Type: Prediction (regression)
* Available on backend: PY_MEMORY

SVC_CLASSIFICATION
------------------

* Type: Prediction (binary or multiclass)
* Available on backend: PY_MEMORY

SVM_REGRESSION
--------------

* Type: Prediction (regression)
* Available on backend: PY_MEMORY

SGD_CLASSIFICATION
------------------

* Type: Prediction (binary or multiclass)
* Available on backend: PY_MEMORY

SGD_REGRESSION
--------------

* Type: Prediction (regression)
* Available on backend: PY_MEMORY

GBT_CLASSIFICATION
------------------

* Type: Prediction (binary or multiclass)
* Available on backend: PY_MEMORY

GBT_REGRESSION
--------------

* Type: Prediction (regression)
* Available on backend: PY_MEMORY

DECISION_TREE_CLASSIFICATION
----------------------------

* Type: Prediction (binary or multiclass)
* Available on backend: PY_MEMORY

DECISION_TREE_REGRESSION
------------------------

* Type: Prediction (regression)
* Available on backend: PY_MEMORY

LIGHTGBM_CLASSIFICATION
-----------------------

* Type: Prediction (binary or multiclass)
* Available on backend: PY_MEMORY

LIGHTGBM_REGRESSION
-------------------

* Type: Prediction (regression)
* Available on backend: PY_MEMORY

XGBOOST_CLASSIFICATION
----------------------

* Type: Prediction (binary or multiclass)
* Available on backend: PY_MEMORY

XGBOOST_REGRESSION
------------------

* Type: Prediction (regression)
* Available on backend: PY_MEMORY

NEURAL_NETWORK
---------------

* Type: Prediction (all kinds)
* Available on backend: PY_MEMORY

MULTI_LAYER_PERCEPTRON_REGRESSION
---------------------------------

* Type: Prediction (regression)
* Available on backend: PY_MEMORY

MULTI_LAYER_PERCEPTRON_CLASSIFICATION
-------------------------------------

* Type: Prediction (binary or multiclass)
* Available on backend: PY_MEMORY

KNN
---

* Type: Prediction (all kinds)
* Available on backend: PY_MEMORY

LARS
----

* Type: Prediction (all kinds)
* Available on backend: PY_MEMORY

MLLIB_LOGISTIC_REGRESSION
-------------------------

* Type: Prediction (binary or multiclass)
* Available on backend: MLLIB

MLLIB_DECISION_TREE
-------------------

* Type: Prediction (all kinds)
* Available on backend: MLLIB

MLLIB_RANDOM_FOREST
-------------------

* Type: Prediction (all kinds)
* Available on backend: MLLIB

MLLIB_GBT
---------

* Type: Prediction (all kinds)
* Available on backend: MLLIB

MLLIB_LINEAR_REGRESSION
-----------------------

* Type: Prediction (regression)
* Available on backend: MLLIB

MLLIB_NAIVE_BAYES
-----------------

* Type: Prediction (all kinds)
* Available on backend: MLLIB

Other
------

* SCIKIT_MODEL
* MLLIB_CUSTOM