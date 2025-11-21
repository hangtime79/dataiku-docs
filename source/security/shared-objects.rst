Shared objects
##############

.. contents::
	:local:

In DSS, projects are the main unit of permissions: groups are granted project-level permissions.
Projects are also the main unit of the Flow: a job builds datasets, models, and folders of a project, from other sources in the project.

There are cases, however, when you want to have objects (datasets, models, folders, model evaluation stores, ...) that are created in a project but used in another project.

* In some of these cases, the same users will have access to both projects. This multiple-projects architecture is then most useful to keep smaller manageable projects. For example, you could want to have an "upstream" project where the initial data preparation takes place and a "downstream" project where the business analysis takes place

* In other cases, different users have access to both projects. For example, you could have an "upstream" project which contains raw, non-anonymized data, with access restricted to a small number of trusted employees. This upstream project produces aggregated anonymized datasets that you want to make available to a large number of business projects, with more relaxed access rights.

Whether there is a security concern or not, cross-project usage of objects is configured in the "Shared objects" settings of the source project.

Quick and managed sharing
=========================

Depending on how you prefer to manage permissions on a given object, two sharing mechanisms are available:

* :ref:`Managed sharing<managed-sharing>`: only users with `Manage shared objects` permissions can share the object from the source project to another project. For each object, they will need to configure to which projects it is shared.
* :ref:`Quick sharing<quick-sharing>`: users with `Manage shared objects` permissions can decide to activate quick sharing on an object. In this case, all users who can see the object will be able to use it and add it to their projects without any other intervention.

.. _managed-sharing:

Sharing objects between projects via managed sharing
====================================================

To share an object from project A to project B with managed sharing, you need to have the `Manage shared objects` permission on project A. See :doc:`permissions` for more information.

To see and manage the whole list of shared objects from a project, go to **Project > Security > Shared objects** screen. For each object, you can configure the projects it is shared with.

You can also share individual objects from their Actions menu ("Share" button).

.. _quick-sharing:

Sharing objects between projects via quick sharing
==================================================

Quick sharing can be enabled on any shareable object of a project by a user with `Manage shared objects` permission on this project. This can be done from the Project's top-level dropdown > Security > Shared objects screen. The object needs to be added to the list of shared objects beforehand. There is no need to select a target project when quick sharing is enabled on an object. 


If quick sharing has been enabled on an object, any user who has the ability to read this object's content (through the project of origin, through a workspace, through a Data Collection, through another project where it has been shared…) will be able to use it directly in another project. They can do so via the "Share" button from the Right Hand panel of the object or the "Use" button in the Data Catalog or the "Search DSS Items" page.

A user who can see an item but cannot read its content is, however, not allowed to quick share it. This is the case for a dataset that is authorized with the DISCOVER authorization mode and can be found in a Data Collection by a user who has no other access to it.

To deactivate quick sharing for an object, you can go to its original project's top-level dropdown > Security > Shared objects screen or manage sharing rules via the "Share" button from the right panel of the object. Deactivating quick sharing for an object won't unshare the object from projects with which it was already shared.

You can unshare an object shared via quick sharing by removing the desired sharing rule on the original project's top-level dropdown > Security > Shared objects screen, or via the shared object's Actions menu in the target project ("Delete" button), the same way you would do for an object shared through managed sharing.

.. note::

   Quick sharing can be disabled for all projects by DSS administrators (in Administration > Settings > Other > Misc. > Access & request).


Permissions on shared objects
=============================

When an object is shared from project A to project B, analysts of project B have read-only access to the object.

Dataset
-------

Analysts of project B can:

* View the dataset's data, with arbitrary sampling settings
* Use it in recipes
* Build charts on it
* Use it in a visual analysis
* Build machine learning models on it
* Use it in notebooks
* Export it (if they have "Export datasets data" permission in project B)
* Put it on a dashboard

They cannot:

* View or change the settings of the dataset
* Build the dataset
* Clear the dataset
* View or change the metrics
* "Analyse" in explore on the full data (only on the sample)

Managed folder
--------------

Analysts of project B can:

* View the contents of the folder
* Use it in recipes
* Use it in notebooks
* Put it on a dashboard

They cannot:

* Upload new files or remove files
* Build the folder
* View or change the metrics

Saved model
-----------

Analysts of project B can:

* View the reports of the model
* Use it in a scoring or evaluation recipe
* Put it on a dashboard

They cannot:

* Retrain the model
* Modify the active version
* Remove old versions
* View or change the metrics


Agents & Agent tools
--------------------
Analysts of project B can:

* Use the following Agent tools without access to project A:

   * Knowledge Bank Search
   * Model Predict
   * API endpoint
   * LLM Mesh Query using an LLM from a connection, a fine-tuned LLM, or a retrieval-augmented LLM (whose underlying model fulfills the same condition)
   * Dataset Lookup
   * Dataset Append
   * Calculator
   * Send message

* Use Agents and other tools (including LLM Mesh Query using an Agent) if they have at least "Read project content" access to project A


Other objects
-------------
Scenarios, Jupyter notebooks, Webapps and R Markdown reports can only be added to a dashboard by analysts of project B.

Wiki articles, Visual analyses, SQL notebooks, recipes, API services and bundles cannot be shared.

Initiating an object-sharing request
====================================

You can request to use in your projects, any object that you can already access. This includes:

* datasets and models contained in projects where you have the `Read project content` permission
* datasets you can access through dashboards
* datasets you can access through workspaces
* datasets you can access through Data Collections (including datasets that are only discoverable)

You can do so through a "Share (Request)" button on the right panel which opens a modal.

You then have to select a target project where the object will be shared. 

Only projects on which you have `Write project content` permission are available as a target.

.. note::	

	To be able to request access to objects, the option *Requests to use objects* must be enabled, either by an administrator in the instance's settings in **Other > Misc. > Access & requests** with the option 
	or by a project administrator on a project level in **Project > Security > Shared objects**.


Managing an object-sharing request
==================================

Project administrators and users with `Manage shared objects` project permission can manage sharing requests from within the project's security section or by handling the request in the requests inbox. 

.. note::	

	Automatic request status updates

	In the following cases, the status of the request will be automatically updated in the requests inbox:

	* Request is considered as approved if the object is shared with the target project (regardless of how it's done)
	* Request is rejected if the target project is deleted, the object is deleted, or if the requester is deleted
	* Request is deleted if the object's project is deleted
