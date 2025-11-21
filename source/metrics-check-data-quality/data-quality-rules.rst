Data Quality Rules
##################


The Data Quality mechanism in Dataiku allows you to easily ensure that your data meets quality standards and automatically monitor the status of your data quality across datasets, projects, and your entire Dataiku instance.

A Data Quality rule tests whether a dataset satisfies set conditions. The computation of a rule yields:

- a status outcome: "Ok", "Error" or "Warning". A less common outcome "Empty" is used to indicate that the condition could not be evaluated because the value is missing.
- an observed value with further detail. This parameter is optional for custom rules.

Each execution of a rule produces one outcome.
Note that if the rule has not yet been computed, the status is "Not Computed".

.. contents::
    :depth: 2
    :local:

.. note::

	The Data Quality mechanism is an improvement introduced in DSS 12.6.0 over the :doc:`checks</metrics-check-data-quality/checks>` system. Data quality rules allow you to specify expectations for datasets in a more streamlined way, and improve reporting of the results via specific dashboards.
	Other flow objects (managed folders, saved models, model evaluation store) still use checks.

Examples of simple Data Quality rules include:

- The record count of a dataset is above 0 (i.e., the dataset is not empty)
- The most frequent value of a column is 'Y'
- A column's values are at most 10% empty

Data Quality rules are configured in the *Data Quality* tab of a dataset, where you can also easily track the evolution of your dataset's data quality over time.



Data Quality rule types
========================

Column min in range
-------------------
Ensures that a column's minimum value falls within a given range.

Options:

- the column(s) to check
- the :ref:`expected range<expected-range>` (minimum / soft minimum / soft maximum / maximum)

Column min is within its typical range
---------------------------------------

Ensures that a column\'s minimum value has not deviated from its typical values within a given time window.

Options:

- the column(s) to check
- the :ref:`change detection parameters<change-detection-params>`

Column avg in range
-------------------
Ensures that a column's average value falls within a numeric range.

Options:

- the column(s) to check
- the :ref:`expected range<expected-range>` (minimum / soft minimum / soft maximum / maximum)

Column avg is within its typical range
---------------------------------------

Ensures that a column\'s average value has not deviated from its typical values within a given time window.

Options:

- the column(s) to check
- the :ref:`change detection parameters<change-detection-params>`

Column max in range
-------------------
Ensures that a column's maximum value falls within a given range.

Options:

- the column(s) to check
- the :ref:`expected range<expected-range>` (minimum / soft minimum / soft maximum / maximum)

Column max is within its typical range
---------------------------------------

Ensures that a column\'s maximum value has not deviated from its typical values within a given time window.

Options:

- the column(s) to check
- the :ref:`change detection parameters<change-detection-params>`

Column sum in range
-------------------
Ensures that a column's sum falls within a given range.

Options:

- the column(s) to check
- the :ref:`expected range<expected-range>` (minimum / soft minimum / soft maximum / maximum)

Column sum is within its typical range
---------------------------------------

Ensures that a column\'s sum value has not deviated from its typical values within a given time window.

Options:

- the column(s) to check
- the :ref:`change detection parameters<change-detection-params>`

Column median in range
----------------------
Ensures that a column's median falls within a given range.

Options:

- the column(s) to check
- the :ref:`expected range<expected-range>` (minimum / soft minimum / soft maximum / maximum)

Column median is within its typical range
------------------------------------------

Ensures that a column\'s median value has not deviated from its typical values within a given time window.

Options:

- the column(s) to check
- the :ref:`change detection parameters<change-detection-params>`

Column std dev in range
-----------------------
Ensures that a column's standard deviation falls within a given range.

Options:

- the column(s) to check
- the :ref:`expected range<expected-range>` (minimum / soft minimum / soft maximum / maximum)

Column std dev is within its typical range
-------------------------------------------

Ensures that a column\'s standard deviation value has not deviated from its typical values within a given time window.

Options:

- the column(s) to check
- the :ref:`change detection parameters<change-detection-params>`

Column values are not empty
---------------------------
Ensures that a column does not contain empty values.

Options:

- the column(s) to check
- the threshold type - you can verify that all values are non-empty, or that at most a certain number / proportion are empty
- the :ref:`expected soft maximum / maximum<expected-range>` for empty values (if threshold type is not all values)

.. note::

    The definition of empty values when computing the rule using a SQL engine is different than when using the stream engine. With a SQL engine, only NULL is considered as an empty value. To also consider empty strings `""`, make sure to only activate the stream engine in the rules computation settings.

Column values are empty
-----------------------
Ensures that a column contains empty values.

