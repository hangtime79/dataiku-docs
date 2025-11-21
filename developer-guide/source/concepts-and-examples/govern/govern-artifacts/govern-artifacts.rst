Govern Artifacts
################

Artifacts are all items in Dataiku Govern.
Note: to learn more about them, go to :doc:`refdoc:governance/navigation`.

List all artifact sign-offs
===========================



.. code-block:: python

    import dataikuapi

    host = "http(s)://GOVERN_HOST:GOVERN_PORT"
    apiKey = "Your API key secret"
    client = dataikuapi.GovernClient(host, apiKey)

    # retrieve a specific artifact by its ID
    artifact = client.get_artifact('ar.1773')

    # list all its sign-offs
    signoffs = artifact.list_signoffs()


Reference documentation
=======================

.. autosummary:: 
    dataikuapi.govern.artifact.GovernArtifact
    dataikuapi.govern.artifact.GovernArtifactDefinition
    dataikuapi.govern.artifact.GovernArtifactSignoffListItem
    dataikuapi.govern.artifact.GovernArtifactSignoff
    dataikuapi.govern.artifact.GovernArtifactSignoffDefinition
    dataikuapi.govern.artifact.GovernArtifactSignoffRecurrenceConfiguration
    dataikuapi.govern.artifact.GovernArtifactSignoffDetails
    dataikuapi.govern.artifact.GovernArtifactSignoffFeedbackListItem
    dataikuapi.govern.artifact.GovernArtifactSignoffFeedback
    dataikuapi.govern.artifact.GovernArtifactSignoffFeedbackDefinition
    dataikuapi.govern.artifact.GovernArtifactSignoffApproval
    dataikuapi.govern.artifact.GovernArtifactSignoffApprovalDefinition
