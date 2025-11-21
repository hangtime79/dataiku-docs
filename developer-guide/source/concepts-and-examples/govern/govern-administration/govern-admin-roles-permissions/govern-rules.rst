Bootstrap default groups matching provided roles
##################################################

Dataiku Govern comes with :doc:`several predefined roles and associated permissions <refdoc:security/govern-permissions>`. 
In a real use case, a company's users and groups cannot be created upfront because they usually depend on the company LDAP setup.

The following script aims to create groups matching each of the provided roles along with their related `role assignment rules <https://knowledge.dataiku.com/latest/mlops-o16n/govern/concept-roles-permissions.html#define-role-assignments>`_. Run this script to quickly try out Dataiku Govern with users **without considering security/permissions matters**.

After running this script, users can be put in these newly created groups to be assigned to the corresponding roles directly.

.. code-block:: python

    import dataikuapi

    # Connect with a GovernClient
    host = "http(s)://GOVERN_HOST:GOVERN_PORT"
    apiKey = "Your API key secret"
    client = dataikuapi.GovernClient(host, apiKey)

    # Create the groups
    client.create_group("readers", "Default group for read-only access")
    client.create_group("contributors", "Default group for contributor access")
    client.create_group("project_managers", "Default group for project manager access")

    # Setup the Role Assignment Rules
    rp = client.get_roles_permissions_handler()

    def setup_rars(blueprint_id):
        try:
            rp.create_role_assignments({ "blueprintId": blueprint_id })
        except:
            pass
        radef = rp.get_role_assignments(blueprint_id).get_definition()
        
        rar = radef.get_raw().get("roleAssignmentsRules", {})

        # set readers
        rar_list_reader = rar.get("ro.reader", [])
        rar_list_reader.append({
            "criteria": [],
            "userContainers": [{ "type": "group", "groupName": "readers" }],
            "fieldIds": []
        })
        rar["ro.reader"] = rar_list_reader

        # set contributors
        rar_list_contributor = rar.get("ro.contributor", [])
        rar_list_contributor.append({
            "criteria": [],
            "userContainers": [{ "type": "group", "groupName": "contributors" }],
            "fieldIds": []
        })
        rar["ro.contributor"] = rar_list_contributor

        # set project_managers
        rar_list_project_manager = rar.get("ro.project_manager", [])
        rar_list_project_manager.append({
            "criteria": [],
            "userContainers": [{ "type": "group", "groupName": "project_managers" }],
            "fieldIds": []
        })
        rar["ro.project_manager"] = rar_list_project_manager

        # re-create the rar
        radef.get_raw()["roleAssignmentsRules"] = rar
        radef.save()

    setup_rars("bp.system.business_initiative")
    setup_rars("bp.system.dataiku_project")

