Capabilities of User Isolation Framework
##########################################

+-----------------------------------------------------------+------------------+----------------------+
|                                    Feature                | Without UIF      | With UIF             |
+===========================================================+==================+======================+
| Access control on projects                                | Yes              | Yes                  |
+-----------------------------------------------------------+------------------+----------------------+
| Access control on connections                             | Yes              | Yes                  |
+-----------------------------------------------------------+------------------+----------------------+
| Enforcement of permissions                                | Yes              | Yes                  |
| to execute code                                           |                  |                      |
+-----------------------------------------------------------+------------------+----------------------+
| Per-user credentials on SQL connections.                  | No               | Yes                  |
+-----------------------------------------------------------+------------------+----------------------+
| Impersonation on Oracle.                                  | No               | Yes                  |
+-----------------------------------------------------------+------------------+----------------------+
| Impersonation on Microsoft SQL Server                     | No               | Yes                  |
+-----------------------------------------------------------+------------------+----------------------+
| Execution of "regular" code (Python, R) locally           | Not isolated     | Isolated             |
+-----------------------------------------------------------+------------------+----------------------+
| Execution of "regular" code (Python, R) on Kubernetes     | Isolated         | Isolated             |
+-----------------------------------------------------------+------------------+----------------------+
| Execution of Spark code (Python, R, Scala) on YARN        | Not isolated     | Isolated             |
+-----------------------------------------------------------+------------------+----------------------+
| Execution of Spark code (Python, R, Scala) on Kubernetes  | Not isolated     | Isolated             |
+-----------------------------------------------------------+------------------+----------------------+
| Connecting to secure Hadoop clusters (Kerberos).          | Yes              | Yes                  |
+-----------------------------------------------------------+------------------+----------------------+
| HDFS ACLs to enforce                                      | No               | Yes                  |
| permissions even against code                             |                  |                      |
| execution                                                 |                  |                      |
+-----------------------------------------------------------+------------------+----------------------+
| Authentication against LDAP directory                     | Yes              | Yes                  |
+-----------------------------------------------------------+------------------+----------------------+
| Authentication with Single-Sign-On                        | Yes              | Yes                  |
+-----------------------------------------------------------+------------------+----------------------+
| Traceability of all actions,                              | Yes              | Yes                  |
| including code execution                                  |                  |                      |
+-----------------------------------------------------------+------------------+----------------------+
| Non-repudiable audit log                                  | No               | Yes                  |
+-----------------------------------------------------------+------------------+----------------------+
| Hadoop-level traceability of individual actions.          | No               | Yes                  |
| (Cloudera Navigator, Atlas, ...)                          |                  |                      |
+-----------------------------------------------------------+------------------+----------------------+

See the `comparison of Dataiku DSS editions <https://www.dataiku.com/dss/editions/>`_ to determine what levels of security apply to your installation.
