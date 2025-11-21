Windowing
###########################

For high frequency or noisy time series data, observing the variations between successive observations may not always provide insightful information. In such cases, it can be useful to filter or compute aggregations over a rolling window of timestamps.

.. _tswindowing_recipe_label:

Windowing recipe
==================
The windowing recipe allows you to perform analytics functions over successive periods in equispaced time series data. This recipe works on all numerical columns (type *int* or *float*) in your data.

.. contents::
	:depth: 1
	:local:

.. _windowing_input_label:

Input Data
-----------
Data that consists of equispaced *n*-dimensional time series in :doc:`wide or long format<../data-formatting>`.

.. note::
   If input data is in the long format, then windowing in any numerical column will be applied separately on each time series in the column.

Parameters
------------
Time column
^^^^^^^^^^^^^^^^^

Name of the column that contains the timestamps. Note that the timestamp column must have the date type as its :ref:`meaning<schema_type_meaning>` (detected by DSS), and duplicate timestamps cannot exist for a given time series.

Long format checkbox
^^^^^^^^^^^^^^^^^^^^
Indicator that the input data is in the long format. See :ref:`ts_long_format_label`.

Time series identifiers
^^^^^^^^^^^^^^^^^^^^^^^
The names of the columns that contain identifiers for the time series when the input data is in the long format. This parameter is available when you enable the "Long format" checkbox. You can select one or multiple columns.

Causal window
^^^^^^^^^^^^^^
Option to use a causal window, that is, a window which contains only past (and optionally, present) observations. The current row in the data will be at the right border of the window.

If you de-select this option, Dataiku DSS uses a bilateral window, that is, a window which places the current row at its center.

Shape
^^^^^
Window shape applied to the *Sum* and *Average* operations. The shape is specified as one of these values:

- Rectangular: simple rectangular window with a flat profile
- Triangle: triangle window (with nonzero values at the endpoints)
- Bartlett: triangle window (with zero values at the endpoints)
- Gaussian: nonlinear window in the shape of a Gaussian distribution
- Parzen: nonlinear window made of connected polynomials of the third degree
- Hamming: nonlinear window generated as a sum of cosines (trigonometric polynomial of order 1)
- Blackman: nonlinear window generated as a sum of cosines (trigonometric polynomial of order 2)

Width
^^^^^^^^^^^
Width of the window, specified as a numerical value (*int* or *float*). 

The window width cannot be smaller than the frequency of the time series. For example, if your timestamp intervals equal 5 minutes, then you cannot specify a window width that is smaller than 5 minutes.

.. _windowing_unit_label:

Unit
^^^^^
Unit of the window width, specified as one of these values:

- Years
- Months
- Weeks
- Days
- Hours
- Minutes
- Seconds
- Milliseconds
- Microseconds
- Nanoseconds

Include window bounds
^^^^^^^^^^^^^^^^^^^^^^
Edges of the window to include when computing aggregations. This parameter is active only when you use a causal window. Choose from one of these values:

- Yes, left only
- Yes, right only
- Yes, both
- No

Aggregations
^^^^^^^^^^^^^
Operations to perform on a window of time series data. Select one or more of these options:

- Retrieve
- Min
- Max
- Average
- Sum
- Standard deviation
- 25th percentile
- Median
- 75th percentile
- First order derivative
- Second order derivative

Output Data
------------
Data consisting of equispaced time series, and having the same number of columns as the input data.

Tips 
-----
* If you have irregular timestamp intervals, first resample your data, using the :ref:`resampling recipe<tsresampling_recipe_label>`. Then you can apply the windowing recipe to the resampled data.
* The windowing recipe works on all numerical columns of a dataset. To apply the recipe on select columns, you must first prepare your data by removing the unwanted columns.


Related pages
===============
* :doc:`./resampling`
* :doc:`./interval-extraction`
* :doc:`./extrema-extraction`
* :doc:`./decomposition`
* :doc:`/other_recipes/window` 


