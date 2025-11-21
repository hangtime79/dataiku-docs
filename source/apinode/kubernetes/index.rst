Deploying on Kubernetes
#########################

Using the API Deployer, you can deploy your API services to a Kubernetes cluster.

Each API Service Deployment (see :doc:`/apinode/concepts`) is setup on Kubernetes as:

* A *Kubernetes deployment* made of several *replicas* of a single pod
* A *Kubernetes service* to expose a publicly available URL which applications can use to query your API

.. toctree::

	setup
	gke
	aks
	eks
	minikube
	sql-connections
	expositions
