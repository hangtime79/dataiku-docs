Dataiku and Govern items getter helpers functions
#################################################

Helpers function definitions
============================

This document presents a set of helper functions for bridging Dataiku items with their Govern counterparts.


Retrieve a Dataiku Project
--------------------------
Fetches a Dataiku project, using a node ID and project key.

.. code-block:: python

    def get_dataiku_project_as_artifact(govern_client, node_id, project_key):
        """
        Retrieve the Dataiku project as an artifact from both a node ID and a project Key

        :param GovernClient govern_client: a govern client connected via the public API to the govern instance
        :param str node_id: the node ID of the project to look for
        :param str project_key: the project Key of the project to look for
        :return: the dataiku project as an artifact or None if not found
        :rtype: GovernArtifact or None
        """
        from dataikuapi.govern.artifact_search import GovernArtifactSearchQuery, GovernArtifactFilterArchivedStatus, GovernArtifactFilterBlueprints, GovernArtifactFilterFieldValue
        results = govern_client.new_artifact_search_request(GovernArtifactSearchQuery(
            artifact_filters=[
                GovernArtifactFilterArchivedStatus(is_archived=False),
                GovernArtifactFilterBlueprints(blueprint_ids=['bp.system.dataiku_project']),
                GovernArtifactFilterFieldValue(condition_type='EQUALS', condition=node_id, field_id='node_id', case_sensitive=True),
                GovernArtifactFilterFieldValue(condition_type='EQUALS', condition=project_key, field_id='project_key', case_sensitive=True),
            ]
        )).fetch_next_batch().get_response_hits()
        if len(results) == 0:
            return None
        return results[0].to_artifact()

.. _govern_from_dataiku_item:

Get the Govern Item of a Dataiku Item
-------------------------------------
Returns the Govern representation (project, bundle, model, or model version) that corresponds to a given Dataiku item.

.. code-block:: python

    def get_govern_item_from_dataiku_item(govern_client, dataiku_item):
        """
        Retrieve the Govern item (could be project, bundle, model, model version) corresponding to the Dataiku item

        :param GovernClient govern_client: a govern client connected via the public API to the govern instance
        :param GovernArtifact dataiku_item: the Dataiku item as input
        :return: the corresponding Govern item or None if not governed
        :rtype: GovernArtifact or None
        """
        definition = dataiku_item.get_definition()
        gb = definition.get_raw().get('fields', {}).get('governed_by', None)
        if gb is None:
            return None
        return govern_client.get_artifact(gb)

Get Dataiku Items of a Govern Item
----------------------------------
Retrieves the list of Dataiku items linked to a given Govern item.  
This is the reverse mapping, useful for exploring which Dataiku items are associated with a Govern item.

.. code-block:: python

    def get_dataiku_items_from_govern_item(govern_client, govern_item):
        """
        Retrieve the Dataiku items (could be project, bundle, model, model version) corresponding to the Govern item

        :param GovernClient govern_client: a govern client connected via the public API to the govern instance
        :param GovernArtifact govern_item: the Govern item as input
        :return: the list of corresponding Dataiku items (several dataiku projects can be governed by the same govern project, for other item types, there should be at max a single value in the list)
        :rtype: list of GovernArtifact
        """
        definition = govern_item.get_definition()
        dku_items = definition.get_raw().get('fields', {}).get('dataiku_item', [])
        return [govern_client.get_artifact(arid) for arid in dku_items]

.. _reference_list_as_artifacts:

Get Artifact from Field Reference
---------------------------------
Some artifact fields are **reference fields**: instead of storing data directly, they store one or more **artifact IDs** (e.g., ``ar.123``) that point to other items.
This helper reads such a field from an artifact and resolves each stored ID into a full ``GovernArtifact`` by fetching it via the Govern API.

.. code-block:: python

    def get_reference_list_as_artifacts(govern_client, artifact, field_id):
        """
        Retrieve the referenced items based on field (list of references) of an artifact

        :param GovernClient govern_client: a govern client connected via the public API to the govern instance
        :param GovernArtifact artifact: the item as input
        :param str field_id: the field ID of the reference list
        :return: the list of corresponding items
        :rtype: list of GovernArtifact
        """
        definition = artifact.get_definition()
        items = definition.get_raw().get('fields', {}).get(field_id, [])
        return [govern_client.get_artifact(arid) for arid in items]

List Bundles of a Govern Project
--------------------------------
Returns all Govern bundles associated with a given Govern project.  
Internally, it reuses :func:`get_reference_list_as_artifacts` (:ref:`reference_list_as_artifacts`)  to resolve the bundle links.

.. code-block:: python

    def get_govern_bundles(govern_client, govern_project):
        """
        Retrieve the list of govern bundles from a govern project

        :param GovernClient govern_client: a govern client connected via the public API to the govern instance
        :param GovernArtifact govern_project: the govern project as input
        :return: the list of govern bundles for this project
        :rtype: list of GovernArtifact
        """
        return get_reference_list_as_artifacts(govern_client, govern_project, 'govern_bundles')

List Models of a Govern Project
-------------------------------
Returns all Govern models associated with a given Govern project.  
Internally, it reuses :func:`get_reference_list_as_artifacts` (:ref:`reference_list_as_artifacts`) to resolve the model links.

.. code-block:: python

    def get_govern_models(govern_client, govern_project):
        """
        Retrieve the list of govern models from a govern project

        :param GovernClient govern_client: a govern client connected via the public API to the govern instance
        :param GovernArtifact govern_project: the govern project as input
        :return: the list of govern models for this project
        :rtype: list of GovernArtifact
        """
        return get_reference_list_as_artifacts(govern_client, govern_project, 'govern_models')

