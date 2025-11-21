Exposing a Visual Model
#######################

.. contents::
    :local:

The primary function of the DSS API Deployer and API Node is to expose as an API a model trained using the :doc:`DSS visual machine learning component </machine-learning/index>`.

The steps to expose a model are:

* Train the model in Analysis
* Deploy the model to Flow
* Create a new API service
* Create an endpoint using the saved model
* Either:
    * Create a package of your API, deploy and activate the package on API nodes
    * Publish your service to the API Deployer, and use API Deployer to deploy your API

This section assumes that you already have a working API node and/or API Deployer setup. Please see :doc:`/apinode/api-deployment-infrastructures` if that's not yet the case.

Creating the model
===================

The first step is to create a model and deploy it to the Flow. This is done using the regular Machine Learning component of DSS. Please refer to the Tutorial 103 of DSS and to :doc:`/machine-learning/index` for more information.

Create the API
===============

There are two ways you can create your API Service

Create the API directly from the Flow
---------------------------------------

* In the Flow, select your model, and click "Create an API"
* Give an identifier to your API Service. This identifier will appear in the URL used to query the API
* Within this API Service, give an identifier to the endpoint. A service can contain multiple endpoints (to manage several models at once, or perform different functions)

The URL to query the API will be like:

* ``/public/api/v1/<service_id>/<endpoint_id>/predict`` for prediction models
* ``/public/api/v1/<service_id>/<endpoint_id>/predict-effect`` for causal prediction models
* ``/public/api/v1/<service_id>/<endpoint_id>/forecast`` for time series forecasting models.

Validate, you are taken to the newly created API Service in the API Designer component.

Create the API service then the endpoint
-----------------------------------------

* Go to the API Designer and create a new service
* Give an identifier to your API Service. This identifier will appear in the URL used to query the API
* Create a new endpoint and give it an identifier. A service can contain multiple endpoints (to manage several models at once, or perform different functions)
* Select the model to use for this endpoint. This must be a saved model (ie. a model which has been deployed to the Flow).

The URL to query the API will be like:

* ``/public/api/v1/<service_id>/<endpoint_id>/predict`` for prediction models
* ``/public/api/v1/<service_id>/<endpoint_id>/predict-effect`` for causal prediction models
* ``/public/api/v1/<service_id>/<endpoint_id>/forecast`` for time series forecasting models.

Validate, you are taken to the newly created API Service in the API Designer component.

Enriching queries features
===========================

See :doc:`enrich-prediction-queries`.

Testing your endpoint
======================

It's a good practice to add a few test queries to check that your endpoint is working as expected.

* Go to test
* Select add test queries. You can select a "test" dataset to automatically create test queries from the rows of this dataset
* Click on "Run test queries"
* You should see the prediction associated to each test query

Test queries are JSON objects akin to the ones that you would pass to the :doc:`api/user-api`. When you click on the "Play test queries" button, the test queries are sent to the dev server, and the result is printed.

Prediction model
----------------

Each test query should look like this for a prediction model (both regular and causal):

.. code-block:: javascript


	{
		"features" : {
			"feature1" : "value1",
			"feature2" : 42
		}
	}

For causal predictions, neither the outcome variable nor the treatment variable are expected.

Time series forecasting model
-----------------------------

For a time series forecasting model, you need to provide a list of past data. The model will forecast one horizon of data after the last date of the list.

For a single time series, the test query should look like this:

.. code-block:: javascript


	{
		"items" : [
			{
				"dateFeature": "2022-01-01T00:00:00.000",
				"targetFeature" : 10,
			},
			{
				"dateFeature": "2022-01-02T00:00:00.000",
				"targetFeature" : 12,
			},
			{
				"dateFeature": "2022-01-03T00:00:00.000",
				"targetFeature" : 11,
			}
		]
	}


For multiple time series, the test query should look like this:

.. code-block:: javascript


	{
		"items" : [
			{
				"identifierFeature": "id1",
				"dateFeature": "2022-01-01T00:00:00.000",
				"targetFeature" : 10,
			},
			{
				"identifierFeature": "id1",
				"dateFeature": "2022-01-02T00:00:00.000",
				"targetFeature" : 12,
			},
			{
				"identifierFeature": "id2",
				"dateFeature": "2022-01-01T00:00:00.000",
				"targetFeature" : 1,
			},
			{
				"identifierFeature": "id2",
				"dateFeature": "2022-01-02T00:00:00.000",
				"targetFeature" : 2,
			}
		]
	}

If your model uses external features, the test query must also contain their future values for one forecast horizon. For instance with a single time series it should look like this:

.. code-block:: javascript


	{
		"items" : [
			{
				"dateFeature": "2022-01-01T00:00:00.000",
				"targetFeature" : 10,
				"externalFeature1" : "value1",
				"externalFeature2" : 0
			},
			{
				"dateFeature": "2022-01-02T00:00:00.000",
				"targetFeature" : 12,
				"externalFeature1" : "value2",
				"externalFeature2" : 1
			},
			{
				"dateFeature": "2022-01-03T00:00:00.000",
				"targetFeature" : 11,
				"externalFeature1" : "value2",
				"externalFeature2" : 0
			},
			{
				"dateFeature": "2022-01-04T00:00:00.000",
				"externalFeature1" : "value1",
				"externalFeature2" : 1
			},
			{
				"dateFeature": "2022-01-05T00:00:00.000",
				"externalFeature1" : "value2",
				"externalFeature2" : 0
			}
		]
	}


Deploying your service
=======================

Please see:

* :doc:`first-service-manual` (if you are not using API Deployer)
* :doc:`first-service-apideployer` (if you are using API Deployer)

Optimized scoring
==================

If your model is java-compatible (See: :doc:`/machine-learning/scoring-engines`), you may select "Java scoring." This will make the deployed model use java to score new records, resulting in extremely improved performance and throughput for your endpoint.

Row-level explanations
=======================

The API node can provide per-row explanations of your models, using the ICE or Shapley methods. For more details about row-level explanations in Dataiku, please see :doc:`/machine-learning/supervised/explanations`

Explanations are not compatible with Optimized scoring.

You can either enable explanations by default for all predictions in the API designer, or request explanations on a per-query basis.

To request explanations, add this to your API request:

.. code-block:: javascript

	{
		"features" : {
			"feature1" : "value1",
			"feature2" : 42
		},
		"explanations": {
			"enabled": true,
			"method": "SHAPLEY",
			"nMonteCarloSteps": 100,
			"nExplanations": 5
   		}
	}

Explanations can also be requested through the Python client (:doc:`api/user-api`)

Getting post-enrichment information
====================================

When using queries enrichment (see :doc:`enrich-prediction-queries`), it can be useful to view the complete set of features after enrichment.

You can ask DSS to:

* Dump the post-enrichment information in the prediction response
* Dump the post-enrichment information in the audit log

Both behaviors can be configured from the "Advanced" tab in the API designer

Performance tuning
====================

Whether you are using directly the API Node or the API Deployer, there are a number of performance tuning settings that can be used to increase the maximum throughput of the API node.

It is possible to tune the behavior of prediction endpoints on the API node side.

For the prediction endpoint, you can tune how many concurrent requests your API node can handle.
This depends mainly on your model (its speed and in-memory size) and the available resources on the server(s) running the API node.

This configuration allows you to control the number of allocated `pipelines`.
One allocated pipeline means one model loaded in memory that can handle a
prediction request. If you have 2 allocated pipelines, 2 requests can be handled
simultaneously, other requests will be queued until one of the pipelines is
freed (or the request times out). When the queue is full, additional requests
are rejected.

.. include:: _endpoint-tuning-pool.rst
