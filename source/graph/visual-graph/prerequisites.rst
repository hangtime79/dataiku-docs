Prerequisites
###############


Visual Graph is installed through the "Visual Graph" that an administrator needs need to install. This plugin has :doc:`Tier 2 support </troubleshooting/support-tiers>`.

You need Dataiku 14.2 at least. Python 3.9 and 3.10 are supported.

Infrastructure
^^^^^^^^^^^^^^

- The components of the plugin can run directly on DSS or in a container.
- The datasets containing the graph configurations can be hosted on any type of dataset. Still, it is recommended to use an SQL-based dataset.
- The files of the embedded graph databases can be hosted on a FileSystem or S3 connection.
- **Visual Graph** uses `the embedded Kuzu graph database technology <https://kuzudb.com/>`_.