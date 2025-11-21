Trend/seasonal decomposition
############################

Trend/seasonal decomposition is useful to understand, clean, and leverage your time series data. Not only is it necessary to retrieve seasonally-adjusted data, but it is also relevant for anomaly detection.
This recipe decomposes the numerical columns of your time series into three components: trend, seasonality and residuals. The recipe relies on STL, seasonal and trend decomposition using Loess. For more information, see `Statsmodel's documentation <https://www.statsmodels.org/devel/generated/statsmodels.tsa.seasonal.STL.html>`_.

.. note::
	The decomposition recipe only supports Python 3.6.

.. contents::
	:depth: 1
	:local:

Input Data
==========
Data that consists of equispaced *n*-dimensional time series in :doc:`wide or long format<../data-formatting>`.

Settings
========
Input parameters
----------------

Time column
^^^^^^^^^^^

Column with parsed dates and no missing values:

- To parse dates, you can use a :doc:`Prepare</preparation/processors/date-parser>` recipe.
- To fill missing values, you can use the Time Series Preparation :doc:`/time-series/time-series-preparation/resampling` recipe.
  
Frequency
^^^^^^^^^
Frequency of the time column, from year to minute:

- For minute and hour frequency, you can select the number of minutes or hours.
- For week frequency, you can select the end-of-week day.

Season length
^^^^^^^^^^^^^
Length of the seasonal **period** in selected frequency unit.

- For example, season length is 7 for daily data with a weekly seasonality 
- Season length is 4 for a 6H frequency with a daily seasonality

Target column(s)
^^^^^^^^^^^^^^^^
Time series columns that you want to decompose. It must be numeric (*int* or *float*). You can select one or multiple columns.


Long format checkbox
^^^^^^^^^^^^^^^^^^^^^
Indicator that the input data is in the long format. See :ref:`ts_long_format_label`.

Time series identifiers
^^^^^^^^^^^^^^^^^^^^^^^
The names of the columns that contain identifiers for the time series when the input data is in the long format. This parameter is available when you enable the "Long format" checkbox. You can select one or multiple columns.

Decomposition parameters
------------------------

Model type
^^^^^^^^^^
The decomposition model of your time series. It may be :

- **Additive** : Time series = trend + seasonality + residuals
- **Multiplicative** : Time series = trend × seasonality × residuals
  
If the magnitude of the seasonality varies with the mean of the time series, then the series is multiplicative. Otherwise, the series is additive.

.. note::

	- A multiplicative model is only compatible with positive numerical values. 
	- For multiplicative STL, the recipe first takes the logarithms of the data, then computes an additive decomposition and finally back-transforms the data. 


Advanced parameters 
-------------------

Seasonal smoother
^^^^^^^^^^^^^^^^^
The window size used to estimate the seasonal component in STL decompositions. It must be an odd integer greater than 7. It controls how rapidly the seasonal component can change.

Robust to outliers
^^^^^^^^^^^^^^^^^^
If selected, the estimation will re-weight data, allowing the model to tolerate larger errors.

Additional parameters
^^^^^^^^^^^^^^^^^^^^^
The map parameter enables you to add any other parameter of the `Statsmodel STL function <https://www.statsmodels.org/devel/generated/statsmodels.tsa.seasonal.STL.html>`_ . To add a parameter, click on "ADD KEY/VALUE", then enter the parameter name as the 'key', and the parameter value as the 'value'.
You may use the following parameters:

**Degree of Loess:** Degrees of the regressions used to estimate the components. It must be 0 or 1.

**Speed jump:** If the speed jump is larger than 1, the LOESS is used every seasonal_jump points. Then, it performs linear interpolation to estimate the
missing points.

**Length of the smoothers:** Number of consecutive timesteps (years, weeks..) used in estimating each value in the decomposition components. It controls how
rapidly a component can change.


Related pages
===============
* :doc:`./resampling`
* :doc:`./interval-extraction`
* :doc:`./extrema-extraction`
* :doc:`./windowing`
