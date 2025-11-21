ERR_BUNDLE_ACTIVATE_BAD_CONNECTION_TYPE: Connection is the wrong type
#####################################################################

The project you are trying to import/activate has a dependency on connection(s) that have been mapped to connection(s) of the wrong type on the target DSS instance. For example, this can happen when importing a project that uses a Snowflake connection named ``connection1`` on a DSS instance that has a MySQL connection named ``connection1``.

Remediation
===========

Use the connection remapping option, and map the connection(s) to ones that have the same type.
The connection remapping is available for both project import (tick the ``Display advanced options after upload``) and bundle activation (in the ``Activation settings`` tab of the bundles management screen).
