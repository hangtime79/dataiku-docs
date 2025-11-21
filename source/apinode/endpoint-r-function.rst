Exposing a R function
###########################

.. contents::
	:local:

You can expose any R function as a endpoint on the API node. Calling the endpoint will call your function with the parameters you specify and return the results of the function.

This might look similar to the :doc:`R prediction endpoint <endpoint-r-prediction>`, but there are a few key differences:

* An R prediction endpoint has a strict concept of input records, and output prediction. It must output a prediction, and thus can only be used for prediction-like use cases. In contrast, a R function can do any kind of action and return any form of result (or even no result). For example, you can use a R function endpoint to store data in a database, a file, ...
* Since there is no concept of input records, you cannot use the :doc:`dataset-based enrichment features <enrich-prediction-queries>` in a R function endpoint

Creating the R function endpoint
======================================

To create a R function endpoint, start by creating an API service from the API Designer.

* Go to the project homepage
* Go to the API Designer and create a new service
* Give an identifier to your API Service. This identifier will appear in the URL used to query the API
* At this point, the API Service is created but not yet have any endpoint, i.e. it does not yet expose any capability. See :doc:`concepts` for what endpoints are.
* Create a new endpoint of type "R function". Give an identifier to the endpoint. A service can contain multiple endpoints (to manage several models at once, or perform different functions)

The URL to query the API will be like ``/public/api/v1/<service_id>/<endpoint_id>/run``.

Validate, you are taken to the newly created API Service in the API Designer component.

DSS prefills the Code part with a sample.

Structure of the code
-----------------------

The code of a R function endpoint must include at least one function, whose name must be entered in the "Settings" tab.

The parameters of the function will be automatically filled from the parameters passed in the endpoint call.

The result of the function must be JSON-serializable.

Using managed folders
-----------------------

A R function endpoint can optionally reference one or several DSS managed folders. When you package your service, the contents of the folders are bundled with the package, and your custom code receives the paths to the managed folder contents.

The paths to the managed folders (in the same order as defined in the UI) is available by calling the ``dkuAPINodeGetResourceFolders()``  function. This function returns a vector of character vectors, each one being the absolute path to the folder.

Testing your code
====================

Developing a custom function implies testing often. To ease this process, a "Development server" is integrated in the DSS UI.

To test your code, click on the "Deploy to Dev Server" button. The dev server starts and load your model. You are redirected to the Test tab where you can see whether your model loads.

You can also define *Test queries*, i.e. JSON objects akin to the ones that you would pass to the :doc:`api/user-api`. When you click on the "Play test queries" button, the test queries are sent to the dev server, and the result is printed.

R packages and versions
==============================

We strongly recommend that you use code environments for deploying custom endpoints if these packages use any external (not bundled with DSS) library.


Using a code env (recommended)
-------------------------------

Each custom endpoint can run within a given DSS :doc:`code environment </code-envs/index>`.

The code environment associated to an endpoint can be configured in the "Settings" tab of the endpoint.

If your endpoint is associated to a code environment, when you package your service, DSS automatically includes the definition of the virtual environment in the package. When the API service is loaded in the API node, DSS automatically installs the code environment according to the required definition.

This allows you to use the libraries and versions that you want for your custom model.

Using the builtin env (not recommended)
------------------------------------------

If you use external libraries by installing them in the DSS builtin env, they are *not* automatically installed in the API Node virtual env. Installing external packages in the API Node virtual env prior to deploying the package is the responsibility of the API node administrator.

Note that this means that:

* Two endpoints in the same service may not use incompatible third-party libraries or versions of third-party libraries
* If you need to have two services with incompatible libraries, you should deploy them on separate API node instances

Available APIs in a custom model code
------------------------------------------

Note that, while the ``dataiku.*`` libraries are accessible, most of the APIs that you use in :doc:`/code_recipes/r` will not work: the code is not running with the DSS Design node, so datasets cannot be read by this API. If you need to access DSS managed folders, see `Using managed folders`_ above.

Using your own libraries
=========================

You will sometimes need to write custom library functions (for example, shared between your custom training recipe and your custom model).

You can place these custom files in the project's "libraries" folder, or globally in the ``lib/R`` folder of the DSS installation. Both recipes and custom models can import modules defined there.

When you package a service, the whole content of the ``lib/R`` folders (both project and instance) are bundled in the package. Note that this means that it is possible to have several generations of the service running at the same time, using different versions of the custom code from ``lib/R``.


Performance tuning
====================

Whether you are using directly the API Node or the API Deployer, there are a number of performance tuning settings that can be used to increase the maximum throughput of the API node.

For the R function endpoint, you can tune how many concurrent requests your API node can handle.
This depends mainly on what your function does (its speed and in-memory size) and the available resources on the server(s) running the API node.

One allocated pipeline means one R process running your code, preloaded with your initialization code,
and ready to serve a function request. If you have 2 allocated pipelines (meaning 2 R processes),
2 requests can be handled simultaneously, other requests will be queued until one of the pipelines is
freed (or the request times out). When the queue is full, additional requests
are rejected.

Each R process will only serve a single request at a time.

It is important to set the "Cruise parameter" (detailed below):

* At a high-enough value to serve your expected reasonable peak traffic. If you set cruise too low, DSS will kill excedental R processes, and will need to recreate a new one just afterwards.

* But also at a not-too-high value, because each pipeline implies a running R process consuming the memory required by the model.

.. include:: _endpoint-tuning-pool.rst