List Model Versions of a Govern Model
-------------------------------------
Returns all Govern model versions associated with a given Govern model.  
Internally, it reuses :func:`get_reference_list_as_artifacts` (:ref:`reference_list_as_artifacts`) to resolve the model version links.

.. code-block:: python

    def get_govern_model_versions(govern_client, govern_model):
        """
        Retrieve the list of govern model versions from a govern model

        :param GovernClient govern_client: a govern client connected via the public API to the govern instance
        :param GovernArtifact govern_model: the govern model as input
        :return: the list of govern model versions for this model
        :rtype: list of GovernArtifact
        """
        return get_reference_list_as_artifacts(govern_client, govern_model, 'govern_model_versions')

Retrieve Related Govern Projects from a Dataiku Project
-------------------------------------------------------

This helper function retrieves all **Govern projects** that correspond to the same underlying
Dataiku project across **Design** and **Automation** nodes, and returns
a ``GovernArtifact`` object for each related project.

Internally, it reuses :func:`get_govern_item_from_dataiku_item` (:ref:`govern_from_dataiku_item`) to resolve the govern item links.

.. code-block:: python

    def get_related_projects(govern_client, dataiku_project):
        """
        Retrieve the list of related govern projects from a dataiku project

        :param govern_client: a govern client connected via the public API to the govern instance
        :type govern_client: GovernClient
        :param dataiku_project: the dataiku project as input
        :type dataiku_project: GovernArtifact
        :return: the list of govern projects for this dataiku project
        :rtype: list[GovernArtifact]
        """
        from dataikuapi.govern.artifact_search import GovernArtifactSearchQuery, GovernArtifactFilterArchivedStatus, GovernArtifactFilterBlueprints, GovernArtifactFilterFieldValue

        fields = dataiku_project.get_definition().get_raw().get('fields',{})
        automation_node = fields.get('automation_node')

        node_id = None
        project_key = None
        results=[]

        if automation_node == True:
            node_id = fields.get('original_node_id')
            project_key = fields.get('original_project_key')

            if node_id and project_key:
                hits = govern_client.new_artifact_search_request(GovernArtifactSearchQuery(
                    artifact_filters=[
                        GovernArtifactFilterArchivedStatus(is_archived=False),
                        GovernArtifactFilterBlueprints(blueprint_ids=['bp.system.dataiku_project']),
                        GovernArtifactFilterFieldValue(
                            condition_type='EQUALS',
                            condition=node_id,
                            field_id='node_id',
                            case_sensitive=True
                        ),
                        GovernArtifactFilterFieldValue(
                            condition_type='EQUALS',
                            condition=project_key,
                            field_id='project_key',
                            case_sensitive=True
                        ),
                        GovernArtifactFilterFieldValue(
                            condition_type='EQUALS',
                            condition='true',
                            field_id='automation_node',
                            negate_condition=True,
                            case_sensitive=True
                        )
                    ]
                )).fetch_next_batch().get_response_hits()
                results.extend([hit.to_artifact() for hit in hits])
            else:
                results.append(dataiku_project)
        else:
            node_id = fields.get('node_id')
            project_key = fields.get('project_key')

        if node_id and project_key:
            hits = govern_client.new_artifact_search_request(GovernArtifactSearchQuery(
                artifact_filters=[
                    GovernArtifactFilterArchivedStatus(is_archived=False),
                    GovernArtifactFilterBlueprints(blueprint_ids=['bp.system.dataiku_project']),
                    GovernArtifactFilterFieldValue(
                        condition_type='EQUALS',
                        condition=node_id,
                        field_id='original_node_id',
                        case_sensitive=True
                    ),
                    GovernArtifactFilterFieldValue(
                        condition_type='EQUALS',
                        condition=project_key,
                        field_id='original_project_key',
                        case_sensitive=True
                    ),
                    GovernArtifactFilterFieldValue(
                        condition_type='EQUALS',
                        condition='true',
                        field_id='automation_node',
                        negate_condition=False,
                        case_sensitive=True
                    )
                ]
            )).fetch_next_batch().get_response_hits()
            results.extend([hit.to_artifact() for hit in hits])


        governed_results = [
            get_govern_item_from_dataiku_item(handler.client, item)
            for item in results
        ]

        return [r for r in governed_results if r is not None]

Few usages
==========

.. code-block:: python

    import dataikuapi

    host = "http(s)://GOVERN_HOST:GOVERN_PORT"
    apiKey = "Your API key secret"
    client = dataikuapi.GovernClient(host, apiKey)

    # search for a specific Dataiku project (could be None if not found)
    dku_project = get_dataiku_project_as_artifact(client, 'design_node_id', 'MY_PROJECT_KEY')
    print(dku_project.get_definition().get_raw())

    # get the associated Govern project tied to it
    govern_project = get_govern_item_from_dataiku_item(client, dku_project)
    print(govern_project.get_definition().get_raw())

    # get back the Dataiku projects tied to this Govern project
    # the returned value is a list since several dataiku project can be governed by the same govern project
    dataiku_projects = get_dataiku_items_from_govern_item(client, govern_project)
    for dkup in dataiku_projects:
        print(dkup.get_definition().get_raw())

    # list the govern bundles from the govern project
    bundles = get_govern_bundles(client, govern_project)
    for bundle in bundles:
        print(bundle.get_definition().get_raw())

