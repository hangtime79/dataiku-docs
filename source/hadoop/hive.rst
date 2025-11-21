Hive
############

.. contents::
	:local:

Hive is a tool of the Hadoop environment that allows running SQL queries on top of large amounts of HDFS data by leveraging the computation capabilities of the cluster. It can be used either as a semi-interactive SQL query interface to obtain query results, or as a batch tool to compute new datasets.

Hive maps datasets to virtual SQL tables.

DSS provides the following integration points with Hive :

* The Hive Recipe allows you to compute HDFS datasets as the results of Hive scripts
* All HDFS datasets can be made available in the Hive environment, where they can be used by any Hive-capable tool, even if these datasets were not computed using a Hive recipe. This is called "Hive metastore synchronization"
* The "Hive notebook" allows you to run Hive queries on any Hive database, whether they have been created by DSS or not
* DSS can import table definitions from Hive, and convert them to DSS HDFS dataset definitions

.. note::

	HDFS datasets in DSS are always true "HDFS datasets". They are primarily a path on HDFS and may have an associated Hive table. DSS does not have "Hive-only datasets",
	and accessing Hive tables as SQL datasets using "Other SQL databases" option is not supported.


Interaction with the Hive global metastore
============================================

The global metastore is the metastore that is used when the
"hive" command is launched without arguments. These tables are defined in the database namespace configured in the corresponding HDFS connection.

DSS can:

	* Create tables for the HDFS datasets into the global Hive metastore
	* Import table definitions from the global Hive metastore as HDFS datasets

.. note::

	It is strongly recommended that your Hadoop cluster uses the "Shared metastore" mode
	for the global metastore.

	This is the default behavior for Cloudera and Hortonworks Hadoop distributions


Synchronisation to the Hive metastore
======================================

HDFS datasets in DSS are primarily what their name implies: HDFS datasets. In other words, a HDFS dataset in DSS is a reference to a folder on HDFS. It is not directly a reference to a Hive table.

However, each HDFS dataset in DSS can point to a Hive table. When a managed dataset is built, DSS automatically "pushes" its definition as the corresponding Hive table in the Hive metastore.

This means that as soon as a compatible HDFS dataset has been built, you can use the Hive notebook or any Hive query tool (like Cloudera Hue)

.. note::

	Whenever possible, metastore synchronization also ensures that the dataset is usable by Impala, ie. you can use the Impala Notebook, perform data visualization, or use with any
	Impala query tool (like impala-shell)

	For more details, please see :doc:`/hadoop/impala`

Metastore synchronization normally happens as part of the normal job run, after the dataset is built, but you can also force it manually by following the procedure outlined below.

If the schema of the DSS dataset has changed, DSS automatically updates it in the Hive metastore.

The Hive database and table associated to each dataset is configured in the settings of this dataset.


For external datasets
----------------------

Only managed datasets are automatically synchronized to the Hive metastore. However, you can also manually synchronize an external HDFS dataset.

* Go to the settings of the HDFS dataset
* Fill in the Hive database and table information in the dataset
* Save the dataset settings
* Go to the Advanced tab
* Click on the "Synchronize" button


Importing from the Hive metastore
====================================

In addition to the ability to "push" datasets' definition into the Hive Metastore, DSS can also read preexisting table definitions from the metastore to create associated HDFS datasets in DSS.

To import Hive tables as HDFS datasets:

 * Go to the datasets list
 * Click "New dataset", then "Import from connection"
 * In the list, select your Hive database

Import lists all tables in the Hive database. If there is already a dataset corresponding to each table, you get a link to the existing dataset.

Select the tables that you want to import. If needed, customize the resulting dataset name, then click "Create".

The tool will report which of the Hive tables it managed to import.

The following limitations apply:

* Existing compression settings are not detected, notably on files in the Parquet format. As a result, the output compression is not preserved (if you plan on using this dataset in write mode).
* For partitioned tables, it tries to detect the partitioning scheme, and will import those tables whose partitioning scheme can be handled by DSS. This excludes notably tables where the partition locations can't all be translated into a concatenation of the partitioning columns' values.
* The table definitions are imported 'as is' and the user's HDFS rights on the table's files are not checked, so that an imported table can not necessarily be read from or written to in DSS.

.. note::

	The name of the created datasets default to the Hive table name. In case of conflict, DSS adds a distinctive suffix	to the dataset name.



.. _hadoop.hive.execution-engines:

Hive execution engines
=========================

Notebooks and metrics
-----------------------

Hive notebooks and metrics computations are always executed using Hiveserver2 (and therefore using the global metastore).

If you encounter issues with tables not found, you can check that the datasets that you try to reach have properly been synchronized to the Hive metastore.

Recipes
---------

There are three ways to run Hive recipes in DSS.

.. warning::

	Hive CLI modes are deprecated and will be removed in a future DSS release. Only HiveServer 2 mode will remain available.


Hiveserver 2
%%%%%%%%%%%%%

In this mode, recipes use Hiveserver2. DSS automatically synchronizes the recipe's inputs and outputs to the global metastore when running such a recipe.

Hive CLI (global metastore)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

.. warning::

	This mode is deprecated and will be removed in a future DSS release

