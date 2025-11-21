Deployment on Minikube
#######################

.. warning::

	Minikube provides a "toy" Kubernetes cluster that is not suitable for anything beyond simple experimentation.

	**Not supported**: Minikube is a :doc:`Not supported </troubleshooting/support-tiers>` feature

You can use the API Deployer Kubernetes integration to deploy your API Services on Minikube clusters.

A minikube cluster doesn't have an image repository. Instead, we'll use the Docker daemon running within the minikube VM directly, and completely skip the "push to image repository" phase.

Setup
======

Create the base image
---------------------

In order to create the base image directly in the Docker daemon running within the minikube VM, you need to run the following command in the same shell that will build your base image:

.. code-block:: bash

	eval `minikube docker-env`

Your session should look like:

.. code-block:: bash

	eval `minikube docker-env`
	./bin/dssadmin build-base-image --type apideployer

Start DSS with proper env
--------------------------

In order to use the Docker daemon running within the minikube VM, you need to start DSS after running:

.. code-block:: bash

	eval `minikube docker-env`

You can do that at the command line:

.. code-block:: bash

	eval `minikube docker-env`
	./bin/dss start

Alternatively, you can add the following line to ``bin/env-site.sh`` (you must restart DSS after)

.. code-block:: bash

	eval `minikube docker-env`

Follow Google documentation on how to create your cluster. We recommend that you allocate at least 7 GB of memory for each cluster node.

Configure infrastructure
==========================

The default "LoadBalancer" mode for service exposition is not usable for minikube.  Instead, you need to use "ClusterIP"

* Go to Infrastructure > Settings
* Go to Service Exposition
* Set ClusterIP as the exposition mode