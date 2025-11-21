API node administration API
#############################

.. contents::
	:local:

The API node can be managed through:

* The ``apinode-admin`` command-line tool. See :doc:`../operations/cli-tool`
* An HTTP REST API.

The REST API
=============

Request and response formats
------------------------------

For POST and PUT requests, the request body must be JSON, with the Content-Type header set to application/json.

For almost all requests, the response will be JSON.

Whether a request succeeded is indicated by the HTTP status code. A 2xx status code indicates success, whereas a 4xx or 5xx status code indicates failure. When a request fails, the response body is still JSON and contains additional information about the error.

Authentication
---------------

Authentication on the admin API is done via the use of API keys. API keys can be managed using the ``apinode-admin`` command-line tool.

The API key must be sent using HTTP Basic Authorization:

* Use the API key as username
* The password can remain blank

Methods reference
------------------

The reference documentation of the API is available at |apinode_admin_doc_url|

Admin REST API Python client
=============================

Dataiku provides a Python client for the API Node administration API. The client makes it easy to write client programs for the API in Python.

Installing
-----------

* The API client is already pre-installed in the DSS Python environment
* From outside of DSS, you can install the Python client by running ``pip install dataiku-api-client``

Reference API doc
------------------

.. autoclass:: dataikuapi.APINodeAdminClient
	:members:
	:undoc-members:

.. automodule:: dataikuapi.apinode_admin.service
	:members:
	:undoc-members:

.. automodule:: dataikuapi.apinode_admin.auth
	:members:
	:undoc-members: