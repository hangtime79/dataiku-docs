Authorized objects
##################

.. contents::
	:local:

:doc:`Workspaces </workspaces/index>`, :doc:`DSS dashboards </dashboards/index>` and :doc:`Data Collections </data-catalog/data-collections/index>` allow users who don't have permission to read or write the full content of a project to access a selected set of insights from the project.

Within a given project, these users (who can't read or write the full content of a project) have thus access to a subset of the objects.

This is handled by the "Authorized objects" mechanism, which is available in Project > Settings > Security > Authorized objects.

Both project-local objects and objects shared from other projects can be "authorized".

Scope
=====

The "Authorized objects" menu defines object permissions for project dashboard-only users as well as workspace members and Data Collection readers who don't have **Read project content** permission on the project.

* Authorized objects have an "authorization mode" that describes the level authorization granted on that object. Most objects can only have the READ mode, but other modes allow for specific behavior (DISCOVER, WRITE and RUN) and interact differently with dashboards, workspaces and Data Collections.

* "Authorized objects" are not tied to a group, but they work in combination with dashboard, workspace and Data Collection authorizations. For example, if an object has a READ authorization mode, it will be readable by:

  * *any* user that has the 'Read dashboards' authorization on the project
  * *any* user that is a member of a workspace the object is published on
  * *any* user that is a reader of a Data Collection the object is published to

* the READ mode allows a user to fully read the object. Importantly, it applies to an entire DSS object (for example, a dataset itself and its associated charts). So, if a dataset is in the list of "Authorized objects" with the READ authorization mode, it is technically possible, even for users who only have access to a limited view of the dataset (a single chart insight on the dashboard for example) to access the full content of the dataset.

Adding objects to "Authorized objects" list
===========================================

You can manage which objects are in the "Authorized objects" in Project > Security > Authorized objects. In order to achieve that you need the "Manage authorized objects" project-level permission. See :doc:`permissions` for more info.

If you publish an object on a dashboard (for example, a chart based on a dataset) that is not yet in the authorized objects list, you will get a warning:

* If you don't have "Manage authorized objects" permission, the warning will indicate that dashboard-only users won't be able to see this insight in the dashboard

* If you do have "Manage authorized objects" permission, the warning will include a prompt to add this item to the list of authorized objects of the project.

When you publish a dashboard or dataset in a workspace, you need a "Publish on workspaces" permission in the project. This permission also implies a "Manage authorized objects" permission and it will add the object automatically to the authorized objects list.

When you publish a dataset to a Data Collection, you will be reminded of its current authorization mode, and will have the option to increase it in order to improve the dataset discoverability.

In Project > Security > Authorized objects, it is also possible to authorize all objects present in a project for dashboards, workspaces, and Data Collections via the toggle at the top of the screen. In that case, all authorizations are considered to be READ authorized.

Details by object type
======================

Dataset
-------

Authorizing a dataset with the READ authorization mode makes it possible to view and create the following insights on this dataset:

* Dataset table
* Chart
* Comments
* Metrics

It also allows a member of a workspace it's published on to see the dataset content or insights about it. This also applies if the dataset is published on the workspace indirectly (eg. used in a dashboard that is itself published on the workspace).

Finally, the READ authorization on a dataset allows readers of a Data Collection it's published on to see the dataset in the Data Collection with full access to its details and the ability to preview it.

Even though the user interface only shows a limited amount of information about the dataset (only a limited chart is available on a dashboard, only the preview in a Data Collection...), authorizing a dataset with the READ mode makes it technically possible to access all data in the dataset. There is no "intra-dataset" security.


Datasets also have the DISCOVER authorization mode. This mode allows a reader of a Data Collection to see the dataset and a limited amount of metadata, but not to see its content, or even to preview it. It allows you to let users know that the dataset exists and see some detail about it, while still being able to control precisely who is allowed to access its content (see the :doc:`Data Collection documentation for details </data-catalog/data-collections/permissions-and-dataset-visibility>`).
Users can request access to the project or request the dataset to be shared if those features are enabled. It does not allow anything for 'dashboard-only' users or workspaces members, and it doesn't allow users to :ref:`quick share<quick-sharing>` the dataset even if it is activated.

Saved model
-----------

Authorizing a saved model with the READ authorization mode makes it possible to view and create the following insights on this model:

* Model report
* Comments
* Metrics

It gives dashboard-only users the ability to view all details (metrics, variables, ...) of the model.

Managed folder
--------------

Authorizing a managed folder with the READ authorization mode makes it possible to view and create the following insights on this folder:

* Managed folder (displays the content of the folder)
* Comments
* Metrics

It gives dashboard-only users the ability to view all files in the folder.

Jupyter notebook
----------------

Authorizing a notebook with the READ authorization mode makes it possible to view and create "Jupyter notebook" insights. These insights are based on *exports* of notebooks, not the notebook itself.

When a Jupyter notebook is dashboard-authorized, it does not give dashboard-only users the ability to execute code in the notebook, nor to create a new export of the notebook.

Web app
-------

Authorizing a web app with the READ authorization mode makes it possible to view and create the following insights on this webapp:

* Web app (displays the content of the webapp)
* Comments

It allows workspace and dashboard-only users to view the webapp. It does not allow them to modify the webapp or to view the backend code.

Scenario
--------

Authorizing a scenario with the READ authorization mode makes it possible to create an insight representing the history of runs of this scenario.

Authorizing a scenario with the RUN authorization mode makes it possible for dashboard-only users to run this scenario. This can lead to interesting use cases. For example, if a scenario takes as input a campaigns reference file on a FTP folder, the marketing team can update the file, and when they want, rerun a scenario directly from the dashboard.
