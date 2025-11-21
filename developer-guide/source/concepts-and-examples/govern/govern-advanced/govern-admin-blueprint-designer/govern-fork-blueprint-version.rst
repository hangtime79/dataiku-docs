Fork a Govern project blueprint version
#########################################

You can fork or create a new blueprint version from an existing blueprint version using the following Python code.

Fork the blueprint version
=============================

.. code-block:: python

    import dataikuapi

    host = "http(s)://GOVERN_HOST:GOVERN_PORT"
    apiKey = "Your API key secret"
    client = dataikuapi.GovernClient(host, apiKey)

    # get the blueprint designer
    blueprint_designer = client.get_blueprint_designer()

    # get the provided govern_project blueprint
    govern_project_bp = blueprint_designer.get_blueprint('bp.system.govern_project')

    # fork a blueprint version
    govern_project_new_version = govern_project_bp.create_version('my_new_version', name='My New Version', origin_version_id='bv.system.default')

    # add a field and save version
    new_ver_def = govern_project_new_version.get_definition()
    new_ver_def.get_raw()['fieldDefinitions']['new_field'] = {
      "description": "my new beautiful text field",
      "fieldType": "TEXT",
      "label": "my new field",
      "required": False,
      "sourceType": "STORE"
    }
    new_ver_def.save()
