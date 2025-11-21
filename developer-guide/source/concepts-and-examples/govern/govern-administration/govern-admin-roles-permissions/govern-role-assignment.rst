Add a rule to assign a role to a new user
###########################################

.. code-block:: python

    import dataikuapi

    host = "http(s)://GOVERN_HOST:GOVERN_PORT"
    apiKey = "Your API key secret"
    client = dataikuapi.GovernClient(host, apiKey)

    # get the role and permissions editor
    rp_editor = client.get_roles_permissions_handler()

    # retrieve the role assignments for the Business initiative blueprint
    bi_ra = rp_editor.get_role_assignments('bp.system.business_initiative')

    # get the definition
    bi_ra_def = bi_ra.get_definition()

    # add a rule to assign the new user to the project manager role
    project_manager_def = bi_ra_def.get_raw()['roleAssignmentsRules'].get('ro.project_manager', [])
    project_manager_def.append({
      "criteria": [],
      "userContainers": [{"type": "user", "login": "new_user"}]
    })
    bi_ra_def.get_raw()['roleAssignmentsRules']['ro.project_manager'] = project_manager_def
    bi_ra_def.save()



