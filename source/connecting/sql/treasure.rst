Treasure Data
###############

.. warning::

	**Tier 2 support**: Connection to Treasure Data is covered by :doc:`Tier 2 support </troubleshooting/support-tiers>`

.. note::

	You might want to start with our resources on `data connections <https://knowledge.dataiku.com/latest/data-sourcing/connections/index.html>`_ in the Knowledge Base.

.. contents::
	:local:

DSS supports the full range of features on Treasure Data:

* Reading and writing datasets
* Executing SQL recipes
* Performing visual recipes in-database
* Using live engine for charts

Connection setup (Dataiku Cloud Stacks or Dataiku Custom)
===========================================================

The Treasure Data JDBC driver is already preinstalled in DSS and does not need to be installed


Authentication
==============

The only supported authentication method is API key.
You can find more information about API keys `here <https://docs.treasuredata.com/articles/#!pd/getting-your-api-keys/a/h1_326587638>`_.


Advanced install of the JDBC driver
====================================

.. note::

	This feature is not available on Dataiku Cloud.

The Treasure Data JDBC driver is already preinstalled in DSS and does not usually need to be installed. If you need to customize the JDBC driver, follow these instructions:

Treasure Data actually relies on the Presto JDBC driver which can be downloaded from a Maven repositories (such as https://mvnrepository.com/artifact/com.facebook.presto/presto-jdbc)

The driver is made of a single JAR file ``presto-jdbc-xxx.jar``

To install:

* Copy this JAR file to the ``lib/jdbc/treasure_data`` subdirectory of the DSS data directory (create it if necessary)
* Restart DSS
* In each Treasure Data connection, switch the driver mode to "User provided" and enter ``lib/jdbc/treasure_data`` as the Treasure Data driver directory
