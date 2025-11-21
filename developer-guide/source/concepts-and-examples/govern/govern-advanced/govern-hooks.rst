Automate actions with Govern Hooks
###################################

Hooks are used to automate actions related to artifacts in Dataiku Govern. They are written in Python and run during specified artifact lifecycle phases, including: 

- CREATE
- UPDATE
- DELETE

Here, we provide some use cases that demonstrate how to use hooks.

Make a field mandatory for a workflow step
============================================
By default, no fields in Dataiku Govern are mandatory for completing a workflow step. However, there might be a case where you want to check if a field is populated before a workflow step is marked as finished. 

In this situation, hooks can be used to define and automatically check this condition.

.. note::
    In the sample hook below, the fields that are mandatory only for setting a workflow step as finished should not be set as “Required” in the field configuration.

.. code-block:: python

    from govern.core.handler import get_handler

    def check_mandatory_step_fields(hookHandler, step_mandatory_field_ids):
    
        def get_ongoing_step_id(newEnrichedArtifact):
            workflow_steps = newEnrichedArtifact.artifact.json.get('workflow', {}).get('steps', {})
            for step in newEnrichedArtifact.blueprintVersion.json.get('workflowDefinition', {}).get('stepDefinitions', []):
                workflow_step = workflow_steps.get(step['id'], {})
                if workflow_step.get('status', 'NOT_STARTED') == 'ONGOING':
                    return step['id']
            return None

        def get_step_index(step_definitions, step_id):
            for i, v in enumerate(step_definitions):
                if v.get('id', None) == step_id:
                    return i

        def field_ids_from_view_component(view_component):
            if view_component is None:
                return []
            field_id = view_component.get('fieldId', '')
            if len(field_id) > 0:
                return [field_id]
            if view_component.get('type', '') == 'container':
                layout = view_component.get('layout', None)
                if layout is not None:
                    if layout.get('type', '') == 'sequential':
                        ret = []
                        for vc in layout.get('viewComponents', []):
                            ret = ret + field_ids_from_view_component(vc)
                        return ret
            return []

        def field_ids_from_step_id(nea, step_id):
            uiStepDefinition = nea.blueprintVersion.json.get('uiDefinition', {}).get('uiStepDefinitions', {}).get(step_id, None)
            if uiStepDefinition is None:
                return []
            view_id = uiStepDefinition.get('viewId', '')
            if len(view_id) <= 0:
                return []
            view = nea.blueprintVersion.json.get('uiDefinition', {}).get('views', {}).get(view_id, {})
            # if view is None or view.get('type', '') != 'card':  # Before 13.3.0
            if view is None:  # After 13.3.0
                return []
            return field_ids_from_view_component(view.get('viewComponent', None))

        # 2/ Then it retrieves all the associated fields by looking at the configuration of the view associated with the workflow step:
        def check_step(nea, step_id, mandatory_fields):
            field_ids = field_ids_from_step_id(nea, step_id)
            # 3/ Finally, looping through the fields attached to the workflow step, it checks the ones defined as mandatory for this step and raises an error if those fields are not set:
            for field_id in field_ids:
                if field_id in mandatory_fields:
                    field_value = nea.artifact.fields.get(field_id, None)
                    if field_value is None or (isinstance(field_value, str) and len(field_value) == 0) or (isinstance(field_value, list) and len(field_value) == 0):
                        handler.fieldMessages[field_id] = "field is mandatory in step id: " + step_id
                        handler.status = "ERROR"

        # 1/ This hook first aims to detect that the user is trying to set a specific workflow step as finished and retrieve the corresponding step id:
        if hookHandler.hookPhase == 'DELETE':
            return
        nea = hookHandler.newEnrichedArtifact
        if nea is None:
            return

        stepDefinitions = nea.blueprintVersion.json.get('workflowDefinition', {}).get('stepDefinitions', [])
        if len(stepDefinitions) <= 0:
            return

        # step_id = nea.artifact.json.get('status', {}).get('stepId', '') #  Before 13.5.0
        step_id = get_ongoing_step_id(nea)  # After 13.5.0
        if step_id is None:
            return

        step_index = get_step_index(stepDefinitions, step_id)

        for i in range(0, step_index):
            previous_step_id = stepDefinitions[i].get('id', '')
            if not previous_step_id in step_mandatory_field_ids:
                continue
            check_step(nea, previous_step_id, step_mandatory_field_ids[previous_step_id])

    handler = get_handler()

    # 4/ The way to attach fields to a workflow step is as follows:
    check_mandatory_step_fields(
        handler,
        {
            # Each step and corresponding fields are identified by their ids. 
            # You can add as many mandatory fields for any workflow step as you wish.
            "exploration": ["mandatory_exploration"],
            "qualification": ["mandatory_qualification", "mandatory_qualification_2"],
            "progress": ["mandatory_ref_progress"]
        }
    )


