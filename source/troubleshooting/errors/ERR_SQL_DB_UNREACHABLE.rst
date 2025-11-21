ERR_SQL_DB_UNREACHABLE: Failed to reach database
##################################################

DSS tried to connect to a SQL database but couldn't establish the connection.

This error can happen:

* when trying to create a new connection to a SQL database
* when trying to read or write a SQL dataset
* when trying to use a SQL notebook

This error indicates that the connection could not be established. The message of the error will contain additional information.

Some common reasons for failure to establish the connection are:

* The connection settings (host, port, ...) to the database are invalid
* The database server is not running or not accepting connections
* There is a firewall blocking connection attempts from DSS to the database server
* Credentials entered in DSS for the database server are invalid

Remediation
===========

.. note::

	This issue can only be fixed by a DSS administrator

The first step for solving this issue is to go to the settings screen for the affected connection (Administration > Connections). You can test connection from here.

* Refer to the :doc:`documentation on SQL databases </connecting/sql/index>` in order to get additional information on the support of your specific database by DSS.
* Make sure that the connection settings are correct
* If you get "connection refused" or similar errors, check that the database server is properly running
* Check if a firewall is blocking connections between DSS and the database server (this can result in either "connection refused" issues, or timeout issues)
