Dataiku REST API
****************

At its core, Dataiku's public API is a collection of RESTful API endpoints that can be queried via HTTP.
Working at this fine-grained level can be cumbersome and require lots of code to manage the HTTP query properly.
While Dataiku's REST API endpoints are `fully documented <https://doc.dataiku.com/dss/api/latest/rest/>`__,
the use of this documentation may require a significant investment.

Prerequisites
#############

* Access to a Dataiku instance via an API key (see :doc:`the documentation <refdoc:publicapi/keys>` for explanations on how to generate one)

Introduction
############

For example, if you want to retrieve the schema of a given dataset, you would send
the following request:

.. code-block:: asc

    GET /public/api/projects/yourProjectKey/datasets/yourDataset/schema

    HTTP/1.1
    Host: yourinstance.com
    Content-Type: application/json
    Authorization: Bearer your-api-key

If it's successful, the response will look like this:

.. code-block:: asc

    HTTP/1.1 200 OK
    Content-Type: application/json;charset=utf-8
    DSS-Version: x.x.x
    DSS-API-Version 1

    {
        columns: [
            {"name": "Column1", type: "string", maxLength: -1},
            {"name": "Column2", type: "bigint"},
            ...
        ]
    }


Sending requests
################

All calls in the Dataiku public API are relative to the ``/public/api`` path on the Dataiku server.

For example, if your Dataiku server is available at ``http://DATAIKU_HOST:DATAIKU_PORT/``,
and you want to call the `List projects API <https://doc.dataiku.com/dss/api/latest/rest/#projects-projects-get>`__,
you must make a GET request on ``http://DATAIKU_HOST:DATAIKU_PORT/public/api/projects/``

Project list
^^^^^^^^^^^^

.. tabs::
    .. group-tab:: cUrl

        .. code-block:: bash

            curl --request GET \
              --url http://DATAIKU_HOST:DATAIKU_PORT/public/api/projects/ \
              --header 'Authorization: Bearer YOUR_USER_API_KEY' \
              --header 'Content-Type: application/json'

    .. group-tab:: javascript

        .. code-block:: javascript

            import axios from "axios";

            const options = {
              method: 'GET',
              url: 'http://DATAIKU_HOST:DATAIKU_PORT/public/api/projects/',
              headers: {
                'Content-Type': 'application/json',
                Authorization: 'Bearer YOUR_USER_API_KEY'
              }
            };

            axios.request(options).then(function (response) {
              console.log(response.data);
            }).catch(function (error) {
              console.error(error);
            });

    .. group-tab:: HTTP client

        .. figure:: ./assets/postman.png
            :align: center
            :class: with-shadow image-popup
            :alt: Figure 1: Postman request.

            Figure 1: Postman request.

