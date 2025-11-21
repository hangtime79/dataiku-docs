Databricks
###########

.. contents::
	:local:

.. note::

	You might want to start with our resources on `data connections <https://knowledge.dataiku.com/latest/data-sourcing/connections/index.html>`_ in the Knowledge Base.

DSS supports the full range of features on Databricks:

* Reading and writing datasets
* Executing SQL recipes
* Performing visual recipes in-database
* Using live engine for charts

Connection setup (Dataiku Cloud Stacks or Dataiku Custom)
===========================================================

The Databricks JDBC driver is already preinstalled in DSS and does not need to be installed

* Fill in the settings of the connection using your Databricks information.
* (Optional but recommended) Fill auto-fast-write settings - see :ref:`connecting-sql-databricks-writing`

To set up the connection with per-user credentials
--------------------------------------------------
* You have to create your connection by entering existing settings,
* Then each user will have to fill in their credentials individually.
* Also, note that therefore the connection can not be tested from the launchpad with this setup.

After the Space Admin has completed this first step in the launchpad, each user needs to do the following in their DSS:

* Go to Dataiku DSS
* Go to User (image icon top right) > Profile and settings (gear icon) > Credentials
* Click the “Edit” button next to the new connection name
* Follow the instructions that appear
* You can now test the connection

Authenticate using OAuth2
==========================

DSS can authenticate to Azure or AWS Databricks using OAuth2.

OAuth2 access is performed either using "per-user" credentials, or using "global" client credentials.

With per-user credentials
--------------------------

Each user must grant DSS permission to access Databricks on their behalf.
Databricks SQL warehouses are configured with OAuth 2.0 authentication.

Setting up OAuth for a Databricks connection requires several steps.

You first need to configure an OAuth App in Databricks.

* Create an App connection in Manage Account > Settings > App connection.
* Note the client id and client secret that appear on this connection creation.

Then, create a new Databricks connection

* Fill in the basic params (Host, Port, HTTP path) as usual
* Select "OAuth" as the "Auth Type".
* Select "Per-user"
* Fill the "Client id", "Client secret" with the ones generated from your OAuth app
* Fill the "OAuth authorization endpoint"

  * for Azure ,  ``https://accounts.azuredatabricks.net/oidc/accounts/<account id>/v1/authorize``
  * for AWS ,  ``https://accounts.cloud.databricks.com/oidc/accounts/<account id>/v1/authorize``
* Fill the "OAuth token endpoint"

  * for Azure ,  ``https://accounts.azuredatabricks.net/oidc/accounts/<account id>/v1/token``
  * for AWS ,  ``https://accounts.cloud.databricks.com/oidc/accounts/<account id>/v1/token``
* Fill the "Scope" with ``sql+offline_access``
* Create the connection
* Test the connection. An error will appear, requiring you to connect your Databricks account to Dataiku DSS.
* Click "Connect your Account" and follow the instructions that appear
* This stores a refresh token for your user. Note that Dataiku does not display the time at which the refresh token was obtained
* The connection is now usable


.. note::

    You may use workspace-level access endpoints if it better suits your needs
        ``https://<databricks-instance>/oidc/v1/authorize``
        ``https://<databricks-instance>/oidc/v1/token``


With global credentials
------------------------

