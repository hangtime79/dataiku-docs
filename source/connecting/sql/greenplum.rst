Pivotal Greenplum
##################

DSS supports the full range of features on Greenplum:

* Reading and writing datasets
* Executing SQL recipes
* Performing visual recipes in-database
* Using live engine for charts

.. note::

	You might want to start with our resources on `data connections <https://knowledge.dataiku.com/latest/data-sourcing/connections/index.html>`_ in the Knowledge Base.

Installing the JDBC driver
============================

The Greenplum driver is pre-installed in DSS. You don't need any further installation.


Controlling distribution
=========================

In Greenplum, you can choose the distribution strategy of a table, i.e. how the rows of the table will be split among the nodes of the Greenplum database.

For each managed Greenplum dataset, you can configure how the rows will be distributed in the dataset settings (Greenplum settings > Distribution strategy):

* "Auto", which will use the first column of the table as the only column for distribution. This may not be desirable, especially if the first column is not spread out enough (in that case, only a few nodes would get most/all of the data).

* "Specify distribution columns" lets you manually enter which column(s) will be used for distribution.

* "Distribute randomly" which spreads rows randomly and equally between all nodes.

At the connection settings level, you can specify what the settings should be for new datasets: either Auto or Distribute Randomly. It is not possible to use "Specify distribution columns" as the connection-level default because you need to explicitly choose the columns for each dataset.

Setting distribute and sort clauses
=====================================

DSS does not have builtin support for setting Greenplum "DISTRIBUTE BY" and "SORT BY" clauses. If you want or need to set it on a managed dataset written by DSS, go to the settings of the dataset, in the "Advanced" tab, and override the "Table creation SQL statement"

Secure connections
===================

Support for secure connections is the same as for PostgreSQL.  Follow the :doc:`postgresql` documentation for instructions on how to set up secure connections in Greenplum.

Limitations
===========

* Random :doc:`sampling </sampling/index>` will not be pushed-down to Greenplum if a random seed is used

