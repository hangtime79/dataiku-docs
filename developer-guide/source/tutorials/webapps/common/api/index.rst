Creating an API endpoint from webapps
*************************************

In this tutorial, you will learn how to build an API from a web application's backend (called headless API)
and how to use it from code.
You will use an ``SQLExecutor`` to fetch information from a dataset, filtering them if needed.

You can use a headless web application to create an API endpoint for a particular purpose
that doesn’t fit well in the API Node.
For example, you may encounter this need if you want to use an SQLExecutor, access datasets, etc.
The API node is still the recommended deployment for real-time inference
and all use cases for which API-Node had been designed
(see :doc:`this documentation <refdoc:apinode/concepts>` for more information about API-Node)

Prerequisites
#############

.. tabs::

    .. group-tab:: Standard - Flask

        * Dataiku >= 13.1
        * A code environment with ``flask``.
        * You must download :download:`this dataset<./assets/pro_customers.csv>` and create an **SQL** dataset named ``pro_customers_sql``.


    .. group-tab:: Standard - FastAPI

        * Dataiku >= 14.1
        * A code environment with ``fastapi`` and ``uvicorn-worker``.
        * You must download :download:`this dataset<./assets/pro_customers.csv>` and create an **SQL** dataset named ``pro_customers_sql``.


    .. group-tab:: Dash

        * Dataiku >= 13.1
        * A code environment with ``dash``.
        * You must download :download:`this dataset<./assets/pro_customers.csv>` and create an **SQL** dataset named ``pro_customers_sql``.

Defining the routes
###################

The first step is to define the routes you want your API to handle.
A single route is responsible for a (simple) process.
Dataiku provides an easy way to describe those routes.
Relying on a python server using either Flask or FastAPI framework helps you return the desired resource types.
Check the **API access** in the web apps' settings to use this functionality, as shown in Figure 1.

.. _tutorial-webapps-common-api-api-access:

.. figure:: ./assets/tutorial-webapps-common-api-api-access.png
    :align: center
    :class: with-shadow image-popup
    :alt: Figure 1: Enabling API access.

    Figure 1: Enabling API access.


This tutorial relies on a single route handling some parameters to filter the data.
The ``get_customer_info`` will provide all data stored in the ``pro_customers_sql`` as raw text.
Filtering is done by adding an  ``id`` parameter to this route.
The answer will be in a JSON format.

For example, a query on ``get_customer_info`` will return the data stored in the dataset,
shown in :ref:`Table 1<tutorial-webapps-common-api-table1>`.

.. _tutorial-webapps-common-api-table1:
.. csv-table:: Table 1: customer ID
   :file: ./assets/pro_customers.csv
   :header-rows: 1

If you query ``get_customer_info?id=fdouetteau``, the API should return only the information about the customer with the ``id == fdouetteau``.

.. note::

    You can still use the backend to create a classical web application.
    Turning a web application into a headless one does not prevent developing a web application.

.. attention::
    The SQL query might be written differently depending on your SQL Engine.

.. tabs::

    .. group-tab:: Standard - Flask

        You must enable the Python backend with Flask Framework and define the route when using a standard web application,
        as shown in :ref:`Code 1<tutorial-webapps-common-api-standard-flask>`.

        .. literalinclude:: ./assets/flask.py
            :language: python
            :caption: Code 1: Python backend
            :name: tutorial-webapps-common-api-standard-flask

    .. group-tab:: Standard - FastAPI

        You must enable the Python backend with FastAPI Framework and define the route when using a standard web application,
        as shown in :ref:`Code 1<tutorial-webapps-common-api-standard-fastapi>`.

        .. literalinclude:: ./assets/fastapi.py
            :language: python
            :caption: Code 1: Python backend
            :name: tutorial-webapps-common-api-standard-fastapi

    .. group-tab:: Dash

        Once you have set the code env in the settings panel, you will define the route,
        as shown in :ref:`Code 1<tutorial-webapps-common-api-dash>`.

        .. literalinclude:: ./assets/dash.py
            :language: python
            :caption: Code 1: Python code of the Dash application
            :name: tutorial-webapps-common-api-dash

        When using Dash as a web application framework, you can access the defined routes directly without enabling API Access.
        Every web application is accessible via the URL ``https://<DATAIKU_ADDRESS>:<DATAIKU_PORT>/public-webapps/<PROJECT_KEY>/<WEBAPP_ID>/``.
        You will find more information on extracting those parameters in :ref:`the cUrl section<tutorial-webapps-common-api-curl-section>`.
        It does not mean that the web application is public; it means that the application is also exposed on this route.
        You can also use Vanity URL if you want.

Interacting with the newly defined API
######################################

To access the headless API, you must be logged on to the instance or have an API key that identifies you.
If you need help setting up an API key, please read :doc:`this tutorial<refdoc:apinode/security>`.
Then, there are several different ways to interact with a headless API.

.. _tutorial-webapps-common-api-curl-section:

.. tabs::


    .. group-tab:: cUrl

        Using cUrl requires an API key to access the headless API or an equivalent way of authenticating,
        depending on the authentication method set on the Dataiku instance.
        Once you have this API key, you can access the API endpoint with the following command.
        The ``WEBAPP_ID`` is the first eight characters (before the underscore) in the webapp URL.
        For example, if the webapp URL in Dataiku is ``/projects/HEADLESS/webapps/kUDF1mQ_api/view``, the ``WEBAPP_ID`` is
        ``kUDF1mQ`` and the ``PROJECT_KEY`` is ``HEADLESS``.

        .. code-block:: bash
            :caption: Code 2: ``cUrl`` command to fetch data
            :name: tutorial-webapps-common-api-curl

            curl -X GET --header 'Authorization: Bearer <USE_YOUR_API_KEY>' \
                'http://<DATAIKU_ADDRESS>:<DATAIKU_PORT>/web-apps-backends/<PROJECT_KEY>/<WEBAPP_ID>/get_customer_info'


    .. group-tab:: Python

        You can access the headless API using the Python API.
        Depending on whether you are inside Dataiku or outside, you will use the ``dataikuapi`` or
        the ``dataiku`` package, respectively, as shown in :ref:`Code 3<tutorial-webapps-common-api-python>`.

        .. literalinclude:: ./assets/python.py
            :language: python
            :caption: Code 3: Fetching data from the Python client
            :name: tutorial-webapps-common-api-python

Wrapping up
###########

If you need to give access to unauthenticated users, you can turn your web application into a public one,
as :doc:`this documentation <refdoc:webapps/public>` suggests.
Now that you understand how to turn a web application into a headless one, you can create an agent-headless API.