Options:

- the column(s) to check
- the threshold type: you can verify that all values / at least a certain number of values / at least a certain proportion of values are empty
- the :ref:`expected soft minimum / minimum<expected-range>` for empty values (if threshold type is not all values)

.. note::

    The definition of empty values when computing the rule using a SQL engine is different than when using the stream engine. With a SQL engine, only NULL is considered as an empty value. To also consider empty strings `""`, make sure to only activate the stream engine in the rules computation settings.

Column empty value is within its typical range
-----------------------------------------------

Ensures that a column\'s empty value count has not deviated from its typical values within a given time window.

Options:

- the column(s) to check
- the :ref:`change detection parameters<change-detection-params>`

.. note::

    The definition of empty values when computing the rule using a SQL engine is different than when using the stream engine. With a SQL engine, only NULL is considered as an empty value. To also consider empty strings `""`, make sure to only activate the stream engine in the rules computation settings.

Column values are unique
------------------------
Ensures that a column's values are unique (no duplicates).
Empty values are ignored (e.g. a column with 50% empty values will only check the uniqueness of the non-empty values).

Options:

- the column(s) to check
- the threshold type: you can verify that all values / at least a certain number of values / at least a certain proportion of values are unique
- the :ref:`expected soft minimum / minimum<expected-range>` for unique values (if threshold type is not all values)

Column unique value is within its typical range
------------------------------------------------

Ensures that a column\'s unique value count has not deviated from its typical values within a given time window.

Options:

- the column(s) to check
- the :ref:`change detection parameters<change-detection-params>`

Column values in set
--------------------------
Ensures all values in a column are in a given set.
Empty values are ignored.

Options:

- the column(s) to check
- the list of values that are expected to contain all values from each selected column of the dataset

Column values in range
----------------------
Ensures all values in a column fall within a given range.
Empty values are ignored.

Options:

- the column(s) to check
- the :ref:`expected range<expected-range>` (minimum / soft minimum / soft maximum / maximum)

Column top N values in set
--------------------------
Ensures that a column's N most frequent values fall into a given set.
Empty values are ignored (the rule will check the N most frequent non-empty values).

Options:

- the column(s) to check
- the number of top values to check (must be less than 100)
- the list of values that are expected to contain the N most frequent values from each selected column of the dataset

Column most frequent value in set
---------------------------------
Ensures that a column's most common value is in a given set.
Empty values are ignored (e.g. most frequent value cannot be empty).

Options:

- the column(s) to check
- the list of values that are expected to contain the most frequent value from each selected column of the dataset

.. _meaning-validity-rule:

Column values are valid according to meaning
--------------------------------------------
Ensures that a column's values are consistent with a :doc:`meaning</schemas/meanings-list>`

Options:

- the column(s) to check
- for each selected column, the meaning to use to assert validity. You can either:

    - use the option "Use meaning from schema" that will use the meaning specified by the dataset's schema. This option allows the rule to adapt to changes to the column's meaning, but requires the meaning to be locked in the schema, which you can do by manually selecting it from the dropdown in the Explore tab
    - explicitly select a meaning in the list. The rule will always check validity according to the selected meaning

- the threshold type - you can verify that all values / at least a certain number / at least a certain proportion are valid
- consider empty as valid - by default, empty cells are considered as invalid. If this option is checked, they will be considered as valid
- the :ref:`expected soft minimum / minimum<expected-range>` for valid values (if threshold type is not all values)

Metric value in range
---------------------
Ensures that a DSS metric's value falls within a given range.

Options:

- the metric to test
- auto-compute metric - if checked, when the rule is run, it will recompute the metric value. Otherwise, it will use the most recent value
- the :ref:`expected range<expected-range>` (minimum / soft minimum / soft maximum / maximum)

Metric value in set
--------------------
Ensures that a DSS metric's value is in a given set of values.

Options:

- the metric to test
- auto-compute metric - if checked, when the rule is run, it will recompute the metric value. Otherwise, it will use the most recent value
- the list of allowed values

Metric value is within its typical range
-----------------------------------------

Ensures that a DSS metric value has not deviated from its typical values within a given time window.

Options:

- the metric to test
- auto-compute metric - if checked, when the rule is run, it will recompute the metric value. Otherwise, it will use the most recent value
- the :ref:`change detection parameters<change-detection-params>`

File size in range
------------------
Ensures that a dataset's file size (in bytes) falls within a given range.
Only available for a file-based dataset.

Options:

- the :ref:`expected range<expected-range>` (minimum / soft minimum / soft maximum / maximum)

