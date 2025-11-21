Documenting your API endpoints
##############################

API endpoints are meant to be integrated in a company ecosystem of applications. They are typically used to add machine learning predictions in other tools. As such, users need to know where and how to query them.

To fulfill this objective, you have the possibility to add a documentation to any API endpoint. This is done at the endpoint level and will produce a standard `OpenAPI JSON file <https://swagger.io/specification/v2/>`_ (version 2). Once served, not only can it be accessed by any API user, it can also be inserted into a corporate API registry.

Add OpenAPI documentation to an API endpoint
============================================
Adding documentation is done in :doc:`API Designer <concepts>`, in the **OpenAPI documentation** section on the left menu.

By default, OpenAPI documentation is disabled on endpoints. Once activated, you will see the actual JSON content on this screen.

For some supported prediction models, Dataiku is able to generate the OpenAPI documentation automatically. For all other cases, you will be provided with a template that needs to be completed.

.. image:: img/openapi-design.png

Once saved, this documentation is embedded in the API service that will be used for deployment.

Publishing OpenAPI documentation
================================
When deploying on an API node, if the service contains endpoints that have OpenAPI documentation, it will be accessible alongside the model endpoint on the API node using an alternate URL that is indicated in the deployment summary tile, on the top left corner of a deployment:

.. image:: img/openapi-deploy-uri.png

You can click on the magnifier icon to see the actual JSON being served. Of course, you can query it from outside Dataiku using a command like ``curl -X GET http://<deployment uri>/swagger`` (e.g. ``curl http://10.1.0.101:12000/public/api/v1/dku_service_mlflow/swagger``).

.. note::

	This additional endpoint will follow the security scheme in place for accessing the main endpoint. As such, if you have a key-based authentication to access the prediction endpoint, the same will be required for accessing the OpenAPI endpoint.

.. note::

	This additional URL for the API documentation is directly available only for deployment on static API nodes. If you want to leverage OpenAPI documentation in this context, you may query the API Deployer directly instead; see below. When deploying on a Kubernetes cluster, you may also make the documentation endpoint available through a custom ingress.


Listing documentation of all API endpoints
==========================================

In addition to serving the OpenAPI file on a specific URL, Dataiku allows you to query all documentation directly on the node where the API Deployer sits, using standard Python APIs, particularly ``DSSAPIDeployerDeployment.get_open_api``.

.. code-block:: python

	import dataiku
	import pprint
	
	pp = pprint.PrettyPrinter(indent=4)
	client = dataiku.api_client()
	adpl = client.get_apideployer()
	
	open_api_json_list = []
	for dpl in adpl.list_deployments():
	    try:
	        json = dpl.get_open_api()
	        open_api_json_list.append(json.get())
	        print(f"Adding OpenAPI documentation for deployment {id(dpl)}")
	    except Exception as e:
	        print(e)
	        continue
	
	print("Number of deployments with OpenAPI documentation enabled : " + str(len(open_api_json_list)))   
	pp.pprint(open_api_json_list)
