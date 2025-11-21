Govern Security: Roles and Permissions
########################################

.. contents::
    :local:

.. note::

  This section only applies to :doc:`Dataiku Govern </governance/index>`


**Roles** and **Permissions** are two distinct notions that Dataiku Govern uses to configure **who** can do **what** in Govern.


They are based on the following Govern concepts:

* **Blueprint**: a category of objects (example: a Govern Project)
* **Blueprint Version**: the template/schema for objects; it contains the field definitions, workflows definitions, etc. (Example: a specific template for Govern Projects, with 5 workflow steps. Another Blueprint Version for Govern Projects might have a template with 9 workflow steps, perhaps for projects on teams with many regulatory requirements.)
  A Blueprint can contain multiple Blueprint Versions that can be seen as variants, with slight variations in their content.
* **Artifact**: this is the actual object. It contains the fields that are defined in the Blueprint Version and that users can fill in. (Example: a Govern Project for "North America Fraud Detection")

Note: to learn more about them, go to the :doc:`/governance/navigation`


**Roles** are simple labels created at Govern instance level. They will be assigned to Users and Global API Keys based on the contextual action and the Roles and Permissions settings.

.. note::

  Roles are different from the Users and Groups that come from the LDAP. The LDAP Users and Groups are usually based on the company structure and so may differ from the intended usage and associated permissions needed in Govern.
  By using Roles instead of directly using LDAP Users and Groups in the Permissions configuration, Roles can be dynamically assigned to Users or Groups, based on any combinations of rules and criteria, making for a highly flexible permissions system.


**Roles Assignments Rules** are a configurable set of rules that define, depending on the contextual action, what Roles are assigned to which Users.

**Permissions** are configurable settings that define what actions are allowed for which Roles.


Concretely, the Roles and Permissions system will work this way:

* **User action**: A User wants to run an action that is permission-locked
* **Roles computation**: Given the Roles Assignments Rules settings and the action, compute the set of Roles assigned to the User
* **Permissions computation**: Given this set of Roles, the Permissions settings, and the action, compute the effective permissions granted to the User
* **Action result**: Based on the effective permissions, the User is allowed, or not allowed, to run the action


For each Blueprint, **Roles Assignment Rules** and **Permissions** settings can be defined.
The **Default Permissions** are **Permissions** settings defined at Govern instance level. If no specific **Permission** is set on a Blueprint, they are used instead in the computation process.

.. note::

  This Roles and Permissions system is not applied in the admin restricted configuration pages, like the Administration page, the Blueprint Designer page, or the Roles and Permissions page.


User actions
============

The Roles and Permissions computation is entirely based on the contextual action the User runs.
The following table lists the actions with their description, the involved Govern objects, and their related Permissions options in the settings.

+------------------------------+--------------------------------------------------------------------------------+--------------------+----------------------------+----------------------------+-------------------------------------------------------------------------+
| Action                       | Description of the action                                                      | Blueprint involved | Blueprint Version involved | Existing Artifact involved | Permissions settings options                                            |
+==============================+================================================================================+====================+============================+============================+=========================================================================+
| Admin Blueprint CRUD         | Create, Read, Update, and Delete a Blueprint in the Blueprint Designer         | **Does not apply, global admin permission is required**                                                                                                |
+------------------------------+--------------------------------------------------------------------------------+--------------------+----------------------------+----------------------------+-------------------------------------------------------------------------+
| Admin Blueprint Version CRUD | Create, Read, Update, and Delete a Blueprint Version in the Blueprint Designer | **Does not apply, global admin permission is required**                                                                                                |
+------------------------------+--------------------------------------------------------------------------------+--------------------+----------------------------+----------------------------+-------------------------------------------------------------------------+
| Blueprint Read               | Access and see the name, icon, colors of a Blueprint                           | ✔                  | ✖                          | ✖                          | Artifact Admin, or Read, or Write, or Create, or Delete                 |
+------------------------------+--------------------------------------------------------------------------------+--------------------+----------------------------+----------------------------+-------------------------------------------------------------------------+
| Blueprint Version Read       | Access and see the definition of a Blueprint Version                           | ✔                  | ✔                          | ✖                          | Artifact Admin, or Read, or Write, or Create, or Delete                 |
+------------------------------+--------------------------------------------------------------------------------+--------------------+----------------------------+----------------------------+-------------------------------------------------------------------------+
| Blueprint Version Field Read | See a specific field definition of a Blueprint Version                         | ✔                  | ✔                          | ✖                          | Artifact Admin, or Read, or Write, or Create, or Delete & Field Read    |
+------------------------------+--------------------------------------------------------------------------------+--------------------+----------------------------+----------------------------+-------------------------------------------------------------------------+
| Artifact Create              | Create a new Artifact                                                          | ✔                  | ✔                          | **✖**                      | Artifact Create & Field Write                                           |
+------------------------------+--------------------------------------------------------------------------------+--------------------+----------------------------+----------------------------+-------------------------------------------------------------------------+
| Artifact Read                | Access, see the name, and the workflow status of an existing Artifact          | ✔                  | ✔                          | ✔                          | Artifact Read                                                           |
+------------------------------+--------------------------------------------------------------------------------+--------------------+----------------------------+----------------------------+-------------------------------------------------------------------------+
| Artifact Field Read          | See a specific field value of an existing Artifact                             | ✔                  | ✔                          | ✔                          | Artifact Read & Field Read                                              |
+------------------------------+--------------------------------------------------------------------------------+--------------------+----------------------------+----------------------------+-------------------------------------------------------------------------+
| Artifact Write               | Edit an existing Artifact                                                      | ✔                  | ✔                          | ✔                          | Artifact Write                                                          |
+------------------------------+--------------------------------------------------------------------------------+--------------------+----------------------------+----------------------------+-------------------------------------------------------------------------+
| Artifact Field Write         | Edit a specific field value of an existing Artifact                            | ✔                  | ✔                          | ✔                          | Artifact Write & Field Write                                            |
+------------------------------+--------------------------------------------------------------------------------+--------------------+----------------------------+----------------------------+-------------------------------------------------------------------------+
| Artifact Delete              | Delete an existing Artifact                                                    | ✔                  | ✔                          | ✔                          | Artifact Delete                                                         |
+------------------------------+--------------------------------------------------------------------------------+--------------------+----------------------------+----------------------------+-------------------------------------------------------------------------+


