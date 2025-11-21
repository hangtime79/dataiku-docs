WARN_SPARK_NON_DISTRIBUTED_READ: Input dataset is read in a non-distributed way
###############################################################################

Spark's performance hinges on its ability to parallelize workloads, and to achieve parallelization, Spark needs to be able to distribute the data to process into tasks, then dispatched to workers. Parallelization is ideally done all the way up to the reading of the data to process, because reading typically involves I/O or network activity, and conversion of raw data to Spark's internal representation (fully or partially). When the reading part cannot be handled by Spark directly, DSS is tasked with reading the data, which is then streamed over the network to a single Spark worker. This implies that there is no parallelization of the reads, and that a single worker has to handle all the I/O and conversion.

Remediation
===========

- ensure the types of the input datasets are compatible with distributed reads. Use preferably HDFS or cloud storage (S3, Azure, GCS). Snowflake datasets can be used if the DSS connection has the Spark integration activated. Hive datasets can also be used if the recipe is set to "use global metastore" (see the ``Advanced`` tab of the recipe)
- check that the user running the recipe can read the details of the connection of the dataset. This means that at least one of the groups of the user should belong to the groups of the ``Details readable by`` setting of the connection
- for file-type datasets, ensure the format is compatible with distributed reads. Use preferable Parquet or ORC. CSV can also be used depending on the CSV settings (typically, using CSV with headers precludes distributed reads)