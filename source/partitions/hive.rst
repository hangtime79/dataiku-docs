Partitioned Hive recipes
##########################

This page deals with the specific case of partitioned datasets in Hive recipes. For general information about Hive recipes, see :doc:`/code_recipes/hive`

Short summary
===============

If your Hive recipe is a "simple" one, ie if:

* You have only one output dataset
* Your query starts with SELECT

Then you don't need to do anything special to deal with partitioning: your query will only run over the selected input partitions and will write directly in the requested output partition.

.. note::

	Even though Hive recipes look like SQL recipes, they act on HDFS datasets, which use files-based partitioning, while SQL recipes can only use column-based partitioning.

What data is read from inputs ?
===============================

Each Hive recipe runs in a separate Hive environment (called a metastore). In this isolated environment, only the datasets that you declared as inputs exist as tables and only the partitions that are needed by the dependencies system are available. Therefore, you do not need to write any WHERE clause to restrict the selected partitions as you would in an SQL recipe. Only the required partitions will be included in the query.

.. note::
  For the query ``SELECT * FROM foo``, Hive includes the partitioning column in the result,
  even if it is not physically written on HDFS.
  If you don't want it, name all columns in the request: ``SELECT a,b,c FROM foo`` (click the column names in the left side panel to do so quickly).


How to write data ?
=========================

If you have only one output dataset and your query starts with a SELECT, Dataiku DSS automatically transforms it into a an INSERT OVERWRITE statement into the relevant partition.

If you want to take control over your insert (see :doc:`/code_recipes/hive`) and the output datasets are partitioned, then you must explicitly write the proper INSERT OVERWRITE statement in the output partition.

The Hive syntax for writing in a partition is:

.. code-block:: sql

	INSERT OVERWRITE TABLE output_dataset_name
		PARTITION (dimension='value', dimension2='value2')
		SELECT your_select_query

The values in the PARTITION clause must be static, i.e., they cannot be computed using the query itself. Each time the recipe is run, the values must be the ones of the partition being computed of this dataset. To automatically set the proper values depending on which partition is being built, you can use :doc:`/partitions/variables`

For example (supposing that the 'customers' dataset is partitioned by 'date' and 'country'):

.. code-block:: sql

	INSERT OVERWRITE TABLE customers
		PARTITION (date='$DKU_DST_date', country='$DKU_DST_country')
		SELECT your_select_query
