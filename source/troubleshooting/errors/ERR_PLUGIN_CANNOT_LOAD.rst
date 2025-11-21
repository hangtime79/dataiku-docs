ERR_PLUGIN_CANNOT_LOAD: Plugin cannot be loaded
############################################################

A plugin failed to be loaded, because :

* another one with the same name but of another type already exist


Remediation
===========

This issue can only be fixed by a DSS administrator.

There is a folder with the same name in plugins/dev and the plugins/installed. Either the plugin in the plugins/dev or the plugins/installed folder needs to be removed.
