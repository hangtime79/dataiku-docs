Main project permissions
#########################

.. contents::
  :depth: 2
  :local:


DSS uses a groups-based model to allow users to perform actions through it.

The basic principle is that users are added to groups, and groups have permissions on each project.

Per-project group permissions
===============================

On each project, you can configure an arbitrary number of groups who have access to this project.
Adding permissions to projects is done in the Permissions pane of the Security menu.

Each group can have one or several of the following permissions. By default, groups don't have any kind of access to a project.


Admin
-------

This group may perform any action on the project, including:

* change the permissions and owner of the project
* create project bundles

This permission implies all other permissions.

Edit permissions
----------------

This group may see and edit permissions of the project.

A user with this permission cannot grant or remove a permission that they do not have themselves (i.e. cannot grant "Read project content" to a user if they do not have that right)

This permission implies the "Read dashboards" permission.

Read project content
-----------------------

This group may see the Flow, access the datasets, read the recipes, ... More generally speaking, this group may read every configuration and data in this project.

This permission implies the "Read dashboards" permission.

Write project content
-----------------------

This group may read and write every configuration and data in this project. This includes the ability to create new datasets, recipes, ...

This also includes the ability to run all jobs in this project.

.. note::

	This permission is the "default" permission that you may want to give to your data team.

This permission implies the "Read project content", "Read dashboards", "Run scenarios" and "Write dashboards" permissions

Publish to Data Collections
---------------------------

This group may be able to publish datasets to :doc:`Data Collections </data-catalog/data-collections/index>`.
Note that DSS administrators must separately grant the global group permission to Publish to Data Collections, regardless of permission on the source project.

Publish on workspaces
---------------------

This group may be able to share objects (Dashboards, Datasets, Wiki pages) to :doc:`workspaces </workspaces/index>`.
Note that DSS administrators must separately grant the group permission to :doc:`share content </workspaces/managing>` into workspaces, regardless of source project.

Export datasets
-----------------

This group may click on the "Download" button to retrieve the content of a dataset.

.. warning::

	Disabling this permission removes the most obvious way to download whole datasets, but through various means, users who have at least "Read project content" will still be able to download datasets.

	If you absolutely want your users not to be able to retrieve the full content of datasets, do not give them access to the project.

Run scenarios
--------------

This group may run scenarios. They may not run jobs that are not part of a scenario. Only scenarios that have a "Run As" user may be run by users who only have this permission.

This permission is generally not very useful without the "Read project content" permission.

Read dashboards
----------------

This group may read dashboards that have been created. They may not modify anything. They can only read dashboard insights that use project objects that have been shared with them using :doc:`authorized-objects`.

Write dashboards
----------------

This group may create their own dashboards, using the project objects that have been shared with them using :doc:`authorized-objects`.

This permission implies "Read dashboards".


Manage authorized objects
---------------------------

This group may modify which objects of the project are usable by dashboard-only users through the :doc:`authorized-objects` and accessible through a workspace or a Data Collection.

This permission is generally not very useful without the "Read project content" permission. This permission is implied by the "Publish on workspaces" and "Publish to Data Collections" permissions.

The main use case for this permission is the following:

* A group of analysts and data scientists creates a Flow
* The data is of medium sensitivity so all dashboard users could use any of the Flow
* However, the dashboard users must not be able to break or modify the Flow
* Thus, the dashboard users (or a subgroup of them) has this permission to gain access to source datasets

Manage shared objects
------------------------

This group may modify which objects of the project are available in other projects through the :doc:`shared-objects`.

This permission is generally not very useful without the "Read project content" permission.

The main use case for this permission is the following:

* A group of analysts and data scientists creates a Flow
* The data is of medium sensitivity so all or some DSS users should be able to reuse it on other projects
* However, the other projects' users must not be able to break or modify the Flow
* Thus, a group of other project's users has permission to go in the project, and "pick" datasets to use in other projects.

Execute app
-----------

This permission is only exposed on projects converted into a :doc:`Dataiku application </applications/index>` or an :doc:`application-as-recipe </applications/application-as-recipe>`.

This group may execute the corresponding application if the application is configured to be instantiated only by user with
this permission. Else this permission is not needed.

Project owner
=============

In addition to the per-group access, each project has a single user who "owns" the project. Being the owner of a project does not grant any additional permissions compared to being in a group who has Administrator access to this project.

This owner status is used mainly to actually grant access to a project to the user who just created it.

.. _project-access:

Project visibility
==================

It is possible to allow all users to access a project's page displaying a limited amount of information about the project regardless of the users' permissions. The information displayed in this case includes the project image, name, short description, owner, tags and status. This is known as a "Discoverable" project. The opposite is a "Private" project, for whom having no read permissions implies the projects existance will not be apparent to a user at all.

Which projects are Discoverable is controlled in the "Project Visibility" setting on the **Administration > Settings > Access & requests** page. You can control the defaults (Private or Discoverable) when projects are created, or you can set all projects to Discoverable, or Private.

Discoverable projects appear in the :doc:`projects page </concepts/homepage/projects-page>`, in the Catalog, and in the "Search DSS Items" page for all users making them easily discoverable. If a user doesn't have access to a discoverable project, the project is denoted with a padlock symbol.

