API Node & API Deployer: Real-time APIs
########################################

Production deployments in DSS are managed from a central place: the Deployer. The Deployer is either available as a dedicated node or attached to a Design node. See :doc:`how to install the Deployer on your environment </deployment/setup>`. The Deployer location is configured by administrator for the whole instance on each Design node in Administration > Settings > Deployer (this operation is automatically done if your are using Fleet Manager).

The Deployer has two separate but similar components, the Project Deployer and the API Deployer, that handle the deployment of projects and API services respectively.
This section focuses on the latter. To know more about the Project Deployer, please refer to :doc:`/deployment/index`.

In DSS Design and Automation nodes, you can create API services and deploy them to one or several API nodes, which are individual servers that do the actual job of answering REST API calls.
The API Deployer allows you to:

* As an administrator, define "API infrastructures", each pointing to either already-installed API node(s), a Kubernetes cluster or a external ML deployment platform
* As a user, deploy your API services on an infrastructure
* For all, monitor the health and status of your deployed APIs

.. toctree::
	:maxdepth: 2

	introduction
	concepts
	installing-apinode
	api-deployment-infrastructures
	first-service-apideployer
	first-service-manual
	deploy-anywhere
	endpoints
	enrich-prediction-queries
	api-documentation
	security
	managing_versions
	kubernetes/index
	api/index
	operations/index
	dev-guide

.. todo::

	* Intro: OK
	* Concepts: OK
	* Installing-apinode: OK
	* Installing-apideployer: OK
	* First-model-manual: OK
	* First-model-manual: API Deployer
	* Std model: OK
	* Custom model: OK
	* Functions: OK
	* Lookup: OK
	* SQL query: OK
	* Enrich: to be reviewed
	* operations/ha: to be reviewed
	* managing_versions: very outdated
	* operations/cli-tool: probably outdated
	* api/user-api: to be reviewed
	* api/admin-api: to be reviewed
	* operations/logging_audit: very outdated
	* operations/health_monitoring: very outdated

	* TODO: Graphite
	* TODO: Kubernetes requests and limits
	* TODO: Kubernetes: troubleshooting
	* TODO: GKE: gcr.io
	* TODO: GKE: nvidia
	* TODO: Published vs Deployed service id
	* TODO: Global performance tuning doc
