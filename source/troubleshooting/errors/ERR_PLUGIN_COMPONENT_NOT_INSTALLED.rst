ERR_PLUGIN_COMPONENT_NOT_INSTALLED: Plugin component not installed or removed
##############################################################################

A plugin has been removed, or parts of a development plugin have been removed. This error can be encountered on any object potentially defined in a plugin, such as:

* datasets
* recipes
* macros
* ...


Remediation
===========

The plugin has been removed so there are 2 cases:

* the removal is intentional: the browser's page need to be refreshed
* the removal is not intentional : this issue can only be fixed by a DSS administrator, either by reinstalling the plugin or by reverting the plugins/dev to a previous state.