Automatically assign sign-off final approvers for a bundle
====================================================================

This hook should be added to the Govern Bundle hooks list, and should run on "UPDATE". As it cannot run on "CREATE" phase (as the link to the Dataiku Bundle won't be set yet), it can be backed up by another hook to trigger a "post-create" run (see below in this doc).
Please note it requires to fork the Govern Bundle template to modify the template / blueprint version, and this behaviour will work only for Govern Bundle using this forked template.
This hook requires the forked bundle to have a new field called "approvers", which is a list of users.

The logic implemented here is the following: 

- the list of potential final approvers of the bundle is defined by the list of the project contributors in DSS
- we don't want the bundle creator to be able to approve their own bundle, so the bundle creator is removed from this list
- the field "approvers" is filled with that list, and can be used to configure the sign-off final-approval permission rule

.. note::
    To get the contributors from DSS, the hook needs to have access to the DSS API key, see the "CONFIGURATION" section in the script below that needs to be changed.
    The users logins should match between DSS and Govern as the matching is done on the login only.

.. code-block:: python

    from govern.core.handler import get_handler
    import dataikuapi
    from dataikuapi.govern.artifact_search import GovernArtifactSearchQuery, GovernArtifactFilterBlueprints
    import logging
    import json
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    ### CONFIGURATION TO CHANGE
    DSS_URL = 'http://localhost:8086'
    DSS_API_KEY = 'dkuaps-XXXXX'
    ### /CONFIGURATION

    handler = get_handler()
    govern_bundle = handler.artifact

    def assign_contributors_as_approvers():
        dataiku_bundle_artifact_ids = govern_bundle.fields.get("dataiku_item", [])  

        if not isinstance(dataiku_bundle_artifact_ids, list) or len(dataiku_bundle_artifact_ids) == 0:  
            # we can't do anything, the govern bundle is not linked to a dataiku bundle (can happen if the dataiku bundle has been removed)
            return

        dataiku_bundle_artifact_id = dataiku_bundle_artifact_ids[0]
        dataiku_bundle_artifact = handler.client.get_artifact(dataiku_bundle_artifact_id)
        raw_artifact_bundle = dataiku_bundle_artifact.get_definition().get_raw()
        project_key = raw_artifact_bundle.get('fields', {}).get('project_key')
        created_by = raw_artifact_bundle.get('fields', {}).get('createdBy')

        # fetch the contributors from dataiku
        dss_client = dataikuapi.DSSClient(DSS_URL, DSS_API_KEY)
        # to turn off the SSL certificate check (for versions >v13.3.2)
        # dss_client = dataikuapi.DSSClient(DSS_URL, DSS_API_KEY, no_check_certificate=True)
        timeline = dss_client.get_project(project_key).get_timeline(item_count=0)
        contributors = timeline.get('allContributors')
        logger.info('found contributors for project ' + project_key + ': ' + json.dumps(contributors))

        # make the list of potential approvers
        potential_approvers = set([contributor.get('login') for contributor in contributors])
        potential_approvers.remove(created_by)
        
        all_users = get_existing_users_logins()
        all_users_logins = set(all_users.keys())
                
        # remove unexisting users (that exist in Dataiku but not in Govern) so the role assignment rule doesn't fail on that
        approvers_logins = potential_approvers.intersection(all_users_logins)
        
        # transform list of logins to list of user artifact ids
        approvers_artifact_ids = [all_users[approver_login] for approver_login in approvers_logins]
        logger.info('removing creator "' + created_by + '" and unexisting users, the list of approvers for ' + project_key + ' is: ' + str(approvers_logins) + ', mapped to artifacts: ' + str(approvers_artifact_ids))

        # update 'approvers' field with the computed list
        govern_bundle.fields['approvers'] = approvers_artifact_ids


    def get_existing_users_logins():
        request = handler.client.new_artifact_search_request(GovernArtifactSearchQuery(artifact_filters=[
            GovernArtifactFilterBlueprints(blueprint_ids=['bp.system.user'])
        ]))

        all_users = {}
        next_batch = True
        while next_batch:
            response = request.fetch_next_batch(page_size=1000).get_raw()
            next_batch = response.get('hasNextPage', False)

            for uiArtifact in response.get("uiArtifacts", []):
                if uiArtifact.get("uiArtifactDetails", {}).get("user") is not None:
                    all_users[uiArtifact["uiArtifactDetails"]["user"]["login"]] = uiArtifact['artifact']['id']
        
        return all_users

    # don't want to fail the artifact save if something goes wrong (e.g Dataiku not available)
    try:
        if handler.hookPhase == 'UPDATE' and govern_bundle.json.get('status', {}).get('stepId', '') == 'review':
            assign_contributors_as_approvers()
    except:
        logger.exception("Can't assign contributors")   


Trigger a post-create update hook
============================================

As some hooks don't have all the information needed on create, it's possible to workaround the issue by calling an update just after the creation has been commited.

The logic implemented here is the following: 

- Create a thread with a max lifetime
- Try to fetch the just-created artifact from the API. If it's found, it means that the creation transaction has been committed / completed successfully and we can move to the next step. If the artifact is not found, this step is repeated while the lifetime of the thread is not reached.
- Run a save from the API on the just-created artifact so it runs the update phase hooks

.. note::
    To trigger the update in Govern, the hook needs to have access to a persistent GOVERN API key (the one given by default to the hook is revoked after hook completion), see the "CONFIGURATION" section in the script below that needs to be changed.

.. code-block:: python

    from govern.core.handler import get_handler
    import dataikuapi
    import time
    import threading
    import logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    ### CONFIGURATION TO CHANGE
    WATCHDOG_TIMEOUT_MAX_FOR_POST_CREATE = 10 # seconds
    MY_GOVERN_ADMIN_API_KEY = "dkuaps-XXXXX"
    ####### /CONFIG

    def post_create(host, api_key, wd_to, ar_id):
        time.sleep(1) # start by sleeping a bit to let the create transaction finish
        time_started = time.time()
        thread_client = dataikuapi.GovernClient(host, api_key)
        while True:
            if time.time() > time_started + wd_to:
                # watchdog return anytime it waited for too long (default 10sec)
                logger.info("watchdog: Ending post-create thread")   
                return
            try:
                ar_def = thread_client.get_artifact(ar_id).get_definition()
                # in this example, this "post create hook" is a bit specific to updating the final approvers, but this line can be removed or adapted
                # won't run the update hook if we don't have the needed information for it to run correctly
                if isinstance(ar_def.get_raw()['fields'].get('dataiku_item', []), list) and len(ar_def.get_raw()['fields'].get('dataiku_item', [])) > 0:
                    ar_def.save() # run the save hook on the govern bundle without any changes to trigger the actual logic code
                    return # only need to run it once
            except:
                # logger.exception("Failed attempt to post-create") # useful to debug
                pass # if the get fails, do not nothing and keep trying
            time.sleep(1) # sleep to make sure the thread breaths

    handler = get_handler()
    hookPhase = handler.hookPhase

    if hookPhase == 'CREATE':
        my_govern_host = handler.client.host
        govern_bundle_artifact_id = handler.artifact.json.get('id', '')
        t1 = threading.Thread(target=post_create, args=(my_govern_host, MY_GOVERN_ADMIN_API_KEY, WATCHDOG_TIMEOUT_MAX_FOR_POST_CREATE, govern_bundle_artifact_id))
        t1.start()
