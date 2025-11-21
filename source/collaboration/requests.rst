Requests
########

.. contents::
	:local:

Dataiku DSS allows any user to initiate a request to gain access to projects, datasets or other objects.

Request types
=============

The following requests are available:

Request to access a project
---------------------------
It allows you to request to be granted project-level permissions on a project with "access requests" enabled.

Read :doc:`/security/project-access` for more details on how these requests are managed and sent.

These requests are sent to the project owner and all users with :doc:`Edit permissions </security/permissions>` permission on the project.

Request to execute an application
---------------------------------
It allows you to request to be granted execute-permission on the application

Read :doc:`/applications/index` for more details on how these requests are managed and sent.

These requests are sent to the application owner and all users with :doc:`Edit permissions </security/permissions>` permissions on the application.

Request to share an object
--------------------------
It allows you to request that an object be shared to a target project. This request can be initiated from the object's right panel in several places in DSS (data catalog, global search, feature store, flow…)

Read :doc:`/security/shared-objects` for more details on how these requests are managed and sent.

These requests are sent to all users with :doc:`Manage shared objects </security/permissions>` permissions on the object's project.

Request to install or update a plugin
-------------------------------------
It allows you to request a plugin installation or update.

These requests are sent to all users with :doc:`Admin </security/permissions>` permissions on the instance.

The request can be activated/deactivated in Administration > Settings > Other > Access & requests > Dataiku object access & requests.
Then check/uncheck Plugins requests: "Allow non-admin users to request a plugin installation"

Request to create a code environment
------------------------------------
It allows you to request a new code environment.

These requests are sent to all users with :doc:`Admin </security/permissions>` permissions on the instance.

The request can be activated/deactivated in Administration > Settings > Other > Access & requests > Dataiku object access & requests.
Then check/uncheck Code-env requests: "Allow non-admin users to request a code-env installation"

.. note::

	Code environment requests are available only on Design nodes.


Request to upgrade profile
------------------------------------
It allows you to request a profile upgrade. You can request a profile upgrade:

* From the navigation bar on the top right
* When you try to perform an action for which you do not have the required profile

These requests are sent to all users with :doc:`Admin </security/permissions>` permissions on the instance. Then the admin can decide which upgraded profile to assign to the user.


The request can be activated/deactivated in Administration > Settings > Other > Misc > Access & requests > Profile upgrade requests.

Then check/uncheck Profile upgrade requests: "Allow users to request a profile upgrade. Requests are reviewed by administrators"

.. note::

	For more information on user profiles, see :doc:`/security/user-profiles`.


Managing requests
=================

The recipient users of the request will be notified that a new request has been made and they will be able to manage it either from the project's security section or directly from the request inbox.

Notifications
-------------

All recipients of a request will be notified by a new notification on their avatars and will be able to see it from their notification panel.

Additionally all recipients of a request with a valid email address will receive an email informing them that a new request has been made.

On the other end, users who initiated a request will be notified by email when their request is approved.

.. note::

   To receive emails:

   * Users must have enabled "Email me when users request access on my projects or objects" or "Email me when I am granted access to projects" in their profile.
   * DSS must be configured to send Notification emails (in Administration > Settings > Collaboration > Notifications & Integration > Notification emails).


Requests Inbox
---------------
All requests made from DSS can be found and managed in the requests section of the recipient's Inbox. The inbox is available from the applications menu.

Users initiating a request will not see their requests appearing in their request inboxes since only requests that need management do appear in the inbox.

If a request has been approved or rejected, its status will be updated for all other recipients of the same request. They will be able to see how and when the request was managed.