In this mode, DSS uses the ``hive`` command-line, targeting the global mode. DSS automatically synchronizes the recipe's inputs and outputs to the global metastore when running such a recipe.


Hive CLI (isolated metastore)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

.. warning::

	This mode is deprecated and will be removed in a future DSS release


In this mode, DSS uses the ``hive`` command-line, but creates a specific metastore for running each recipe.

This mode ensures that your query only uses the proper input and output datasets, since only these ones will be added to the isolated metastore.

Choosing the mode
%%%%%%%%%%%%%%%%%%%%%%%%%

When DSS :doc:`/user-isolation/index` is enabled, only Hiveserver2 mode is supported.

In some setups, running the Hive CLI is not possible. For these setups, only Hiveserver2 mode is possible.

"Hive CLI (isolated metastore)" mode has interesting safety advantages: because the isolated metastore only contains the requested datasets and partitions, you cannot accidentally access data which is not properly declared in your Flow, thus improving the reproducibility.

However, the isolated metastore does not have dataset stats. When Hive runs on Tez, dataset stats are used to compute an optimal execution plan. Not having dataset stats can lead to worse performance. In that case, we recommend using "Hive CLI (global metastore)" or HiveServer2 modes.

In addition, depending on the Hive authorization mode, only some recipe modes might be possible. Check below for more information.

Configuring the mode
%%%%%%%%%%%%%%%%%%%%%

The execution mode can be configured in each Hive recipe (and also in visual recipes running with the Hive engine), in the "Advanced tab".

In addition, you can configure in Administration > Settings > Hive the "Default execution engine", which will select the initial value for newly created recipes. This global setting has no impact on existing recipes.

Support for Hive authentication modes
======================================

DSS supports the following authentication modes for HiveServer2:

* PLAIN authentication for non-secure Hadoop clusters
* KERBEROS authentication for secure Hadoop clusters

.. _hive.authorization-modes:

Support for Hive authorization modes
=====================================

DSS supports several security authorization modes for Hive, depending on the DSS security mode.
For more information, please see  :doc:`/user-isolation/index`

Please read carefully the information below, since some authorization modes impose additional constraints.

Modes not explicitly listed here are not supported.

No Hive security (No DSS User Isolation)
----------------------------------------

In this mode, the Hive metastore accepts requests to create external tables without checks on the storage permissions. HiveServer2 impersonation must be enabled.


Ranger (No DSS User Isolation)
------------------------------

When Ranger is enabled, it controls:

* DDL and DML queries through Hive policies
* HDFS access through HDFS policies

Prerequisites for this mode are:

* Ranger enabled
* Hiveserver2 impersonation disabled

In this mode, you need to add Hive policies in Ranger to allow the ``dssuser`` user full access on the databases used by DSS. In addition, you need to add in your Hive policies grants on other databases used as inputs in DSS.

If, in addition to Ranger, storage-based metastore security is enabled (which is the default on HDP when enabling Ranger mode), you must add a HDFS policy allowing the ``hive`` user full control on the root paths of the DSS HDFS connections.
This is required because, since HiveServer2 does not impersonate in this mode, queries to create tables on the metastore are done on behalf of the ``hive`` user, who must thus have write access to the locations of the created tables.


Ranger (DSS User Isolation enabled)
---------------------------------------

When Ranger is enabled, it controls:

* DDL and DML queries through Hive policies
* HDFS access through HDFS policies

Prerequisites for this mode are:

* Ranger enabled
* Hiveserver2 impersonation disabled

In this mode, you need to add Hive policies in Ranger to allow the ``dssuser`` user full access on the databases used by DSS. In addition, you need to add in your Hive policies grants on other databases used as inputs in DSS.

If, in addition to Ranger, storage-based metastore security is enabled (which is the default on HDP when enabling Ranger mode), you must go to Administration > Settings > Hadoop and check the "Write ACL in datasets" setting. This will automatically add a write ACL to the Hive user when building datasets and synchronizing permissions. This is required because, since HiveServer2 does not impersonate in this mode, queries to create tables on the metastore are done on behalf of the ``hive`` user, who must thus have write access to the locations of the created tables.

Storage-based security (No DSS User Isolation)
-------------------------------------------------

In this mode:

* Storage-based security is enabled in the metastore (ie the metastore checks that a user requesting DDL has rights on the underlying HDFS directories)
* HiveServer2 impersonation is enabled

Since HiveServer2 impersonation is enabled, the user requesting the metastore is ``dssuser``, so no further action is necessary.

.. note::

	This is the default setup for HDP

Supported file formats
=======================

Hive only recognizes some formats, so not all HDFS datasets can be synchronized to Hive or used in a Hive recipe.

The following formats are handled:

* CSV, only in "Escaping only" or "No escaping nor quoting" modes
* Parquet. If the dataset has been built by DSS, it should use the "Hive flavor" option of the Parquet parameters.
* Hive Sequence File
* Hive RC File
* Hive ORC File
* Avro

Limitations
------------

* Hadoop does not support at all CSV files with newlines embedded within fields. Trying to parse such files with Hadoop or any Hadoop tool like Hive will fail and generate invalid data

Internal details
=================

Data Science Studio creates all tables as EXTERNAL tables in the Hive meaning of the term.

.. todo::
  * Date formats support
  * Complex type stuff
