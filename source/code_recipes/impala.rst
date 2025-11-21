Impala
##############

.. contents::
	:local:


Impala is an engine that runs Impala SQL queries on a hadoop cluster and offers performance gains over executing the same queries in Hive.

In its simplest form, the Impala recipe can be used to compute a new HDFS dataset by writing a SQL SELECT query.

Pre-requisites
================

Prior to writing Impala recipes, you need to ensure that DSS and Hadoop are properly configured together, as well as DSS and Impala. See :doc:`/hadoop/installation` and :doc:`/hadoop/impala`.

Creating a simple Impala recipe
===============================

* Create a new Impala recipe
* Select the input datasets. Only HDFS datasets that have a compatible set of params will be proposed.
* Select the dataset that will store the results of the Impala query. You can use an existing not-yet-connected HDFS dataset or create a new managed dataset (which can only be stored on HDFS)

If you create a new managed dataset and your input is partitioned, it’s recommended to use the « Copy partitioning » option.

You can then write your Impala SQL query.

In the query, the datasets that you selected as input will automatically be available as tables with their proper schema.
For example, if you declared dataset A as input of the recipe, and A has columns a1 and a2, you can write "SELECT a1 from A".

When you run the query, the results of the SELECT query are automatically inserted in the output dataset (or output partition of the dataset, if the output dataset is partitioned). Whether the dataset is replaced by the new data, or the new data appended to the dataset, is controlled by the "Append" checkbox on the "I/O" tab.

Validation and schema handling
================================

At any time while writing your Impala recipe, you can click the "Validate" button to perform a comprehensive validation of your script. The validate button performs all checks that Impala normally performs, like:

* Erroneous table/fields names
* Impala QL syntax errors
* Wrong types

When you validate, the schema of the output datasets are compared to the output of your Impala query. If the schemas don’t match (which will always be the case when you validate for the first time after adding a new empty output dataset), DSS will explain the incompatibilities and propose to automatically adjust the output dataset schema.

Stream mode
===========

Because of Impala's limitations when it comes to writing its output, it is sometimes desirable to simply not use Impala for writing the query output back to HDFS. By activating the "Stream mode" on the "Advanced" tab of the recipe, the user can let DSS handle the output. This makes it possible to use any type of output format and/or compression supported by DSS, and to avoid any problem that could arise from setting up or synchronizing file access permissions.


Available tables and partitions
=================================

Impala queries are run on table definitions from the global metastore, so you need to use variables to filter on partitions (if using partitioned datasets). See :doc:`/partitions/variables` for information on variables in SQL queries in DSS.
