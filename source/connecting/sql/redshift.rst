.. _connecting-sql-redshift:

Amazon Redshift
################

.. note::

	You might want to start with our resources on `data connections <https://knowledge.dataiku.com/latest/data-sourcing/connections/index.html>`_ in the Knowledge Base.

DSS supports the full range of features on Redshift:

* Reading and writing datasets
* Executing SQL recipes
* Performing visual recipes in-database
* Using live engine for charts

.. contents::
	:local:


Setting up (Dataiku Custom or Dataiku Cloud Stacks)
====================================================

Selecting the JDBC driver
---------------------------

There are two JDBC drivers for Redshift:

* Redshift can use the PostgreSQL driver. This driver is pre-installed in DSS. You don't need any further installation.

* Redshift can use a dedicated Redshift driver

When setting up the connection, you can choose which driver to use.

The dedicated driver is required for the following capabilities:

* Reading external tables (also known as "Redshift Spectrum")
* Using an IAM role for connecting
* Reading or writing more than 2 billion records from/to a Redshift dataset (apart from using the In-database SQL engine)

Installing the dedicated driver
--------------------------------

* Download the JDBC driver from AWS 

* Create a new folder under DATA_DIR/lib/jdbc, such as DATA_DIR/lib/jdbc/redshift-dedicated

* Copy the `redshift-jdbc42-X.Y.Z.T.jar` file to `DATA_DIR/lib/jdbc/redshift-dedicated`

* Restart DSS

In the connection settings, set "Redshift driver (user-provided)" as "Driver to use", and enter `lib/jdbc/redshift-dedicated` as "Driver jars directory".

Writing data into Redshift
===========================

Loading data into Redshift using the regular SQL "INSERT" or "COPY" statements is extremely inefficient (a few dozens of records per second) and should only be used for extremely small datasets.

The recommended way to load data into Redshift is through a bulk COPY from files stored in Amazon S3.

DSS can automatically use this fast load method. For that, you require a S3 connection. Then, in the settings of the Redshift connection:

* Enable "Automatic fast-write"
* In "Auto fast write connection", enter the name of the S3 connection to use
* In "Path in connection", enter a relative path to the root of the S3 connection, such as "redshift-tmp". This is a temporary path that will be used in order to put temporary upload files. This should not be a path containing datasets.

DSS will now automatically use the optimal S3-to-Redshift copy mechanism when executing a recipe that needs to load data "from the outside" into Redshift, such as a code recipe.

Note that when running visual recipes directly in-database, this does not apply, as the data does not move outside of the database.

Constraints on the S3 connection
---------------------------------

In order for automatic fast-write to work, the following are needed:

* The S3 bucket and the Redshift cluster must be in the same Amazon AWS region

Explicit sync from S3
-----------------------

In addition to the automatic fast-write that happens transparently each time a recipe must write into Redshift, the Sync recipe also has an explicit "S3 to Redshift" engine. This is faster than automatic fast-write because it does not copy to the temporary location in S3 first.

It will be used automatically if the following constraints are met:

* The source dataset is stored on S3 
* The destination dataset is stored on Redshift
* The S3 side is stored with a CSV format, using the UTF-8 charset
* For the S3 side, the "Unix" CSV quoting style is not used
* For the S3 side, the "Escaping only" CSV quoting style is only supported if the quoting character is ``\``
* For the S3 side, the files must be all stored uncompressed, or all stored using the GZip compression format

In addition:

* The S3 bucket and the Redshift cluster must be in the same Amazon AWS region
* The schema of the input dataset must match the schema of the output dataset, and values stored in fields must be valid with respect to the declared Redshift column type.

Technical details about implementation
--------------------------------------

S3-to-Redshift sync and automatic fast-write are implemented by first saving a manifest file under a temporary directory in the "default path for managed datasets" of the EC2 connection corresponding to the input S3 dataset, then sending the appropriate COPY command to the Redshift database, causing it to load the files referenced in the manifest. Note that this manifest file is not deleted when the copy is complete, for debug and history purposes. Past manifest files are normally small enough not to cause any space issue, and can be manually deleted at any time after the copy.

Additional details about the bulk loading process of a Redshift database from S3 files can be found in the Redshift documentation at http://docs.aws.amazon.com/redshift/latest/dg/t_Loading_tables_with_the_COPY_command.html and http://docs.aws.amazon.com/redshift/latest/dg/r_COPY.html.

Unloading data from Redshift to S3
===================================

Unloading data from Redshift directly to DSS using JDBC is reasonably fast. However, if you need to unload data from Redshift to S3, the sync recipe has a "Redshift to S3" engine that implements a faster path.

In order to use Redshift to S3 sync, the following conditions are required:

* The source dataset must be stored on Amazon Redshift
* The destination dataset must be stored on Amazon S3
* Buckets that mandate SSE-KMS encryption are not supported (only SSE-S3 is supported)
* The S3 bucket and the Redshift cluster must be in the same Amazon AWS region
* The S3 side must be stored with a CSV format, using the UTF-8 charset
* For the S3 side, the "Unix" CSV quoting style is not supported
* For the S3 side, the "Escaping only" CSV quoting style is only supported if the quoting character is ``\``
* For the S3 side, the files must be all stored uncompressed, or all stored using the GZip compression format

Additionally, the schema of the input dataset must match the schema of the output dataset, and values stored in fields must be valid with respect to the declared Redshift column type.

Reading external tables
========================

DSS can read external tables (also known as "Redshift Spectrum") starting in DSS 10.0.6

This capability requires using the Redshift driver

Controlling distribution and sort clauses
==========================================

In Redshift, you can control:

* How the rows are distributed between the nodes of the Redshift database
* How the rows are sorted among one slice of the database

For each managed Redshift dataset, you can configure both distribution style and sort key in the dataset settings (Redshift settings)

For distribution, you can select:

* "Auto", which will assign an optimal distribution based on the size of the table data.
* "Distribute evenly" which distributes rows evenly between nodes
* "Copy table to all nodes", which makes a copy of all rows in all nodes (use only for very small tables)
* "Select a distribution key" to select manually a distribution column

For sort, you can choose between non sorted, or compound or interleaved sort. In the latter cases, you can select the sort columns.

For more details, please see the `Redshift documentation <https://docs.aws.amazon.com/redshift/latest/dg/c_choosing_dist_sort.html>`_.

When you create a new dataset, it is always created with "Auto" distribution and no sort key (it is not possible to set a default sort key at the connection level, because the columns depend on the dataset).

Limitations
============

* The fast data load from S3 to Redshift ignores the timezone information of dates. Only dates expressed in UTC timezone are supported. 
* Random :doc:`sampling </sampling/index>` will not be pushed-down to Redshift if a random seed is used
