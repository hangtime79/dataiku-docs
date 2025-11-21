Setting up
###########

Prerequisites
==============

.. warning::

	API Deployer is not responsible for starting and managing your Kubernetes cluster, which must already exist.

The prerequisites for deploying API services on Kubernetes are:

* You need to have an existing Kubernetes cluster. The "kubectl" command on the API Deployer node must be fully functional and usable by the user running DSS.
* The local "docker" command must be usable by the user running DSS. That includes the permission to build images, and thus access to a Docker socket
* You need to have an image registry, accessible by your Kubernetes cluster
* The local "docker" command must have permission to push images to your image registry

Limitations
============

* The MacOS installation of DSS does not support Kubernetes
* API services using conda-based code environments are not supported
* Your DSS machine must have direct outgoing Internet access in order to install packages
* Your containers must have direct outgoing Internet access in order to install packages

Build the base image
=====================

Before you can deploy to Kubernetes, a "base image" must be constructed. Each API Deployer deployment will then create a final Docker image made of:

* The base image
* An additional layer containing the API Service data and settings

Each Deployment infrastructure on the API Deployer can use a different base image. If you don't configure anything specific, all infrastructures will use a default base image.

.. warning::

	After each upgrade of DSS, you must rebuild all base images

From the DSS Datadir, run

.. code-block:: bash

	./bin/dssadmin build-base-image --type api-deployer

For more details on building base images and customizing base images, please see :doc:`/containers/setup-k8s` and :doc:`/containers/custom-base-images`.

Create the Kubernetes infrastructure in DSS
=============================================

* Go to API Deployer > Infrastructures
* Create a new infra with type Kubernetes
* Go to Settings > Kubernetes cluster

The elements you may need to customize are:

* Kubectl context: if your kubectl configuration file has several contexts, you need to indicate which one DSS will target - this allows you to target multiple Kubernetes cluster from a single API Deployer by using several kubectl contexts
* Kubernetes namespace: all elements created by DSS in your Kubernetes cluster will be created in that namespace
* Registry host
