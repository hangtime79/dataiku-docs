.. _visualization-sampling:

Sampling & Engine
############################

.. contents::
	:local:

Charts Execution Engines
============================

The choice of execution engine determines how Dataiku DSS processes data for charts.  DSS will automatically suggest an engine based upon the dataset and sampling settings.  The DSS engine is available for all dataset types, while the In-database engine is available for some data sources that support SQL queries.  See below for details.


DSS
-----------------------------

The DSS engine uses a highly-optimized column-based and compressed storage format, which enables it to perform blazing fast aggregations and other visual analytics queries. The DSS engine takes full advantage of modern CPU caches.

The DSS engine does not require that the chart data be loaded in memory, but is instead able to efficiently stream data from disk and perform queries on the fly. This allows you to perform visual analytics on very large data extracts that would not fit in RAM using commodity hardware.

The DSS engine extracts data from your data source, transforms it in its optimized format, and then performs all queries using the pre-optimized data. Once data has been loaded in the Charts Engine, it won't need to access your data source anymore, unless the source data changes.

The DSS engine can therefore perform visual analytic queries on all data sources that DSS supports, even data sources that are not at all suited for analytics, like CSV files.

In-database
----------------------------

In addition to the DSS Charts Engine, DSS can perform visual analytic queries directly in the database, using DB-specific SQL queries. Switching between engines can be useful, for example, to prepare your charts on a sample of the full dataset using the DSS engine and then switch to the In-database engine for full-dataset analytics.

In-database processing is available for the following datasets:

* PostgreSQL
* MySQL
* Vertica
* HDFS - Using Cloudera Impala, if it is installed and the HDFS data source is compatible with Impala.

.. note::

	The In-database engine is not available in Visual Analyses.

Sampling
=========

By default, the charts engine uses the same sample defined on the Explore tab.  You can define a charts-specific sample using the same :doc:`sampling options available in Explore </explore/sampling>`.

.. note::

	The DSS Charts Engine does not require data to fit in memory, however it stores its optimized format on the disk on which DSS resides.

	Therefore, for large samples, you need to make sure that you have enough space on this disk to store your data extracts.

Limit Memory Usage
=========================

RAM
-----------------------------
By default, DSS limits the memory usage of a chart to 150MB.  In general, you shouldn't need to adjust this, but you can increase the value to improve the performance of charts, or decrease the value to improve the performance of your server.

Number of bins
-----------------------------
By default, the number of bins on a chart is limited to 50000. It can be changed by editing the file ``DATADIR/config/dip.properties`` and set the key ``dku.charts.maxBins`` to the new desired limit.
