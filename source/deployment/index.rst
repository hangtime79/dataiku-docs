Production deployments and bundles
####################################

Production deployments in DSS are managed from a central place: the Deployer. The Deployer is usually deployed as a dedicated node in your DSS cluster, but may also be run locally on a Design or Automation node. See below for instructions on how to install the Deployer in your environment.

The Deployer has two separate but similar components, the Project Deployer and the API Deployer, that handle the deployment of projects and API services respectively.
This section focuses on the former. To know more about the API Deployer, please see :doc:`/apinode/index`.

The DSS Automation Node provides a way to separate your DSS development and production environments and makes it easy to deploy and update DSS projects in production.
The DSS Design Node is your development environment, it is the place where you can design your flow and build or improve your data logic. Once this logic has been tested and a new version is ready to be released and deployed, you can export it to your production environment and use production data as inputs in your flow, on the Automation node. Metrics and scenarios on the Automation node allow for better assessment of the performance of your models and more control over your production data.

Deploying projects built in the Design node to the Automation node is done at project-level with project bundles. Bundles are archives that contain a given version of the flow you built in the Design node.

The Project Deployer allows you to:

* Manage all your Automation nodes
* Deploy bundles to your Automation nodes
* Monitor the health and status of your deployed Automation node projects

.. toctree::

	setup
	creating-bundles
	project-deployment-infrastructures
	deploying-bundles
	manually-importing-bundles
