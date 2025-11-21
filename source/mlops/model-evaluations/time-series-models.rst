Evaluating Dataiku Time Series Forecasting models
####################################################

.. contents:: :depth: 1
    :local:

Creating an Evaluation Recipe for :doc:`Time series Forecasting models </machine-learning/time-series-forecasting/index>` is similar to doing so for Classification and Regression models (see :doc:`dss-models`).
This section highlights the key differences.

Input dataset
=============

The input dataset for the Evaluation Recipe should contain at least:

- The time column
- The time series identifiers columns (if any)
- The target column
- The external features columns (if any)


Outputs
===============

Output dataset
--------------

The Evaluation Recipe computes the evaluation dataset by moving the forecast/evaluation window (of size *forecast horizon*) from the end of the input dataset to the beginning as many times as possible (given the size of the timeseries), 
or a fixed number of times if the **Max. nb. forecast horizons** is set.

Metrics dataset
---------------

The output metrics dataset contains the computed metrics. If the input dataset contains multiple time series, choose between aggregated metrics (one single row, default) or per time series metrics (one row per series).

Model Evaluation Store
----------------------

The Model Evaluation Store and Model Evaluations work similarly to classification or prediction tasks
(see :doc:`/mlops/model-evaluations/analyzing-evaluations`), but there are a few important differences to be aware of:

- For models predicting multiple time series, performance metrics at the model evaluation level are aggregated as described
  in :ref:`forecasting-results-performance-metrics`. In addition to that, for metrics aggregated using an average,
  the Evaluation Recipe records the worst metrics values across all time series. These metrics are prefixed with "WORST"
  in the Model Evaluation Store screens.
- Input Data Drift and Prediction Drift are not supported.



Refitting for statistical models
================================

Statistical models (ARIMA and Seasonal LOESS) can be refit on the input data before evaluation.

.. warning::

  Evaluation with Seasonal LOESS only works with refitting enabled.
