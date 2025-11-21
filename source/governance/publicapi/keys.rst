Public API Keys
################

All calls to the Dataiku Govern public API, either performed using :doc:`rest` or :doc:`the Python client <devguide:concepts-and-examples/govern/index>` must be authenticated using API keys.

There are only a single kind of API keys for the Dataiku Govern REST API:

* Global API keys

Global API keys
=================

Global API keys are keys that are defined for the whole Dataiku Govern instance. Global API keys can only be created and modified by DSS administrators.

Global API keys are not equivalent to a DSS user. Global API keys have their own access rights, and calls performed will appear as having been performed by this key.

Global API keys are defined in Administration > Security > Global API Keys

Global admin
--------------

This special permission gives global admin rights to this key. A global admin key has all permissions in the Dataiku Govern instance. It can also perform global DSS administration tasks:

* Manage users
* Manage log files
* Access the Blueprint Designer
* Access the Role and Permissions Editor
* Access the Custom Page Editor
