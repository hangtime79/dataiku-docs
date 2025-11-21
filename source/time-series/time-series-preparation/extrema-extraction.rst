Extrema extraction
###########################

Time series extrema are the minimum and maximum values in time series data. It can be useful to compute aggregates of a time series around extrema values to understand trends around those values.

.. _extrema_recipe_label:

Extrema extraction recipe
==========================
The extrema extraction recipe allows you to extract aggregates of time series values around a global extremum (global maximum or global minimum). 

Using this recipe, you can find a global extremum in one dimension of a time series and perform windowing functions around the timestamp of the extremum on all dimensions. See :doc:`windowing` for more details about the windowing operations.

This recipe works on all numerical columns (*int* or *float*) in your time series data.

.. contents::
	:depth: 1
	:local:

.. _extrema_input_label:

Input Data
-----------
Data that consists of equispaced *n*-dimensional time series in :doc:`wide or long format<../data-formatting>`.

If input data is in the long format, then the recipe will find the extremum of each time series in the column on which you operate. See :ref:`extrema_algorithms_label` for more details.


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

.. _extrema_column_label:

Find extremum in column
^^^^^^^^^^^^^^^^^^^^^^^^^
Name of column from which to extract the extremum value.

Extremum type
^^^^^^^^^^^^^^^^^^^^^^^^^
Type of extremum to find, specified as "Global minimum" or "Global maximum".

Causal window
^^^^^^^^^^^^^^
Option to use a causal window, that is, a window that contains only past (and optionally, present) observations. The timestamp for the extremum point will be at the right border of the window.

If you deselect this option, Dataiku DSS uses a bilateral window, that is, a window that places the timestamp for the extremum point at its center.

Shape
^^^^^
Window shape applied to the *Sum* and *Average* operations. The shape can take on one of these values:

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

The window width cannot be smaller than the frequency of the time series. For example, if your timestamp intervals equal 5 minutes, you cannot specify a window width smaller than 5 minutes.

.. _extrema_unit_label:

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

.. _extrema_aggregations_label:

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
Data consisting of the results of extrema extraction, one row for each time series. Each row contains the timestamp of the extremum and the computed :ref:`aggregations<extrema_aggregations_label>` for a window of data around the extremum.

.. _extrema_algorithms_label:

Algorithms
-----------
If the input data is in the wide format, the recipe works as follows:

 1. Find the global extremum and corresponding timestamp for a :ref:`specific column<extrema_column_label>`.
 2. For all columns, apply a window around the timestamp and compute :ref:`aggregations<extrema_aggregations_label>`.

If the input data is in the long format, then the recipe implements slightly different steps, as follows:

 1. Find the global extremum and corresponding timestamp for *each* time series in a :ref:`specific column<extrema_column_label>`.
 2. For all columns, apply a window around the timestamps found in step 1 and then compute aggregations.
 
Tips 
----
* If you have irregular timestamp intervals, first resample your data using the :ref:`resampling recipe<tsresampling_recipe_label>`. Then you can apply the extrema extraction recipe to the resampled data.
* The extrema extraction recipe works on all numerical columns of a dataset. To apply the recipe to select columns, you must first prepare your data by removing the unwanted columns.

Related pages
===============
* :doc:`./interval-extraction`
* :doc:`./windowing`
* :doc:`./resampling`
* :doc:`./decomposition`
