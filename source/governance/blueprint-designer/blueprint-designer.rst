Introduction to Blueprint Designer
#####################################

.. contents::
	:local:

Overview
==========
The Blueprint Designer lets you customize your Dataiku Govern instance. More specifically, it allows you to organize how information is stored in an :ref:`artifact <govern.item.content>`.

Information is stored in a hierarchical fashion. This hierarchy will be explained next.

.. image:: img/bp-bpv-and-artifacts.png


Blueprints
--------------
A **blueprint** is simply a collection of blueprint versions. Blueprints are containers used to organize and store the templates procured and/or created.

The Blueprint Designer contains different types of blueprints:

- **Govern blueprints**: used for Standard Govern items such as business initiatives, projects, bundles, models, and model versions. 
- **Dataiku blueprints**: embedding information coming from the Design and the Deployer node in order to surface them in Govern. 
- It is also possible to create **new types of blueprints** that are not related to Dataiku items or existing artifacts if you want to track other types of information or workflows in Dataiku Govern.

Blueprint versions
--------------------
Blueprint versions are **templates** that are applied to Govern items such as business initiatives, projects, bundles, models, and model versions. 

The blueprint version of an item determines what information is collected and stored about that item. For example, a project from a Design node can be Governed using a Govern Project blueprint version.

You can have multiple blueprint versions of a Blueprint to allow for different needs. For example, blueprint versions for a "GxP Compliance Govern Project" and an "EU AI Act Govern Project" necessitate different templates which can be applied to the appropriate items. 

Blueprint versions can either be "Draft," "Active," or "Archived." They must be set to **Active** to be used in Dataiku Govern.

.. note:: 
    Information regarding the design and customization of blueprint versions can be found in :doc:`blueprint-version-design`.

Actions in Blueprint Designer
================================

Blueprints
----------------------------------------------
The actions you can perform on a blueprint include:

- Creating a new blueprint 
- Importing a JSON blueprint provided by Dataiku or exported from another Govern node
- Exporting a blueprint 
- Editing exisiting blueprints


Blueprint versions
----------------------------------------------
A blueprint version is always created inside a blueprint. When creating a new blueprint version, you can: 

- Create a blank template 
- Create a copy of an existing blueprint version (Forking)
- Import a JSON file provided by Dataiku or exported from another Govern node

.. note:: 
    It is **strongly** advised to start from a copy of an existing blueprint version because some fields and workflow steps are required to properly work (sign-off for deployments, reviewers settings, etc.)

Additional actions you can perform on a blueprint version include:

- Editing a blueprint version
- Exporting a blueprint version
- Deleting a blueprint version
- Archiving a blueprint version

.. seealso::
    To learn more about blueprint version design, visit :doc:`blueprint-version-design`.

    To practice creating a blueprint version, visit this `tutorial <https://knowledge.dataiku.com/latest/mlops-o16n/govern/tutorial-blueprint-designer.html>`_.

Migrations
----------------------------------------------
Migrations are used to map elements from one blueprint version to another. In the Blueprint Designer, you can:

- Script a new migration
- Edit a migration
- Remove a migration

You can learn how to apply a migration in this `how-to <https://knowledge.dataiku.com/latest/mlops-o16n/govern/how-to-switch-templates.html>`_.

.. You can also learn how to write a migration script in :doc:`devguide:concepts-and-examples/govern/govern-advanced/govern-admin-blueprint-designer/govern-blueprint-migration`.

.. caution::
    Migrations can only be applied to blueprint versions within the same blueprint. You can not migrate across blueprints.