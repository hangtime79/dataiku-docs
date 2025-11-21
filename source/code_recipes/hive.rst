Hive recipes
############

.. toctree::

For an overview of how DSS and Hive interact, please refer to :doc:`/hadoop/hive`.

In its simplest form, the Hive recipe can be used to compute a new HDFS dataset by writing a SQL SELECT query.

Pre-requisites
================

Prior to writing Hive recipes, you need to ensure that DSS and Hadoop are properly configured together. See :doc:`/hadoop/installation`.

Creating a simple Hive recipe
==============================

* Create a new Hive recipe
* Select the input datasets. Only HDFS datasets that have a compatible set of params will be proposed.
* Select the dataset that will store the results of the Hive query. You can use an existing not-yet-connected HDFS dataset or create a new managed dataset (which can only be stored on HDFS)

If you create a new managed dataset and your input is partitioned, it’s recommended to use the « Copy partitioning » option.

You can then write your HiveQL query.

In the query, the datasets that you selected as input will automatically be available as tables with their proper schema.
For example, if you declared dataset A as input of the recipe, and A has columns a1 and a2, you can write "SELECT a1 from A".

When you run the query, the results of the SELECT query are automatically inserted in the output dataset (or output partition of the dataset, if the output dataset is partitioned). As usual with Data Science Studio, this insertion is made in "overwrite" mode. The previous content of the dataset (resp. partition) is erased and replaced with the new one.

Validation and schema handling
================================

At any time while writing your Hive recipe, you can click the "Validate" button to perform a comprehensive validation of your script. The validate button performs all checks that Hive normally performs, like:

* Erroneous table/fields names
* Hive QL syntax errors
* Wrong types

When you validate, the schema of the output datasets are compared to the output of your Hive queries. If the schemas don’t match (which will always be the case when you validate for the first time after adding a new empty output dataset), DSS will explain the incompatibilities and propose to automatically adjust the output dataset schema.


Available tables and partitions
=================================

Each Hive recipe runs in a separate Hive environment (called a metastore). In this isolated environment, only the datasets that you declared as inputs exist as tables. If you get table not found errors when running the query, you are probably trying to access a dataset that you did not declare as input.

If your input datasets are partitioned, only the partitions that are needed by the dependencies system are available. Therefore, you do not need to write any WHERE clause to restrict the selected partitions. Only the required partitions will be included in the results.


Writing more complex queries
==============================

The cases we covered until now were cases where you actually only want to insert into the output dataset the results of a single Hive query. Behind the scene, Data Science Studio automatically rewrote your Hive query to include the Hive INSERT commands.

That simple case does not however cover all possible cases of the Hive recipe. Some example use cases include:

* Write temporary tables to compute your dataset
* Write several datasets in a single Hive recipe (which can be useful for performance reasons)

In that case, you need to write the full INSERT statement.
Basically, you must write a statement like "INSERT OVERWRITE TABLE output_dataset_name SELECT your_select_query".

.. note::
	This statement does not cover the partitioned case. For more information about inserting when writing partitioned Hive recipes, see :doc:`/partitions/hive`.
