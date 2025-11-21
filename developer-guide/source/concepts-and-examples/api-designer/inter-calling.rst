Calling another endpoint
========================

A common use-case is to have an API Service with several endpoints (for example several prediction models), and to have an additional "dispatcher" code endpoint that orchestrates the other endpoints.

Users only directly query the dispatcher endpoint, and this dispatcher endpoint in turns needs to query the other endpoints of the same API Service

For example, a dispatcher endpoint could query several prediction models and provide an "aggregated" answer, or it could select which endpoint to query based on query parameters.

For this kind of cases, the dispatcher endpoint would normally need:

 * To have an API key in order to query the other endpoint, which may not be known at design time
 * To know the service identifier in order to query the proper URL, which may not be known at design time
 * To know the port on which the API node server is running, which may not be known at design time

In order to facilitate this kind of setup, in a Python function or prediction endpoint, you can obtain a :class:`dataikuapi.APINodeClient` that is already preconfigured to query other endpoints of the same service.

Use the following code

.. code-block:: python

	from dataiku.apinode import utils

	def my_api_function():
		client = utils.get_self_client()

		# client is now a dataikuapi.APINodeClient, so you can use the regular methods
		# to query other endpoints
		result = client.predict_record("other_endpoint", {"feature1" : "value1", "feature2" : 42})

.. warning::

	The call to ``utils.get_self_client()`` must be called *within* your function or ``predict`` method. Calling this in your initialization will not retrieve the API Key.


.. note::

	You may cache the returned client, in order to keep persistent HTTP connections. However, doing that will
	cause subsequent queries to service to reuse the same API key, which may be undesirable.