.. note::

  * The Admin Blueprint, and Blueprint Version Create, Read, Update, and Delete actions in the Blueprint designer are based on the global admin permission and not on the Roles and Permissions system
  * The Blueprint Read, Blueprint Version Read, and Blueprint Version Field Read actions are based on the Artifact Read and Field Read permissions, there is no Blueprint Read option in the Permissions settings (check the `Permissions`_ section to learn more)
  * No Existing Artifact is involved for the Artifact Create action because it does not exist yet (it is important to consider this when configuring Roles Assignment Rules with criteria, check the `Criteria`_ section to learn more)


Roles Assignment
================

Roles Assignment Rules
----------------------

For a specific Blueprint and for each Role, a list of Role Assignments Rules can be defined.
For the Role to be assigned, at least one Rule must be valid.

A Rule is configured by selecting specific Users and Global API Keys for them to be assigned to the selected Role.

A Rule contains a list of criteria (conditions) that can be empty. For a Rule to be valid, all the criteria must comply.
In the case of an empty list of criteria, the Rule is considered valid and the Role will be assigned.

The logic is to always **add** Roles. If a Rule is valid, the associated Role will be assigned to the User. 
There is no way to create exceptions to the Rules to remove the assigned Role afterward.


User & API Keys selection
+++++++++++++++++++++++++

There are several ways to select Dataiku Govern Users and Global API Keys to be assigned to a Role:

* a list of users - all users in this list are selected
* a list of user groups - all users in these user groups are selected
* a list of Global API Keys - all API Keys in this list are selected (Global API Keys are an independent way to authenticate to Dataiku Govern)
* a list of field IDs - only for actions involving a specific existing Artifact - a dynamic way to select Users and Global API Keys: all Users/Groups/Global API Keys stored in this artifact fields are selected. Warning: any user that can modify a field in this list on an artifact will consequently modify Users and Global API Keys permissions, please double check who has field write access on these fields.


Criteria
++++++++

* Blueprint Version criterion: 
  
  * restricts the Rule to be valid only in the context of an action involving a **Blueprint Version**
  * restricts the Role assignment to one specific Blueprint Version defined by the given Blueprint Version ID

* Field value criterion:
  
  * restricts the Rule to be valid only in the context of an action involving an **Existing Artifact**
  * restricts the Role assignment based on a field value. Multiple operators exist, such as Equals or Contains

* Workflow criterion: 
  
  * restricts the Rule to be valid only in the context of an action involving an **Existing Artifact**
  * restricts the Role assignment based on the active step in the workflow that must be the one defined by the given Step ID

* Artifact existing criterion: 
  
  * restricts the Rule to be valid only in the context of an action involving an **Existing Artifact**

* Artifact deleted criterion: 
  
  * restricts the Rule to be valid only in the context of an action involving a **Deleted Artifact**

* No criterion:
  
  * doesn't restrict the Rule at all

.. image:: img/rar-criterion.png

.. note::

  As it is shown on the `User actions`_ table above, the actions are involving some Govern objects. As a result, it may narrow the list of criteria that can be applied when the current action does not provide the needed object to evaluate the rule. For instance, during an **Artifact Create** action, a Rule with a **Field Value** criterion will never comply because this criterion requires the involvement of an **Existing Artifact**.


Roles Inheritance
------------------

In addition to Roles assignment Rules, a Blueprint can be configured to use **Roles Inheritance**.
It helps centralizing Roles assignment Rules in one place when they apply to multiple Govern objects.
For instance, it is useful in the context of a hierarchical structure between Govern items.

