Project exports and bundles
###########################

Code Studios are created from template in projects.

.. contents::
	:local:

When exporting or bundling a project, only Code Studios that are published as webapps are included. For included Code Studios, both versioned and resource files of the Code Studio are exported. But project resources are not exported by default, and need to be manually checked, if some of the published Code Studios use them.

.. note::

	Code studio templates are not included in bundles, and need to be installed separately on the target node, with the same name. As with plugins, the user gets a warning with the list of templates installed on the node from which the bundle originates.
