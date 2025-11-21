Setup with Kubernetes
#######################

This reference architecture will guide you through deploying on your DSS running some workloads on Kubernetes.

This applies both to "static" Kubernetes clusters and "dynamic / managed by DSS" Kubernetes clusters.

This document covers:

* The fundamental local isolation code layer
* Security for running "regular" workloads on Kubernetes (Python, R, Machine Learning)
* Security for running Spark workloads on Kubernetes

In the rest of this document:

* ``dssuser`` means the UNIX user which runs the DSS software
* ``DATADIR`` means the directory in which DSS is running

.. contents::
	:local:

Initial setup
================

Please read carefully the :doc:`../prerequisites-limitations` documentation and check that you have all required information.

Common setup
=============

Initialize UIF (including local code isolation), see :doc:`/user-isolation/initial-setup`

.. include:: ../capabilities/_kubernetes-workloads.rst

One-namespace-per-user setup
-----------------------------

* In the Spark configuration, enable the "Managed K8S configuration" checkbox
* In "Target namespace", enter something like ``dss-ns-${dssUserLogin}``
* Enable "Auto-create namespace"
* Set Authentication mode to "Create service accounts dynamically"

Each time a user U starts a Job that uses this particular Spark configuration, DSS will:

* Create if needed the ``dss-ns-U`` namespace
* Create a service account, and grant it rights limited to ``dss-ns-U``
* Get the secret of this service account and pass it to the Spark driver
* The Spark driver will use this secret to create and manage pods in the ``dss-ns-U`` namespace (but does not have access to any other namespace)
* At the end of the job, destroy the service account

One-namespace-per-team setup
----------------------------

* In the Spark configuration, enable the "Managed K8S configuration" checkbox
* In "Target namespace", enter something like ``${adminProperty:k8sNS}``
* Set Authentication mode to "Create service accounts dynamically"

Then, for each user, you need to set an "admin property" named ``k8sNS``, with the name of the team namespace to use for this user. This can be automated through the API. See above for how this will work.

With this setup, there may be a fixed number of namespaces so you don't need to auto-create namespaces. The account running Dataiku only needs full access to these namespaces in order to create service accounts in them. This can be useful if you don't have the ability to create namespaces. However, this leaves the possibility that skilled hostile users can try to attack other Spark jobs running in the same namespace.
