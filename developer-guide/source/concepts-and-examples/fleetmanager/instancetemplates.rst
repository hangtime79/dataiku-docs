Fleet Manager Instance Templates
################################

Instance settings templates allow to set several properties used when creating a new instance.

Create a new settings template
==============================

.. code-block:: python

    import dataikuapi

    key_id = "<my key id>"
    key_secret = "<my key secret>"

    # <Cloud vendor> is either AWS, Azure or GCP
    client = dataikuapi.FMClient<Cloud vendor>("https://localhost", key_id, key_secret)
    creator = client.new_instance_template_creator("MyTemplate")
    # set the properties of your template
    ...
    setting_template = creator.create()


Reference documentation
=======================

.. autosummary:: 
    dataikuapi.fm.instancesettingstemplates.FMInstanceSettingsTemplate
    dataikuapi.fm.instancesettingstemplates.FMInstanceSettingsTemplateCreator
    dataikuapi.fm.instancesettingstemplates.FMAWSInstanceSettingsTemplateCreator
    dataikuapi.fm.instancesettingstemplates.FMAzureInstanceSettingsTemplateCreator
    dataikuapi.fm.instancesettingstemplates.FMGCPInstanceSettingsTemplateCreator
    dataikuapi.fm.instancesettingstemplates.FMSetupAction
    dataikuapi.fm.instancesettingstemplates.FMSetupActionStage
    dataikuapi.fm.instancesettingstemplates.FMSetupActionAddJDBCDriverDatabaseType