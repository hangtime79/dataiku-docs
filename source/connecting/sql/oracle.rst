Oracle
#######

.. note::

	You might want to start with our resources on `data connections <https://knowledge.dataiku.com/latest/data-sourcing/connections/index.html>`_ in the Knowledge Base.

DSS supports the full range of features on Oracle and Exadata:

* Reading and writing datasets
* Executing SQL recipes
* Performing visual recipes in-database
* Using live engine for charts

Installing the JDBC driver
===========================

The Oracle JDBC driver can be downloaded from `Oracle website <https://www.oracle.com/database/technologies/appdev/jdbc-downloads.html>`_.

* Look for the latest JDBC driver which supports your database version.
* Download the ``ojdbcX.jar`` file (you'll need to accept the license agreement first, you may need to create an account)

  The driver is a single JAR file called ``ojdbcX.jar`` where 'X' is the minimum supported Java release. Make sure to use a version compatible with the version of Java used by DSS (for instance at the time of writing, ``ojdbc8.jar`` is compatible with Java 8 and Java 11, ``ojdbc11.jar`` is compatible with Java 11 to 21).

* Install the JAR file in DSS as explained in :doc:`Custom Dataiku instructions </installation/custom/jdbc>` or :doc:`Dataiku Cloud Stacks for AWS instructions </installation/cloudstacks-aws/templates-actions>`
* Restart DSS

Advanced connection properties
==============================

Connect using Service Name 
---------------------------

The Oracle connection expects an Oracle SID in the "Service name" parameter. If you need to connect with a true Service name, you can connect by toggling the "Use custom JDBC URL" parameter *on* and using the following Connection URL format: 

.. code-block:: bash

    jdbc:oracle:thin:@//[HOST][:PORT]/SERVICE_NAME


Kerberos authentication
-----------------------

.. note::

	This feature is not available on Dataiku Cloud.

In default connection mode, DSS authenticates to Oracle by way of a username and password defined in the connection
configuration page.

Alternatively, it is possible for DSS to connect to the database with Kerberos authentication, provided a number of
prerequisites are met:

* Kerberos 5 authentication should be enabled on the database.

* The Kerberos client configuration file (typically ``/etc/krb5.conf``) should be correctly configured on the DSS host.

* Create a Kerberos account for DSS on the KDC (or domain controller) and note the Kerberos principal for it,
  say ``DSSKerberosPrincipal@KERBEROS.REALM``.

* Create a keytab file for this account, and store it in a file accessible only to DSS.

* Create an externally authenticated user account in the Oracle database, mapped to this Kerberos principal.
  This is typically done with:

  .. code-block:: sql

	CREATE USER dssOracleUser IDENTIFIED EXTERNALLY AS 'DSSKerberosPrincipal@KERBEROS.REALM';

* At the DSS level, configure the Oracle connection as follows:

	* Login with Kerberos: enabled

	* Principal: the Kerberos principal created above

	* Keytab: absolute path to the keytab file for this Kerberos principal

	* Advanced JDBC properties: add any Oracle-specific advanced connection properties required by your database setup.
	  This would typically be:

	  .. code-block:: sh

	  	oracle.net.authentication_services : (KERBEROS5)
	  	oracle.net.kerberos5_mutual_authentication : true

User impersonation
------------------

.. note::

	This feature is part of the :doc:`User Isolation Framework </user-isolation/index>` and requires an Enterprise license of DSS.

It is possible to configure the Oracle DSS connection to authenticate to the database using one Oracle account, and perform
all data manipulation and SQL queries using another. This typically allows DSS to impersonate its end-users when accessing the
database, much as is done for Hadoop or local computations when running in User Isolation Framework mode.

At the DSS level, this is configured by entering the Oracle account name to impersonate in the ``Impersonated user``
field of the connection configuration page.

Typical uses of this feature would include:

* defining this field as ``%{dssUserLogin}`` to directly use the DSS user login name as Oracle account name,
  in case the DSS and Oracle account databases match one-for-one

* defining this field as ``%{adminProperty:oracleLogin}`` where ``oracleLogin`` is a custom per-user admin property
  defined in the DSS user database, in the more general case where usernames have to be remapped

At the Oracle level, this impersonation mechanism uses the native Oracle "proxy authentication" feature, and should have been
authorized accordingly by the database administrator. This is typically done with one of the following directives:

.. code-block:: sql

	-- authorizes the DSS service account to impersonate Oracle user 'jeff'
	ALTER USER jeff GRANT CONNECT THROUGH dssOracleUser;

	-- authorizes the DSS service account to impersonate Oracle user 'jeff' for a subset of its roles
	ALTER USER jeff GRANT CONNECT THROUGH dssOracleUser ROLE role1, role2;

.. note::

	When the connection is configured for impersonation, the DSS service account itself only needs to be granted
	authorization to connect to the database, as in:

	.. code-block:: sql

		GRANT CREATE SESSION TO dssOracleUser;
