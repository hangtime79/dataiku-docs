Introduction
###############

You can define API services in Design and Automation nodes and push these services to the API Deployer. The API Deployer in turn deploys the services to one or several API nodes, which are individual servers that do the actual job of answering REST calls.

The main use case for API services is to expose predictive models through a REST API, but it can also expose other types of capabilities, known as **endpoints**.  See the API services :doc:`concepts` for more information.

.. contents::
	:local:


Exposing predictive models
============================

By using DSS only, you can compute predictions for all records of an unlabeled dataset. Using the REST API of the DSS API deployer, you can request predictions for new previously-unseen records in real time.

The DSS API deployer provides high availability and scalability for scoring of records.

It can expose as API both:

* "Regular" prediction models, trained using the visual DSS machine learning component
* "Custom" prediction models, written in Python or R.

Thanks to its advanced features, the DSS API node is at the heart of the feedback and improvement loop of your predictive models:

* Powerful logging and auditing capabilities
* A/B testing and multi-version evaluation of models
* User-aware version dispatch

Exposing arbitrary Python and R functions
===========================================

You can expose any Python or R function written in DSS as a endpoint on the API Deployer. Calling the endpoint will call your function with the parameters you specify and return the results of the function.

The DSS API Deployer provides automatic multithreading capabilities, high availability and scalability for execution of your function.

Exposing SQL queries
======================

You can expose a parametrized SQL query as a DSS API Deployer endpoint.  Calling the endpoint with a set of parameters will execute the SQL query with these parameters.

The DSS API Deployer automatically handles pooling connections to the database, high availability and scalability for execution of your query.

Performing lookups in datasets
================================

The "Dataset lookup" endpoint allows you to fetch records from one or several DSS datasets, through a lookup in a SQL database.

The DSS API Deployer automatically handles pooling connections to the database, high availability and scalability for execution of your lookup.

Querying the API nodes
=======================

The API nodes expose an HTTP REST API. For more information about this API, see :doc:`api/user-api`

The API nodes themselves don't have a UI but the API Deployer acts as a centralized administration and management platform.

Designing APIs
================

Creation and preparation of endpoints used by the API Deployer is always done using DSS, in the *API Designer* section of a project.

Managing services and API nodes
================================

The API node itself is a server application-only, it does not have an UI. The API deployer acts as the centralized administration server for managing a fleet of API nodes, and deploying new APIs to them. The API Deployer is also fully controllable through an API.

In addition, you can manage the API node directly through a REST API or a command-line tool. See :doc:`operations/cli-tool` and :doc:`api/admin-api`. This feature is not available in Dataiku Cloud.
