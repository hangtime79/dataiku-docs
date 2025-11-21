Setting up Spark integration
###############################

.. contents::
	:local:

There are four major ways to setup Spark in Dataiku:

* If you are using :doc:`Dataiku Cloud </installation/index>` installation, Spark is already setup and ready to use, you do not need any further action

* If you are using :doc:`Dataiku Cloud Stacks </installation/index>` installation, Spark on Elastic AI clusters is already setup and ready to use, you do not need any further action

* If you are doing a custom installation with :doc:`Elastic AI </containers/index>`, this will configure and enable Spark on Elastic AI clusters

* If you are doing a custom installation with :doc:`Hadoop </hadoop/index>`, Spark will be available through your Hadoop cluster. Please see :doc:`/hadoop/spark` for more details.

* Using "Unmanaged Spark on Kubernetes"


Unmanaged Spark on Kubernetes
===============================

.. warning::

	This is a very custom setup. We recommend that you leverage Dataiku Elastic AI capabilities rather.

The precise steps to follow for Spark-on-Kubernetes depend on which managed Kubernetes offering you are using and which cloud storage you want to use.

We strongly recommend that you rather use :doc:`Elastic AI </containers/index>`.

The rest of this page provides indicative instructions for non-managed deployments


Configure DSS
--------------

You first need to configure DSS to use your Spark 3.4

Build your Docker images
--------------------------

Follow the Spark documentation to build Docker images from your Spark distribution and push it to your repository.

Note that depending on which cloud storage you want to connect to, it may be necessary to modify the Spark Dockerfiles. See our guided installation procedures for more details.

Create the Spark configuration
--------------------------------

Create a named Spark configuration (see :doc:`configuration`), and set at least the following keys:

* ``spark.master``: ``k8s://https://IP_OF_YOUR_K8S_CLUSTER``
* ``spark.kubernetes.container.image``: ``the tag of the image that you pushed to your repository``
