Govern Artifact Search
######################

The artifact search handler is used to search among artifacts.

Search for all the Govern Project artifacts
===========================================



.. code-block:: python

    import dataikuapi
    from dataikuapi.govern.artifact_search import GovernArtifactSearchQuery, GovernArtifactFilterBlueprints

    host = "http(s)://GOVERN_HOST:GOVERN_PORT"
    apiKey = "Your API key secret"
    client = dataikuapi.GovernClient(host, apiKey)

    # build a query
    govern_projects_query = GovernArtifactSearchQuery(artifact_filters=[GovernArtifactFilterBlueprints(blueprint_ids=['bp.system.govern_project'])])

    # build a request
    request = client.new_artifact_search_request(govern_projects_query)

    # perform the search (first batch)
    result_1 = request.fetch_next_batch()

    # continue the search (next batch)...
    result_2 = request.fetch_next_batch()


Reference documentation
=======================

.. autosummary:: 
    dataikuapi.govern.artifact_search.GovernArtifactSearchRequest
    dataikuapi.govern.artifact_search.GovernArtifactSearchResponse
    dataikuapi.govern.artifact_search.GovernArtifactSearchResponseHit
    dataikuapi.govern.artifact_search.GovernArtifactSearchQuery
    dataikuapi.govern.artifact_search.GovernArtifactSearchSource
    dataikuapi.govern.artifact_search.GovernArtifactSearchSourceAll
    dataikuapi.govern.artifact_search.GovernArtifactSearchSort
    dataikuapi.govern.artifact_search.GovernArtifactSearchSortName
    dataikuapi.govern.artifact_search.GovernArtifactSearchSortWorkflow
    dataikuapi.govern.artifact_search.GovernArtifactSearchSortField
    dataikuapi.govern.artifact_search.GovernArtifactSearchSortFieldDefinition
    dataikuapi.govern.artifact_search.GovernArtifactFilter
    dataikuapi.govern.artifact_search.GovernArtifactFilterBlueprints
    dataikuapi.govern.artifact_search.GovernArtifactFilterBlueprintVersions
    dataikuapi.govern.artifact_search.GovernArtifactFilterArtifacts
    dataikuapi.govern.artifact_search.GovernArtifactFilterFieldValue
    dataikuapi.govern.artifact_search.GovernArtifactFilterArchivedStatus