Blueprint Inheritance
+++++++++++++++++++++

By adding a Blueprint reference in the **Inherit Blueprint role assignment rules** settings option, the Blueprint will inherit Roles from another Blueprint.
In this case, Govern will compute the assigned Roles in the context of the selected Blueprint (only involving this Blueprint).
All the computed Roles will be added to the normal Role computation mecanism based on Roles Assignments Rules as described above.
The logic is to always **add** Roles. So by setting up **Blueprint Inheritance** only new Roles can be added and none can be removed.

The Blueprint Inheritance involves a Blueprint but does not involve a Blueprint Version, nor an Existing Artifact, nor a Deleted Artifact.
As a side effect, only Rules without criteria are valid for Blueprint Inheritance.

Artifact Inheritance
+++++++++++++++++++++

By setting a field ID in the **Inherit computed roles from Artifact (based on reference field)** settings option, the Blueprint will inherit Roles from an Existing Artifact.
If this option contains a valid field ID, and if the field contains a valid Artifact reference to an Existing Artifact, Govern will compute the assigned Roles in the context of this referenced Existing Artifact (only involving this Existing Artifact, its related Blueprint and Blueprint Version).
All the computed Roles will be added to the normal Role computation mechanism based on Roles Assignments Rules as described above.
The logic is to always **add** Roles. So by setting up **Artifact Inheritance** only new Roles can be added and none can be removed.

The Artifact Inheritance involves an Existing Artifact (the referenced one) and all criteria that rely on an Existing Artifact will be based on the referenced Artifact and not another one.

.. image:: img/rar-inheritance.png



Permissions
===========

The **Permissions** settings are configured at the Blueprint level so each Blueprint can have its own configuration.
The **Default Permissions** are global settings that are used instead when the Blueprint-specific **Permissions** settings are not set.

.. note::

  All permissions will be granted to Govern admins.


Artifact Permissions
--------------------

Configuration per Role
++++++++++++++++++++++

Permissions settings are configured per Role.

There are four Artifact permissions to be configured: **Artifact Read**, **Artifact Write**, **Artifact Create**, and **Artifact Delete**.
Granting any of the **Artifact Write**, **Artifact Create** and **Artifact Delete** permissions automatically also grants the **Artifact Read** permission.

There are two Artifact Field permissions to configure: **Field Read** and **Field Write**.
Granting the **Field Write** permission automatically also grants the **Field Read** permission.

.. image:: img/blueprint-permissions.png

For any field, it is possible to define a permission exception.
If a field does not have a permission exception, the computation mechanism will fall back on the **Field Read** and **Field Write** permissions.

.. image:: img/field-permission-exceptions.png

.. note::

  The **Default Permissions** does not have permissions exceptions for fields.


Configuration for Everyone
++++++++++++++++++++++++++

It is possible to create a permission configuration for **everyone** - these permissions will be granted to every users even to users with no assigned Roles.

The tool to configure permissions for **everyone** contains the same configuration as the configuration for specific roles:

* **Artifact Read**, **Artifact Write**, **Artifact Create**, and **Artifact Delete** permissions
* **Field Read** and **Field Write** permissions
* Field permission exceptions

.. note::

  If the **Field Read** permission is checked in this **everyone** block, every field that does not have a permission exception configured will be readable by everyone. The same applies to the **Field Write** permission.


Blueprint and Blueprint Version Permissions
-------------------------------------------

In most cases, Users won't interact directly with Blueprint and Blueprint Versions; instead they interact directly with Artifacts that are based on a Blueprint and a Blueprint Version.

That is why Blueprint and Blueprint Version permissions cannot be configured, they are computed based on the Artifact permissions.

In a context of an action involving an Existing Artifact, any granted Artifact permission (**Artifact Admin**, **Artifact Read**, **Artifact Write**, **Artifact Create**, **Artifact Delete**) implies the permission to read and access to the corresponding Blueprint and Blueprint Version.
For all fields that the User does not have the **Field Read** permission, their definition will be filtered out of the Blueprint Version.

.. note::

  When a User wants to access a Blueprint directly (ie. listing the available Blueprints), the Role computation will be done involving only the **Blueprint**. Thus only Rules without criteria will apply. The permissions computation will still consider the Artifact permissions to allow or not the access of the Blueprint.
  When a User wants to access a Blueprint Version directly (ie. listing the Blueprint Versions of a Blueprint), the Role computation will be done involving only the **Blueprint Version** and its **Blueprint**. Thus only Rules without criteria or with the Blueprint Version criteria will apply. The permissions computation will still consider the Artifact permissions and Artifact Field permissions to allow or not the access of the Blueprint and the field definitions.

.. note::

  Only Govern admins can add, edit, or delete Blueprints and Blueprint Versions in the Blueprint Designer page.

.. seealso:: 
	More information on Govern roles and permissions can be found in `Concept | Govern roles and permissions <https://knowledge.dataiku.com/latest/mlops-o16n/govern/concept-roles-permissions.html>`_.