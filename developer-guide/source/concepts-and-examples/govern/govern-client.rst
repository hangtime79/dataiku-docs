The main GovernClient class
###########################

The REST API Python client makes it easy to write client programs for the Dataiku Govern REST API in Python. The REST API Python client is in the ``dataikuapi`` Python package.

The client is the entrypoint for many of the capabilities listed in this chapter.

Creating a Govern client
========================

To work with the API, a connection needs to be established with Dataiku Govern, by creating an ``GovernClient`` object. Once the connection is established, the ``GovernClient`` object serves as the entry point to the other calls.

To use the Python client from outside Dataiku Govern, simply install it from pip.

.. code-block:: sh

    pip install dataiku-api-client

This installs the client in the system-wide Python installation,
so if you are not using virtualenv, you may need to replace ``pip`` by ``sudo pip``.

Note that this will always install the latest version of the API client. You might need to request a version compatible with your version of Dataiku Govern.

When connecting from the outside world, you need an API key. See :doc:`refdoc:governance/publicapi/keys` for more information on how to create an API key and the associated privileges.

You also need to connect using the base URL of your Dataiku Govern instance.

.. code-block:: python

    import dataikuapi

    host = "http(s)://GOVERN_HOST:GOVERN_PORT"
    apiKey = "Your API key secret"
    client = dataikuapi.GovernClient(host, apiKey)

    # client is now a GovernClient and can perform all authorized actions.
    # For example, list the blueprints for which the API key has access
    client.list_blueprints()

Disabling SSL certificate check
-------------------------------

If your Dataiku Govern has SSL enabled, the package will verify the certificate. In order for this to work, you may need to add the root authority that signed the Govern SSL certificate to your local trust store. Please refer to your OS or Python manual for instructions.

If this is not possible, you can also disable checking the SSL certificate by using ``GovernClient(host, apiKey, insecure_tls=True)``


Reference documentation
=======================

.. autosummary:: dataikuapi.govern_client.GovernClient
