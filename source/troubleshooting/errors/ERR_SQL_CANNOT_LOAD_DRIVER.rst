ERR_SQL_CANNOT_LOAD_DRIVER: Failed to load database driver
############################################################

To connect to SQL databases, DSS uses a small piece of code called a JDBC driver.

Each database kind (MySQL, PostgreSQL, Oracle, SQLServer, ...) needs its own specific JDBC driver. JDBC drivers are provided by your database's vendor, and must be installed in DSS.

This error can happen:

* when trying to create a new connection to a SQL database
* when trying to read or write a SQL dataset
* when trying to use a SQL notebook

This error indicates that the JDBC driver for this specific type of database is not found or not properly installed.

If the issue is encountered in a containerized job, you might need to rebuild the :doc:`containerized dss engine image </containers/containerized-dss-engine>`.

Remediation
===========

.. note::

	This issue can only be fixed by a DSS administrator

* Refer to the :doc:`documentation on JDBC drivers </installation/custom/jdbc>` in order to know how to install JDBC drivers.
* Make sure that you restarted DSS after installing the JDBC driver
* If none of these helps, the error message may contain additional details.
* Refer to the documentation of your JDBC driver which may contain specific installation instructions
* Some JDBC drivers need several JAR files, make sure you have installed all of them, as indicated by the documentation of your JDBC driver