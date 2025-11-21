Vertica
############

.. note::

	You might want to start with our resources on `data connections <https://knowledge.dataiku.com/latest/data-sourcing/connections/index.html>`_ in the Knowledge Base.

DSS supports the full range of features on Vertica:

* Reading and writing datasets
* Executing SQL recipes
* Performing visual recipes in-database
* Using live engine for charts

DSS is tested on Vertica 7.1 and 7.2

Installing the JDBC driver
===========================

The Vertica JDBC driver can be downloaded from the `Vertica website <https://my.vertica.com/download/vertica/client-drivers/>`_.

* If your database version is 7.1 or below, you need the 7.1 driver
* Else, we recommend the latest driver

The driver is a single JAR file called ``vertica-driver-VERSION.jar``

* Copy the JAR file to the ``lib/jdbc`` driver of DSS
* Restart DSS

Timezones support
==================

Versions of the JDBC driver below 8.0 have some bugs related to timezones handling when reading "Timestamp (no timezone)" or "Date" kind of fields. Please use a more recent driver for full timezone support.
