DSS as virtual metastore 
#########################

When you don't have a Hadoop cluster (and hence don't have a HiveServer2), and if you are not running on AWS, you do not have a metastore service available.

For this kind of scenario, DSS itself can play the role of a metastore.

To enable DSS metastore, go to Admin > Settings > Metastore catalogs and select "DSS".

With this configuration, all synchronization to metastore will be done to the virtual DSS metastore. DSS will respect per-project security on its builtin metastore.

When submitting Spark jobs, DSS will automatically configure Spark to use DSS as metastore with the appropriate credentials.

