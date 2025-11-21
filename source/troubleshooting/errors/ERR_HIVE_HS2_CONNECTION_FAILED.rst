ERR_HIVE_HS2_CONNECTION_FAILED: Failed to establish HiveServer2 connection
##########################################################################

DSS tried to connect to HiveServer2 but couldn't establish the connection.

This error can happen:

* when trying to synchronize the metastore on an HDFS dataset
* when trying to run Hive recipes, or recipes on Hive engine
* when trying to run queries on a Hive SQL notebook
* when trying to import table definitions from the Hive Metastore

This error indicates that the connection could not be established. The message of the error will contain additional information.

Some common reasons for failure to establish the connection are:

* The connection settings (host, port, ...) to the server are invalid
* The HiveServer2 server is not running or not accepting connections
* There is a firewall blocking connection attempts from DSS to HiveServer2

Remediation
===========

.. note::

	This issue can only be fixed by a DSS administrator or a cluster administrator

The first step for solving this issue is to go to the Hive settings screen (Administration > Settings > Hive)

* Refer to the :doc:`documentation on DSS and Hive </hadoop/hive>` in order to get additional information on Hive support by DSS.
* Refer to the :doc:`documentation on SCP/SFTP sources </hadoop/installation>` in order to get additional information on Hive support by DSS.
* Make sure that the connection settings are correct
* If you get "connection refused" or similar errors, check that the Hiveserver2 server is properly running and that the Hive settings in DSS allow for authentication over JDBC.
* Check if a firewall is blocking connections between DSS and the Hiverserver2 server (this can result in either "connection refused" issues, or timeout issues)
