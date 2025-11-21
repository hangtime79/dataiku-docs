ERR_PLUGIN_WRONG_TYPE: Unexpected type of plugin
############################################################

An operation in the plugin development tools of DSS has targeted a plugin that is not in dev (add file, edit file, ...)


Remediation
===========

This issue can only be fixed by a DSS administrator.

The plugin was probably installed on the instance as a final version, and now exists in the plugins/installed folder of the DSS data directory. If development needs to continue on the plugin, the version in plugins/installed needs to be removed.
