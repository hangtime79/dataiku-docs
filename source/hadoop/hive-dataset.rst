Hive datasets
###############

.. contents::
	:local:

Most of the time, to read and write data in the Hadoop ecosystem, DSS handles HDFS datasets, that is file-oriented datasets pointing to files residing on one or several HDFS-like filesystems.

DSS can also handle Hive datasets. Hive datasets are pointers to Hive tables already defined in the Hive metastore.


* Hive datasets can only be used for reading, not for writing
* To read data from Hive datasets, DSS uses HiveServer2 (using a JDBC connection). In essence a Hive dataset is a SQL-like dataset

Use cases
==========

HDFS dataset remains the "to-go" dataset for interacting with Hadoop-hosted data. The HDFS dataset provides the most features, the most ability to parallelize work and execute it on the cluster.

However, there are some cases of (existing) source data for which the HDFS isn't able to read them properly. In that case, using a Hive dataset as the source of your Flow will allow you to read your data. Since Hive dataset is read-only, only the sources of the Flow use a Hive dataset, and subsequent parts of the Flow revert to regular HDFS datasets.

Hive views
------------

If you have existing data which is available through a Hive view, there are no HDFS files materializing this particular data. In that case, you cannot use a HDFS dataset and should use a Hive dataset.

No read access on source files
-------------------------------

Through the Hive security mechanisms (Ranger), it is possible to have existing tables in the Hive metastore, with read access to these tables using HiveServer2, but not read access to the underlying HDFS files.

In that case, you cannot use a HDFS dataset and should use a Hive dataset.

ACID tables (ORC)
------------------

You can create ACID tables in Hive (in the ORC format). These tables support UPDATE statements that regular Hive tables don't support. These tables are stored in a very specific format that only HiveServer2 can read. DSS cannot properly read the underlying files of these tables.

In that case, you cannot use a HDFS dataset and should use a Hive dataset.

DATE and DECIMAL data types
----------------------------

There are various difficulties in reading tables containing these kind of columns. It is recommended to use Hive datasets preferably when reading these tables.

Creating a Hive dataset
==========================

You do not need to setup a connection to create a Hive dataset. As soon as connectivity with Hadoop (and your HiveServer2) is established, you can create Hive datasets

New dataset
------------

* Select New Dataset > Hive
* Select the database and the table
* Click on test to retrieve the schema
* Your Hive dataset is ready to use

Import
-------

Either from the catalog or connections explorer, when selecting an existing Hive table, you will have the option to import it either as a HDFS dataset or Hive dataset.

Using a Hive dataset
=====================

A Hive dataset can be used with most kinds of DSS recipes.

Hive recipes
--------------

You can create Hive recipes with Hive datasets as inputs.

.. note::

	The recipe MUST be in "Hive CLI (global metastore)" or HiveServer2 mode for this to work. Please see :doc:`hive` for more information.

Visual recipes with Hive as execution engine
--------------------------------------------

You can create visual recipes and select the Hive execution engine (when available) with Hive datasets as inputs.

.. note::

	The recipe MUST be in "Hive CLI (global metastore)" or HiveServer2 mode for this to work. Please see :doc:`hive` for more information.

Spark recipes
-------------

You can create Spark (code) recipes with Hive datasets as inputs.

.. note::

	The recipe MUST be in "Use global metastore)" mode for this to work.

.. note::

	You must have filesystem-level access to the underlying files of this Hive table for this to work.


Visual recipes with Spark as execution engine
-----------------------------------------------

You can create visual recipes and select the Spark execution engine (when available) recipes with Hive datasets as inputs.

.. note::

	The recipe MUST be in "Use global metastore)" mode for this to work.

.. note::

	You must have filesystem-level access to the underlying files of this Hive table for this to work.


Limitations
------------

* SQL recipes cannot be used. Use a Hive recipe instead
* Spark engine (and Spark recipes) cannot be used if you don't have filesystem access to the underlying tables. 