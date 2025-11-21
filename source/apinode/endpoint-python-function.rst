Exposing a Python function
###########################

.. contents::
	:local:

You can expose any Python function as a endpoint on the API node. Calling the endpoint will call your function with the parameters you specify and return the results of the function.

This might look similar to the :doc:`Python prediction endpoint <endpoint-python-prediction>`, but there are a few key differences:

* A Python prediction endpoint has a strict concept of input records, and output prediction. It must output a prediction, and thus can only be used for prediction-like use cases. In contrast, a Python function can do any kind of action and return any form of result (or even no result). For example, you can use a Python function endpoint to store data in a database, a file, ...
* Since there is no concept of input records, you cannot use the :doc:`dataset-based enrichment features <enrich-prediction-queries>` in a Python function endpoint

Creating the Python function endpoint
======================================

To create a Python function endpoint, start by creating an API service from the API Designer.

* Go to the project homepage
* Go to the API Designer and create a new service
* Give an identifier to your API Service. This identifier will appear in the URL used to query the API
* At this point, the API Service is created but not yet have any endpoint, i.e. it does not yet expose any capability. See :doc:`concepts` for what endpoints are. 
* Create a new endpoint of type "Python function". Give an identifier to the endpoint. A service can contain multiple endpoints (to manage several models at once, or perform different functions)

The URL to query the API will be like ``/public/api/v1/<service_id>/<endpoint_id>/run``.

Validate, you are taken to the newly created API Service in the API Designer component.

DSS prefills the Code part with a sample

Structure of the code
----------------------

The code of a Python function endpoint must include at least one function, whose name must be entered in the "Settings" tab.

The parameters of the function will be automatically filled from the attributes of the object passed in the endpoint call. The function's parameters list *need* to be the same as the object's attributes list. 

For example if the object passed in the endpoint call has the following structure: 

.. code-block:: none

	{
	   "age": 35,
	   "days": 344,
	   "price": 600
	}

Then the function's signature must be the following:

.. code-block:: python

	def my_api_function(age, days, price):

Since this can get quite tedious when the attribute's list evolves or get too long, you can use the following workaround:

.. code-block:: python

	def api_py_function(z=0, **data):

The result of the function must be JSON-serializable.

Using managed folders
-----------------------

A Python function endpoint can optionally reference one or several DSS managed folders. When you package your service, the contents of the folders are bundled with the package, and your custom code receives the paths to the managed folder contents.

The paths to the managed folders (in the same order as defined in the UI) is available in a ``folders`` global variable which is transparently available in your code.

For example, the following code loads a pickle file from the 2nd managed folder at startup, and uses it in the ``my_api_function`` API function

.. code-block:: python

	import cPickle as pickle
	import os.path

	folder_path = folders[1]
	file_path = os.path.join(folder_path, "mydata.pkl")

	with open(file_path) as f:
		data = pickle.load(f)

	def my_api_function(myparam):
		return data.do_something(myparam)

Testing your code
====================

Developing a custom function implies testing often. To ease this process, a "Development server" is integrated in the DSS UI.

To test your code, click on the "Deploy to Dev Server" button. The dev server starts and loads your function. You are redirected to the Test tab where you can see whether your function loads.

You can also define *Test queries*, i.e. JSON objects akin to the ones that you would pass to the :doc:`api/user-api`. When you click on the "Play test queries" button, the test queries are sent to the dev server, and the result is printed.

Python packages
=================

We strongly recommend that you use code environments for deploying custom function packages if these packages use any external (not bundled with DSS) library.


Using a code env (recommended)
-------------------------------

Each custom endpoint can run within a given DSS :doc:`code environment </code-envs/index>`.

The code environment associated to an endpoint can be configured in the "Settings" tab of the endpoint.

If your endpoint is associated to a code environment, when you package your service, DSS automatically includes the definition of the virtual environment in the package. When the API service is loaded in the API node, DSS automatically installs the code environment according to the required definition.

This allows you to use the libraries that you want for your custom model.

Using the builtin env (not recommended)
------------------------------------------

If you use external libraries by installing them in the DSS builtin env, they are *not* automatically installed in the API Node virtual env. Installing external packages in the API Node virtual env prior to deploying the package is the responsibility of the API node administrator.

Note that this means that:

* Two endpoints in the same service may not use incompatible third-party libraries or versions of third-party libraries
* If you need to have two services with incompatible libraries, you should deploy them on separate API node instances

Performance tuning
====================

Whether you are using directly the API Node or the API Deployer, there are a number of performance tuning settings that can be used to increase the maximum throughput of the API node.

For the Python function endpoint, you can tune how many concurrent requests your API node can handle. 
This depends mainly on what your function does (its speed and in-memory size) and the available resources on the server(s) running the API node.

One allocated pipeline means one Python process running your code, preloaded with your initialization code,
and ready to serve a function request. If you have 2 allocated pipelines (meaning 2 Python processes),
2 requests can be handled simultaneously, other requests will be queued until one of the pipelines is
freed (or the request times out). When the queue is full, additional requests
are rejected.

Each Python process will only serve a single request at a time.

It is important to set the "Cruise parameter" (detailed below):


* At a high-enough value to serve your expected reasonable peak traffic. If you set cruise too low, DSS will kill excedental Python processes, and will need to recreate a new one just afterwards.

* But also at a not-too-high value, because each pipeline implies a running Python process consuming the memory required by the model.

.. include:: _endpoint-tuning-pool.rst