Record count in range
---------------------
Ensures that a dataset's row count falls within a given range.

Options:

- the :ref:`expected range<expected-range>` (minimum / soft minimum / soft maximum / maximum)

Record count is within its typical range
-----------------------------------------

Ensures that a dataset\'s row count has not deviated from its typical values within a given time window.

Options:

- the :ref:`change detection parameters<change-detection-params>`


Column count in range
---------------------
Ensures that a dataset's column count falls within a given range.

Options:

- the :ref:`expected range<expected-range>` (minimum / soft minimum / soft maximum / maximum)

Column count is within its typical range
-----------------------------------------

Ensures that a dataset\'s column count has not deviated from its typical values within a given time window.

Options:

- the :ref:`change detection parameters<change-detection-params>`

.. _dataset-schema-equals:

Dataset schema equals
---------------------

Ensures that a dataset :doc:`schema</schemas/index>` matches an expected schema.

At rule creation, the expected schema is set to the current schema of the dataset. You can then edit existing columns (name, type, meaning), remove columns, or add new columns to the expected schema. You can change column order by clicking the up or down arrows. At any point, you can reset the expected schema to the current schema of the dataset with the "Reset to current schema" button.

The rule will return "Error" if an expected column is missing from the dataset, has a different type, has a different meaning, is in a different order than expected, or if an unexpected column is present in the dataset. If the column type is "complex" (array, map, object), the rule will recursively check the sub-fields. Strings are furthermore checked for maximum length, with default "-1" value for infinite length.

The rule outcome is ranked by "Index", which corresponds to the index in the expected schema. Unexpected columns are added at the end of the list.

Options:

- columns names
- columns types
- columns meanings: "Any" means that the column meaning is not checked, otherwise you can select a meaning from the list of available meanings
- columns order

Dataset schema contains
-----------------------

Ensures that a dataset :doc:`schema</schemas/index>` contains an expected schema.

At rule creation, the expected schema is set to the current schema of the dataset. You can then edit existing columns (name, type, meaning), remove columns, or add new columns to the expected schema. At any point, you can reset the expected schema to the current schema of the dataset with the "Reset to current schema" button.

The rule will return "Error" if an expected column is missing from the dataset, or has a different type or meaning. If the column type is "complex" (array, map, object), the rule will recursively check the sub-fields. Strings are furthermore checked for maximum length, with default "-1" value for infinite length.

.. note::

    Unlike the :ref:`Dataset schema equals<dataset-schema-equals>` rule, columns order does not matter here.

The rule outcome is ranked by "Index", which corresponds to the index in the expected schema.

Options:

- columns names
- columns types
- columns meanings: "Any" means that the column meaning is not checked, otherwise you can select a meaning from the list of available meanings

Python code
-----------
You can also write a custom rule in Python.
This rule is equivalent to the "Python check", so the same code can be used.

The Python method must return a tuple of two strings:

- the first value is the outcome 'Ok', 'Warning' or 'Error'
- the second value is the optional observed value message

If there are any errors during the Python code execution, the rule will return an "Error" status.

Options:

- The code env to use to run the python code
- the python code itself

Compare values of two metrics
-----------------------------
Compares a metric from the current dataset to a metric from the current dataset or another.

Options:

- the primary metric (from the current dataset)
- auto-compute primary metric - if checked, when the rule is run, it will recompute the primary metric value. Otherwise, it will use the most recent value.
- an operator describing which comparison must be done.
- the comparison dataset, eg the dataset in which you pick the comparison metric. Using the current dataset is supported.
- the comparison metric, to be compared with the primary metric

.. note::

	The behavior or the comparison depends on the type of metrics manipulated.
	If both metrics are numeric, comparison is done using the numerical order.
	If one or more of the two metrics are non-numeric, comparison will be done using the alphabetical order.


Plugin rules
------------
You can use a plugin to define rules via Python code, using a similar syntax to the Python rule.
Existing plugin checks are valid plugin rules.
See :doc:`custom metrics and checks</metrics-check-data-quality/custom_metrics_and_checks>`


Rule configuration
==================

The below settings are available for both partitioned and non-partitioned datasets. Note that partitioned datasets have additional settings which you can read about :ref:`below<dq-partitioned-settings>`.

Testing the rule
----------------

The `Test` button in the rule edition panel allows you to check the rule outcome, but does not save the result or update the status of the rule.
When the rule relies on the computation of an underlying metric, it will also not save its result in the dataset metric history.


.. _expected-range:

Hard and soft minimums and maximums
-----------------------------------

