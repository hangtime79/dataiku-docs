Governance checks with multi envs
#################################

Concept
=======

Dataiku Deployer has pre-deployment hooks which can be used to add additional checks when deploying.
In this example, we will perform a check prior to deployment that a specific sign-off is properly approved before deployment.

This code example is designed to work with the Project Deployer.
It must be written in an infrastructure settings, as a "pre-deployment" hook.


Code example
============

.. code-block:: python

    def execute(requesting_user, deployment_id, deployment_report, deployer_client, automation_client, deploying_user, deployed_project_key, **kwargs):
        
        host = '' # the govern instance host
        apikey = '' # a govern instance admin api key
        pre_prod_signoff_step_id = 'review' # to be changed to the step_id of the step which holds the sign-off to check for approval state
        
        import dataikuapi
        from dataikuapi.govern.artifact_search import GovernArtifactSearchQuery, GovernArtifactFilterArchivedStatus, GovernArtifactFilterBlueprints, GovernArtifactFilterFieldValue
        gc = dataikuapi.GovernClient(host, apikey)
        # gc = dataikuapi.GovernClient(host, apikey, insecure_tls=True) # this line can be be used instead to disable checking the SSL certificate
        deployer_node_id = deployer_client.get_instance_info().node_id

        # first get the synced deployment on govern
        results = gc.new_artifact_search_request(GovernArtifactSearchQuery(
            artifact_filters=[
                GovernArtifactFilterArchivedStatus(is_archived=False),
                GovernArtifactFilterBlueprints(blueprint_ids=['bp.system.project_deployer_deployment']),
                GovernArtifactFilterFieldValue(condition_type='EQUALS', condition=deployer_node_id, field_id='node_id', case_sensitive=True),
                GovernArtifactFilterFieldValue(condition_type='EQUALS', condition=deployment_id, field_id='deployment_id', case_sensitive=True),
            ]
        )).fetch_next_batch().get_response_hits()
        if len(results) <= 0:
            return HookResult.error('Deployment is not synced to govern, wait a bit more, or perform a manual full sync of deployer items in the settings.')
        govern_deployment = results[0].to_artifact()

        # get the related bundle
        dku_bundle_id = govern_deployment.get_definition().get_raw().get('fields', {}).get('dataiku_bundle', None)
        if dku_bundle_id is None:
            return HookResult.error('Govern deployment has no linked bundle, perform a manual full sync of deployer items in the settings.')
        dku_bundle = gc.get_artifact(dku_bundle_id)

        # get the related govern bundle (associated governance layer)
        gov_bundle_id = dku_bundle.get_definition().get_raw().get('fields', {}).get('governed_by', None)
        if gov_bundle_id is None:
            return HookResult.error('Associated bundle is not governed, artifact_id: ' + dku_bundle_id)

        # get the associated signoff
        signoff_def = gc.get_artifact(gov_bundle_id).get_signoff(pre_prod_signoff_step_id).get_definition().get_raw()

        # perform the signoff status check
        if signoff_def.get('status', None) != 'APPROVED':
            return HookResult.error('Pre-prod sign-off on bundle is not approved: ' + gov_bundle_id + ', stepid: ' + pre_prod_signoff_step_id)

        # if all good, return success
        return HookResult.success("Pre-prod sign-off is approved")
        
