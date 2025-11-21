Dataiku and Govern items modifier helpers functions
###################################################


Delete all Dataiku artifacts linked to a node id
================================================

When changing or decommissioning a **Design**, an **Automation**, or a **Deployer** node you may want to clean up the synced Dataiku Items coming from the old node. Doing this one-by-one in Govern can be tedious if many items are involved. This helper shows how to:

* programmatically list Dataiku blueprints,
* search for artifacts linked to a given ``node_id``, and
* (optionally) delete them in bulk.

.. warning::
   This operation **permanently deletes** Govern artifacts. Use ``dry_run=True`` first to review what would be removed before executing a real deletion.

Helper function
---------------

The function below:

* discovers **Dataiku** blueprints dynamically via ``client.list_blueprints()``,
* restricts the search to blueprints whose IDs start with ``bp.system.dataiku_``,
* queries artifacts that also match the provided ``node_id`` (case-sensitive), and
* either returns the list (``dry_run=True``) or deletes them (``dry_run=False``).

.. code-block:: python

   import dataikuapi
   from dataikuapi.govern.artifact_search import (
       GovernArtifactSearchQuery,
       GovernArtifactFilterBlueprints,
       GovernArtifactFilterFieldValue,
   )

   def delete_dataiku_artifacts_by_node_id(client, node_id, page_size=1000, dry_run=False):
       """
       Delete all Govern artifacts synced from Dataiku (project, dataset, bundles, models, etc.)
       that are linked to the given Dataiku node id.

       Parameters
       ----------
       client : dataikuapi.GovernClient
           An authenticated Govern client.
       node_id : str
           The Dataiku node identifier to match (exact, case-sensitive).
       page_size : int
           Pagination size for the search request.
       dry_run : bool
           If True, nothing is deleted and the matching artifact IDs are returned.

       Returns
       -------
       list[str]
           List of artifact IDs matched (and deleted if dry_run is False).
       """

       # Helper to robustly extract the blueprint id from list items
       def _bp_id(bp):
           raw = bp.get_raw()
           return raw.get("blueprint",{}).get("id")

       # Discover Dataiku system blueprints dynamically
       dataiku_bp_ids = []
       blueprints = client.list_blueprints()
       for bp in blueprints:
           raw = bp.get_raw()
           bp_id = raw.get("blueprint", {}).get("id", "")
           if bp_id.startswith("bp.system.dataiku_"):
               dataiku_bp_ids.append(bp_id)


       if not dataiku_bp_ids:
           print("No Dataiku blueprints found; nothing to do.")
           return []

       # Build the artifact search
       query = GovernArtifactSearchQuery(artifact_filters=[
           GovernArtifactFilterBlueprints(blueprint_ids=dataiku_bp_ids),
           GovernArtifactFilterFieldValue(
               "EQUALS", field_id="node_id", condition=node_id, case_sensitive=True
           ),
       ])
       request = client.new_artifact_search_request(query)

       # Collect matching artifact ids
       artifact_ids = []
       has_next = True
       while has_next:
           raw = request.fetch_next_batch(page_size=page_size).get_raw()
           has_next = raw.get("hasNextPage", False)
           for ui in raw.get("uiArtifacts", []):
               artifact_ids.append(ui["artifact"]["id"])

       print(f"Matched {len(artifact_ids)} artifact(s).")

       if dry_run:
           # Only preview; do not delete
           return artifact_ids

       # Delete artifacts
       for aid in artifact_ids:
           print(f"Deleting artifact {aid} …")
           client.get_artifact(aid).delete()

       print(f"Deleted {len(artifact_ids)} artifact(s).")
       return artifact_ids

Usage examples
--------------

.. code-block:: python

   import os
   import dataikuapi

   govern_url = os.environ["GOVERN_URL"]
   govern_token = os.environ["GOVERN_TOKEN"]

   client = dataikuapi.GovernClient(host=govern_url, api_key=govern_token)

   # Preview what would be deleted
   to_delete = delete_dataiku_artifacts_by_node_id(client, node_id="dss1", dry_run=True)
   print(to_delete)

   # Proceed with deletion
   delete_dataiku_artifacts_by_node_id(client, node_id="dss1", dry_run=False)

