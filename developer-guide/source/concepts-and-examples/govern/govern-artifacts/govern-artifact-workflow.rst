Govern Artifact Workflow
########################

Workflow management has changed in Dataiku Govern 13.5.0
`artifact.status.stepId` is now deprecated. While it's still supported in a best-effort way, some behaviors can be not totally supported anymore. Please use `artifact.workflow` instead.

New artifact property `artifact.workflow` structure
===================================================

.. code-block:: json

    {
        "workflow": {
            "steps": {
                "development": {
                    "status": "FINISHED",
                    "visible": true
                },
                "review": {
                    "status": "SKIPPED",
                    "visible": false
                },
                "deployment": {
                    "status": "ONGOING",
                    "visible": true
                },
                "production": {
                    "status": "NOT_STARTED",
                    "visible": true
                }
            }
        }
    }

Note that since it is a JSON object, these steps are not ordered. If you want to manipulate them in proper order, you must iterate over the `blueprintVersion.workflowDefinition.stepDefinitions` property.

.. code-block:: python

    from dataikuapi import GovernClient

    govern_client = GovernClient(host, api_key)
    artifact = govern_client.get_artifact('ar.5').get_definition().get_raw()
    blueprint_version = govern_client.get_blueprint(artifact.get('blueprintVersionId').get('blueprintId')).get_version(artifact.get('blueprintVersionId').get('versionId')).get_definition().get_raw()
    for step_definition in blueprint_version.get('workflowDefinition', {}).get('stepDefinitions', []):
        artifact_step = artifact.get('workflow', {}).get('steps', {}).get(step_definition.get('id'), {})
        step_status = artifact_step.get('status')
        step_visibility = artifact_step.get('visible')
        print('Step %s %s is visible : %s' % (step_definition.get('id'), step_status, step_visibility))


Legacy `artifact.status.stepId` behavior
========================================

The `artifact.status.stepId` will be set according to the `artifact.workflow` following those priority rules :

        1. null if no workflow on artifact's blueprint version
        2. null if workflow is not started (only not started steps)
        3. the current ongoing step id if there is one
        4. the id of the first not started step
        5. the last finished step id if all steps are finished


If the current ongoing step is not visible anymore, the workflow will not have a visible ongoing step. The `artifact.status.stepId` will be the next not started visible step id. The only way to actually put the workflow on this step is to use the new `artifact.workflow` property.

The `artifact.status.stepId` is now null when creating an artifact, if no `artifact.status.stepId` or `artifact.workflow` is provided. If some custom hooks were defined this way, they might not function anymore.
