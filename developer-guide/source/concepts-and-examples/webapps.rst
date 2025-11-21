Webapps
##########

..
  this code samples has been verified on DSS: 13.2.0
  Date of check: 04/10/2024
  this code samples has been verified on DSS: 14.1.0
  Date of check: 09/09/2025

The webapps API can control all aspects of managing a webapp.


Example use cases
=================

In all examples, ``project`` is a :class:`dataikuapi.dss.project.DSSProject` handle, obtained using :meth:`~dataikuapi.DSSClient.get_project` or :meth:`~dataikuapi.DSSClient.get_default_project`

List the webapps of a project and get a handle for the first one
----------------------------------------------------------------

By default, :meth:`~dataikuapi.dss.project.DSSProject.list_webapps` returns a list of dict items describing the webapps of a project.
From the dict item, the :class:`~dataikuapi.dss.webapp.DSSWebApp` handle can be obtained using the :meth:`~dataikuapi.dss.webapp.DSSWebAppListItem.to_webapp` method.
Documentation of the :meth:`~dataikuapi.dss.project.DSSProject.list_webapps` and :meth:`~dataikuapi.dss.project.DSSProject.get_webapp` methods can be found in the :doc:`API projects documentation </api-reference/python/projects>`.

.. code-block:: python

    project_webapps = project.list_webapps()
    my_webapp_dict = project_webapps[0]
    print("Webapp name : %s" % my_webapp_dict["name"])
    print("Webapp id : %s" % my_webapp_dict["id"])
    my_webapp = project_webapps[0].to_webapp()

Get a webapp by id, check if the webapp is running and if not, start it
-----------------------------------------------------------------------

A handle to a webapps state :class:`~dataikuapi.dss.webapp.DSSWebAppBackendState` object can be obtained using the :meth:`~dataikuapi.dss.webapp.DSSWebApp.get_state` method.

.. code-block:: python

    my_webapp = project.get_webapp(my_webapp_id)
    if (not my_webapp.get_state().running):
        my_webapp.start_or_restart_backend()


Stop a webapp backend
----------------------
.. code-block:: python

    my_webapp = project.get_webapp(my_webapp_id)
    my_webapp.stop_backend()


Get the settings of a webapp to change its name
-----------------------------------------------

A handle to a webapps settings :class:`~dataikuapi.dss.webapp.DSSWebAppSettings` object can be obtained using the :meth:`~dataikuapi.dss.webapp.DSSWebApp.get_settings` method.

.. code-block:: python

    my_webapp = project.get_webapp(my_webapp_id)
    settings = my_webapp.get_settings()
    print("Current webapp name : %s" % settings.data["name"])
    settings.data["name"] = "new webapp name"
    print("New webapp name : %s" % settings.data["name"])
    settings.save()


Reference documentation
========================

Classes
-------

.. autosummary::
    dataikuapi.dss.project.DSSProject
    dataikuapi.dss.webapp.DSSWebApp
    dataikuapi.dss.webapp.DSSWebAppBackendState
    dataikuapi.dss.webapp.DSSWebAppListItem
    dataikuapi.dss.webapp.DSSWebAppSettings

Functions
---------

.. autosummary::
    ~dataikuapi.DSSClient.get_default_project
    ~dataikuapi.DSSClient.get_project
    ~dataikuapi.dss.webapp.DSSWebApp.get_settings
    ~dataikuapi.dss.webapp.DSSWebApp.get_state
    ~dataikuapi.dss.project.DSSProject.get_webapp
    ~dataikuapi.dss.project.DSSProject.list_webapps
    ~dataikuapi.dss.webapp.DSSWebAppSettings.save
    ~dataikuapi.dss.webapp.DSSWebApp.start_or_restart_backend
    ~dataikuapi.dss.webapp.DSSWebApp.stop_backend
    ~dataikuapi.dss.webapp.DSSWebAppListItem.to_webapp