Hadoop Impersonation (HDFS, YARN, Hive, Impala)
##################################################

The core of traditional Hadoop Distributions like Cloudera is based on:

* A HDFS cluster (NameNode + DataNodes)
* A YARN cluster (ResourceManager + NodeManagers), primarily running Spark and Hive workflows
* A HiveServer and HiveMetastore
* Impala servers

All of these support the Hadoop *proxyuser* mechanism that DSS can leverage as part of the User Isolation Framework.

Interaction with HDFS
======================

When UIF for Hadoop is enabled, access to HDFS is impersonated, i.e. performed with an end-user identity rather than the ``dssuser`` identity.

Data created by DSS needs to have specific permissions applied to it in order to both permit access by all authorized users (impersonated) and deny access by other users.

UIF interacts with HDFS permissions through Ranger. Ranger will manage all authorizations on HDFS data, both at the raw HDFS level and Hive/Impala level. You need to manage the permissions through the native mechanism of Ranger.

There is a legacy DSS-managed ACL synchronization", where DSS will automatically place HDFS ACLs on the managed datasets that it builds. Note that you will also need to leverage Ranger ACLs for Hive/Impala level.

**We recommend that you use Ranger preferably to DSS-managed ACLs**.

There are several limitations to the "DSS-managed ACL synchronization" mode:

* HDFS has a strong and non-workaroundable limitation to 32 ACL entries per file. The DSS-managed ACLs require a larger number of ACLs per path, which can overflow the limit to 32 ACLs per path in HDFs. This can lead to situations where it is not possible to have more than 32 groups in a DSS instance.
* Appending in a HDFS dataset can only be done by a single user. If another user tries to append, he will get permission issues. The dataset must be cleared before another can write.
* In some circumstances with partitioned datasets, occasional failures can happen and require retries.
* HDFS ACLs are not supported for :ref:`per-project-single-user-permissions`.

Ranger have integration points in the NameNode and have more pervasive and flexible access, implying fewer limitations than DSS-managed ACLs. The three main advantages of using Sentry / Ranger mode are:

* Centralized authorization in Sentry / Ranger rather than requiring managing Sentry rules in addition to the HDFS ACLs.
* For some customer deployments, working around limitations in number of HDFS ACLs.
* Appending to HDFS datasets using multiple users becomes possible.

Interaction with Hive
======================

When UIF is enabled, all interactions between DSS and Hive happen through HiveServer2.

HiveServer2 itself uses Ranger to authorize access to Hive databases and tables.

DSS does not push authorization rules to Ranger nor does it pull authorization rules from these systems.

Thus, you need to declare authorization rules both in the DSS projects, and in Ranger.

For more information about the supported Hive security modes, see :doc:`/hadoop/hive`.

Interaction with Impala
=========================

Details of security interaction between DSS and Impala are detailed in :doc:`/hadoop/impala`.


Interaction with Spark on YARN
===============================

Architecture
-------------

When running a Spark job as user ``A`` in DSS:

* DSS acquires Hadoop delegation tokens on behalf of ``A``
* DSS starts the Spark driver using the sudo mechanism, as ``A`` user, passing the Hadoop delegation tokens
* The Spark driver can then start its executors as ``A``, using its Yarn delegation tokens.

Thus, DSS only supports the ``yarn-client`` deployment of YARN. Running a standalone master or local mode is not recommended, because it is the YARN application manager who is responsible for renewing the delegation tokens.

DSS does not support the ``yarn-cluster`` mode.

Hive Metastore
---------------

On Hadoop, it is possible to restrict the access to the Hive metastore server so that only HiveServer2 can talk to the metastore server.

In a "regular" setup, any user can authenticate (using Kerberos) to the metastore server and issue DDL commands. If the metastore is secured, only Hiveserver2 may do so.

Spark does not use Hiveserver2 and when you create a ``HiveContext`` in Spark, it always talks directly to the Hive metastore. Thus, when the Hive metastore is configured for restricted access, Spark access to the metastore will fail. This has the following consequences:

* Using a HiveContext in Spark code recipes fails (SQLContext remains available)
* Using table definitions from the Hive metastore in Spark code recipes is not possible (including SparkSQL)
* Running some visual recipes on Spark (since they require HiveContext-only features) will fail

Authorizing access to the Hive metastore is typically done through the ``hadoop.proxyuser.hive.groups`` and
``hadoop.proxyuser.hive.hosts`` configuration keys. You should make sure that the former authorizes all DSS users,
and the latter authorizes the DSS host.

.. note::

	On Cloudera Manager, this configuration is accessible through the ``Hive Metastore Access Control and Proxy User Groups Override`` 
	entry of the Hive configuration.