Some rules check whether a specific numeric value falls within a given range.
For these rules, you can configure up to four values: minimum, soft minimum, soft maximum and maximum.
The rule outcome is defined as follows:

- value below minimum : "Error"
- value below soft minimum : "Warning"
- value above soft maximum : "Warning"
- value above maximum : "Error"
- value in range : "Ok"


.. _change-detection-params:

Change detection rules and settings
------------------------------------

After the *learning period* has passed, we look at the observed metric values within the *lookback window*, to compute the typical range, and see if the new value falls within or outside of that range.

Let's explore the process step by step:

#. The historical data is collected in order to control that the *learning period* has passed. If not, the rule will not attempt to compare the current value with the history, and will immediately yield an `EMPTY` result.
#. The first and third quartiles of the historical data withing the *lookback window* are computed (designated Q1 and Q3), then the inter-quartile range (`IQR = Q3 - Q1`)
#. The typical ranges are computed (for error using the *IQR factor* parameter, and for warnings using *Soft IQR factor*):

    - `Lower bound = Q1 - (iqrFactor * IQR)`
    - `Upper bound = Q3 + (iqrFactor * IQR)`

#. The current value of the metric is compared to those ranges


This behavior is controlled by the following parameters:

- Period unit: `Days` or `runs`. Applies to both *learning period* and *lookback window*.
- Learning period: a minimum amount of metric data required to consider the rule as computable
- Lookback window: controls the number of data point considered as part of the history.

    - If period unit is `runs`, the inter-quartile range will be based on the last *n* data points, regardless of how old they are.
    - If it's `days`, the inter-quartile range will be computed with all data points that are less than *n* days old. If this results in less than 3 data points, the rule will yield a `WARNING`, as it would make change detection unreliable.

- IQR factor: factor used to compute a hard typical range - if the current value falls outside of this range, the rule will yield an error
- Soft IQR factor: factor used to compute a soft typical range - if the current value falls outside of this range, the rule will yield a warning (only applicable if the hard IQR check passed)

Enable / disable
----------------

Rules can be enabled or disabled individually.
A disabled rule is ignored when computing the rules and when updating the status of the dataset.


Auto-run after build
--------------------

When the "Auto-run after build" option is set, the rule will be computed automatically after each build of the dataset.
This ensures that the rule status is always updated alongside the dataset content.

This setting is ignored for input datasets (dataset that are not the output of any recipe), as they cannot be built within DSS.

Rules computed as part of a dataset build and returning an "Error" status will cause the build job to fail.

Changing the rule type
-----------------------

Starting DSS 13.4, it is possible to change the type of an existing rule.
Changing a rule type allows you to upgrade a rule to a similar but more adequate type while keeping its history (for example, changing a 'Column min in range' rule into a 'Column min is within its typical range' in order to take advantage of the dynamically computed range).
Using it as a way to repurpose a rule into something completely different is not recommended, as the history may become inconsistent.

Only similar settings between the previous and the new rule type will be preserved. You may have to set or fix some settings for the new rule type to be valid.

Data Quality monitoring views
=============================

You can easily track the status of Data Quality rules at either the dataset, project, or instance level in Dataiku.

This makes it easy to quickly identify potential data quality issues at a high level and efficiently drill down into specific issues for further investigation.

The Data Quality views are available for both partitioned and non-partitioned datasets. Partitioned dataset have some specificities related to how statuses are aggregated across partitions which you can read about :ref:`below<dq-partitioned-views>`.

Dataset level view
------------------

This view provides detail on a dataset's Data Quality rules and computation results.

- the *Current status* tab provides the overall dataset status as well as the current status of each rule and run details.
  Time information is displayed using the user's timezone

- the *Timeline* tab enables you to explore the evolution of the dataset's daily status and of each of the rules that influenced it, even if they have been disabled or deleted since.
  Time information is displayed using the UTC timezone.

    - the *last status* of a rule is the outcome of its last computation before the end of the selected day
    - the *worst daily status* of a rule is the worst outcome of all computations that happened throughout the selected day

- the *Rule History* tab allows you to see all past rule computations
  Time information is displayed using the user's timezone

You can also toggle the *Monitoring* flag from the Current Status tab.
When Monitoring is turned on, the dataset is included in the project-level status.
Datasets are monitored by default as soon as any rules are added.


Project level view
------------------

The project Data Quality tab provides an overview of the project status as well as the statuses of all included datasets.

- the *Current status* tab gives you an overview of the *current status* of the project as a whole as well as each dataset. The *current status* of the project is the worst *current status* of its monitored datasets.
  Time information is displayed using the user's timezone

