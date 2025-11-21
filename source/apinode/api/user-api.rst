API node user API
#############################

.. contents::
	:local:

Predictions are obtained on the API node by using the User REST API.

The REST API
=============

Request and response formats
------------------------------

For POST and PUT requests, the request body must be JSON, with the Content-Type header set to application/json.

For almost all requests, the response will be JSON.

Whether a request succeeded is indicated by the HTTP status code. A 2xx status code indicates success, whereas a 4xx or 5xx status code indicates failure. When a request fails, the response body is still JSON and contains additional information about the error.

Authentication
---------------

Each service declares whether it uses authentication or not. If the service requires authentication, the valid API keys are defined in DSS.

The API key must be sent using `HTTP Basic Authentication <https://en.wikipedia.org/wiki/Basic_access_authentication>`_:

* Use the API key as username
* The password can remain blank

The valid API keys are defined on the DSS side, not on the API node side. This ensures that all instances of an API node will accept the same set of client keys

Methods reference
------------------

The reference documentation of the API is available at |apinode_user_doc_url|

API Python client
=============================

Dataiku provides a Python client for the API Node user API. The client makes it easy to write client programs for the API in Python.

Installing
-----------

* The API client is already pre-installed in the DSS virtualenv
* From outside of DSS, you can install the Python client by running ``pip install dataiku-api-client``

Reference API doc
------------------

.. autoclass:: dataikuapi.APINodeClient
	:members:
	:undoc-members: