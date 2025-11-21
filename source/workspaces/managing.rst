Managing Workspaces
=====================

Workspaces can be created by anyone whose security group has been granted :doc:`permission </security/permissions>` to create workspaces by the instance admin in **Global group permissions**.

Workspace settings
--------------------

To populate your workspace with members and to help orient them, you can edit the workspace settings. If you are an Admin in a workspace, you can change the workspace’s name, give it a description, change the workspace icon’s color, and manage users. 

Managing Workspace Users
------------------------

If you click on a workspace’s user list, you’ll see the full list of users and groups in the workspace and their roles.
If you are a workspace Admin, you can add/remove DSS users and groups to this list of users and change their roles.

Workspace Roles
---------------

Within a workspace, there are 3 types of roles: **Admins, Contributors, and Members.** 

- Admins control access to the workspace by adding and removing users. They also assign roles to users in the workspace (Admin, Contributor or Member). 
- Contributor can share content into a workspace. In order to share objects from a DSS project, a Contributor needs to have permission from the project owner; this is granted separately from workspace membership, and is granted at the project-level. See ‘Sharing DSS objects into a workspace’ for more information. 
- Members can access and interact with content in the workspace. 

Permissions
-----------

Everyone in a workspace is granted a **read** permission on objects and is able to create and contribute to :doc:`discussion threads </collaboration/discussions>`.
If a DSS user has more permissions on an object, previously granted through other types of project access, they’ll be able to open the object in ‘project view’ with the button **GO TO SOURCE** and perform actions there.

Sharing workspaces via email
----------------------------

You can also invite non-DSS users to your workspace via email.

If a valid mail channel (e.g. SMTP) is configured in Administration > Settings > Notifications & Integrations, an invitation will be sent to the specified email.

Once the user registers with that email, they will be granted access to the workspace.

Invitations by email can be disabled on the **Administration > Settings > Access & requests** page.

