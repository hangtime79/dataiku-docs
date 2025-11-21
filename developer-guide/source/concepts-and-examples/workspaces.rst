Workspaces
##########

..
  this code samples has been verified on DSS: 14.2.0-alpha3
  Date of check: 10/09/2025

  this code samples has been verified on DSS: 13.2.0
  Date of check: 04/10/2024


You can interact with the Workspaces through the API.

Basic operations
================

Listing workspaces
------------------

.. code:: python
	
	workspaces = client.list_workspaces(True)
	# Returns a list of DSSWorkspace
	for workspace in workspaces:
		# Access to main information in the workspace
		print("Workspace key: %s" % workspace.workspace_key)
		print("Display name: %s" % workspace.get_settings().display_name)
		print("Description: %s" % workspace.get_settings().description)
		print("Permissions: %s" % workspace.get_settings().permissions) # Returns a list of DSSWorkspacePermissionItem
		# You can also list the objects in a workspaces
		print("Objects: %s" % workspace.list_objects())

Modifying workspace
-------------------

.. code-block:: python

	from dataikuapi.dss.workspace import DSSWorkspacePermissionItem

	workspace = client.get_workspace("WORKSPACE_KEY")
	settings = workspace.get_settings()
	settings.permissions = [*settings.permissions, DSSWorkspacePermissionItem.member_user("LOGIN"), DSSWorkspacePermissionItem.contributor_group("GROUP")]
	settings.save()

Deleting a workspace
--------------------

.. code-block:: python
	
	workspace = client.get_workspace("WORKSPACE_KEY")
	workspace.delete()

Adding and deleting the objects in a workspace
===================================================

.. code-block:: python
	
	workspace = client.get_workspace("WORKSPACE_KEY")
	workspace_objects = workspace.list_objects()
	for workspace_object in workspace_objects:
		workspace_object.remove()
	
	workspace.add_object(client.get_project("PROJECT_KEY").get_dataset("DATASET_NAME")) # To add a dataset
	workspace.add_object(client.get_project("PROJECT_KEY").get_wiki().get_article("ARTICLE"))  # To add an article
	workspace.add_object(client.get_app("APP_ID")) # To add an app
	workspace.add_object({"htmlLink": {"name": "Dataiku", "url": "https://www.dataiku.com/", "description": "Dataiku website"}}) # You can also specify the content as a dict, here we add a link


Reference documentation
=======================

Classes
-------

.. autosummary::
    dataikuapi.dss.workspace.DSSWorkspace
    dataikuapi.dss.workspace.DSSWorkspaceObject
    dataikuapi.dss.workspace.DSSWorkspaceSettings
    dataikuapi.dss.workspace.DSSWorkspacePermissionItem

Functions
---------

.. autosummary::
    ~dataikuapi.dss.workspace.DSSWorkspace.add_object
    ~dataikuapi.dss.workspace.DSSWorkspace.delete
    ~dataikuapi.dss.workspace.DSSWorkspace.get_settings
    ~dataikuapi.DSSClient.get_workspace
    ~dataikuapi.dss.workspace.DSSWorkspace.list_objects
    ~dataikuapi.DSSClient.list_workspaces