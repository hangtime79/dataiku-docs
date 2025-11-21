Azure Synapse
##############

.. note::

	You might want to start with our resources on `data connections <https://knowledge.dataiku.com/latest/data-sourcing/connections/index.html>`_ in the Knowledge Base.

.. contents::
	:local:

DSS has native support for Microsoft Azure Synapse Dedicated SQL Pools (formerly known as Azure SQL Data Warehouse)

DSS supports the full range of features on Microsoft Azure Synapse

* Reading and writing datasets
* Executing SQL recipes
* Performing visual recipes in-database
* Using live engine for charts

Installing the JDBC driver
===========================

Azure Synapse uses the Microsoft SQL Server JDBC driver, which can be downloaded from Microsoft website (at time of writing,
from https://docs.microsoft.com/en-us/sql/connect/jdbc/download-microsoft-jdbc-driver-for-sql-server).

Make sure to select a version which is appropriate for your version of SQL Server and your version of Java.
At the time of writing, these constraints are summarized
`here <https://docs.microsoft.com/en-us/sql/connect/jdbc/system-requirements-for-the-jdbc-driver>`_.

* Download the "tar.gz" distribution archive (for Unix)
* Unarchive the downloaded file
* Look into the "enu/jars" subdirectory

The driver is the single JAR file called ``mssql-jdbc-VERSION.jreX.jar`` where X is the corresponding Java version.

* Copy the JAR file to the ``lib/jdbc`` driver of DSS
* Restart DSS

Write into Azure Synapse
=========================

Loading data into Synapse using the regular SQL "INSERT" statements is very inefficient and should only be used for extremely small datasets.

The recommended way to load data into a Synapse table is through a bulk COPY from files stored in Azure Blob Storage.

DSS can automatically use this fast load method. For that, you require an Azure Blob Storage connection. Then, in the settings of the Synapse connection:

* Enable "Automatic fast-write"
* In "Auto fast write connection", enter the name of the Azure Blob Storage connection to use
* In "Path in connection", enter a relative path to the root of the Azure Blob Storage connection, such as "synapse-tmp". This is a temporary path that will be used in order to put temporary upload files. This should not be a path containing datasets.

DSS will now automatically use the optimal Azure-Blob-to-synapse copy mechanism when executing a recipe that needs to load data "from the outside" into Synapse, such as a code recipe.

Note that when running visual recipes directly in-database, this does not apply, as the data does not move outside of the database.

Explicit sync from Azure Blob Storage
---------------------------------------

In addition to the automatic fast-write that happens transparently each time a recipe must write into Synapse, the Sync recipe also has an explicit "Azure Blob to Synapse" engine. This is faster than automatic fast-write because it does not copy to the temporary location in Azure Blob first.

Unload data from Synapse to Azure Blob
=======================================

Unloading data from Synapse directly to DSS using JDBC is reasonably fast. However, if you need to unload data from Synapse to Azure Blob, the sync recipe has a "Synapse to Azure Blob" engine that implements a faster path.

In order to use Synapse to Azure Blob sync, the following conditions are required:

* The source dataset must be stored on Azure Synapse
* The destination dataset must be stored on Azure Blob
* The Azure Blob bucket and the Synapse cluster must be in the same Azure region

The schema of the input dataset must match the schema of the output dataset, and values stored in fields must be valid with respect to the declared Synapse column type

Login using OAuth
======================================

DSS can login using OAuth on Azure Synapse. OAuth login can be performed either:

* Using a single service account
* Using per-user credentials. In the latter case, each user must grant DSS permission to access the database on his behalf.

Login as a single account
--------------------------

* Make sure that you have at least version 7.2 of the JDBC driver
* Create a new App (Azure Portal  > Azure Active Directory > App registrations). DSS will connect with the identity of this app
* In the Overview tab, note the `Application (client) ID`
* In the Overview tab, click `Endpoints` and note the ``OAuth 2.0 token endpoint (v1)`` URL
* Create a client secret for this application (App registration > Certificates & Secrets), note the client secret
* Add this app as a user in the Azure SQL Server database (see below)
* Create a new SQLServer connection
* Fill the "Host" and "Database" fields with the SQL Server host and database name
* Enable "Login with Azure OAuth"
* The STS URL is the ``OAuth 2.0 token endpoint (v1)`` URL
* Client id is the application id
* Client secret is the one you created earlier

.. note::

	How to add the app as a user in the Azure SQL Server database

	Before DSS can login as an app, this app must be registered as a valid user in the Azure SQL server database. This is done by entering the SQL command `CREATE USER [appName] FROM EXTERNAL PROVIDER` while connected as an administrator to the database.

	This is technically independent from DSS, but it can be practical to do it from DSS. The difficulty is that in order to perform this command, you must be logged in as an AD user on the database.

	The following procedure is provided as a best-effort help:

	* First, make sure that you have setup a AAD user as administrator of this database. Follow instructions here: https://docs.microsoft.com/en-us/azure/sql-database/sql-database-aad-authentication-configure

	* Create a new temporary SQL Server connection in DSS

		* Fill the "Host" and "Database" fields with the SQL Server host and database name
		* Enter the AD login/password of the AD admin user
		* Add a new JDBC property with key `authentication` and password `ActiveDirectoryPassword`
		* Create the connection

	* Create a new SQL notebook on this connection

	* Run the command `CREATE USER [appName] FROM EXTERNAL PROVIDER` with "appName" the name of the app you created previously

	* Delete the SQL Server connection (from now on, you'll be logging as the app instead)



Login with per-user OAuth tokens
---------------------------------

* Make sure that you have at least version 7.2 of the JDBC driver
* Create a new App (Azure Portal  > Azure Active Directory > App registrations). DSS will connect with the identity of this app
* In the Overview tab, note the `Application (client) ID`
* In the Overview tab, click `Endpoints` and note the ``OAuth 2.0 token endpoint (v1)`` URL
* Go to API permissions, Add a permission, APIs my organization uses
* Search for  ``Azure SQL`` and add the ``Azure SQL Database`` permission, Delegated permissions, user_impersonation
* Go to Authentication, and set "Default client type" > "Treat as a public client" to "Yes". Check the "login.microsoftonline.com" URL in the "Suggested Redirect URIs" section. Save your changes.
* Create a new SQLServer connection
* Fill the "Host" and "Database" fields with the SQL Server host and database name
* Set "Credentials mode" to "Per user"
* Enable "Login with Azure OAuth"
* The STS URL is the ``OAuth 2.0 token endpoint (v1)`` URL
* Client id is the application id
* Create the connection (you can't test it yet)

Then for each user:

* Go to user profile > connection credentials
* Click the "Edit" button next to the new connection name
* Follow the instructions that appear

Important: the account you log with must be a "Member" on the AAD directory. A "guest" account cannot login


Common errors
---------------

* Problem: when clicking on "Continue" in the OAuth setup modal, the user gets ``AADSTS70016: Pending end-user authorization.``
* Solution: the user has not completed the devicelogin registration

.

* Problem: When the user goes to the devicelogin page, he gets ``AADSTS500113: No reply address is registered for the application.``
* Solution: You have not checked the "login.microsoftonline.com" URL in the "Suggested Redirect URIs" section.

.

* Problem: You were able to authenticate the end-user, but connection fails with ``SQLServerException: Azure Active Directory is only supported on Windows operating systems.``
* Solution: Your driver is too old; Upgrade to 7.2 or higher

.

* Problem: You were able to authenticate the end-user, but connection fails with ``SQLServerException: Login failed for user 'NT AUTHORITY\ANONYMOUS LOGON'.``
* Solution: the user account is a "Guest" on the AAD. Only "Members" are acceptable
