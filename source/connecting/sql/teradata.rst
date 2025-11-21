Teradata
#########

.. note::

	You might want to start with our resources on `data connections <https://knowledge.dataiku.com/latest/data-sourcing/connections/index.html>`_ in the Knowledge Base.

.. contents::
	:local:

DSS supports the following features on Teradata:

* Reading and writing datasets
* Executing SQL recipes
* Performing visual recipes in-database
* Using in-database engine for charts

Please see below for limitations and detailed instructions.


Installing the JDBC driver
===========================

The Teradata JDBC driver can be downloaded from `Teradata website <https://downloads.teradata.com/download/connectivity/jdbc-driver>`_.

The driver contains the following JAR file:

* terajdbc4.jar

To install:

* Copy the JAR file to the ``lib/jdbc`` subdirectory of the DSS data directory
* Restart DSS

Connecting using TD2 (default) authentication
==============================================

By default, the Teradata connector uses the TD2 authentication mechanism. Simply enter the login/password.

Using per-user-credentials with TD2 authentication
---------------------------------------------------

Use the classic :doc:`per-user-credentials </security/connections>` procedure.

Connecting using LDAP authentication
=====================================

By default, the Teradata connector uses the TD2 authentication mechanism. To use other kinds of authentication mechanism, enable the "Use custom JDBC URL".

Enter "jdbc:teradata://YOUR-TERADATA-HOSTNAME/" as both the "connection URL" and "displayed URL".

Add Advanced JDBC properties as documented in the Teradata JDBC driver documentation.

To log in using LDAP, add the following properties:

* ``LOGMECH`` = ``LDAP``
* ``LOGDATA`` = ``username@@password``


Using per-user-credentials with LDAP authentication
----------------------------------------------------

First, get familiar with per-user-credentials: :doc:`/security/connections`

Switch the connection to "per-user credentials mode". Then add the following properties:

* ``LOGMECH`` = ``LDAP``
* ``LOGDATA`` = ``%{pucUser}@@%{pucPassword}``

The ``%{pucUser}`` and ``%{pucPassword}`` will be replaced by the per-user-credential login and password at runtime.

Connecting using Kerberos authentication
=========================================

.. note::

	This feature is not available on Dataiku Cloud.

In order to use Kerberos authentication, you need a principal and keytab for that principal, authorized to connect to the Teradata database.

The keytab must be saved on the DSS machine, readable by the DSS user (and not readable by impersonated users)

* Enable "Login with Kerberos" option
* Enter the principal (fully-qualified)
* Enter the absolute path to the keytab

Using per-user-credentials with Kerberos authentication
--------------------------------------------------------

It is not possible to use per-user-credentials with Kerberos authentication. Instead, you can use impersonation (see below).

Impersonation
==============

It is possible to use the Teradata PROXYUSER mechanism in order to implement impersonation on Teradata.

This is implemented by using a ``SET QUERY_BAND`` statement as a "Post-connect statement". The post-connect statement will contain a reference to a variable indicating the user currently trying to connect

Prerequisites
--------------

* The connection must be in "global credential" mode.
* The user specified in the connection is the "trusted user" and must have the right to impersonate other users. This means that for each impersonated user (aka proxy user), a ``GRANT CONNECT THROUGH trusted_user TO PERMANENT proxy_user WITHOUT ROLE`` or similar must be issued, accompanied with ``GRANT CONNECT THROUGH trusted_user WITH TRUST_ONLY``.
* You must add the following advanced JDBC property to the connection: ``TRUSTED_SQL`` with value ``ON`` (DSS will automatically mark user-submitted code as untrusted)

.. warning::

	Make sure to use the ``WITH TRUST_ONLY`` statement. Without this, the proxy user would be able to switch back to the trusted user

Setup (same DSS / Teradata users)
----------------------------------

This requires that the DSS users have the same login as the Teradata users

In the Teradata connection, add the following post-connect statement:

``SET QUERY_BAND='PROXYUSER=${dssUserLogin};' FOR SESSION``

When user A (a DSS user) connects to the database, DSS will execute ``SET QUERY_BAND='PROXYUSER=A``, and further commands will execute as the Teradata user A.


Setup (different users)
------------------------

If your Teradata users have different logins than the DSS user, then the DSS administrator needs to setup an "administrator property" for each DSS user, which indicates the name of the Teradata user.

If you have a DSS user A_D that you want to remap to a Teradata user A_T:

* Go to the user profile of A_D
* In "Admin properties", add something like ``"teradataUser" : "A_T"``

