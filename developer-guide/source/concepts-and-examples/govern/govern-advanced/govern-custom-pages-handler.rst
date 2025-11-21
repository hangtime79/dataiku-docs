Govern Custom Pages Handler
###########################

Admins can manage custom pages.

Retrieve the definition of a custom page
========================================



.. code-block:: python

    import dataikuapi

    host = "http(s)://GOVERN_HOST:GOVERN_PORT"
    apiKey = "Your API key secret"
    client = dataikuapi.GovernClient(host, apiKey)

    # retrieve the custom pages handler
    custom_pages_handler = client.get_custom_pages_handler()

    # get a custom page by its ID
    custom_page = custom_pages_handler.get_custom_page('cp.cust_page_1')

    # get its definition
    custom_page_def = custom_page.get_definition()

    # print its definition
    print(custom_page_def.get_raw())

    # retrieve custom pages order
    order = custom_pages_handler.get_order()

    # update custom pages order
    order = custom_pages_handler.save_order(["cp.id1", "cp.id2"])


Reference documentation
=======================

.. autosummary:: 
    dataikuapi.govern.admin_custom_pages_handler.GovernAdminCustomPagesHandler
    dataikuapi.govern.admin_custom_pages_handler.GovernAdminCustomPageListItem
    dataikuapi.govern.admin_custom_pages_handler.GovernAdminCustomPage
    dataikuapi.govern.admin_custom_pages_handler.GovernAdminCustomPageDefinition
