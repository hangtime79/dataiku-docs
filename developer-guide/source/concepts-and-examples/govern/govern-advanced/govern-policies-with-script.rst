Scripts for Governance Policies
###############################

When using **scripts** to define governance policies, you write the logic in a single Python script that is executed for all item types where the governance mode is set to "**Use script**". This includes:

- Projects
- Bundles
- Models
- Model versions

.. seealso::
    For the complete list of supported item types and a detailed explanation of their behavior, please see :doc:`Types of Govern items <refdoc:governance/types-govern-items>`.

The script's output is communicated via the ``handler.script_output`` object, which determines whether the item should be governed, hidden, or left untouched, along with any related configuration. This enables automated and policy-driven governance workflows across your platform.

This page describes how to populate ``handler.script_output`` for various governance scenarios.
In the code examples below, the term *artifact* can be found as the technical name for items.

Accessing Artifact Metadata
===========================

Since governance behavior may differ across artifact types, it is essential to identify and handle the current artifact type accordingly.

You can access metadata about the artifact currently being processed via the ``handler.enrichedArtifact`` object. The most commonly used attributes include:

.. code-block:: python

   # Get the artifact type by its blueprint ID
   artifact_type = handler.enrichedArtifact.blueprint.id  # e.g. "bp.system.dataiku_project"

   # Get the unique ID of the artifact
   artifact_id = handler.enrichedArtifact.artifact.id  # e.g. "ar.123"

   # Get a dictionary of metadata fields attached to the artifact
   fields = handler.enrichedArtifact.artifact.fields  # e.g. {"tags": ["test"], "governed_by": "ar.1337"}

   # Get the node id of the artifact
   node_id = handler.enrichedArtifact.artifact.fields.get("node_id")  # e.g. "dss_node"

These properties allow you to selectively apply logic depending on the artifact's type or attributes.

Governance Actions
==================

Governing Artifacts
-------------------

Artifacts can be governed automatically  or as a suggested action when managing the artifact manually.

When governing, you typically associate the artifact with a **blueprint version**.

Automatically govern an artifact
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The artifact will be governed without user input using the provided blueprint.

.. code-block:: python

   handler.script_output.action = "GOVERN"
   handler.script_output.blueprintVersionId = {"blueprintId": "bp.system.govern_project", "versionId": "bv.system.default"}
   handler.script_output.status = "AUTO"

**Prefilling Artifact Fields**

When an artifact is being governed, you can prefill metadata fields to help users later on.

This is useful for providing default values for example.

.. code-block:: python

   handler.script_output.artifactPrefill.fields["fieldId"] = "myNewValue"


Suggest governing an artifact
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The artifact governance is proposed to the user when managing the artifact manually.

.. code-block:: python

   handler.script_output.action = "GOVERN"
   handler.script_output.blueprintVersionId = {"blueprintId": "bp.system.govern_project", "versionId": "bv.system.default"}
   handler.script_output.status = "SUGGESTED"

Governing projects with linked artifacts
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When governing **projects**, you have additional options to associate them with existing govern projects or link them to business initiatives.

.. note::
    These fields are available both in ``AUTO`` and ``SUGGESTED`` modes of governing

**Associate with an existing governed project**

If you want to govern two projects (e.g. synced from different nodes) with the same govern project, you can associate the second project to the existing govern artifact instead of creating a new one.

.. code-block:: python

   handler.script_output.action = "GOVERN"
   handler.script_output.status = "AUTO"
   handler.script_output.projectExistingArtifactId = "ar.1337"

**Link to a business initiative**

If you want to create a **new governed project**, you can link it to a business initiative artifact of your choice based on the context of the project being governed.

.. code-block:: python

   handler.script_output.action = "GOVERN"
   handler.script_output.blueprintVersionId = {"blueprintId": "bp.system.govern_project", "versionId": "bv.system.default"}
   handler.script_output.status = "AUTO"
   handler.script_output.projectBusinessInitiativeArtifactId = "ar.1337"

Hiding Artifacts
----------------

Artifacts can be hidden either automatically or as a suggested action when managing the artifact manually.

**Automatically hide an artifact**


Use this to immediately hide an artifact without user interaction.

.. code-block:: python

   handler.script_output.action = "HIDE"
   handler.script_output.status = "AUTO"

**Suggest hiding an artifact**

Use this to propose hiding the artifact, but allow the user to override the suggestion.

.. code-block:: python

   handler.script_output.action = "HIDE"
   handler.script_output.status = "SUGGESTED"

Customizing Child Artifact Behavior
-----------------------------------

Some artifact types, such as projects and models, have nested artifact (e.g., bundles, models, model versions). You can control governance or visibility on these child elements independently using the ``childrenConfiguration`` field.

