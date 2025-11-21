:orphan:

Dynamic AWS EMR clusters
##########################

.. contents::
	:local:

.. warning::

  **Removed**: Support for EMR clusters is now Removed from DSS. Starting from version 14.2, the plugin is no longer available for download.

  We recommend that you use a fully Elastic AI infrastructure based on EKS. Please see :doc:`/containers/index`, or get in touch with your Dataiku Customer Success Manager, Technical Account Manager or Sales Engineer for more information and studying the best options.


DSS can create and manage multiple EMR clusters, allowing you to easily scale your workloads across multiple clusters, use clusters dynamically for some scenarios, ...

For more information on dynamic clusters and the usage of a dynamic cluster for a scenario, please see :doc:`multi-clusters`.

Support for dynamic EMR clusters is provided through the "EMR Dynamic clusters" plugin. You will need to install this plugin in order to use this feature.


Prerequisites and limitations
==============================

* Like for other kind of multi-cluster setups, the server that runs DSS needs to have the client libraries for the proper Hadoop distribution. In that case, your server needs to have the EMR client libraries for the EMR version you will use. Dataiku provides a ready-to-use AMI that already includes the required EMR client libraries 

* The previous requirement implies that the server that will run DSS and start the EMR clusters cannot be an edge node of a different kind of cluster. For example, you cannot manage dynamic EMR clusters from a DSS machine primarily connected to a MapR cluster.

* When working with multiple EMR clusters, all clusters should run the same EMR version. If running different versions, some incompatibilities may occur.

* It is not possible to create secure dynamic clusters

Create your first cluster
==========================

Machine setup
--------------

We strongly recommend that you use our "dataiku-emrclient" AMI which contains everything required for EMR support.

This AMI is named ``dataiku-emrclient-EMR_VERSION-BUILD_DATE``, where EMR_VERSION is the EMR version with which it is
compatible, and BUILD_DATE is its build date using format YYYYMMDD.

At the time of writing, the latest version of this AMI supports EMR 5.30.2 ("dataiku-emrclient-5.30.2-20220126").
It is available in the following AWS regions:

* eu-west-1 (AMI id: ami-0a3edce0134083c4f)
* us-east-1 (AMI id: ami-0cda7552753449447)
* us-west-1 (AMI id: ami-0c4d7c638ac4a9097)
* us-west-2 (AMI id: ami-00846b24187673dd2)

This AMI can be copied to other regions as desired.

.. warning::

  EMR versions earlier than 5.30 are based on the Amazon Linux 1 Linux distribution, which is not supported by DSS any more.
  Although "dataiku-emrclient" images are still available for these EMR versions, they should not be used for new deployments.

Dataiku may periodically rebuild this image to incorporate new updates or support new EMR versions. It is
recommended to check for its latest versions, as follows:

* using the AWS EC2 console: select the "AMIs" display in the leftmost column, select "Public images" in the drop-down menu at
  the left of the search field, and search for "dataiku-emrclient".

* using the AWS CLI: 

  .. code-block:: bash

     aws ec2 --region eu-west-1 describe-images \
       --owners 067063543704 \
       --filter 'Name=name,Values=dataiku-emrclient-*' \
       --query 'Images[].[ImageId,Name]' \
       --output table

The AMI does not include DSS. You need to install DSS using the regular DSS installation procedure.

AWS credentials
----------------

The user account running DSS must have the required credentials in order to create EMR clusters.

The two main ways to accomplish this are:

* Make sure that your machine has an IAM role that grants sufficient rights to create EMR clusters
* Make sure that your ``~/.aws/credentials`` file has valid credentials. This can be achieved by running ``aws login`` prior to starting DSS

Install the plugin
--------------------

From Administration > Plugins, install the "EMR dynamic clusters" plugin.

Define EMRFS connections
-------------------------

Most of the time, when using dynamic EMR clusters, you will store all inputs and outputs of your flows on S3. Access to S3 from DSS and from the EMR cluster is done through EMRFS.

* Go to Administration > Connections, and add a new HDFS connection
* Enter "s3://your-bucket" or "s3://your-bucket/prefix" as the root path URI

Unless the DSS host has implicit access to the bucket through its IAM role or default credentials in
``~/.aws/credentials``, define connection-level S3 credentials in "Extra Hadoop conf":

* Add a property called "fs.s3.awsAccessKeyId" with your AWS access key id
* Add a property called "fs.s3.awsSecretAccessKey" with your AWS secret key

Create the cluster and configure it
------------------------------------

Go to Administration > Cluster and click "Create cluster"

In "Type", select "EMR cluster (create cluster)" and give a name to your new cluster. You are taken to the "managed cluster" configuration page, where you will set all of your EMR cluster settings.

The minimal settings that you need to set are:

* Your AWS region (leave empty to use the same as the EC2 node running DSS)
* The EC2 instance type for the master and worker nodes 
* The total number of instances you require (there will be 1 master and N-1 slaves in the CORE group)
* The version of EMR you want to use. Beware, this should be consistent with the AMI you used.
* The VPC Subnet identifier in which you want to create your EMR cluster. This should be the same VPC that the DSS machine is running. Leave empty to use the same as the EC2 node running DSS
* The security groups to associate to all of the cluster machines. Make sure to add security groups that grant full access between the DSS host and the EMR cluster members.

Click on "Start/Attach". Your EMR cluster is created. This phase generally lasts 5 to 10 minutes. When the progress modal closes, you have a working EMR cluster, and an associated DSS dynamic cluster definition that can talk to oit

Use your cluster
----------------

In any project, go to Settings > Cluster, and select the identifier you gave to the EMR cluster. Any recipe or Hive notebook running in this project will now use your EMR cluster

Stop the cluster
----------------

Go to Administration > Clusters > Your cluster and click "Stop/Detach" to destroy the EMR cluster and release resources. 

Note that the DSS cluster definition itself remains, allowing you to recreate the EMR cluster at a later time. Projects that are configured to use this cluster while it is in "Stopped/Detached" state will fail.

Using dynamic EMR clusters for scenarios
=========================================

For a fully elastic approach, you can create EMR clusters at the beginning of a sequence of scenarios, run the scenarios and then destroy the EMR cluster, fully automatically.

Please see :doc:`multi-clusters` for more information. In the "Setup Cluster" scenario step, you will need to enter the EMR cluster configuration details


Cluster actions
================

In addition to the basic "Start" and "Stop", the Dynamic EMR clusters plugin provides the ability to scale up and down an attached EMR cluster.

Manual run
-----------

Go to the "Actions" tab of your cluster, and select the "Scale" action. You will have to specify the target number of instances in the CORE and TASK groups. We recommend that you never scale down the CORE group (which contains a small HDFS needed for cluster operations), and instead scale up and down the TASK group

As part of a scenario
----------------------

You can scale up/down a cluster as part of a scenario

* Add a "Execute macro" step
* Select the "Scale cluster up/down" step
* Enter the DSS cluster identifier, either directly, or using a variable - the latter case is required if you setup your cluster as part of the scenario.
* Select the settings

In this kind of setup you will generally scale up at the beginning of the scenario and scale down at the end. You will need two steps for that. Make sure to select "Run this step > Always" for the "scale down" step. This way, even if your scenario failed, the scale down operation will be executed.

Advanced settings
=================

In addition to the basic settings outlined above, the Dynamic EMR Clusters plugin provides some advanced settings

Security settings
------------------

* Key pair
* Roles
* Security configuration

Metastore
---------

* Database mode

Tags
----

You can add tags to your cluster. Variables expansion is not supported here.

Misc
-----

* Path for logs
