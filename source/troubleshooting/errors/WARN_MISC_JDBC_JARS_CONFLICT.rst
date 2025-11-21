WARN_MISC_JDBC_JARS_CONFLICT: JDBC drivers - some JARs are prone to version conflicts
#####################################################################################

When multiple JDBC drivers are present in the same directory, conflicts can arise due to naming conflicts and version incompatibilities. This can result in unexpected behavior, such as errors or incorrect query results.

Remediation
===========

To avoid conflicts with these JDBC drivers, it is recommended to isolate them in separate directories. Make sure to edit the JDBC connection settings in Dataiku to point to the correct driver.
