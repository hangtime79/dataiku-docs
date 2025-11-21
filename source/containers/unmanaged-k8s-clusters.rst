Unmanaged Kubernetes clusters
##############################

.. contents::
	:local:

Using a single unmanaged cluster
---------------------------------

This is the "default" and simplest behavior.

To use a single unmanaged cluster, you must have an existing Kubernetes cluster that is running version 1.10 or later. Also, the ``kubectl`` command on the DSS machine node must be fully functional and usable by the user running DSS.

No additional configuration is required. In other words, you only need to do the following:

* Perform all of the initial setup steps (see :doc:`setup-k8s`)
* Create a container runtime configuration
* Setup the image repository in the base image
* Push the base image
* Use the container runtime configuration

Using multiple unmanaged clusters
----------------------------------

.. warning::

	This is an exotic setup. We recommend discussing with your Dataiku Customer Success Manager

DSS can connect to several existing Kubernetes clusters. If you already have multiple clusters (either managed by a cloud provider, or clusters that you deployed yourself), DSS can leverage all of them, using multiple containerized execution configurations.

DSS leverages the ``kubectl`` tool for Kubernetes. The *kubectl configuration file* can define multiple "contexts". Each kubectl context defines a cluster (API server URL) and credentials to use.

To use multiple clusters (or multiple sets of credentials to a cluster):

* Create your clusters, running version 1.10 or later — this is not handled by DSS. To have DSS automatically manage Kubernetes clusters for you, see :doc:`managed-k8s-clusters`.
* Define multiple contexts in your kubectl configuration file.
* Define multiple container runtime configurations, each one referencing a kubectl context.

Each container runtime configuration can thus reference a different Kubernetes cluster, and you can dispatch between projects this way.