.. note::

    - This field is available in all the types of actions (``DO_NOTHING``, ``HIDE``, ``GOVERN``)
    - This field is available both in ``AUTO`` and ``SUGGESTED`` statuses

**Custom child configuration for a project**

In this example, the script does nothing with bundles, governs the models automatically with the specified blueprint version, and suggests hiding model versions.

.. code-block:: python

   handler.script_output.action = "GOVERN"
   handler.script_output.blueprintVersionId = {"blueprintId": "bp.system.govern_project", "versionId": "bv.system.default"}
   handler.script_output.status = "AUTO"
   handler.script_output.childrenConfiguration = {
       "bundlesConfig": {
           "action": "DO_NOTHING",
       },
       "modelsConfig":  {
           "action": "GOVERN",
           "status": "AUTO",
           "blueprintVersionId": {"blueprintId": "bp.system.govern_model", "versionId": "bv.system.default"}
       },
       "modelVersionsConfig": {
           "action": "HIDE",
           "status": "SUGGESTED"
       },
   }

**Custom child configuration for a model**

Here, only model versions are configured, and the script suggests hiding them.

.. code-block:: python

   handler.script_output.action = "GOVERN"
   handler.script_output.blueprintVersionId = {"blueprintId": "bp.system.govern_model", "versionId": "bv.system.default"}
   handler.script_output.status = "AUTO"
   handler.script_output.childrenConfiguration = {
       "modelVersionsConfig": {
           "action": "HIDE",
           "status": "SUGGESTED"
       },
   }


Advanced Example
================

Example 1: Conditional Hiding and Governance
--------------------------------------------

This script applies governance logic based on artifact type and metadata:

- Projects:
    - Automatically hidden if they include the tag: "test".
    - Otherwise ignored.
- Bundles:
    - If linked to a governed project rated as "High" risk, governance is suggested using the system default blueprint.
    - Otherwise ignored.
- All other artifacts:
    - Explicitly ignored.

**Behavior Summary**

+------------------------+----------------------------------------------+-----------------------------+
| Artifact Type          | Condition                                    | Action                      |
+========================+==============================================+=============================+
| Project                | Contains tag `"test"`                        | Automatically hide          |
+------------------------+----------------------------------------------+-----------------------------+
| Project                | Does *not* contain `"test"`                  | Do nothing                  |
+------------------------+----------------------------------------------+-----------------------------+
| Bundle                 | Associated project has `"High"` risk rating  | Suggest governance          |
+------------------------+----------------------------------------------+-----------------------------+
| Bundle                 | Any other case                               | Do nothing                  |
+------------------------+----------------------------------------------+-----------------------------+
| Other artifact types   | —                                            | Do nothing                  |
+------------------------+----------------------------------------------+-----------------------------+

.. note::

    - This example uses the system default blueprint (``bv.system.default``) for bundle governance.
    - The script uses ``handler.client`` to look up associated project and governance metadata.

**Code**

You can find below the script implementation:

.. code-block:: python

   from govern.core.autogovernance_handler import get_autogovernance_handler

   handler = get_autogovernance_handler()

   def handle_project():
       fields = handler.enrichedArtifact.artifact.fields
       tags = fields.get("tags", [])

       if "test" in tags:
           handler.script_output.action = "HIDE"
           handler.script_output.status = "AUTO"
       else:
           handler.script_output.action = "DO_NOTHING"

   def handle_bundle():
       artifact = handler.enrichedArtifact.artifact
       dku_project_id = artifact.fields.get("dataiku_project")

       if dku_project_id is None:
           handler.script_output.action = "DO_NOTHING"
           return None

       dku_project_json = (
           handler.client.get_artifact(dku_project_id)
           .get_definition()
           .get_raw()
       )

       govern_project_id = dku_project_json.get("fields", {}).get("governed_by")

       if govern_project_id is None:
           handler.script_output.action = "DO_NOTHING"
           return None

       govern_project_json = (
           handler.client.get_artifact(govern_project_id)
           .get_definition()
           .get_raw()
       )

       risk_rating = govern_project_json.get("fields", {}).get("qualification_risk_rating")

       if risk_rating == "High":
           handler.script_output.action = "GOVERN"
           handler.script_output.blueprintVersionId = {"blueprintId": "bp.system.govern_bundle", "versionId": "bv.system.default"}
           handler.script_output.status = "SUGGESTED"
       else:
           handler.script_output.action = "DO_NOTHING"

   if handler.enrichedArtifact.blueprint.id == "bp.system.dataiku_project":
       handle_project()
   elif handler.enrichedArtifact.blueprint.id == "bp.system.dataiku_bundle":
       handle_bundle()
   else:
       handler.script_output.action = "DO_NOTHING"

