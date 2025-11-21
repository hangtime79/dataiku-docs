Interval extraction
###########################

It is sometimes useful to identify periods when time series values are within a given range. For example, a sensor reporting time series measurements may record values that fall outside an acceptable range, thus making it necessary to extract segments of the data.   

.. _interval_extraction_recipe_label:

Interval extraction recipe
==========================
The interval extraction recipe identifies segments of the time series where the values fall within a given range. See :ref:`interval_algorithms_label` for more information.

This recipe works on all numerical columns (*int* or *float*) in your time series data.

.. contents::
	:depth: 1
	:local:

.. _interval_input_label:

Input Data
-----------
Data that consists of equispaced *n*-dimensional time series in :doc:`wide or long format<../data-formatting>`.

If input data is in the long format, then the recipe will separately extract the intervals of each time series that is in a column. See :ref:`interval_algorithms_label` for more information.


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


.. _interval_column_label:

Apply threshold to column
^^^^^^^^^^^^^^^^^^^^^^^^^^
Name of the column to which the recipe applies the threshold parameters.

.. _min_value_label:

Minimal valid value
^^^^^^^^^^^^^^^^^^^^
Minimum acceptable value in the time series interval, specified as a numerical value (*int* or *float*). The minimal valid value and the maximum valid value form the range of acceptable values.

.. _max_value_label:

Maximum valid value
^^^^^^^^^^^^^^^^^^^^
Maximum acceptable value in the time series interval, specified as a numerical value (*int* or *float*). The maximum valid value and the minimal valid value form the range of acceptable values.

.. _interval_unit_label:

Unit
^^^^^
Unit of the :ref:`acceptable deviation<interval_acceptable_deviation_label>` and the :ref:`minimal segment duration<interval_minimal_duration_label>`, specified as one of these values:

- Days
- Hours
- Minutes
- Seconds
- Milliseconds
- Microseconds
- Nanoseconds

.. _interval_acceptable_deviation_label:

Acceptable deviation
^^^^^^^^^^^^^^^^^^^^
Maximum duration of the specified :ref:`unit<interval_unit_label>`, for which values within a valid time segment can deviate from the range of acceptable values.

For example, if you specify 400 - 600 as a range of acceptable values, and an acceptable deviation of 30 seconds, then the recipe can return a valid time segment that includes values outside the specified range, provided that those values last for a time duration that is less than 30 seconds.

.. _interval_minimal_duration_label:

Minimal segment duration
^^^^^^^^^^^^^^^^^^^^^^^^
The minimum duration for a time segment to be valid, specified as a numerical value of the :ref:`unit<interval_unit_label>` parameter.

For example, you can specify 400 - 600 as a range of acceptable values, and a minimal segment duration of 3 minutes. If all the values in a time segment are between 400 and 600 (or satisfy the acceptable deviation), but the segment lasts less than 3 minutes, then the time segment would be invalid.

Output Data
------------
Data consisting of equispaced and *discontinuous* time series. Each interval in the output data will have an id ("interval_id").

.. _interval_algorithms_label:

Algorithms
-----------
For values of the :ref:`minimal segment duration<interval_minimal_duration_label>` and :ref:`acceptable deviation<interval_acceptable_deviation_label>`, the recipe implements the following steps.

 1. Evaluate if consecutive values of a time series satisfy at least one of these conditions:

	 a. the values are in the range of acceptable values (between the :ref:`minimal valid value<min_value_label>` and the :ref:`maximum valid value<max_value_label>`)
	 b. the values deviate from the range of acceptable values but last for a time period that is smaller than the acceptable deviation

  * If yes, then these values form a segment and the recipe proceeds to step 2.
  * If no, then the values are not acceptable, and the recipe repeats step 1 for successive values in the time series.

 2. Evaluate if the segment lasts for a time duration that is greater than the *minimal segment duration*.
 
  * If yes, then keep this segment as an acceptable interval 
  * If no, then this segment is not an acceptable time interval
	 
  Return to step 1 to evaluate successive values in the time series.
 
.. note::
   If the input data is in the long format, then for each time series in a :ref:`specified column<interval_column_label>`, the recipe will perform the interval extraction algorithm separately.

Tips 
----
* If you have irregular timestamp intervals, first resample your data, using the :ref:`resampling recipe<tsresampling_recipe_label>`. Then you can apply the interval extraction recipe to the resampled data.
* The interval extraction recipe works on all numerical columns of a dataset. To apply the recipe on select columns, you must first prepare your data by removing the unwanted columns.

Related pages
===============
* :doc:`./extrema-extraction`
* :doc:`./windowing`
* :doc:`./resampling`
* :doc:`./decomposition`