- the *Timeline* tab enables you to explore the evolution of the status of the project and its datasets, even if they have been deleted since.
  Time information is displayed using the UTC timezone.
  Statuses are computed as follows:

    - the *last status* of a dataset is the worst outcome of the last computation of all enabled rules before the end of the selected day
    - the *worst daily status* of a dataset is the worst outcome of all rule computations that happened throughout the selected day

By default, the project-level views are filtered to only display monitored datasets.


Instance level view
-------------------

The instance Data Quality view, available from the Navigation menu, gives you a high level view of Data Quality statuses of the *monitored projects* you have access to.

A *monitored project* is a project that contains at least one monitored dataset.

The *current status* of a project is the worst *current status* of its monitored datasets.


Timezone limitations
--------------------

Data Quality timelines and worst daily statuses require grouping rule outcomes per day.
Since this information is computed and shared at the instance level, it cannot adapt to the user's current timezone.

All daily Data Quality data is computed based on the days in UTC timezone.


Other data quality views
========================

Dataset right panel
-------------------

The Data Quality right panel tab offers a quick view of the *current status* of all enabled rules.
You can access it from the right panel of datasets from the flow, from any dataset screen and from the Data Catalog.


Data Quality Flow view
----------------------

The Data Quality flow view provides a quick view of the *current status* of all datasets with Data Quality rules configured within a project.

.. _dq-partitioned-settings:

Data Quality on partitioned datasets
====================================

.. _computation-scope:

Computation scope
-----------------

On partitioned datasets, rules may be relevant to specific partitions and/or the whole dataset.
The "Computation scope" setting allows you to control whether a given rule should be computed on partitions, the whole dataset, or both, when performing a mass computation.

- "Partitions": the rule will be computed individually on each selected partition only
- "Whole dataset": the rule will be computed on the whole dataset only
- "Both": the rule will be computed both on each selected partition and on the whole dataset

For example, if you have a dataset partitioned by Country
and you want to ensure that the median of ``columnA`` is at least 20 in every Country partition,
and that the average of ``columnB`` is at most 50 across the whole dataset (but not individually for each Country), you would use:

- a "Column median in range" rule on ``ColumnA`` with the setting "Partitions" and a minimum of 20
- a "Column avg in range" rule on ``ColumnB`` with the setting "Whole dataset" and a maximum of 50

If you clicked "Compute all" and selected "Whole dataset" and two Countries "Belgium" and "Canada" in the modal, the ``ColumnA`` rule would only actually be computed on the partitions "Belgium" and "Canada", and the ``ColumnB`` rule would only actually be computed on the whole dataset.

This setting applies to any mass computation (auto-run after build, from scenarios, with the "Compute all" button).
Manually computing a single rule, however, forces the computation on the selected partition regardless of the "Computation scope" setting.

Auto-run after build
--------------------

For partitioned datasets, this option triggers the computation of the rule on each newly built partition and/or on the whole dataset, depending on the "Computation scope" option.
For example, if a job builds a single partition A, it will trigger:

- the computation on partition A of all rules that have "Partitions" or "Both" as computation scope
- the computation on the whole dataset of all rules that have "Whole dataset" or "Both" as computation scope

.. _dq-partitioned-views:

Data Quality monitoring views
-----------------------------

For partitioned datasets, the dataset level view shows information for either a single partition or for the whole dataset.

In the project level view, dataset statuses are defined as the worst status of all last computed partitions.
The status of each partition is the worst outcome of all enabled rules for that partition (same definition as the status of a non-partitioned dataset)

The current and last status aggregations don't necessarily include all partitions. They first identify the last day any rule computation happened and only include the partitions that had rule computations on that day.
For example, if a dataset has 3 partitions A, B, and C, and on June 5th rules are computed on partitions A and B,
then on June 7th rules are computed on partition B, C and on the whole dataset,
the dataset statuses will take into account:

- partitions A and B on the 5th and 6th
- partitions B, C and whole dataset on the 7th and later


Retro-compatibility with Checks
===============================

Data Quality rules are a super-set of checks, ensuring full retro-compatibility.
Any existing checks will be displayed in the *Data Quality* panel as a rule of the corresponding type.

The Data Quality views, however, rely on data that did not exist previously, and will therefore suffer some limitations:

- timelines for periods before the introduction of Data Quality will stay empty
- current status for datasets will be missing until a single rule is computed on the dataset or the settings are changed
- external checks will not be taken into account in the dataset status until they receive a new value
- current status for projects will only consider dataset that have a status, eg that had a rule computed since the introduction of Data Quality rules
