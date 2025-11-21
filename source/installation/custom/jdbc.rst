Installing database drivers
###########################

Before being able to create SQL-based datasets, you need to install the proper JDBC drivers for the database that you intend to connect to.

Additionally, PostgreSQL script recipe support requires the command-line `psql` client to be installed. See `PostgreSQL support`_.

Download the driver
======================

Data Science Studio comes with bundled drivers for :

* PostgreSQL
* Pivotal Greenplum
* Amazon Redshift
* SQlite

Drivers for other databases must be downloaded from your database vendor.

.. list-table:: Database Drivers
   :header-rows: 1
   :widths: 14 46 40

   * - Database
     - Website
     - Download link
   * - MySQL
     - http://dev.mysql.com/downloads/connector/j/
     - https://dev.mysql.com/get/Downloads/Connector-J/mysql-connector-j-8.4.0.tar.gz
   * - Vertica
     - https://my.vertica.com/download-community-edition/
     - Requires a My Vertica account
   * - Oracle
     - http://www.oracle.com/technetwork/database/features/jdbc/index-091264.html
     -
   * - SQL Server
     - https://msdn.microsoft.com/en-us/data/aa937724.aspx
     - https://learn.microsoft.com/en-us/sql/connect/jdbc/download-microsoft-jdbc-driver-for-sql-server
   * - BigQuery
     - See note below
     -

To install BigQuery driver, please follow the instructions listed in :doc:`connecting to BigQuery </connecting/sql/bigquery>`

Stop Data Science Studio
=========================

In this page, DATA_DIR refers to the data directory where you installed Data Science Studio.

.. note::

    On macOS, the DATA_DIR is always: $HOME/Library/DataScienceStudio/dss_home

Installation of JDBC drivers must be done while Data Science Studio is stopped.

.. code-block:: bash

    DATA_DIR/bin/dss stop

Copy the driver
=================

Copy the driver's JAR file (and its dependencies, if any) to the DATA_DIR/lib/jdbc folder

Restart Data Science Studio
===========================

.. code-block:: bash

    DATA_DIR/bin/dss start

PostgreSQL support
==================

Data Science Studio supports datasets stored in PostgreSQL 9 and above.

.. warning:: PostgreSQL version 8 is not supported.

PostgreSQL script recipe support additionally requires the command-line `psql` client
to be available in the search PATH of the Studio Linux account.

You should install a command-line client compatible with your version of the server.
Depending on your Linux distribution, the appropriate client may be available in a standard
OS package named "postgresql-client" (Debian / Ubuntu) or "postgresql" (RedHat / CentOS / AlmaLinux).
If that is not the case, you can install the correct client for your server and OS by
configuring an extra package repository as described at http://www.postgresql.org/download/ .
