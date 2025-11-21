Limitations and supported versions
##################################


Dataiku makes best effort to ensure that the MLflow import capability is compatible with a wide variety of MLflow models.

However, MLflow imposes extremely few constraints on models, and different MLflow models are allowed to behave in arbitrary non-standard ways and to return completely different kind of data.

It is thus not possible to guarantee unfettered ability to use all features (notably advanced features such as performance evaluation, model comparison or drift analysis) with all types of models.

This page lists known compatibilities and incompatibilities

Import and scoring
==================


The MLflow model import capability and scoring recipes in "direct output" mode are usually compatible with MLflow models supporting the "pyfunc" variant.

As of September 2024, this has been tested with:

* Python Function
* H2O
* Keras
* Pytorch
* Scikit-learn
* TensorFlow 2
* ONNX
* MXNet Gluon
* XGBoost
* LightGBM
* Catboost
* Spacy
* FastAI 2
* Statsmodels
* Prophet

Dataiku does not support R MLflow models nor Spark Mlflow models

The import of MLflow models in DSS was successfully tested with MLflow versions 2.17.2 (Python 3.8) and 2.22.0 (Python 3.10). Later versions may also work, but modifications of implementation details of MLflow may cause bugs. Version 2.17.2 (Python 3.9) should generally be preferred.

.. warning::
    MLflow versions prior to 2.0.0 are no longer supported; versions 3.0 and above are not supported and may lead to compatibility issues.


The following ML packages are supported in the versions specified in the below table. When using one of these packages, you should create
a code environment including:

* dataiku core packages
* the specified version(s) of the ML package(s)
* scikit-learn==1.0.2
* statsmodels==0.13.5
* numpy<1.27

+-----------------------------+-------------------------------+--------------------------------------------+
| ML package                  | ML packages versions          | MLflow version *(Python version)*          |
|                             |                               |                                            |
|                             |                               | Recommended / Tested                       |
+-----------------------------+-------------------------------+--------------------------------------------+
| CatBoost                    | catboost==1.2.5               |         2.17.2 *(3.9)* / 2.22.0 *(3.10)*   |
+-----------------------------+-------------------------------+--------------------------------------------+
| fast.ai 2                   | fastai==2.7.10                |         2.17.2 *(3.9)* / 2.22.0 *(3.10)*   |
+-----------------------------+-------------------------------+--------------------------------------------+
| LightGBM                    | lightgbm>=3.0,<3.1            |         2.17.2 *(3.9)* / 2.22.0 *(3.10)*   |
+-----------------------------+-------------------------------+--------------------------------------------+
| ONNX                        | onnx==1.12.0                  |         2.17.2 *(3.9)* / 2.22.0 *(3.10)*   |
|                             |                               |                                            |
|                             | onnxruntime==1.12.0           |                                            |
|                             |                               |                                            |
|                             | (compatible ML package)       |                                            |
+-----------------------------+-------------------------------+--------------------------------------------+
| PyTorch                     | torch==1.13.0                 |                                            |
|                             |                               |                                            |
|                             | torchvision==0.14             |         2.17.2 *(3.9)* / 2.22.0 *(3.10)*   |
|                             |                               |                                            |
|                             | torchmetrics==0.11.0          |                                            |
|                             |                               |                                            |
|                             | pytorch-lightning==1.8.2      |                                            |
+-----------------------------+-------------------------------+--------------------------------------------+
| TensorFlow 2 / Keras 2.13.1 | tensorflow==2.13.1            |                                            |
|                             |                               |                                            |
|                             | tensorflow-estimator==2.13.0  |         2.17.2 *(3.9)* / 2.22.0 *(3.10)*   |
|                             |                               |                                            |
|                             | keras==2.13.1                 |                                            |
+-----------------------------+-------------------------------+--------------------------------------------+
| XGBoost                     | xgboost==1.7.6                |         2.17.2 *(3.9)* / 2.22.0 *(3.10)*   |
+-----------------------------+-------------------------------+--------------------------------------------+

.. code-block::
   :caption: A code env for Pytorch should include, **in addition to dataiku core packages**:

   mlflow==2.17.2
   scikit-learn==1.0.2
   statsmodels==0.13.5
   torch==1.13.0
   torchvision==0.14
   torchmetrics==0.11.0
   pytorch-lightning==1.8.2

.. code-block::
   :caption: A code env for TensorFlow 2 / Keras 2.13.1 should include, **in addition to dataiku core packages**:

   mlflow==2.17.2
   scikit-learn==1.0.2
   statsmodels==0.13.5
   tensorflow==2.13.1
   tensorflow-estimator==2.13.0
   keras==2.13.1


Evaluation
==========

DSS also features the evaluation of regression or classification models on tabular input data. As of December 2023, this feature has been successfully tested in the following circumstances.

Please note that this is not a guarantee that you would necessarily be able to do the same, due to the high variability
of models that can be saved (even within a single framework).

In all cases, the `prediction_type` should be set when importing the model. Please see below supported prediction types for the supported ML packages:

+--------------------------------+-----------------------+---------------------------+------------+
| ML package                     | binary classification | multiclass classification | regression |
+--------------------------------+-----------------------+---------------------------+------------+
| CatBoost                       |           ✓           |             ✓             |      ✓     |
+--------------------------------+-----------------------+---------------------------+------------+
| fast.ai 2                      |           ✗           |             ✗             |      ✓     |
+--------------------------------+-----------------------+---------------------------+------------+
| LightGBM                       |           ✓           |             ✓             |      ✓     |
+--------------------------------+-----------------------+---------------------------+------------+
| ONNX                           |           ✓           |             ✓             |      ✓     |
+--------------------------------+-----------------------+---------------------------+------------+
| PyTorch                        |           ✓           |             ✓             |      ✓     |
+--------------------------------+-----------------------+---------------------------+------------+
| scikit-learn 1.0.2             |           ✓           |             ✓             |      ✓     |
+--------------------------------+-----------------------+---------------------------+------------+
| TensorFlow 2 / Keras 2.13.1    |           ✓           |             ✓             |      ✓     |
+--------------------------------+-----------------------+---------------------------+------------+
| XGBoost                        |           ✓           |             ✓             |      ✓     |
+--------------------------------+-----------------------+---------------------------+------------+

