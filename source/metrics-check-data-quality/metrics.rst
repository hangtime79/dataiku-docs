Metrics
#########

.. contents::
    :depth: 2
    :local:

The metrics system in DSS allows you to automatically compute measurement on Flow items (datasets, managed folders, and saved models).

.. note::

	Metrics are often used in conjunction with scenarios but are not strictly dependent on scenarios.

Examples of metrics on a dataset include:

* The size (in MB) of the dataset
* The number of rows in the dataset
* The average of a given column

Metrics are configured in the *Status* tabs of datasets, managed folders and saved models.

Metrics are automatically historicized, which is very useful to track the evolution of the status of a dataset. For example, how did the average of ``basket`` evolve in the last month?

Probes and metrics
===================

The whole system is made around the concept of a **Probe**. A probe is a component which computes several metrics on an item.

As much as possible, the probes execute all of their computations in a single pass over the data. Furthermore, the DSS metrics system automatically "merges" together probes when there is an efficient execution path which combines several probes.

Each probe has a configuration which indicates what should be computed for this probe.

Furthermore, each probe can be configured to run automatically after each build of the dataset or not.

Dataset probes
----------------

The following probes are available on a dataset.

Basic info
%%%%%%%%%%%%

This probe computes the size (when relevant) and the number of files (when relevant) of the dataset

Records
%%%%%%%%%

This probe computes the number of records in the dataset.

.. note::

	On non-Hadoop non-SQL datasets, this probe requires enumerating the whole dataset, which can be costly. See the execution engines section.


Partitioning
%%%%%%%%%%%%%

This probe computes the number of partitions and the list of partitions. It only makes sense for a partitioned dataset.

Basic column statistics
%%%%%%%%%%%%%%%%%%%%%%%%

This probe computes descriptive statistics on dataset columns (MIN, MAX, AVG, ...). You can enable multiple metrics on multiple columns


Advanced column statistics
%%%%%%%%%%%%%%%%%%%%%%%%%%%%

This probe computes more descriptive statistics on dataset columns: most frequent value and top N values.

This probe is separate from the "Basic column statistics" because its computation costs are much higher.

Column data validity statistics
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

This probe computes the number and ratio of invalid data in a column. Invalid is defined here with regard to the Meaning of the column. For more information about meanings and storage types, see :doc:`/schemas/index`.

Note that you can only enable this probe on columns for which there is a forced meaning, i.e. it is not possible to check validity compared to a meaning which is only automatically inferred by DSS.

SQL
%%%%%%%

On SQL dataset, probes can be written using a SQL query. Each value in the first row of the query's result is stored as a metric, using the column name of the value as name for the metric. 

.. note::

    If the option "is a single aggregate" is selected, your aggregate metric will automatically be wrapped by the corresponding ``SELECT``, ``FROM``, and ``WHERE`` clauses. 
	
    For example, if this option is selected, the following would be a valid probe statement: ``SUM(cost) / COUNT(customers)``. 
    
    If you were to run this probe on the dataset ``orders`` with the partition ``order_date`` set to '2018-01-01', your aggregation would get translated into the following SQL statement: ``SELECT SUM(cost) / COUNT(customers) as "col_0" FROM orders WHERE order_date='2018-01-01'``.

Python
%%%%%%%

You can also write a custom probe in Python.

Metrics display UI
====================

The value of metrics can be viewed in the "Status" tab of a dataset, managed folder or saved model.

Since there can be a lot of metrics on an item, you must select which metrics to display, by clicking on the ``X/Y metrics`` button

Datasets and managed folders
-----------------------------

There are two main metric views:

* A "tile" view which displays the latest value of each selected metric. Clicking on the value of a metric will bring up a modal box with the history of this value.

* A "ribbon" view which displays the history of all selected metrics.

Note that not all metric values are numerical. For example, the "most frequent value" for a given column is not always numerical. Therefore, the history view sometimes shows history as tables rather than charts.

Probe execution engines
=========================

Depending on the type of dataset and selected probe configurations, dataset probes can use the following execution engines for their computations:

* Hive

    * If selected for a dataset, the Hive engine will be used on datasets that are larger than 10MB in size. The Streaming data engine will be used on smaller datasets.

* Impala
* SQL database

	* This engine is used for SQL datasets, for probes that can perform their computation as a SQL query. The query is fully executed in the database, with no data movement.

* No specific engine

	* For example, the "files size" probe does not require any engine, it simply reads the size of the files

* Streaming data engine

	* Data is streamed into DSS for computation
	* This engine is generally much slower since it needs to move all of the data
	* This engine acts as a fallback if no other engine is possible (for example, )

Metrics on partitioned datasets
================================

On partitioned datasets, the metrics can be computed either on a per-partition basis or on the whole dataset.

.. note::

	Metrics must actually be computed independently on each partition and on the whole dataset, since for a lot of metrics, the metric on the whole dataset is not the "sum" of metrics on each partition.

	For example, the median of a column.

For these datasets, there are 4 views into the metrics:

* The regular "tile" view, showing the last value of selected metrics, either for a given partition or the whole dataset.

* The regular "ribbon" view, showing the history of the values of selected metrics, either for a given partition or the whole dataset.

* A "partitions table" view, showing the last values of several metrics on all partitions, as a data table

* A "partitions chart" view, which tries to display the last values of each metric on all partitions as a chart. This view particularly makes sense for time-based partitions, where the chart will actually be a timeline chart.
