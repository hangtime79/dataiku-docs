Connections security
#########################

.. contents::
    :depth: 2
    :local:

Securing access to connections
===============================

It is possible to restrict access to connections. If access to a DSS connection is restricted, only members of selected groups may "freely use" this connection.

This can be configured in the settings of each individual connection.

"Freely using" a connection means being able to:

* Create new datasets on the connection
* Modify the settings of a dataset using the connection
* Browse in any way the connection
* Send code (like SQL) which may be used indirectly to browse in any way the connection.

Note that this does NOT restrict the ability to read datasets which have already been defined on a connection.

For example, with a SQL database, you may want a few people to be able to create datasets based on specific tables of the connection, and then have a larger group of analysts using this data, but who are  not allowed to read other tables in this database.

In that configuration, you would have the small group being granted the "freely use" permission on the database connection, create the datasets in a project, and grant read/write access to the project to the larger group. The analysts are able to read the data, but cannot access other tables from the database in any way.

Note that access to a connection can only be granted to a group. Thus, it cannot be granted to a non-personal API key (since these API keys do not belong to groups). In order to access connections (using the rules described above) with an API key, you will need to use either:

* An admin API key
* Or a personal API key

.. _connections.read-details:

Reading details of a connection
================================

By default, even if a user may "freely use" a connection, he may not read the details of the connection.

The details of the connection include:

* The path (for filesystem-connection)
* The HDFS properties (for HDFS connections)
* The hostname / database / ... (for SQL connections)
* The credentials (for all connections which include a credential)

In the settings page of the connection, an administrator may grant the right to some groups to read the details of a connection. The details can only be read using code, as no part in the UI will show it.

.. note::

	Granting "Details readable by" on a connection to a group gives users access to the unencrypted credential for this connection. Make sure that you wish this.

	Beware that for Hadoop filesystem datasets that actually point to S3, WASB, ..., the details of the HDFS connection usually contain a secret credential in order to connect to the cloud storage.

.. note::

	Granting "Details readable by" on HDFS and S3 connections is strongly recommended in order to obtain good performance in Spark.
	If Spark processes do not have the "Details readable by" permission, they are forced into a slow path that very strongly degrades performance of Spark jobs.

	For more information, see :doc:`/spark/datasets`

Note that access to a connection can only be granted to a group. Thus, it cannot be granted to a non-personal API key (since these API keys do not belong to groups). In order to access connections (using the rules described above) with an API key, you will need to use either:

* An admin API key
* Or a personal API key


Per-user credentials for connections
======================================

.. note::

	While this feature is distinct from the User Isolation Framework feature, it is only available for DSS licenses where the User Isolation Framework is enabled.

For DSS connections which require credentials (most SQL connections, MongoDB, FTP, ...), the administrator can configure the connection so that instead of having a global service credential, each user can enter his personal credentials. Each action on the database performed by this user will use his personal credential.

To configure a connection with per-user credentials:

* Go to Administration > Connections and select the connection
* In "Connections credentials", select "Per-user"
* Save the connection

Users can then enter their personal credentials by going to their Profile > Credentials.

Note that in this mode, there is no global credential at all anymore. Thus, it is not possible to test a connection immediately, because no credentials available. The proper initialization sequence for a new connection is thus:

* The admin enters connection details, but no credentials, and enables per-user credentials
* The admin saves the new connection
* The admin goes to his profile and enters his credentials
* The admin can then go back to the connection's page and test the connection

User credentials are stored encrypted. Please see :doc:`passwords-security` for more details.

Personal connections
=====================

You can grant to user groups the permission to create their own connections. Connections are normally only created by the DSS administrator. By granting this "personal connection" permission, end users can create their own connections.

This feature is only available for connections for which a credential is required (most SQL connections, MongoDB, FTP, ...).
