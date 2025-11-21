WARN_SPARK_NON_DISTRIBUTED_WRITE: Output dataset is written in a non-distributed way
####################################################################################

Spark's performance hinges on its ability to parallelize workloads, and to achieve parallelization, Spark needs to be able to distribute the data to process into tasks, then dispatched to workers. Parallelization is ideally done all the way up to the writing of the data produced, because writing typically involves I/O or network activity, and conversion of raw data from Spark's internal representation. When the writing part cannot be handled by Spark directly, DSS is tasked with writing the data, which is then streamed over the network from a single Spark worker. This implies that there is no parallelization of the writes, and that a single worker has to handle all the I/O and conversion.

Remediation
===========

- ensure the types of the output datasets are compatible with distributed writes. Use preferably HDFS or cloud storage (S3, Azure, GCS). Snowflake datasets can be used if the DSS connection has the Spark integration activated. Hive datasets can also be used if the recipe is set to "use global metastore" (see the ``Advanced`` tab of the recipe)
- check that the user running the recipe can read the details of the connection of the dataset. This means that at least one of the groups of the user should belong to the groups of the ``Details readable by`` setting of the connection
- for file-type datasets, ensure the format is compatible with distributed writes. Use preferable Parquet or ORC. CSV can also be used depending on the CSV settings (typically, using CSV with headers precludes distributed writes)