Exposing a SQL query
###########################

.. contents::
	:local:

You can expose a parametrized SQL query as a DSS API node endpoint.  Calling the endpoint with a set of parameters will execute the SQL query with these parameters.

The DSS API node automatically handles pooling connections to the database, high availability and scalability for execution of your query.

.. note::

	Only "regular" SQL connections are possible. Hive and Impala are not supported.

.. note::

	You'll need to install the JDBC driver on the API node servers. The installation procedure is the same as for regular DSS design and automation nodes.

	If you are using API Deployer on a Kubernetes infrastructure, this is handled automatically based on the JDBC drivers present in the API Deployer node

Creating the SQL query endpoint
======================================

To create a SQL Query endpoint, start by creating an API service from the API Designer.

* Go to the project homepage
* Go to the API Designer and create a new service
* Give an identifier to your API Service. This identifier will appear in the URL used to query the API
* At this point, the API Service is created but not yet have any endpoint, i.e. it does not yet expose any capability. See :doc:`concepts` for what endpoints are. 
* Create a new endpoint of type "SQL Query". Give an identifier to the endpoint. A service can contain multiple endpoints (to manage several models at once, or perform different functions)

The URL to query the API will be like ``/public/api/v1/<service_id>/<endpoint_id>/query``.

Validate, you are taken to the newly created API Service in the API Designer component.

DSS prefills the Code part with a sample
In "Settings", select the connection you want to target

In "Query":

* Write your query, using '?' as the placeholder for parameters 
* Add one parameter name for each ? that you inserted in the query.

For example:

.. code-block:: sql

	select * from mytable where email = ?;

	Parameter names:
		* target_email


When you submit an API query with the "target_email" parameter set to "test@test.com", it will run the query ``select * from mytable where email = 'test@test.com'`` and return the results.

You must not surround the ``?`` markers by quotes, the database engine will handle that itself.

Non-SELECT statements
======================

It is possible to use non-SELECT statements (for example INSERT or DELETE). In that case, the result will not include columns and rows, but instead a ``updatedRows`` indicating how many rows were impacted by the query.

Transaction commit
-------------------

By default, DSS does not COMMIT the connection in a SQL query endpoint. You can activate the "post-commit" option to have DSS commit the connection after the execution of the query. This is required when using INSERT or DELETE statements.

Using multiple queries
========================

The code that you enter in the query field can include multiple SQL statements. For example, you could start by creating a temporary table, selecting from it and removing it. DSS automatically splits the query into statements.

However, the following rules apply:

* Only the last SELECT statement will receive the parameters. It is not possible to "spread" the parameters over multiple statements.
* If there is no SELECT statement, the last statement will receive the parameters.

Some complex use cases cannot fit these requirements, for example:

 * Creating a temporary table using the parameters
 * Selecting from it, possibly using more parameters

For this, you can use multiple queries. Click on the "Add a query" button, and enter the second code and parameter names. Each query can have different parameters, but they can also use the same parameter: if you use the same parameter name in two different queries, both will use the same parameter from the REST API query.

All queries are executed within the same connection so temporary tables will persist. Commit happens after each query if you enable the "post-commit" option.

Testing your queries
======================

To ease the process of testing your endpoints, a "Development server" is integrated in the DSS UI.

To test your code, click on the "Deploy to Dev Server" button. The dev server starts and load your model. You are redirected to the Test tab where you can see whether your model loads.

You can then define *Test queries*, i.e. JSON objects akin to the ones that you would pass to the :doc:`api/user-api`. When you click on the "Play test queries" button, the test queries are sent to the dev server, and the result is printed.


Defining the connection on the API node
=========================================

.. note::

	This is not applicable for Kubernetes deployments using the API Deployer

Before you can activate your service on a API node, the API node must have the definition of the connection (with the same name as it was on the design node)

Add the connection in a top-level ``remappedConnections`` in the API node's ``DATA_DIR/config/server.json``:

.. code-block:: json

	{
		"remappedConnections": {
			"MY-CONNECTION": {
				"type": "PostgreSQL",
				"params": {
					"host": "my-db-host",
					"db": "my-db",
					"user": "my-user",
					"password": "my-password"
				}
			},
			"MY-OTHER-CONNECTION": { "..." }
		},
		"..."
	}

The connection parameters to use can be found in the ``config/connections.json`` file in the DSS design or automation node. The password is encrypted on the design/automation node, you'll need to retype it in the API node ``DATA_DIR/config/server.json`` file.

Performance tuning
====================

It is possible to tune the behavior of SQL query endpoints on the API node side.
DSS maintains a pool of persistent connections to the database. These tuning settings are used to tune parameters of the connection pool to the database.

Without API Deployer
----------------------

You can configure this by creating a JSON file in the ``config/services`` folder in the API node's data directory.

.. code-block:: bash

    mkdir -p config/services/<SERVICE_ID>

Then create or edit the ``config/services/<SERVICE_ID>/<ENDPOINT_ID>.json`` file

This file must have the following structure and be valid JSON (the values shown here are the defaults):

.. code-block:: json

    {
        "sql" : {
            "connectionsEvictionTimeMS" : 60000,
            "evictionIntervalMS" : 30000,
            "maxPooledConnections": 10
        }
    }

Those parameters are all positive integers:

* ``connectionsEvictionTimeMS`` `(default: 60000)`: Connections that have not been used for that amount of time are closed

* ``evictionIntervalMS`` `(default: 30000)`: How often to check for connections that can be closed

* ``maxPooledConnections`` `(default: 10)`: Maximum number of connections that can be opened to the database

With API Deployer
------------------

You can configure the connections pool parameters for the endpoint in the Deployment settings, in the "Endpoints tuning" setting.

* Go to the Deployment Settings > Endpoints tuning
* Add a tuning block for your endpoint by entering your endpoint id and click Add
* Configure the parameters


* ``SQL eviction time`` `(default: 60000)`: Connections that have not been used for that amount of time are closed

* ``SQL eviction interval`` `(default: 30000)`: How often to check for connections that can be closed

* ``SQL max pool`` `(default: 10)`: Maximum number of connections that can be opened to the database
