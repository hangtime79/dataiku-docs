Hive metastore (through HiveServer2)
######################################

This kind of metastore catalog is the default when you install DSS.

It requires that you have one or multiple Hadoop clusters. DSS will leverage the HiveServer2 of your current Hadoop cluster to read and write from the Hive metastore server.

When running Spark jobs, Spark will talk directly to the Hive metastore server.