.. _per-project-single-user-permissions:

Per-project single user permissions
===================================

In addition to the per-group access, on each project, you can configure an arbitrary number of individual users who have access to this project.
Adding permissions to projects is done in the Permissions pane of the Security menu.

Each user can be granted the same kind of project permissions than groups above.
This is useful for a non-administrator to give access to a project to some users individually, without the need for those users to belong to specific groups.

.. warning::

	When using :doc:`/user-isolation/index` in "DSS-managed ACL" mode,
	HDFS ACLs are not supported for individual user permissions on projects.
	See :doc:`/user-isolation/capabilities/hadoop-impersonation`.


Sharing project via email
==========================

You can also invite non-DSS users to your project via email.

If a valid mail channel (e.g. SMTP) is configured in Administration > Settings > Notifications & Integrations, an invitation will be sent to the specified email.

Once the user registers with that email, they will be granted access to the project.

Invitations by email can be disabled on the **Administration > Settings > Access & requests** page.

Global group permissions
==========================

In addition to the per-project permissions, groups can also be granted several global permissions that apply to all DSS.

These permissions are configured in the settings screen of the group.


* Administrator: members of a group with this permission can perform any action on DSS. DSS administrators are implicitly administrators of all DSS projects and may access any project, even without explicitly being granted access through a project-group grant.

.. _projects-creation:

Projects creation
-------------------


* Create projects: members of a group with this permission can create their own projects, using a blank project, project duplication of project import

* Create projects using macros: members of a group with this permission can create projects using a :doc:`project creation macro </concepts/projects/creating-through-macros>`

* Create projects using templates: members of a group with this permission can create projects using predefined templates (Dataiku samples and tutorials)


* "Write in root project folder": members of a group with this permission can create folders and projects in the root folder, or move them to the root.

Workspaces
----------

* Create workspaces: members of a group with this permission can create their own workspaces.

* Publish on workspaces: members of a group with this permission can share objects to workspaces.

Data Collections
----------------

* Create Data Collections: members of a group with this permission can create Data Collections.

* Publish to Data Collections: members of a group with this permission can publish datasets to Data Collections.

Code execution
---------------

* "Write isolated code": members of a group with this permission can write code which will run with impersonated rights. This permission is only available when :doc:`User Isolation Framework </user-isolation/index>` is enabled.

* "Write unisolated code": members of a group with this permission can write code which will be executed with the UNIX privileges of the DSS UNIX user.

* "Create active Web content": members of a group with this permission can author Web content that is able to execute Javascript when viewed by other users. This includes webapps, Jupyter notebooks and RMarkdown reports


Code envs & Dynamic clusters
------------------------------

* "Manage all/own code envs": members of a group with this permission can create and manage :doc:`code environments </code-envs/index>`; their own, those they've been given administrative access to, and even others, if given the 'all' permission.

* "Manage all/own clusters": members of a group with this permission can create and manage clusters; their own, those they've been given administrative access to, and even others, if given the 'all' permission.


Advanced permissions
---------------------

* "Develop plugins": members of a group with this permission can create and edit :doc:`development plugins </plugins/reference/index>`.  Be aware that this permission could allow a hostile user to circumvent the permissions system.

* "Edit lib folders": members of a group with this permission can edit the Python & R libraries and the static web resources in the DSS instance.

* "Create personal connections": members of a group with this permission can create new connections to SQL, NoSQL, and Cloud storage.

* "View indexed Hive connections": members of a group with this permission can use the Data Catalog to view indexed Hive connections.

* "Manage user-defined meanings": members of a group with this permission can create instance-wide user-defined meanings, which will be accessible and usable by all DSS projects.


* "Create published API services": members of a group with this permission can create an API service endpoint and :doc:`publish it to a DSS API node through the DSS API Deployer </apinode/index>`.

.. _security.permissions.write_unsafe_code:

Write unisolated code: details
-------------------------------

For more information about enabling user isolation, see :doc:`User Isolation Framework </user-isolation/index>`

Regular security mode
%%%%%%%%%%%%%%%%%%%%%%

When UIF is disabled, DSS runs as a single UNIX user. All code which is written through the interface and executed locally is therefore ran with the permissions of this said user.

This includes notably:

* Python and R recipes
* Python and R notebooks
* PySpark and SparkR recipes
* Custom Python code in preparation recipes
* Custom Python code for machine learning models

No user (even with the Data Scientist profile) may write such code if they are not granted the "Write unisolated code" permission.

It is important to note that since the DSS Unix user has filesystem access to the DSS configuration, a user who has the "write unisolated code" permission is able to alter the DSS configuration, including security-related controls. This means that a hostile user with these privileges would be able to bypass DSS authorization mechanisms.

User isolation enabled
%%%%%%%%%%%%%%%%%%%%%%%%%%

When UIF is enabled, most of the aforementioned code runs with end-user permissions. The "write unisolated code" permission only applies to the following specific locations where the code is not ran using end-user impersonation:

* Write custom partition dependency functions
* Write Python UDF in data preparation


Multiple group membership
==========================

Users may belong to several groups. All permissions are cumulative: being a member of a group who has a given permission grants it, even if you are also member of a group who doesn't have said permission.

DSS does not have negative permissions.
