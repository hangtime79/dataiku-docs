The server selected protocol version TLS10 is not accepted by client preferences [TLS12]
########################################################################################

You may encounter this error or a similar error when attempting to connect to a dataset:

.. code-block:: bash

    Connection failed: The driver could not establish a secure connection to SQL Server by using Secure Sockets Layer (SSL) encryption.     
    Error: "The server selected protocol version TLS10 is not accepted by client preferences [TLS12]". 

This error can occur when connecting to a database that does not have TLS 1.2 enabled. As of April 2021, OpenJDK disabled TLS 1.0 and TLS 1.1 by default. If you recently encountered this error, it might be due to a recent Java upgrade on your database server. 

Note that TLS 1.0 has been `officially deprecated <https://datatracker.ietf.org/doc/rfc8996/>`_ and you can read more about this change and the reasons for it in this `blog post <https://aws.amazon.com/blogs/opensource/tls-1-0-1-1-changes-in-openjdk-and-amazon-corretto/>`_. 

Resolution
----------

In order to resolve this, your database administrator should enable TLS 1.2 on your database server host. See more information on TLS 1.2 support for `SQL Server <https://support.microsoft.com/en-us/topic/kb3135244-tls-1-2-support-for-microsoft-sql-server-e4472ef8-90a9-13c1-e4d8-44aad198cdbe>`_ and `MySQL <https://dev.mysql.com/doc/refman/8.0/en/encrypted-connection-protocols-ciphers.html>`_.

