Trino/Starburst
###############

.. warning::

	**Tier 2 support**: Connection to Trino/Starburst is covered by :doc:`Tier 2 support </troubleshooting/support-tiers>`

.. note::

	You might want to start with our resources on `data connections <https://knowledge.dataiku.com/latest/data-sourcing/connections/index.html>`_ in the Knowledge Base.

.. contents::
	:local:

DSS supports connecting to Trino clusters, including Starburst ones:

* Reading and writing datasets
* Executing SQL recipes
* Performing visual recipes in-database
* Using live engine for charts

Connection setup (Dataiku Cloud Stacks or Dataiku Custom)
===========================================================

The Trino JDBC driver is already preinstalled in DSS and does not need to be installed

* Fill in the settings of the connection using your Trino/Starburst information.
* (Optional but recommended) Fill auto-fast-write settings - see :ref:`connecting-sql-trino-writing`


Authenticate using JWT tokens
=============================

DSS can authenticate to Trino using `JWT tokens <https://trino.io/docs/current/security/jwt.html>`_, which DSS retrieves from an OAuth2 provider. The provider authenticates the user, gives DSS an access token in JWT form, and the Trino cluster verifies the validity of the JWT token then uses the identity and roles defined in the token for its own permission system.

OAuth2 access is performed either using "per-user" credentials, or using "global" client credentials.


.. _connecting-sql-trino-writing:

Writing data into Trino
============================

Loading data into a Trino dataset in DSS, using the regular SQL ``INSERT`` statements, is inefficient and should only be used for extremely small datasets.

The recommended way to load data into a Trino table is through a bulk COPY from files stored in a cloud storage.

DSS can automatically use this fast load method. For that, you need a S3, GCS or Azure Blob connection, where DSS automatically writes the temporary data, before using a bulk `COPY INTO` statement in Trino. Then, in the settings of the Trino connection:

* Enable "Automatic fast-write"
* In "Auto fast write connection", enter the name of the cloud storage connection to use
* In "Path in connection", enter a relative path to the root of the cloud storage connection, such as "db-tmp". This is a temporary path that will be used in order to put temporary upload files. This should not be a path containing datasets.
* in "Catalog for fast-load", enter the name of a Trino catalog that covers the cloud storage location for the connection you put for "Auto fast write connection". The catalog needs to allow external locations, which implies it is a catalog using the `Hive connector <https://trino.io/docs/current/connector/hive.html>`_. If left empty, DSS will use the same catalog as the target table.

DSS will now automatically use the optimal cloud-to-Trino copy mechanism when executing a recipe that needs to load data "from the outside" into Trino, such as a code recipe.

Note that when running visual recipes directly in-database, this does not apply, as data do not move outside of the database.


Explicit sync from cloud
------------------------

In addition to the automatic fast-write that happens transparently each time a recipe must write into Trino, the Sync recipe also has an explicit "Cloud to Trino" engine. This is faster than automatic fast-write because it does not copy to the temporary location in the cloud storage first.

It will be used automatically if the following constraints are met:

* The source dataset is stored on S3, GCS or Azure Blob Storage
* The destination dataset is stored on Trino

Note that the Trino fast-path may still fail:

* if the catalog of the target dataset is not a Hive catalog in Trino, and "Catalog for fast-load" isn't set on the Trino connection
* if the Trino/Starburst cluster has no actual access to the cloud storage (for example Starburst clusters can only work on one cloud storage at a time)

In that case, the Sync recipe's engine should be forced to DSS and the "automatic fast write" setup on the Trino connection.

Unloading data from Trino to Cloud
=======================================

Unloading data from Trino directly to DSS using JDBC is reasonably fast. However, if you need to unload data from Trino to S3, GCS or Azure Blob Storage, the sync recipe has a "Trino to Cloud" engine that implements a faster path.

In order to use Trino to Cloud sync, the following conditions are required:

* The source dataset must be stored on Trino
* The destination dataset must be stored on Amazon S3, GCS or Azure Blob Storage


Advanced install of the JDBC driver
====================================

.. note::

	This feature is not available on Dataiku Cloud.

The Trino JDBC driver is already preinstalled in DSS and does not usually need to be installed. If you need to customize the JDBC driver, follow these instructions:

The Trino JDBC driver can be downloaded from Maven repositories (such as https://mvnrepository.com/artifact/io.trino/trino-jdbc)

The driver is made of a single JAR file ``trino-jdbc-xxx.jar``

To install:

* Copy this JAR file to the ``lib/jdbc/trino`` subdirectory of the DSS data directory (make it if necessary)
* Restart DSS
* In each Trino connection, switch the driver mode to "User provided" and enter "lib/jdbc/trino" as the Trino driver directory
