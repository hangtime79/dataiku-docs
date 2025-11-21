ERR_BUNDLE_ACTIVATE_MISSING_CONNECTION: Connection is missing
#############################################################

The project you are trying to import/activate has a dependency on connection(s) that either do not exist or have been remapped to connection(s) that do not exist on the DSS instance.

Remediation
===========

Use the connection remapping option, and map the missing connection(s) to ones that exist on the DSS instance.
The connection remapping is available for both project import (tick the ``Display advanced options after upload``) and bundle activation (in the ``Activation settings`` tab of the bundles management screen).