Then in the Teradata connection, add the following post-connect statement:

``SET QUERY_BAND='PROXYUSER=${adminProperty:teradataUser};' FOR SESSION``

When DSS user A_D connects to the database, DSS will execute ``SET QUERY_BAND='PROXYUSER=A_T``, and further commands will execute as the Teradata user A_T

Controlling the primary index
==============================

In Teradata, the Primary Index of a table defines how this table will be distributed among the multiple AMPs that make up a Teradata database.

For each managed Teradata dataset, you can configure how the Primary Index will be created in the dataset settings (Teradata settings > Primary index strategy):

* "Auto", which will use the default setting of the database. In other words, no "PRIMARY INDEX" will be added to the table creation statement. In many cases, this leads to using the first column of the table as the only column of the primary index. This may not be desirable, especially if the first column is not spread out enough (in that case, only a few AMPs would get most/all of the data).

* "Specify index columns" lets you manually enter which column(s) will make up the primary index. You can also specify whether you want a unique index (which makes a ``CREATE TABLE``) or non-unique index (which makes a ``CREATE MULTISET TABLE``)

* "No primary index" which uses ``NO PRIMARY INDEX``. In that case, rows are randomly assigned to AMPs

At the connection settings level, you can specify what the settings should be for new datasets: either Auto or No Primary Index. It is not possible to use "Specify index columns" as the connection-level default because you need to explicitly choose the columns for each dataset.

Tracing additional query information
=====================================

In order to provide for better audit, it can be interesting to add in the Query band of your Teradata queries information about the queries that are being performed.

You can do that by adding/putting elements in a ``SET QUERY_BAND`` post-connect statement. You can only use user-level information here.

For example, you can use the following post-connect statement: ``SET QUERY_BAND='DSS_USER=${dssUserLogin};' FOR TRANSACTION``. This will add the logfin of the DSS user in the Query band. You can then find this query band in various Teradata tracing options (like the ``dbc.dbqlogtbl`` table).

You can also access user and admin properties using ``${userProperty:XXX}`` and ``${adminProperty:XXX}``

In addition, you can add "job-specific post-connect statements". These statements will only execute for Teradata queries that are emitted as part of a job. In these job-specific post-connect statements, you can access the following additional variables:

* ``${jobProjectKey}`` (contains the project key in which the job executes)
* ``${jobId}`` (contains the full identifier of the job)
* ``${activityId}`` (contains the recipe name and output partition)
* All variables of the project

For example, the following job-specific post-connect statement will log information about the job being executed in the query band:

.. code-block:: sql

	SET QUERY_BAND = 'JPK=${jobProjectKey};JID=${jobId};AID=${activityId};USER=${dssUserLogin};' FOR TRANSACTION

Autocommit Mode
===============

Teradata connections can be put in "autocommit" mode, which makes it much easier to write DDL statements, use stored procedures, write stored procedures or use third-party plugins.

This is configured by selecting the checkbox "Autocommit mode" in the Advanced Params of the connection. If you are attempting to call Teradata stored procedures, this setting should be enabled.  

Limitations
============

Personal Connections
---------------------

Creating personal connections with Teradata is not supported.

In-database charts
-------------------

Breakdown by "Quarter" and "Week" are not supported for in-database charts on Teradata. You can workaround by using the DSS charts (this will be slower).

Sort recipe
------------

The Sort recipe is not supported on Teradata inputs. You can workaround by setting the engine of the recipe to DSS engine (this will be slower).

Note that sorting with a Teradata output will have no effect since Teradata does not preserve order on write.

Split recipe
--------------

The "Random dispatch of data" with "subset of columns" mode is not supported on Teradata. You can workaround by setting the engine of the recipe to DSS engine (this will be slower).

Parallel build of partitioned datasets
---------------------------------------

The first build job creating a partitioned dataset (either the first time, or subsequent times after the dataset has been cleared) must not be run on multiple partitions in parallel.

If this "first build", which creates the table, is run on multiple partitions in parallel, some partitions may randomly fail. You can either set the parallelism of the recipe to 1, or first build a single partition before building others.

Random sampling
---------------

Random :doc:`sampling </sampling/index>` will not be pushed-down to Teradata if a random seed is used

Fast sync using TDCH
=====================

Fast synchronization of datasets between Teradata and HDFS is possible using TDCH. Please see :doc:`/hadoop/tdch` .

Notes
=====

* If your password contains a comma, you need to enclose the whole password in single-quotes
