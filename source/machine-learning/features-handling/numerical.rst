Numerical variables
#####################

The **Numerical handling** and **Missing values** methods, and their related controls, specify how a numerical variable is handled.

Numerical handling
==================

- **Keep as a regular numerical feature** simply takes the numerical input as is, with optional :ref:`Rescaling`.
  In addition, post-rescaling, you can request that derived features such as sqrt(x), x^2, ... be generated and considered in the model.
- :ref:`Datetime cyclical encoding` (Python training backend only).
- **Replace by 0/1 flag indicating presence**.
- **Binarize based on a threshold** replaces the feature values with a 0/1 flag that indicates whether the value is above or below the specified threshold.
- **Quantize** replaces the feature values with their quantiles in the feature's empirical distribution. More precisely if we set the number of quantiles to :math:`n`, the numerical feature will be split into :math:`n` intervals (quantiles), each containing one :math:`nth` of the feature values. Finally each numerical value is replaced by the index (from :math:`0` to :math:`n - 1`) of the interval it belongs to.

All numerical handlings (except 0/1 presence flag) offer the possibility to keep the original numerical feature as an extra feature that can in turn be rescaled.

.. _Datetime cyclical encoding:

Datetime cyclical encoding
--------------------------

Datetime cyclical encoding transforms datetime features (timestamps) into numerical features, while preserving the cyclical significance of date and time periods.

More specifically for every selected time period :math:`T` (either minute, hour, day, week, month, quarter or year), the datetime cyclical encoding converts the timestamp or date to a number of seconds :math:`t` and then encodes :math:`t` into two numerical features using the following formulas:

.. math::
	\begin{cases}
	\sin\left(\dfrac{2\pi \cdot t}{T}\right) \\ \\
	\cos\left(\dfrac{2\pi \cdot t}{T}\right)
	\end{cases}


In order to take into account leap seconds and leap years, the timestamp is first converted to a number of seconds for each selected period. 
By way of example, we'll detail the computation for the `2021-09-27T02:17:35` reference timestamp.

- **minute**: :math:`t` is defined as the number of seconds since the beginning of the same minute (i.e. 35 seconds in our example).
- **hour**: :math:`t` is defined as the number of seconds since the beginning of the same hour (i.e. 17*60 + 35 seconds in our example).
- **day**: :math:`t` is defined as the number of seconds since the beginning of the same day, at 00:00:00 (i.e. 2*3600 + 17*60 + 35 seconds in our example).
- **week**: :math:`t` is defined as the number of seconds since Monday of the same week, at 00:00:00 (i.e. since 2021-09-21T00:00:00 in our example).
- **month**: :math:`t` is defined as the number of seconds since the first day of the same month, at 00:00:00 (i.e. since 2021-09-01T00:00:00 in our example). 
- **quarter**: :math:`t` is defined as the number of seconds since the first day of the same quarter,at 00:00:00 (i.e. since 2021-07-01T00:00:00 in our example).
- **year**: :math:`t` is defined as the number of seconds since the first day of the same year, at 00:00:00 (i.e. since 2021-01-01T00:00:00 in our example). 


The reference period durations are:

- :math:`T = 60\ s` for **minute**,
- 60 minutes (:math:`T = 3600\ s`) for **hour**,
- 24 hours (:math:`T = 86400\ s`) for **day**,
- 7 days (:math:`T = 604800\ s`) for **week**,
- 31 days (:math:`T = 2678400\ s`) for **month**,
- 92 days (:math:`T = 7948800\ s`) for **quarter**,
- 366 days (:math:`T = 31622400\ s`) for **year**.


.. _Rescaling:

Rescaling
=========

Rescaling can be performed prior to training, which can improve model performance in some instances. We advise to rescale numeric variables in the following cases:

- Algorithms that are not based on decision trees (rescaling has no effect on decision trees) are selected.
- There are large differences in the absolute values of the features.

There are two implementations of rescaling.

  - **Standard rescaling** scales the feature to a standard deviation of one and a mean of zero (default setting).
  - **Min-max rescaling** sets the minimum value of the feature to zero and the max to one.


Missing values
==============

There are a few choices for handling missing values in numerical features.

- **Impute...** replaces missing values with the specified value.  This should be used for **randomly missing** data that are missing due to random noise.
- **Drop rows** discards rows with missing values from the model building.  *Avoid discarding rows, unless missing data is extremely rare*.
