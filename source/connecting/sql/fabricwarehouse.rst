Microsoft Fabric Warehouse
############################

.. contents::
	:local:

DSS supports the full range of features on Microsoft Fabric Warehouses:

* Reading and writing datasets
* Executing SQL recipes
* Performing visual recipes in-database
* Using live engine for charts

.. note::

	You might want to start with our resources on `data connections <https://knowledge.dataiku.com/latest/data-sourcing/connections/index.html>`_ in the Knowledge Base.

Installing the JDBC driver
===========================

Microsoft Fabric Warehouse uses the Microsoft SQL Server JDBC driver, which can be downloaded from Microsoft website (at time of writing,
from https://learn.microsoft.com/en-us/sql/connect/jdbc/download-microsoft-jdbc-driver-for-sql-server?view=fabric).

Make sure to select a version which is appropriate for your version of Microsoft Fabric Warehouse and your version of Java.
At the time of writing, these constraints are summarized
`here <https://learn.microsoft.com/en-us/sql/connect/jdbc/system-requirements-for-the-jdbc-driver?view=fabric>`_.

* Download the "tar.gz" distribution archive (for Unix)
* Unarchive the downloaded file
* Look into the "enu/jars" subdirectory

The driver is the single JAR file called ``mssql-jdbc-VERSION.jreX.jar`` where X is the corresponding Java version.

* Copy the JAR file to the ``lib/jdbc`` driver of DSS
* Restart DSS

Write into Microsoft Fabric Warehouse
========================================

Loading data into Fabric Warehouses using the regular SQL "INSERT" statements is very inefficient and should only be used for extremely small datasets.

The recommended way to load data into a Fabric Warehouse table is through a bulk COPY from files stored in Azure Blob Storage.

DSS can automatically use this fast load method. For that, you require an Azure Blob Storage connection. Then, in the settings of the Fabric Warehouse connection:

* Enable "Automatic fast-write"
* In "Auto fast write connection", enter the name of the Azure Blob Storage connection to use
* In "Path in connection", enter a relative path to the root of the Azure Blob Storage connection, such as "fabric-warehouse-tmp". This is a temporary path that will be used in order to put temporary upload files. This should not be a path containing datasets.

DSS will now automatically use the optimal "Azure Blob Storage to Synapse Warehouse" copy mechanism when executing a recipe that needs to load data "from the outside" into Fabric Warehouse, such as a code recipe.

Note that when running visual recipes directly in-database, this does not apply, as the data does not move outside of the database.

Explicit sync from Azure Blob Storage
---------------------------------------

In addition to the automatic fast-write that happens transparently each time a recipe must write into Synapse, the Sync recipe also has an explicit "Azure Blob Storage to Synapse Warehouse" engine. This is faster than automatic fast-write because it does not copy to the temporary location in Azure Blob first.

Login using OAuth
======================================

DSS can login using OAuth on Microsoft Fabric Warehouse. OAuth login can be performed either:

* Using a single service account
* Using per-user credentials.

Login as a single service account
---------------------------------

* Make sure that you have at least version 7.2 of the JDBC driver
* Create a new App (Azure Portal  > Azure Active Directory > App registrations). DSS will connect with the identity of this app
* In the Overview tab, note the `Application (client) ID`
* In the Overview tab, note the `Directory (tenant) ID` and use it to replace the {tenanId} in the templates for the `OAuth2 Authorization endpoint` and `OAuth2 Token endpoint` fields
* Go to API permissions, Add a permission, APIs my organization uses
* Search for  ``Azure SQL`` and add the ``Azure SQL Database`` permission, Delegated permissions, user_impersonation
* Search for  ``Azure Storage`` and add the ``Azure Storage`` permission, Delegated permissions, user_impersonation
* Search for  ``Microsoft Graph`` and add the ``Microsoft Graph`` permission, Delegated permissions, User.Read
* Create a client secret for this application (App registration > Certificates & Secrets), note the client secret
* Create a new Microsoft Fabric Warehouse connection
* From the Fabric Warehouse parameters in the ``About`` section retrieve the value of the ``SQL connection string`` and use it to fill the `host`` field
* Client id is the application id
* Client secret is the one you created earlier



Login with per-user OAuth tokens
---------------------------------

* Make sure that you have at least version 7.2 of the JDBC driver
* Create a new App (Azure Portal  > Azure Active Directory > App registrations). DSS will connect with the identity of this app
* In the Overview tab, note the `Application (client) ID`
* In the Overview tab, note the `Directory (tenant) ID` and use it to replace the {tenanId} in the templates for the `OAuth2 Authorization endpoint` and `OAuth2 Token endpoint` fields
* Go to API permissions, Add a permission, APIs my organization uses
* Search for  ``Azure SQL`` and add the ``Azure SQL Database`` permission, Delegated permissions, user_impersonation
* Search for  ``Azure Storage`` and add the ``Azure Storage`` permission, Delegated permissions, user_impersonation
* Search for  ``Microsoft Graph`` and add the ``Microsoft Graph`` permission, Delegated permissions, User.Read
* Go to Authentication,  click on `Add a platform`, select `Web`, in the redirect URIs field enter ``http://{dss_instance_domain}/dip/api/oauth2-callback`` and click on configure
* Create a new Microsoft Fabric Warehouse connection
* From the Fabric Warehouse parameters in the ``About`` section retrieve the value of the ``SQL connection string`` and use it to fill the `host`` field
* Set "Credentials mode" to "Per user"
* Client id is the application id
* Create the connection (you can't test it yet)

Then for each user:

* Go the the Fabric Workspace dashboard, click `Manage access` and add the user and grant them at least `Contributor` permissions
* In DSS, go to user profile > connection credentials
* Click the "Edit" button next to the new connection name
* Follow the instructions that appear

Important: the account you log with must be a "Member" on the Entra ID directory. A "guest" account cannot login
