Prerequisites and limitations
###############################

.. contents::
	:local:

.. note::

	This document only lists basic requirements for deploying the User Isolation Framework. Individual components may have additional requirements. Please refer to the detailed capabilities and reference architectures sections for more details.

Prerequisites
==============

Local machine
--------------

This setup is mandatory for all deployments of UIF.

* ACL support must be enabled on the filesystem which hosts the DSS data directory
* You need root access to setup the User Isolation Framework

For each UNIX user which will be impersonated by the DSS end-user (see :doc:`concepts` for more details), the following requirements must be met:

* The user must have a valid UNIX account.
* The user must have a valid shell (ie, must be able to perform shell actions).
* The user must have a writable home directory on HDFS.

Each group of users in DSS should have a matching UNIX group of users locally.

Hadoop
-------

Isolation framework capabilities are available on Cloudera CDP

The following configuration is required on your Hadoop cluster:

* Kerberos security must be enabled.
* You need a keytab for the ``dssuser``, as described in :doc:`/hadoop/secure-clusters`
* You need administrator access to your Hadoop cluster to setup user isolation (to setup the DSS impersonation authorization)

If you want to leverage Hive:

* You must have Ranger enabled
* HiveServer2 impersonation must be disabled (this is the default setting)

DSS can work with a restricted-access Hive metastore (ie, when only HiveServer2 can talk to the Metastore server), but due to limitations in Spark, a restricted-access metastore will disable the following features:

* Using a HiveContext in Spark code recipes (SQLContext remains available)
* Using table definitions from the Hive metastore in Spark code recipes (including SparkSQL)
* Running some visual recipes on Spark (since they require HiveContext-only features)

See :doc:`/hadoop/impala`, :doc:`/spark/index` and :doc:`/hadoop/hive` for more information.

For each Hadoop which will be impersonated by the DSS end-user (see :doc:`concepts` for more details), the following requirements must be met:

* The user must have a writable home directory on HDFS

Each group of users in DSS should have a matching group of users on Hadoop.

LDAP
-----

While manual configuration of all user accounts is fully possible, we recommend that you use a LDAP directory to have a unique source of truth for all users and group mappings, in DSS, on UNIX, and on Hadoop.

DSS
----

Migrating a DSS instance which was previously running without UIF is highly not recommended. We highly recommend starting with an empty DSS instance when setting up UIF.

"Downgrading" a DSS instance by disabling UIF is not supported.

Required information
---------------------

In addition to the above prerequisites, you need to gather some information.

You will need to obtain an initial list of UNIX groups that your end users belong to. Only users belonging to these groups will be allowed to use the impersonation mechanisms.

Limitations
============

Unsafe features
----------------

When UIF is enabled, the following features are not available for end-users unless they have the "Write unsafe code" permission:

* Write custom partition dependency functions
* Write Python UDF in data preparation

.. TODO:: specify only for Jython?

For more information about the "Write unsafe code" permission, see :ref:`security.permissions.write_unsafe_code`

HDFS datasets
---------------

Write in "append" mode in a HDFS dataset can only be done if you always use the same end-user. Append by multiple Hadoop end-users is not supported.
