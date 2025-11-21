Scoring recipe
##############

.. contents:: :depth: 1
    :local:

Without external features
=========================

If the model was not trained with external features, the input dataset for the scoring recipe should contain the past time steps for:

- The time column
- The time series identifiers columns (if any)
- The target column

The scoring recipe will then output one forecasting horizon after the last past time step in the input dataset. By default, it will also output all the past data, equally resampled.


With external features
======================

If the model was trained with external features, the input dataset for the scoring recipe should contain the past time steps for:

- The time column
- The time series identifiers columns (if any)
- The target column
- The external features columns

It should also contain enough future time steps (at least one forecast horizon) for:

- The time column
- The time series identifiers columns (if any)
- The external features columns

The future data for the target variable must be empty, as they will be forecasted.

For example, if the forecasting horizon is 3 days, the input dataset must contain 3 extra days with external features and empty target:

.. csv-table::
   :header: "date", "external_feature", "target"

    2022-01-01,1,4
    2022-01-02,0,4
    2022-01-03,1,5
    2022-01-04,1,4
    2022-01-05,0,5
    2022-01-06,1,3
    2022-01-07,1,2
    2022-01-08,0,4
    2022-01-09,0,
    2022-01-10,1,
    2022-01-11,1,

The model will use external features from the last 3 time stamps (2022-01-09, 2022-01-10, 2022-01-11) to forecast their target values.

The scoring recipe will then output one forecasting horizon after the last past time step in the input dataset. By default, it will also output all the past data, equally resampled.


Refitting for statistical models
================================

Statistical models (ARIMA and Seasonal LOESS) can be refit on the input data before scoring. This retrains the model on the scoring dataset, with the same hyperparameters, before forecasting.

.. note::

  Scoring with Seasonal LOESS only works with refitting enabled.
