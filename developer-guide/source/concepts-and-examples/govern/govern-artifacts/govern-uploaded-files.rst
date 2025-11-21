Retrieve files from Govern artifacts
#####################################

Download an uploaded file
===========================

.. code-block:: python

    import dataikuapi

    host = "http(s)://GOVERN_HOST:GOVERN_PORT"
    apiKey = "Your API key secret"
    client = dataikuapi.GovernClient(host, apiKey)

    # retrieve a specific artifact of type govern project by its ID
    artifact = client.get_artifact('ar.1773')

    # get the first uploaded file stored in the related_docs field
    uf = client.get_uploaded_file(artifact.get_definition().get_raw()['fields']['related_docs'][0])

    # get the file description
    f_desc = uf.get_description()

    # retrieve the file as a stream
    f_stream = uf.download()


Reference API doc
==================

.. autosummary:: dataikuapi.govern.uploaded_file.GovernUploadedFile
