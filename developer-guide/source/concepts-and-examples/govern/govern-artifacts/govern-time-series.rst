Retrieve time series data from Govern artifacts
################################################

Get values
============

.. code-block:: python

    import dataikuapi

    host = "http(s)://GOVERN_HOST:GOVERN_PORT"
    apiKey = "Your API key secret"
    client = dataikuapi.GovernClient(host, apiKey)

    # retrieve a specific artifact of type dataiku model version by its ID
    artifact = client.get_artifact('ar.1773')

    # get the time series ID from a field
    ts = client.get_time_series(artifact.get_definition().get_raw()['fields']['evaluation_metrics_auc'])

    # get the time series values
    values = ts.get_values()


Reference API doc
==================

.. autosummary:: dataikuapi.govern.time_series.GovernTimeSeries
