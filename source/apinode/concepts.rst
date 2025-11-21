Concepts
###########

API Node
=========

The API Node is the application server that does the actual job of answering HTTP requests.  API Nodes are horizontally scalable and highly available.  They can be deployed either as a set of servers, or as containers through the use of Kubernetes (which allows you to deploy either on-premises, or on a serverless stack on the cloud).

The API Node can be administratively configured using the command-line or a REST API. The UI for using API nodes is the API Deployer.

API Deployer
=============

With the API Deployer you can:

* Define "API infrastructures", each pointing to either already-installed API node(s) or a Kubernetes cluster
* Deploy new API services on an infrastructure (i.e. to all API nodes in the infrastructure)
* Monitor the health and status of your API nodes
* Manage the lifecycle of your APIs from development to production

The API Deployer can control an arbitrary number of API nodes, and can dynamically deploy new API nodes as containers through the use of Kubernetes (which allows you to deploy either on-premises, or on a serverless stack on the cloud).

The API Deployer is part of the Deployer, which is usually deployed as a dedicated node in your DSS cluster. Please refer to :doc:`/deployment/index`.

Usage of the API Deployer is optional. You can deploy API Services directly to API Nodes using the API Node CLI or API.

API Designer
=============

The API Designer is a section of each DSS Project that you use for creating, designing, and developing your APIs.

API Service
=============

An API service is the unit of management and deployment for the API node. Services are declared and prepared in the DSS API Designer and are then deployed on the API Deployer.

A single service can host several *endpoints*. All endpoints of a service are updated and managed at once.

Endpoint
=========

An endpoint is a single path on the API and is contained within an API Service. Each endpoint fulfills a single function.

The API node supports 7 kinds of endpoints:

* The :doc:`Prediction or Clustering <endpoint-std>` endpoint to predict or cluster using models created with the DSS Visual Machine Learning component.
* The :doc:`Python prediction <endpoint-python-prediction>` endpoint to perform predictions using a custom model developed in Python
* The :doc:`MLflow Prediction <endpoint-mlflow>` endpoint to predict using imported MLflow models
* The :doc:`R prediction <endpoint-r-prediction>` endpoint to perform predictions using a custom model developed in R
* The :doc:`Python function <endpoint-python-function>` endpoint to call specific functions developed in Python
* The :doc:`R function <endpoint-r-function>` endpoint to call specific functions developed in R
* The :doc:`SQL query <endpoint-sql-query>` endpoint to perform parametrized SQL queries
* The :doc:`Dataset lookup  <endpoint-dataset-lookup>` endpoint to perform data lookups in one or more DSS datasets

An API service can host several endpoints. All endpoints of an API service are updated and managed at once. Having several endpoints in an API service is useful if you have several predictive models that are not mixable together, but you still want a unique management and access point.

Version
========

API Services in DSS are versioned. You create new versions of the API Service using the API Designer in DSS. These versions are then sent to the API Deployer, where they become available to be deployed on the API Nodes.

The version of a single Deployment on the API Deployer can be changed without losing any query. After activating a new version, queries hitting the API node instance use the newer version of all models in the API service.

The API Deployer and API Nodes provide advanced management of version. The basic use case is when you have a single  version of a service which is active (the newest, generally). However, you can also have several concurrent active versions. In that case, you define the probability of queries using each generation of the service and dispatch policies. Combined with the powerful logging capabilities, this lets you very easily create A/B testing strategies.

Deployment Infrastructure
==========================

The API Deployer manages several independent pools of API nodes. This allows you for example to have one pool of API nodes for development, one for testing, one for production.

Each deployment infrastructure can either be:

* A *static* infrastructure: a set of pre-deployed API nodes that the API Deployer manages
* A *Kubernetes* infrastructure: the API Deployer dynamically creates containers in your Kubernetes cluster to run the API Node server.

The infrastructures are organized into *Lifecycle Stages* (like "Development", "Preproduction" and "Production") that organize how your various deployments will be shown.

Each infrastructure has access permissions

Deployment
===========

In the API Deployer, the main object that you manage is called a *deployment*.

A deployment is made of a version (or set of versions) of a single API Service running on a single Deployment infrastructure.

You can dynamically change which version (or versions) of your API Service is running on each deployment (this version change happens without any service interruption). Each Deployment has one or several service URLs that the API clients need to use to query this deployment.

In essence, a Deployment acts as a scalable and highly-available *instance* of an API service.

Package
=========

Packages are the physical representation of different versions of a service. Each time you want to update an API service (for example to use retrained models), you create a new package from the DSS interface.

The package is then transferred to the API node instances, and activated. A package contains all endpoints of a single API Service.
