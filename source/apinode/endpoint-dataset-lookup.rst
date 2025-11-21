Exposing a lookup in a dataset
##################################

.. contents::
	:local:

The "dataset(s) lookup" endpoint offers an API for searching records in a DSS dataset by looking it up using lookup keys.

For example, if you have a "customers" dataset in DSS, you can expose a "dataset lookup" endpoint where you can pass in the email address and retrieve other columns from the matching customer.

A "dataset lookup" endpoint can:

* lookup in multiple datasets at once
* lookup multiple input records at once
* lookup based on multiple lookup keys
* retrieve arbitrary number of columns

However, note that each lookup can not return more than one dataset line for each input lookup records. Multiple results either generate an error or get dropped.

.. note::

	The "dataset lookup" endpoint is very similar to the :doc:`feature to enrich prediction queries <enrich-prediction-queries>` before passing them to a prediction model.
	
	In essence the "Dataset lookup" endpoint is only the "Enrich" part of prediction endpoints

Creating the lookup endpoint
===============================

To create a dataset lookup endpoint, start by creating an API service from the API Designer.

* Go to the project homepage
* Go to the API Designer and create a new service
* Give an identifier to your API Service. This identifier will appear in the URL used to query the API
* At this point, the API Service is created but not yet have any endpoint, i.e. it does not yet expose any capability. See :doc:`concepts` for what endpoints are. 
* Create a new endpoint of type "Dataset lookup". Give an identifier to the endpoint. A service can contain multiple endpoints (to manage several models at once, or perform different functions)

The URL to query the API will be like ``/public/api/v1/<service_id>/<endpoint_id>/lookup``.

Validate, you are taken to the newly created API Service in the API Designer component.

Configuration and deployment
-----------------------------

Configuration, deployment options and specificities are the same as for the :doc:`feature to enrich prediction queries <enrich-prediction-queries>` before passing them to a prediction model.

Performance tuning
====================

Whether you are using directly the API Node or the API Deployer, there are a number of performance tuning settings that can be used to increase the maximum throughput of the API node.

For the Dataset lookup endpoint, you can tune how many concurrent requests your API node can handle. 

This configuration allows you to control the number of allocated `pipelines`.
One allocated pipeline means one persistent connection to the database. 
If you have 2 allocated pipelines, 2 requests can be handled
simultaneously, other requests will be queued until one of the pipelines is
freed (or the request times out). When the queue is full, additional requests
are rejected.

.. include:: _endpoint-tuning-pool.rst
