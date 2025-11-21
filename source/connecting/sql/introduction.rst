Introduction
#############

.. contents::
    :local:

Supported databases
====================

DSS provides full support for many databases and experimental support for others. Click on a link for detailed support information for that database.

Full support
-------------

DSS fully supports the following databases:

* :doc:`snowflake`
* :doc:`synapse`
* :doc:`bigquery`
* :doc:`redshift`
* :doc:`postgresql`
* :doc:`teradata`
* :doc:`oracle`
* :doc:`sqlserver`
* :doc:`greenplum`
* :doc:`mysql`
* :doc:`vertica`


Tier 2 support
---------------------

DSS has :doc:`Tier 2 support </troubleshooting/support-tiers>` for the following databases:


* :doc:`saphana`
* :doc:`athena`
* :doc:`exasol`
* :doc:`netezza`
* :doc:`db2`
* :doc:`trino`
* :doc:`../kdbplus`

Other databases
-----------------

In addition, DSS can connect to any database that provides a JDBC driver.

.. warning::
	For databases not listed previously, we cannot guarantee that anything will work.
	Reading datasets often works, but it is rare that writing works out of the box.

You might be able to get a better behavior by selecting a specific dialect from the dropdown in the JDBC connection screen


Defining a connection
======================

.. note::
	Before you try to connect to a database, make sure that the proper JDBC driver for it is installed. For information on how to install JDBC drivers, see :doc:`Custom Dataiku instructions </installation/custom/jdbc>` or :doc:`Dataiku Cloud Stacks for AWS instructions </installation/cloudstacks-aws/templates-actions>`

The first step to work with SQL databases is to create a connection to your SQL database.

* Go to the Administration > Connection page.
* Click "New connection" and select your database type.
* Enter a name for your connection.
* Enter the requested connection parameters. See the page of your database for more information, if needed
* Click on Test. DSS attempts to connect to the database, and gives you feedback on whether the attempt was successful.
* Save your connection.

Advanced connection settings
=============================

Advanced JDBC properties
-------------------------

For all databases, you can pass arbitrary key/value properties that are passed as-is to the database's JDBC driver. The possible properties depend on each JDBC driver. Please refer to the documentation of your JDBC driver for more information

Custom JDBC URL
---------------

For all databases for which DSS has a specific connection kind, DSS automatically constructs the JDBC URL from the structured settings. For advanced use cases, you can enable the "Custom JDBC URL" mode and enter your own JDBC URL

Fetch size
-----------

When DSS reads records from the database, it fetches them by batches for improved performance. The "fetch size" parameter lets you select the size of this batch. If you leave this parameter blank, DSS uses a reasonable default. Setting the fetch size to high values (above a few thousands) can improve performance, especially if your network connection to the database has high latency, at the expense of increased memory usage.

Truncate to clear data
-----------------------

By default, when writing non-partitioned managed datasets, DSS drops the table and recreates it (which avoid schema discrepancy problems). You can enable this option to TRUNCATE the table instead.

Naming rules
------------

See :doc:`../relocation`
