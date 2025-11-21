Public API Keys
################

All calls to the DSS public API, either performed using :doc:`rest` or :doc:`devguide:api-reference/python/index` must be authenticated using API keys.

There are three kinds of API keys for the DSS REST API:

* Project-level API keys
* Global API keys
* Personal API keys

.. note::

	When using the API through the Python client from within DSS, you don't need an API key. You
	can obtain a Python client with ``dataiku.api_client()``. This client will automatically
	inherit all your personal access rights. In essence, it will behave as is you had used a
	personal API key, but without needing to actually create one.


Personal API keys
====================

Personal API keys are created by each user independently in Profile & Settings > API keys. They can be listed and deleted by admin, but can only be created by the end user.

A personal API key gives exactly the same permissions as the user who created it. For all purposes, a personal API key impersonates the user, and calls made using this personal API key behave as if they had been performed by the user. In timelines, Git log and audit log, calls performed using a personal API key will appear as having been performed by the user.

Some features in DSS are based on group-level security, and can thus only be performed by a personal API key, or a globally admin key (see below). This includes:

* Creating datasets on connections that have restrictive access
* Performing SQL queries on connections that have restrictive access

Project-level keys
====================

These keys give privileges on the content of the project only. They cannot give access to anything which is not in their project. Project-level keys are exported when you export a project.

Project-level keys are configured in the project settings (Project Home > Security > API Keys). When you create a new API Key, the permissions JSON objects are prefilled with sample data.

A project-level key actually provides two kinds of privileges:

* Project-wide privileges
* Per-dataset privileges

Project-wide permissions
---------------------------

The following project-wide permissions types can be set on a project-level key. Each of these permissions mirror the project-level permissions defined in :doc:`/security/permissions`. The relations between these permissions are also mirror of the project-level permissions (things like: Write conf implies Read conf).

* READ_CONF: Read the whole configuration of the objects in the project (but NOT the project itself)
* WRITE_CONF: Write the whole configuration of the objects in the project
* EXPORT_DATASETS_DATA
* SHARE_TO_WORKSPACE
* READ_DASHBOARDS
* WRITE_DASHBOARDS
* MODERATE_DASHBOARDS
* RUN_SCENARIOS
* MANAGE_DASHBOARD_AUTHORIZATIONS
* MANAGE_EXPOSED_ELEMENTS
* ADMIN: manage the whole project (get/set permissions and project metadata)

Dataset-specific permissions
------------------------------

In addition, on a project-level key, you can define some permissions that only apply to a set of datasets. This allows you to create very limited API keys that can only be used to read a small number of "published" datasets.

.. note::

	The Webapp builder in DSS and its Javascript API use project-level API keys with dataset-specific permissions

The following permissions can be granted on a set of datasets:

* READ_DATA
* WRITE_DATA
* READ_METADATA
* WRITE_METADATA
* READ_SCHEMA
* WRITE_SCHEMA

Associated user
----------------

Unlike personal API keys, project-level API keys are not equivalent to a DSS user. API keys have their own access rights, and calls performed by a project-level API key will appear as having been performed by this key.

For the sole purpose of :doc:`User Isolation Framework </user-isolation/index>`, it is possible to define an "associated user for impersonation" in the configuration of the API key. The identity of this user will be used to compute the impersonation rules for access to HDFS datasets. However, the key still needs to have proper permissions for the action to be granted.


Global API keys
=================

Global API keys are keys that can encompass several projects. Global API keys can only be created and modified by DSS administrators.

Global API keys are defined in Administration > Security > Global API keys

Global API keys are not bound to a project and are not exported.

Project-level permissions
---------------------------

A global API key can define project-level permissions on any project in DSS. This way, you can for example create a key that has READ_CONF permissions on one project and READ_CONF + WRITE_CONF on another project.

Global admin
--------------

This special permission gives global admin rights to this key. A global admin key has all permissions and all projects. It can also perform global DSS administration tasks:

* Manage users
* Manage log files
* Manage global variables


Associated user
----------------

Unlike personal API keys, project-level API keys are not equivalent to a DSS user. API keys have their own access rights, and calls performed by a project-level API key will appear as having been performed by this key.

For the sole purpose of :doc:`User Isolation Framework </user-isolation/index>`, it is possible to define an "associated user for impersonation" in the configuration of the API key. The identity of this user will be used to compute the impersonation rules for access to HDFS datasets. However, the key still needs to have proper permissions for the action to be granted.

