The REST API
################

At its core, the DSS public API is a REST HTTP API. The reference HTTP documentation of the DSS REST API can be found here: |api_doc_url|.

The API base URL is: http://dss_host:dss_port/public/api/

Request and response formats
===============================

For POST and PUT requests, the request body must be JSON, with the Content-Type header set to application/json.

For almost all requests, the response will be JSON.

Whether a request succeeded is indicated by the HTTP status code. A 2xx status code indicates success, whereas a 4xx or 5xx status code indicates failure. When a request fails, the response body is still JSON and contains additional information about the error.


Authentication
============================

Authentication on the REST API is done via the use of :doc:`API keys <keys>`. API keys can be managed through the DSS administration UI.

The API key can be sent using either HTTP Bearer Token Authentication or Basic Authentication:

* When using Bearer Token Authentication, use the API key as the token
* When using Basic Authentication, leave the username blank and use the API key as the password

Authorization
===============================

Each API key has access rights and scopes. DSS has a simple UI to edit API key permissions, as JSON objects.

There are two kinds of API keys for the DSS REST API.

For more information about API keys, see :doc:`keys`

Methods reference
======================

The reference documentation of the API is available at |api_doc_url|

The API base URL is: http://dss_host:dss_port/public/api/