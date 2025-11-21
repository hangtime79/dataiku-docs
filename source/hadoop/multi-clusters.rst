Multiple Hadoop clusters
#########################


.. warning::

    **Deprecated**: Support for multiple Hadoop clusters is :doc:`Deprecated </troubleshooting/support-tiers>` and will be removed in a future DSS version

	We strongly advise against using Multiple Hadoop Clusters for "traditional" Hadoop clusters, given the very high associated complexity.


DSS can connect to several "Hadoop clusters", meaning:

* Several YARN resource managers
* Several HiveServer2 servers
* Several sets of Impala servers

This capability to connect to multiple clusters doesn't include multiple Hadoop filesystems, which is covered by :doc:`hadoop-fs-connections`

.. contents::
	:local:

Concepts
========

Builtin cluster
----------------

A Hadoop cluster is mainly defined by the client-side configuration, usually found in ``/etc/hadoop/conf``, which indicates (among others) the address of the YARN resource manager.

When Hadoop integration is setup in DSS, DSS will use a "system-level" Hadoop configuration, which is put in the classpath of DSS.

In DSS, this is called the "builtin cluster", whose configuration is accessible in Administration > Settings > Hadoop.

The builtin cluster also has associated Hive, Impala and Spark configurations defined in the respective Administration > Settings screens.

Additional clusters
--------------------

In addition to the builtin cluster, you can define additional clusters in the Administration > Cluster screens.

Each additional cluster is defined by:

* A set of Hadoop configuration keys that indicate how to connect to the YARN of the additional cluster
* HiveServer2 connection details for the additional cluster
* Impala connection details for the additional cluster
* A set of Spark configuration keys specific to the additional cluster

Managed dynamic clusters
-------------------------

In addition to "static" additional clusters, where you have to define all the connection settings, DSS has a notion of "managed dynamic clusters". Through a plugin installed in DSS, dynamic clusters can be created by DSS, configured as additional clusters, and shutdown through DSS.

This capability is most often used in cloud deployments, either using the cloud provider's native Hadoop cluster capability or dynamic Hadoop clusters directly created based on cloud provider's virtual machines capabilities.

Use an additional cluster
----------------------------

Each project defines whether recipes/notebooks/... of this project run against the builtin cluster or one of the additional clusters.

Per-scenario additional clusters
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

In addition to project-level definition of which cluster to use, a scenario can:

* Create a dynamic cluster (for example an EMR cluster)
* Execute all of its steps on the dynamic cluster
* Shutdown the dynamic cluster at end

This allows you to have a minimal cluster or no cluster at all for the "design" of the project, and to spawn clusters dynamically for execution of scenarios, leading to a fully elastic resource usage approach. This capability is more often used for automation nodes.

Restrictions
=============

* When using multiple Hadoop clusters, all clusters must use the same Hadoop distribution. It is not supported for example to have the builtin cluster running Cloudera, and an additional cluster running Hortonworks

* All clusters must either be unsecure, or secure using the same Kerberos realms (DSS will only use the principal and keytab of the builtin cluster)

* User mappings must be similar between clusters

* Running multiple Spark versions (for example one cluster with Spark 1.6 and one cluster with Spark 2.2) is not supported

* Multiple MapR clusters is not validated and not supported

Define an additional static cluster
======================================

This assumes that DSS is already properly connected and setup to work with primary cluster.

* Go to Administration > Clusters and create a new cluster
* Give an identifier to your new cluster

The configuration of an additional cluster is divided in a number of sections. For each section, you need to choose whether you want to inherit the settings of the builtin cluster, or override them for this particular cluster.

Hadoop
-------

In this section, you'll always override the "Hadoop config keys" section. You must enter here the keys used to define the YARN addresses.

These settings will be passed to:

* Data preparation jobs running on MapReduce engine

Although this varies, you'll usually need to define the following keys:

* ``fs.defaultFS`` usually pointing to the native HDFS of the cluster (used notably for various staging directories), ie something like ``hdfs://namenodeaddress:8020/``
* ``yarn.resourcemanager.address`` pointing to the host/port of your resource manager, i.e. something like ``resourcemanageraddress:8032``

.. warning::

	These Hadoop configuration keys are not passed to Spark jobs. See below.

Other settings are for advanced usage only

Hive
----

In this section, you'll always override "connection settings" to point to the HiveServer2 of your additional cluster. Refer to :doc:`hive` for more information about configuring this.

If your builtin cluster does not use "HiveServer2" as default recipe engine, override "creating settings" and select HiveServer2

.. todo::

	Are the Hive config settings needed ?

Other settings are for advanced usage only

Impala
-------

In this section, you'll always override "connection settings" to point to the impalad nodes of your additional cluster. Refer to :doc:`impala` for more information about configuring this.

Other settings are for advanced usage only

Spark
------

.. note::

	Only the "yarn" master in "client" deployment mode really makes sense here.

In this section, you'll need to add configuration keys to point Spark to your YARN. Note that the configurations defined in the "Hadoop" section do not apply to Spark as Spark uses different keys.

Choose to override runtime config.

The first section "Config keys added to all configurations" contains configuration keys that will be added to all Spark named configurations defined at the global level. The second section "Configurations" contains configuration keys that are added only to a single Spark named conf.

You cannot add new Spark named conf at the additional cluster level.

You'll often need to add the following keys (note the ``spark.hadoop`` prefix used to pass Hadoop configuration keys to Spark):

* ``spark.hadoop.fs.defaultFS`` usually pointing to the native HDFS of the cluster (used notably for various staging directories), ie something like ``hdfs://namenodeaddress:8020/``
* ``spark.hadoop.yarn.resourcemanager.address`` pointing to the host/port of your resource manager, i.e. something like ``resourcemanageraddress:8032``
* ``spark.hadoop.yarn.resourcemanager.scheduler.address`` pointing to the the host/port of the scheduler part of your resource manager, i.e. something like ``resourcemanageraddress:8030``

Other settings are for advanced usage only.


Use a specific cluster for scenarios
==================================================

For this, you'll use the variables expansion mechanism of DSS.

Instead of writing a cluster identifier as the contextual cluster to use at the project level, you can use the syntax ``${variable_name}``. At runtime, DSS will use the cluster denoted by the ``variable_name`` variable.

Your scenario will then use a scenario-scoped variable to define the cluster to use for the scenario.

For example, if you want to use the cluster ``regular1`` for the "design" of the project, and all non-scenario-related activities, and the ``fast2`` cluster for a scenario.

Setup your project as such:

* Cluster: ``${clusterForScenario}``
* Default cluster: ``regular1``

With this setup, when the ``clusterForScenario`` variable is not defined (which will be the case outside of the scenario), DSS will fallback to ``regular1``

In your scenario, add an initial step "Define scenario variables", and use the following JSON definition:

.. code-block:: json

	{
		"clusterForScenario" : "fast2"
	}

The steps of the scenario will execute on the ``fast2`` cluster

Permissions
===========

Each cluster has an owner and groups who are granted access levels on the cluster:

* **Use cluster** to be able to select the cluster and use it in a project
* **Operate cluster** to be able to modify cluster settings
* **Manage cluster users** to be able to manage the permissions of the cluster

In addition, each group can be granted global permissions to:

* Create clusters and manage the clusters they created
* Manage all clusters, including the ones they are not explicitly granted access to