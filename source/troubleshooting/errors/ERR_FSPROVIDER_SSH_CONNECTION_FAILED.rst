ERR_FSPROVIDER_SSH_CONNECTION_FAILED: Failed to establish SSH connection
##########################################################################

DSS tried to connect to a SSH server but couldn't establish the connection.

This error can happen:

* when trying to create a new connection to a SSH source
* when trying to read or write a SCP or SFTP dataset

This error indicates that the connection could not be established. The message of the error will contain additional information.

Some common reasons for failure to establish the connection are:

* The connection settings (host, port, ...) to the server are invalid
* The SSH server is not running or not accepting connections
* There is a firewall blocking connection attempts from DSS to the SSH server
* Credentials entered in DSS for the SSH server are invalid

Remediation
===========

.. note::

	This issue can only be fixed by a DSS administrator

The first step for solving this issue is to go to the settings screen for the affected connection (Administration > Connections). You can test the connection from here.

* Refer to the :doc:`documentation on SCP/SFTP sources </connecting/scp-sftp>` in order to get additional information on SSH support by DSS.
* Make sure that the connection settings are correct
* If you get "connection refused" or similar errors, check that the SSH server is properly running
* Check if a firewall is blocking connections between DSS and the SSH server (this can result in either "connection refused" issues, or timeout issues)
