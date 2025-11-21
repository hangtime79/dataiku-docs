Fleet Manager Instances
#######################

Instances are the DSS instances that Fleet Manager will manage.

Create an instance
==================


.. code-block:: python

    import dataikuapi

    key_id = "<my key id>"
    key_secret = "<my key secret>"

    # <Cloud vendor> is either AWS, Azure or GCP
    client = dataikuapi.FMClient<Cloud vendor>("https://localhost", key_id, key_secret)

    my_template_id = "ist-default"
    my_network_id = "vn-default"
   
    # create an instance
    creator = client.new_instance_creator("My new designer", my_template_id, my_network_id, "dss-11.0.3-default")
    dss = creator.create()

    # provision the instance
    status = dss.reprovision()
    res = status.wait_for_result()



Reference documentation
=======================

.. autosummary:: 
    dataikuapi.fm.instances.FMInstance
    dataikuapi.fm.instances.FMInstanceCreator
    dataikuapi.fm.instances.FMAWSInstance
    dataikuapi.fm.instances.FMAWSInstanceCreator
    dataikuapi.fm.instances.FMAzureInstance
    dataikuapi.fm.instances.FMAzureInstanceCreator
    dataikuapi.fm.instances.FMGCPInstance
    dataikuapi.fm.instances.FMGCPInstanceCreator
    dataikuapi.fm.instances.FMInstanceEncryptionMode
    dataikuapi.fm.instances.FMInstanceStatus
    dataikuapi.fm.instances.FMSnapshot
