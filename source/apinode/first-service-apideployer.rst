First API (with API Deployer)
###############################

This page will guide you through the process of creating and deploying your first API service.  For this example, we'll use a :doc:`prediction endpoint <endpoint-std>`, used to expose a model developed using the :doc:`DSS visual machine learning component </machine-learning/index>` as a REST API service.

The steps to expose a prediction model are:

.. contents::
    :local:

.. warning::

	This section assumes that you already have installed and configured the DSS API Deployer, and already have an infrastructure connected to it. Please see :doc:`api-deployment-infrastructures` if that's not yet the case.

Create the model
===================

The first step is to create a model and deploy it to the Flow. This is done using the regular Machine Learning component of DSS. Please refer to the `Machine Learning Basics <https://knowledge.dataiku.com/latest/ml-analytics/model-design/ml-basics/tutorial-index.html>`_ and to :doc:`/machine-learning/index` for more information.

Create the API Service
========================

There are two ways you can create your API Service:

Create the API directly from the Flow
---------------------------------------

.. note::

	This method can only be used for prediction endpoints, and cannot be used for other kinds of endpoints

* In the Flow, select your model, and click "Create an API"
* Give an identifier to your API Service. This identifier will appear in the URL used to query the API
* Within this API Service, give an identifier to the endpoint. A service can contain multiple endpoints (to manage several models at once, or perform different functions)

The URL to query the API will be like ``/public/api/v1/<service_id>/<endpoint_id>/predict`` for prediction models, and ``/public/api/v1/<service_id>/<endpoint_id>/forecast`` for time series forecasting models.

Click Append, and you are taken to the newly created API Service in the API Designer component.

Create the API service then the endpoint in API Designer
---------------------------------------------------------

* Go to the project homepage
* Go to the API Designer and create a new service
* Give an identifier to your API Service. This identifier will appear in the URL used to query the API
* At this point, the API Service is created but not yet have any endpoint, i.e. it does not yet expose any model. See :doc:`concepts` for what endpoints are.
* Create a new endpoint of type "Prediction". Give an identifier to the endpoint. A service can contain multiple endpoints (to manage several models at once, or perform different functions)
* Select the model to use for this endpoint. This must be a saved model (ie. a model which has been deployed to the Flow).

The URL to query the API will be like ``/public/api/v1/<service_id>/<endpoint_id>/predict`` for prediction models, and ``/public/api/v1/<service_id>/<endpoint_id>/forecast`` for time series forecasting models.

Click Append, and you are taken to the newly created API Service in the API Designer component.

For a simple service, that's it! You don't need any further configuration.

(Optional) Add test queries
============================

It's a good practice to add a few test queries to check that your endpoint is working as expected, both in the API Designer and the API Deployer

* Go to test queries
* Select add test queries. You can select a "test" dataset to automatically create test queries from the rows of this dataset
* Click on "Run test queries"
* You should see the prediction associated to each test query

Push a version to the API Deployer
===================================

Click on "Push to API Deployer". This does two things:

* It creates the first *Version* (i.e. snapshot) of your API service using the currently active version of the saved model.
* It pushes this version to the API Deployer, where it will create a new *Published Service* on the API Deployer.

Click on the link that appears, which takes you to the API Deployer screen.

Deploy your version
====================

In the API Deployer, you now need to actually deploy your service to your infrastructure.

* From the left column of the API Deployer, click on the version we just uploaded, and select "Deploy"
* Select the infrastructure you wish to deploy to
* Give an identifier to your deployment. This identifier will not appear in the URL
* Validate

Your deployment is ready. You can either modify its settings, or Start it.

When you click on the "Deploy" (or the "Update") button, DSS sends your API Service to the API nodes and activates it. When this process completes, you can see:

* Public URLs from which your applications can query the service
* Monitoring charts for your service (if enabled)
* Sample code in various languages demonstrating how to query the service
* Test queries for verifying the service’s behavior in the live environment
* Stored update information, available in the **Last Updates** tab of the deployment

That's it, you've now deployed your predictive model as an API!

Perform real queries
======================

Once you have confirmed that your service endpoint works, you can actually use the API to integrate in your application.

See :doc:`api/user-api`

The API Deployer provides prebuilt code samples that you can directly use to query your API nodes.

Next steps
==========

Head over to the documentation page for each endpoint to get more information about how to use each one of them.
