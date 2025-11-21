Govern Custom Pages
###################

Custom pages are pages that you can create and configure, and that will appear as new entries in the Govern top navigation bar.

Retrieve the custom pages
===========================



.. code-block:: python

    import dataikuapi

    host = "http(s)://GOVERN_HOST:GOVERN_PORT"
    apiKey = "Your API key secret"
    client = dataikuapi.GovernClient(host, apiKey)

    # list custom pages
    custom_pages = client.list_custom_pages()


Reference documentation
=======================

.. autosummary:: 
    dataikuapi.govern.custom_page.GovernCustomPageListItem
    dataikuapi.govern.custom_page.GovernCustomPage
    dataikuapi.govern.custom_page.GovernCustomPageDefinition
