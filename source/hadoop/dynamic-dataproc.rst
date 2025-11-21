:orphan:

Dynamic Google Dataproc clusters
################################

.. contents::
	:local:

.. warning::

	**Removed**: Support for Dataproc clusters is now Removed from DSS. Starting from version 14.2, the plugin is no longer available for download.

	We recommend that you use a fully Elastic AI infrastructure based on GKE. Please see :doc:`/containers/index`, or get in touch with your Dataiku Customer Success Manager, Technical Account Manager or Sales Engineer for more information and studying the best options.

DSS can create and manage multiple Dataproc clusters, allowing you to easily scale your workloads across multiple clusters, dynamically create and scale clusters for some scenarios, etc.

For more information on dynamic clusters and the usage of a dynamic cluster for a scenario, please see :doc:`multi-clusters`.

Support for dynamic  clusters is provided through the "Dataproc clusters" DSS plugin. You will need to install this plugin in order to use this feature.


Prerequisites and limitations
==============================

* Like for other kinds of multi-cluster setups, the server that runs DSS needs to have the client libraries for the proper Hadoop distribution. In that case, your server needs to have the Dataproc client libraries for the version of Dataproc you will use.

* When working with multiple clusters, all clusters should run the same Dataproc version. If running different versions, some incompatibilities may occur.

Create your first cluster
==========================

Before Running
----------------

The Google Compute Engine (GCE) VM that hosts DSS is associated with a given service account, which MUST have the following AMI permissions to run properly:

* Dataproc Editor
* Dataproc Service Agent

Otherwise the user account running DSS must have the required credentials in order to create Dataproc clusters.


Install the plugin
--------------------

From the "Plugins" section of the Administration panel, go to the store and install the Dataproc clusters plugin.

Define GCS connections
-------------------------

Most of the time, when using dynamic Dataproc clusters, you will store all inputs and outputs of your flows on GCS. Access to GCS from DSS and from the Dataproc cluster is done through GCS.

* Go to Administration > Connections, and add a new HDFS connection
* Enter "gs://your-bucket" or "gs://your-bucket/prefix" as the root path URI

Unless the DSS host has implicit access to the bucket through its IAM role or default credentials in environment variable ``GOOGLE_APPLICATION_CREDENTIALS``, define connection-level credentials in "Extra Hadoop conf":

* Add a property called "spark.hadoop.google.cloud.auth.service.account.enable" with value true
* Add a property called "spark.hadoop.google.cloud.auth.service.account.json.keyfile" with path to your keyfile on the server

Create the cluster and configure it
------------------------------------

Go to Administration > Cluster and click "Create cluster"

In "Type", select "Dataproc cluster (create cluster)" and give a name to your new cluster. You are taken to the "managed cluster" configuration page, where you will set all of your Dataproc cluster settings.

You will then need to fill in the following fields:

* The GCP project ID in which to build the Dataproc Cluster
* The cluster name on GCP
* The DataProc version to use (MUST be the same Linux distribution and version as your GCE VM)
* The desired region/zone 
* The network tags you want to attach to your cluster nodes 
* The instance type for the master and worker nodes
* The total number of worker nodes you require


Click on "Start/Attach". Your Dataproc cluster is created. This phase generally lasts 5 to 10 minutes. When the progress modal closes, you have a working Dataproc cluster, and an associated DSS dynamic cluster definition that can talk to it.

Use your cluster
----------------

In any project, go to Settings > Cluster, and select the identifier you gave to the Dataproc cluster. Any recipe or Hive notebook running in this project will now use your Dataproc cluster.

Stop the cluster
----------------

Go to Administration > Clusters > Your cluster and click "Stop/Detach" to destroy the Dataproc cluster and release resources.

Note that the DSS cluster definition itself remains, allowing you to recreate the Dataproc cluster at a later time. Projects that are configured to use this cluster while it is in "Stopped/Detached" state will fail.

Using dynamic Dataproc clusters for scenarios
=================================================

For a fully elastic approach, you can create Dataproc clusters at the beginning of a sequence of scenarios, run the scenarios and then destroy the Dataproc cluster, fully automatically.

Please see :doc:`multi-clusters` for more information. In the "Setup Cluster" scenario step, you will need to enter the Dataproc cluster configuration details


Cluster actions
================

In addition to the basic "Start" and "Stop", the Dataproc clusters plugin provides the ability to scale up and down an attached Dataproc cluster.

Manual run
-----------

Go to the "Actions" tab of your cluster, and select the "Scale cluster up or down" macro. You will then choose the new number of desired worker nodes, with the option of creating spot (pre-emptible) nodes.

As part of a scenario
----------------------

You can scale up/down a cluster as part of a scenario

* Add an "Execute macro" step
* Select the "Scale cluster up or down" macro
* Enter the DSS cluster identifier, either directly, or using a variable - the latter case is required if you setup your cluster as part of the scenario.
* Select the settings

In this kind of setup you will generally scale up at the beginning of the scenario and scale down at the end. You will need two steps for that. Make sure to select "Run this step > Always" for the "scale down" step. This way, even if your scenario fails, the scale down operation will be executed.

Advanced settings
=================

In addition to the basic settings outlined above, the Dataproc clusters plugin provides some advanced settings:


Hive metastore
--------------

* Metastore database type (transient or persisted)
* Databases to use

Labels
------

You can add labels to your cluster. Variables expansion is not supported here.