In Databricks, create the following objects (see https://docs.databricks.com/en/dev-tools/auth/oauth-m2m.html for more details)

* Create a service principal (in Manage Account > User Management > Service Principal)
* Create an OAuth secret in this service
* In Workspaces, give the permissions to this service principal

Then, create a new Databricks connection

* Fill in the basic params (Host, Port, HTTP path) as usual
* Select "OAuth" as the "Auth Type".
* Select "Global"
* Fill the "Client id", "Client secret" with the OAuth secret ones you just have created
* Fill the "OAuth token endpoint"

  * for Azure ,  ``https://accounts.azuredatabricks.net/oidc/accounts/<account id>/v1/token``
  * for AWS ,  ``https://accounts.cloud.databricks.com/oidc/accounts/<account id>/v1/token``
* Fill the "Scope" with ``sql``
* Create the connection

.. note::

    You may use workspace-level access endpoints if it better suits your needs
        ``https://<databricks-instance>/oidc/v1/token``

.. _connecting-sql-databricks-writing:


Access to Databricks Volumes
============================

A Databricks connection in DSS can be used to access tables by means of SQL, but also `Volumes <https://docs.databricks.com/en/volumes/index.html>`_ . In order to make it possible to use a Databricks Volume in DSS:

- create or use a Databricks connection whose credentials correspond to a user with read/write access to the Databricks Volume in the Unity catalog
- ensure ``allow write`` is enabled on the Databricks connection
- ensure ``allow managed folders`` is enabled on the Databricks connection
- put the name of the Databricks volume in the ``Volume for managed folders`` field. It is recommended to fill the ``Managed data subpath`` field as well, so that managed folders are not created at the root of the volume.

You can then create managed folders on the Databricks connection in your flow, and read/write to them

.. note:: 

    The Databricks Volume SDK puts size limits on uploads and downloads, so these managed folders cannot be used to store files of arbitrary size.


Writing data into Databricks
============================

Loading data into a Databricks database using the regular SQL ``INSERT`` or ``COPY`` statements is inefficient and should only be used for extremely small datasets.

The recommended way to load data into a Databricks table is through a bulk COPY from files stored in Amazon S3 or Azure Blob Storage (depending on the cloud your Databricks is running on).

DSS can automatically use this fast load method. For that, you need a Cloud storage connection (S3 or Azure Blob connection) or a Databricks connection on which managed folders in a Databricks Volume are possible. Then, in the settings of the Databricks connection:

* Enable "Automatic fast-write"
* In "Auto fast write connection", enter the name of the cloud storage connection or databricks connection to use. Note that a Databricks connection can use itself as a fast path, as long as it has the settings for a Databricks Volume
* In "Path in connection", enter a relative path to the root of the cloud storage connection, such as "db-tmp". This is a temporary path that will be used in order to put temporary upload files. This should not be a path containing datasets.

DSS will now automatically use the optimal cloud-to-Databricks copy mechanism when executing a recipe that needs to load data "from the outside" into Databricks, such as a code recipe.

Note that when running visual recipes directly in-database, this does not apply, as data do not move outside of the database.

Requirements on the cloud storage connection
----------------------------------------------

* For Azure Blob

	* You must `generate a SAS Token <https://docs.databricks.com/storage/azure-storage.html#connect-to-azure-data-lake-storage-gen2-or-blob-storage-using-azure-credentials>`_, then save the token in the Azure Blob Storage connection settings in the "SAS Token" field.

Explicit sync from cloud
------------------------

In addition to the automatic fast-write that happens transparently each time a recipe must write into Databricks, the Sync recipe also has an explicit "Cloud to Databricks" engine. This is faster than automatic fast-write because it does not copy to the temporary location in the cloud storage first.

It will be used automatically if the following constraints are met:

* The source dataset is stored on S3 or Azure Blob Storage
* The destination dataset is stored on Databricks

Unloading data from Databricks to Cloud
=======================================

Unloading data from Databricks directly to DSS using JDBC is reasonably fast. However, if you need to unload data from Databricks to S3 or Azure Blob Storage, the sync recipe has a "Databricks to Cloud" engine that implements a faster path.

In order to use Databricks to Cloud sync, the following conditions are required:

* The source dataset must be stored on Databricks
* The destination dataset must be stored on Amazon S3 or Azure Blob Storage


Databricks Connect integration
=================================

Dataiku can leverage the Databricks Connect package in order to read Dataiku datasets stored in Databricks, build queries using DataFrames and then write the result back to a Databricks dataset.

The Databricks Connect integration can be used in Python code recipes and in Jupyter notebooks.

In order to use it, you will need:

  * A Databricks cluster with a runtime in version at least 13.0
  * A Databricks connection with Security option "Details readable by" set to Every analyst or Selected groups.
  * A Dataiku Code Env based on Python 3.10, with the package requirement "databricks-connect==13.0.*" (or more recent), and built.


If you have Databricks datasets pointing to some tables in Databricks, then you can get a DataFrame representing the underlying Databricks table. From there, you can use the full Databricks Connect API with the DataFrame.

.. code-block:: python

	# get handle to interact via databricks-connect
	from dataiku.dbconnect import DkuDBConnect
	dbc = DkuDBConnect()
	# get the DSS dataset handle
	import dataiku
	input_ds = dataiku.Dataset("the_input_dataset_name")
	# get the data from the table that the dataset points to
	df = dbc.get_dataframe(input_ds)
	df.show(5)

Likewise, to save a DataFrame into a dataset backed by a Databricks table, you can run:

.. code-block:: python

	# get handle to interact via databricks-connect
	from dataiku.dbconnect import DkuDBConnect
	dbc = DkuDBConnect()
	# get the data from some dataset
	import dataiku
	input_ds = dataiku.Dataset("the_input_dataset_name")
	df = dbc.get_dataframe(input_ds)
	# perform a simple aggregation on the table
	counts = df.groupBy('some_column_name').count()
	# and save back the aggregates to a dataset
	output_ds = dataiku.Dataset("the_output_dataset_name")
	dbc.write_with_schema(output_ds, counts)


If you want to go further, you can retrieve and directly use a session. Databricks Connect works by creating a handle
on a Databricks cluster, called a session. DSS will create a session based on the credentials of a connection, which
you can pass explicitly by name, or implicitly by passing a dataset from which DSS will grab a connection name.

.. code-block:: python

	# Getting a session from a connection directly
	from dataiku.dbconnect import DkuDBConnect
	dbc = DkuDBConnect()
	session = dbc.get_session('the_connection_name')

Once the session is created, it can be used to run SQL commands against the cluster.

.. code-block:: python

	session.sql("show databases").show()


The `sql()` function actually produces a PySpark DataFrame, on which the usual PySpark functions can be applied.


.. code-block:: python

	# get the data from some table
	df = session.sql("select * from some_catalog.some_schema.some_table_name")
	# perform a simple aggregation on the table
	counts = df.groupBy('some_column_name').count()
	# and show the results
	counts.show()


Since the session is a PySpark handle, you can access tables in Databricks with `read.table()`.

.. code-block:: python

	# get the data from some table with SQL...
	df = session.sql("select * from some_catalog.some_schema.some_table_name")
	# ... or directly
	df = session.read.table("some_table_name")


And you can save a DataFrame into a Databricks table using `saveAsTable()`.

.. code-block:: python

	# get the data from some table
	df = session.read.table("some_table_name")
	# perform a simple aggregation on the table
	counts = df.groupBy('some_column_name').count()
	# and save back the aggregates
	counts.write.saveAsTable("some_databricks_table_name")


Advanced install of the JDBC driver
====================================

.. note::

	This feature is not available on Dataiku Cloud.

The Databricks JDBC driver is already preinstalled in DSS and does not usually need to be installed. If you need to customize the JDBC driver, follow these instructions:

The Databricks JDBC driver can be downloaded from Databricks website (https://docs.databricks.com/integrations/jdbc-odbc-bi.html#download-the-databricks-jdbc-driver)

The driver is made of a single JAR file ``DatabricksJDBC42.jar``

To install:

* Copy this JAR file to the ``lib/jdbc/databricks`` subdirectory of the DSS data directory (make it if necessary)
* Restart DSS
* In each Databricks connection, switch the driver mode to "User provided" and enter "lib/jdbc/databricks" as the Databricks driver directory
