Partition identifiers
######################

When dealing with partitioned datasets, you need to identify or refer to partitions.
Within a dataset, a partition identifier uniquely identifies a partition.

The identifier of a partition is made by concatenating the dimension values, separated by | (pipe)

Time dimension identifiers
==============================

The format of a time dimension identifier depends on the time dimension granularity

+--------+-------------------+-------------------+
| Period |       Format      |      Example      |
+========+===================+===================+
| Year   | ``YYYY``          | ``2020``          |
+--------+-------------------+-------------------+
| Month  | ``YYYY-MM``       | ``2020-01``       |
+--------+-------------------+-------------------+
| Day    | ``YYYY-MM-DD``    | ``2020-01-17``    |
+--------+-------------------+-------------------+
| Hour   | ``YYYY-MM-DD-HH`` | ``2020-01-17-13`` |
+--------+-------------------+-------------------+

Some special keywords are also available:

* CURRENT_HOUR
* CURRENT_DAY
* CURRENT_MONTH
* CURRENT_YEAR
* PREVIOUS_HOUR
* PREVIOUS_DAY
* PREVIOUS_MONTH
* PREVIOUS_YEAR


Discrete dimension identifiers
===================================

The identifier of a discrete dimension value is the value itself. As such, discrete dimensions should only contain letters and numbers.

Multiple dimensions
=====================================

For example, if you have a time dimension named "date" with a "DAY" granularity and a discrete dimension named "country", then you could have partitions like:

* ``2020-01-01|France``
* ``2020-01-01|Italy``
* ``2020-01-02|France``
* ``2020-01-02|Italy``

Ranges specifications
=======================

In various locations in DSS, you can use a "partition range specification" syntax to refer to a set of partitions or values of a dimension.

For example:

	* In "Exact values" dependency function
	* When building datasets
	* When creating scheduled jobs
	* ...

The generic syntax is:

* ``PARTITION_SPEC = DIMENSION_SPEC|DIMENSION_SPEC|....``

* ``DIMENSION_SPEC =``

    *  ``DATE``            # Single Date (Time)
    *  ``DATE/DATE``      # Date Range (Time)
    *  ``Any``             # Actual Value (ExactValue)
    *  ``Any/Any/Any/...`` # Several values (ExactValue)

Examples:

* ``2020-01-25/2020-01-28``: Single DAY dimension, select 3 days
* ``2020-01-25-14/2020-01-28-15``: Single HOUR dimension, select 73 hours
* ``2020-02/2020-03|FR/IT``: One MONTH dimension and one discrete dimension, select a total of 4 partitions:

	* ``2020-02|FR``
	* ``2020-02|IT``
	* ``2020-03|FR``
	* ``2020-03|IT``
