Code Studios
############

..
  this code samples has been verified on DSS: 14.2.0-alpha3
  Date of check: 11/09/2025

  this code samples has been verified on DSS: 13.2.0
  Date of check: 04/10/2024

The API offers methods to:

* Create and list code studios
* Start/stop them and trigger file synchronizations

For code studio templates, the API offers methods to:

* list code studio templates
* build them


Build a code studio template
============================

.. code-block:: python
    
    client = dataiku.api_client()
    
    template_id = "my_template_id"
    
    # Obtain a handle on the code studio template
    my_template = client.get_code_studio_template(template_id)
    
    # Build the template. This operation is asynchronous
    build_template = my_template.build()
    build_template.wait_for_result()


Reference documentation
========================

Classes
-------

.. autosummary:: 
    dataikuapi.dss.admin.DSSCodeStudioTemplateListItem
    dataikuapi.dss.admin.DSSCodeStudioTemplate
    dataikuapi.dss.admin.DSSCodeStudioTemplateSettings
    dataikuapi.dss.codestudio.DSSCodeStudioObject
    dataikuapi.dss.codestudio.DSSCodeStudioObjectConflicts
    dataikuapi.dss.codestudio.DSSCodeStudioObjectListItem
    dataikuapi.dss.codestudio.DSSCodeStudioObjectSettings
    dataikuapi.dss.codestudio.DSSCodeStudioObjectStatus
    dataikuapi.dss.future.DSSFuture

Functions
---------
.. autosummary::
    ~dataikuapi.dss.admin.DSSCodeStudioTemplate.build
    ~dataikuapi.DSSClient.get_code_studio_template
    ~dataikuapi.dss.future.DSSFuture.wait_for_result