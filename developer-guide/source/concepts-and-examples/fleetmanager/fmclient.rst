The main FMClient class
#######################
The REST API Python client makes it easy to write client programs for the Fleet Manager REST API in Python. The REST API Python client is in the ``dataikuapi`` Python package.

The client is the entrypoint for many of the capabilities listed in this chapter.

Creating a Fleet Manager client
===============================

To work with the API, a connection needs to be established with Fleet Manager, by creating an ``FMClient`` object. Once the connection is established, the ``FMClient`` object serves as the entry point to the other calls.

Depending on your cloud provider, you will have to create the dedicated ``FMClient``:

* a ``FMClientAWS`` for Amazon Web Services
* a ``FMClientAzure`` for Microsoft Azure
* a ``FMClientGCP`` for Google Cloud Platform

To connect you will need to provide the URL of your Fleet Manager server, and a key identifier and secret

.. code-block:: python

    import dataikuapi

    key_id = "<my key id>"
    key_secret = "<my key secret>"

    client = dataikuapi.FMClientAWS("https://localhost", key_id, key_secret)

    client = dataikuapi.FMClientAzure("https://localhost", key_id, key_secret)

    client = dataikuapi.FMClientGCP("https://localhost", key_id, key_secret)

    # client is now a FMClient and can perform all authorized actions.
    # For example, list the Dataiku instances in the fleet for which you have access
    client.list_instances()



Reference API doc
=================

.. autosummary::
    dataikuapi.fmclient.FMClient
    dataikuapi.fmclient.FMClientAWS
    dataikuapi.fmclient.FMClientAzure
    dataikuapi.fmclient.FMClientGCP
