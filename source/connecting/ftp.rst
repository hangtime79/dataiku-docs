FTP
#####################

Data Science Studio can use FTP servers to:

* Read and write datasets
* Read and write managed folders

.. note::

  You can use the DSS :doc:`/other_recipes/download` to cache the contents from a FTP server.

  This can provide better performance if you need to read FTP files a lot of time,
  and don't mind the copy of the data which is made into a DSS managed folder.

  By default, the download recipe will still check the FTP server for updates when its
  output folder is rebuilt. This behavior can be disabled.

Creating a FTP connection
==========================

.. note::

  Creating FTP connections can only be done by DSS administrators (except if you use "personal connections")

Interactive with a FTP server first requires the definition of a connection to the remote server, as follows:

* Go to Administration > Connections
* Click the "New connection" button and select FTP
* Enter a name for the new connection, and the required connection parameters
* Save the new connection

FTP connection parameters
-------------------------

+------------------+---------------------------------------------------------------------+
|       Name       |                             Description                             |
+==================+=====================================================================+
| Host             | Host name or IP address of the FTP server to access (Mandatory)     |
+------------------+---------------------------------------------------------------------+
| User             | FTP username to use, or empty for an anonymous FTP connection       |
+------------------+---------------------------------------------------------------------+
| Password         | FTP password to use, or empty for an anonymous FTP connection       |
+------------------+---------------------------------------------------------------------+
| Use passive mode | Check to use FTP "passive" data transfer mode (default).            |
|                  | Using FTP passive mode is often mandatory when there is a           |
|                  | firewall between the Data Science Studio server and the FTP server. |
+------------------+---------------------------------------------------------------------+
| Path             | Path to the remote folder to use once connected to the FTP server.  |
|                  | Start with a ``/`` to specify an absolute path, without ``/`` the   |
|                  | path will be relative to the startup directory.                     |
+------------------+---------------------------------------------------------------------+
| Writable         | Check to allow DSS to write datasets on this server.                |
|                  | Those datasets will be written in a subfolder or the ``path`` (or   |
|                  | the startup directory if ``path`` is empty) bearing the name of the |
|                  | dataset.                                                            |
+------------------+---------------------------------------------------------------------+
| Allow managed    | Check to allow DSS to write                                         |
| datasets         | :ref:`managed datasets <managed-datasets>` on this server.          |
|                  | Requires ``Writable``.                                              |
+------------------+---------------------------------------------------------------------+
| Allow managed    | Check to allow DSS to write                                         |
| folders          | managed folders on this server.                                     |
|                  | Requires ``Writable``.                                              |
+------------------+---------------------------------------------------------------------+
| Use global proxy | When checked, use the :ref:`global proxy <proxy>` for this          |
|                  | connection. Uncheck this if the FTP server is directly accessible.  |
|                  | If you have an HTTP proxy, passive mode is mandatory.               |
+------------------+---------------------------------------------------------------------+

Creating FTP datasets
========================

After setting up a FTP connection, simply add a new
dataset to your project, choosing the "FTP" type. Select your FTP
connection.

If necessary, specify a path (subpath of the connection's path if it is not
empty) or click "Browse" and select a file or directory.

If the final path a directory, the data is the union of all the data in all the
files in that directory (including sub-directories). The preview displayed in the dataset creation screen will
only present data from the first non-empty file.

Use the FTP dataset for writing
===============================

Two cases are supported:

1. In a folder:
    - the data will be written in possibly multiple files
    - the content of the folder is wiped before writing
    - writing a :ref:`managed dataset <managed-datasets>` requires a directory
2. In a file:
    - you must create the file beforehand (it may be empty)
    - the file is emptied before writing
