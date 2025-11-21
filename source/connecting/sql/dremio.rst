Dremio
########

.. warning::

	**Experimental**: Connection to Dremio is :doc:`Experimental </troubleshooting/support-tiers>`


Dataiku has experimental support for interacting with Dremio:

* Reading data from Dremio
* SQL notebook
* Performing in-database computation for Dremio->Dremio recipes 
* Performing in-database charts
* Limited support for write-back to Dremio from non-Dremio data

Support has been tested on Dremio Cloud.


Setting up
===========

Dataiku support for Dremio leverages the "Flight SQL" driver. You can download the driver from Dremio's site: https://docs.dremio.com/current/client-applications/drivers/arrow-flight-sql-jdbc-driver

Put the driver in a subfolder of your ``lib/jdbc`` driver, such as ``lib/jdbc/dremio``

In Dataiku, create an "Other databases (JDBC)" connection

* JDBC driver class: ``org.apache.arrow.driver.jdbc.ArrowFlightJdbcDriver``

* JDBC URL: ``jdbc:arrow-flight-sql://HOST:443/?token=ENCODED_TOKEN&catalog=CATALOG_GUID``, where:
 
  * For Dremio Cloud, HOST is usually ``data.dremio.com`` or ``data.eu.dremio.com``

  * CATALOG_GUID is the project id of a project in your Dremio. It can be found in the Sonar "Settings" page for your project
  * ENCODED_TOKEN is a Personal Access Token, URL-encoded

* Drivers jars directory: ``lib/jdbc/dremio`` (or another folder that you may have selected)

* SQL Dialect: ``Dremio``

* User/Password: Leave empty

* Can browse catalogs: Disable

Importing tables
=================

You can import tables using the usual Connection Explorer.

A specificity of Dremio is that within dataset settings, table and schema names should be quoted. Unlike other databases, in Dremio, the schema can be made of several quoted chunks, representing the hierarchical nature of Dremio.

For example, the famous TPCDS datasets can be accessed with:

* Table: ``"call_center"``
* Schema: ``"Samples"."samples.dremio.com"."tpcds_sf1000"``

Limitations
============

* Writing data into Dremio "from the outside" (which is done through JDBC inserts) is **extremely** slow (about one record every 2-5 seconds)

* Dremio does not have a "timestamp with time zone" data type, so the "datetime with tz" type of DSS gets converted to a timestamp-unaware field in Dremio. Various timezone shift issues may be encountered.

* In charts, support for dates / timestamps is limited