Microsoft SQL Server
######################

.. contents::
	:local:

DSS supports the full range of features on Microsoft SQL Server:

* Reading and writing datasets
* Executing SQL recipes
* Performing visual recipes in-database
* Using live engine for charts

SQL Server on Google Cloud SQL is also supported.

Installing the JDBC driver
===========================

The SQL Server JDBC driver can be downloaded from Microsoft website (at time of writing,
from https://docs.microsoft.com/en-us/sql/connect/jdbc/download-microsoft-jdbc-driver-for-sql-server).

Make sure to select a version which is appropriate for your version of SQL Server and your version of Java.
At the time of writing, these constraints are summarized
`here <https://docs.microsoft.com/en-us/sql/connect/jdbc/system-requirements-for-the-jdbc-driver>`_.

* Download the "tar.gz" distribution archive (for Unix)
* Unarchive the downloaded file
* Look into the "enu/jars" subdirectory

The driver is the single JAR file called ``mssql-jdbc-VERSION.jreX.jar`` where X is the corresponding Java version.

* Install the JAR file in DSS as explained in :doc:`Custom Dataiku instructions </installation/custom/jdbc>` or :doc:`Dataiku Cloud Stacks for AWS instructions </installation/cloudstacks-aws/templates-actions>`
* Restart DSS

Requirements
============

* Dataiku does not require any specific SQL Server version, and is not known to have any incompatibility with any SQL Server version
* The "SHOWPLAN" permission is required

Azure SQL Data Warehouse / Synapse support
===========================================

Support for Azure Synapse dedicated pools (formerly known as Azure SQL Data Warehouse) is now handled by a dedicated connection. For more details, please see :doc:`synapse`

Kerberos authentication
=========================

.. note::

	This feature is not available on Dataiku Cloud.

In default connection mode, DSS authenticates to SQL Server by way of a username and password defined in the connection
configuration page.

Alternatively, it is possible for DSS to connect to the database with Kerberos authentication, provided a number of
prerequisites are met:

* Kerberos authentication should be enabled on the SQL Server

* The Kerberos client configuration file (typically ``/etc/krb5.conf``) should be correctly configured on the DSS host.

* Create a Kerberos account for DSS on the KDC (or domain controller) and note the Kerberos principal for it,
  say ``DSSKerberosPrincipal@KERBEROS.REALM``.

* Create a keytab file for this account, and store it in a file accessible only to DSS.

* At the DSS level, configure the SQL Server connection as follows:

	* Login with Kerberos: enabled

	* Principal: the Kerberos principal created above

	* Keytab: absolute path to the keytab file for this Kerberos principal

	* Advanced JDBC properties: add any SQLServer-specific advanced connection properties required by your database setup.
	  This would typically be:

	  .. code-block:: sh

	  	integratedSecurity : true
	  	authenticationScheme : JavaKerberos
	  	# the following is needed only if the database server service principal name (SPN)
	  	# is different from the default : MSSQLSvc/FQDN:PORT@KERBEROS.REALM
	  	serverSpn : SERVER_SPN

User impersonation with Kerberos
==================================

.. note::

	While this feature is distinct from the User Isolation Framework feature, it is only available for DSS licenses that enable the User Isolation Framework.

	This feature requires the database server to be integrated with a Windows Active Directory domain controller.

It is possible to configure DSS to authenticate to the database using one database account,
and perform all data manipulation and SQL queries using another. This typically allows DSS to impersonate its end-users
when accessing the database, much as is done for Hadoop or local computations when running in User Isolation Framework mode.

At the DSS level, this is configured by entering the database account name to impersonate in the ``Impersonated user``
field of the connection configuration page.

Typical uses of this feature would include:

* defining this field as ``%{dssUserLogin}`` to directly use the DSS user login name as SQLServer account name,
  in case the DSS and SQLServer account databases match one-for-one

* defining this field as ``%{adminProperty:sqlServerLogin}`` where ``sqlServerLogin`` is a custom per-user admin property
  defined in the DSS user database, in the more general case where usernames have to be remapped

This impersonation mechanism uses the Active Directory "constrained delegation" feature, and should have been
authorized accordingly by the domain administrator. This is typically done as follows (refer to Microsoft documentation
for details):

* Add a Service Principal Name to the Active Directory service account used by DSS.
  This is typically done with ``setspn``, or directly with the ``ktpass`` command when creating the Kerberos keytab for DSS

* In the "Active Directory Users and Computers" tool, open the DSS service account entry, and select the "Delegation" tab
  (this tab is only visible for accounts which have a SPN set).

* Check "Trust this user for delegation to specified services only"

* Check "Use any authentication protocol"

* Locate or search for the SQL server service entry, and allow the DSS account to delegate to it.


Login using OAuth on Azure SQL Server
======================================

DSS can login using OAuth on Azure SQL Server. OAuth login can be performed either:

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
