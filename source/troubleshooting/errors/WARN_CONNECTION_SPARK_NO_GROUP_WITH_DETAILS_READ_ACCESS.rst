WARN_CONNECTION_SPARK_NO_GROUP_WITH_DETAILS_READ_ACCESS: no groups allowed to read connection details
#####################################################################################################

Spark is enabled but no user groups have been granted permission to read the connection's details. Spark interaction may be slow.

Remediation
===========

Grant “Details readable by” on the connection to the user groups using Spark. See :ref:`connections.read-details` for more details.