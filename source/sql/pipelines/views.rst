Views in SQL pipelines
#######################

.. contents::
    :local:


DSS uses SQL views to represent virtualized datasets in a SQL pipeline. Therefore, when querying a virtualized dataset, DSS references the view (instead of the the table backing the virtualized dataset) by using the view name. The view name contains these components:

* [tableName]: name of the table from which the view is derived
* [partitionID]: ID of the partition corresponding to the view (if working with a :doc:`partitioned SQL table dataset</partitions/sql_datasets>`)
* [randomString]: randomly-generated 5-character alphanumeric string

Using these components, views are named as follows:

* prefix: ``DSSVIEW_``
* middle: ``[tableName]_[partitionID]``
* suffix: ``_[randomString]`` 

Because some databases have strict limits on the length of view names, the middle characters in the view name ``[tableName]_[partitionID]`` may be truncated to ensure that the prefix and suffix fit.

.. _view-cleanup-sql-pipelines:

Cleanup of views in pipelines
======================================

Leaving views behind at the end of a pipeline can cause problems if you later try to drop the table from which the view was derived. Therefore, DSS has a process for automatically cleaning up all views at the end of pipelines.

.. note::

	If using version **1.1.5.1005** of the Simba BigQuery JDBC driver, you can run into an error that occurs when the view cleanup loop stops, even though views appears to be dropped. Consider upgrading your driver to version **1.2.0.1000** of the Simba BigQuery JDBC driver to avoid running into this error.

.. _Tips-views-sql-pipelines:

Tip
=======

* If you run into a pipeline execution error that is linked to old views being left behind, you can use the naming convention ``DSSVIEW_[tableName]_[partitionID]_[randomString]`` to find the views that DSS created, and manually drop them.
* A macro that attempts to clean up any old views has been added to DSS. You can find it alongside the other macros under the name "Drop pipeline views". You must have full DSS Administrator privileges to run it.


Related Pages
===============

* :doc:`./partitions`
* :doc:`/partitions/sql_datasets`
* :doc:`/partitions/sql_recipes`
