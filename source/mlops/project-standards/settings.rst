Project Standards settings
##########################

You can manage your Project Standards settings in the Administration > Project Standards tab. Here, you can configure checks and scopes for Project Standards.

.. important::
    You need to be a member of a group with the `Administrator` permission to see this page.

Terminology
===========

Check specification
___________________

A check specification (or check spec) is a Python class that will verify if a project respects a good practice.
It takes a project key as an input and returns a severity, a number between 0 and 5.
A check specification can have other parameters in its config.
If the project respects the standards, a severity of 0 will be returned.
If the project has some issues, it will return a severity between 1 and 4, depending on the importance of the issue.

Check specifications are created using DSS :doc:`plugins </plugins/index>`. A check specification is a plugin component of the kind "Project Standards check spec". 
You can add more check specifications in your DSS instance by importing or creating plugins containing "Project Standards check spec" components.

Check
_____

A check is an instantiation of a check specification.
It has its own configuration, so you can import the same check specification multiple times and use different configs.
In the settings, use the edit button of the check to update its name, description, or config.

Settings sections
=================

Checks library
______________

You will find in the checks library all the checks that have been imported into your instance.
You can add, edit, or delete checks using the corresponding buttons.

A check can be created by importing a check specification. You will first select the plugin, then the check specification you want to import. You can import several check specifications at the same time.
A freshly created check uses a default config. Edit the check if you want to change its config.

Scopes
______

Admins can create scopes in Project Standards to organize their quality checks. Scopes are used to determine which set of checks should run for which set of projects. Scopes can be applied to a specific set of projects, or all projects in a specific folder or with a specific tag.

If a project is included in several scopes, the scope located higher has priority, and its checks will be run and included in the Project Standards report.

In all cases, you will have a Default scope. All projects that do not match any custom scope criteria will use this default scope. Note that you can have only this scope in your configuration; this means all projects will have the same setup.

General parameters
__________________

You will find here other parameters related to Project Standards.
