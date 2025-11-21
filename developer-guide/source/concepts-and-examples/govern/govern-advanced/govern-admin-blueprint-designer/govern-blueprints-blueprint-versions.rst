View blueprints and blueprint versions
########################################

Blueprint versions are templates describing the items in Dataiku Govern.
Several blueprint versions are gathered within the same blueprint that represents a logical concept.

List all blueprints
===================

.. code-block:: python

    import dataikuapi

    host = "http(s)://GOVERN_HOST:GOVERN_PORT"
    apiKey = "Your API key secret"
    client = dataikuapi.GovernClient(host, apiKey)

    # List the blueprints for which the API key has access
    client.list_blueprints()


Reference API doc
==================

.. autosummary:: 
    dataikuapi.govern.blueprint.GovernBlueprintListItem
    dataikuapi.govern.blueprint.GovernBlueprint
    dataikuapi.govern.blueprint.GovernBlueprintDefinition
    dataikuapi.govern.blueprint.GovernBlueprintVersionListItem
    dataikuapi.govern.blueprint.GovernBlueprintVersion
    dataikuapi.govern.blueprint.GovernBlueprintVersionTrace
    dataikuapi.govern.blueprint.GovernBlueprintVersionDefinition