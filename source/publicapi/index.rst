Public REST API
##################

The DSS public API allows you to interact with DSS from any external system. It allows you to perform a large variety of administration and maintenance operations, in addition to access to datasets and other data managed by DSS.

The DSS public API is available:

 * As a :doc:`Python API client <devguide:api-reference/python/index>`. This allows you to easily send commands to the public API from a Python program. This is the recommended way to interact with the API.

 * As an :doc:`HTTP REST API <rest>`. This lets you interact with DSS from any program that can send an HTTP request. This requires more work.


The Python API client can be used both from inside DSS and from the outside world. Using the Python API client from inside DSS lets you do advanced automation and introspection tasks. Example usage of the Python client can be found at  :doc:`devguide:api-reference/python/index`


.. toctree::
	:maxdepth: 2

	features
	keys
	rest
