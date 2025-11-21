Introduction
############

Time series forecasting is used when you have a time-dependent **target** variable that you want to forecast.
For instance, you may want to forecast future sales to optimize inventory, predict energy consumption to adapt production levels, etc.
In theses cases, sales and energy consumption are the **target** variables to forecast.

You can find an example project that leverages Dataiku visual capabilities to build forecasting models `here <https://www.dataiku.com/learn/samples/time-series-forecasting/>`_.

.. contents:: :depth: 1
    :local:


Prerequisites and limitations
==============================

Training & running the time series forecasting models requires a compatible :doc:`code environment </code-envs/index>`.

Select one of the "Visual Machine Learning and Timeseries Forecasting" package presets in a code env's Packages to install > Add sets of packages, depending on your architecture (CPU or GPU) and update your code-env.

.. warning::

	Time series forecasting is incompatible with the following:

	* MLflow models
	* Models ensembling
	* Model export:
	
	  * Java export
	  * PMML export
	  * SQL export / scoring
	  * Notebook export


Train a time series forecasting model
=====================================

From your dataset, in the *Lab* sidebar, select *Time Series Forecasting*. Specify the columns to use as target variable and time variable. If your dataset contains several time series, select the identifier columns.

Time variable
-------------

Your dataset should contain a time variable (with meaning *Datetime with zone*, *Datetime no zone* or *Date only*).

Forecasting models require a uniform time step in the dataset. However this is not mandatory for the input dataset, 
as DSS provides a way to impute missing time steps when setting up the time series forecasting task:

1. First, :ref:`adjust the time step used for time series resampling<forecasting-time-step-parameters>` if necessary (DSS guesses it based on the input dataset)
2. Then, :ref:`choose the imputation method<forecasting-resampling>` for numerical and non-numerical features interpolation (missing time steps in the middle of the time series) and extrapolation (missing time steps before the start, or after the end of the time series).

.. warning::

	Dates are converted to UTC before resampling.


Time series identifier columns
------------------------------

Some dataset contain multiple stacked time series, each identified by the value of one or more identifier columns.

DSS supports both single and multiple time series datasets. For multiple time series you need to specify which columns
should be taken as identifiers to distinguish them.

A typical example of multiple time series dataset is sales per shop, and/or per country. The time series identifier columns in this case are the shop and country identifiers.
