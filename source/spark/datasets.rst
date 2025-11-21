Interacting with DSS datasets
##############################

.. contents::
    :local:

DSS can read and write all datasets using Spark.

If you have a Spark engine (which does not need a cluster installation), using Spark on local datasets can still bring performance improvements, for example for the Grouping and Join recipes. Additionally, using Spark will bring you the ability to run SparkSQL, even if you don't have a Hadoop cluster.

However, only HDFS and S3 datasets fully benefit from the Spark distributed nature out of the box. This is because for HDFS and S3 datasets, Spark has builtin support for reading data from these backend, and for splitting the data into multiple partitions.


Hadoop FS datasets
====================

In order for Spark jobs to read HDFS datasets directly, you need to make sure that the user running the Spark job has the "Details readable by" permission on the connection. For more information on this flag, see :doc:`/security/connections`.

Having this flag allows the Spark job to access the URI of the HDFS dataset, which permits it to access the filesystem directly. If this flag is not enabled, DSS needs to go to the slow path described below. This will very strongly degrade the performance of the Spark job.

For "true" HDFS datasets, the "details" of the HDFS connection generally do not contain any secret (only a root path). However, for Hadoop filesystem datasets that actually point to S3, WASB, ..., the details of the HDFS connection usually contain a secret credential in order to connect to the cloud storage. Giving the "Details readable by" permission on these datasets will give the user running te Spark job the ability to read this credential. A common setup is to have multiple such connections, each with its own credential, and each accessible to only one group of users, in order to provide both isolation and ability to read datasets with good performance.


S3 datasets
=============

In order for Spark jobs to read S3 datasets directly, you need to make sure that the user running the Spark job has the "Details readable by" permission on the connection. For more information on this flag, see :doc:`/security/connections`.

Having this flag allows the Spark job to access the S3 bucket, which permits it to read the data directly. If this flag is not enabled, DSS needs to go to the slow path described below. This will very strongly degrade the performance of the Spark job.

The details of the S3 connection usually contain an AWS key pair in order to connect to the cloud storage. Giving the "Details readable by" permission on these datasets will give the user running te Spark job the ability to read this credential. A common setup is to have multiple such connections, each with its own credential, and each accessible to only one group of users, in order to provide both isolation and ability to read datasets with good performance.

Other
=====

For other kinds of datasets, since Spark does not natively read and split them, DSS makes them available in Spark using a simplified reader. These datasets are read and written using a single Spark partition (not to be confused with DSS partitions). A single Spark partition will be processed in a single thread (per Spark stage). Furthermore, in some operations, a single Spark partition is restricted to 2GB of data. Therefore, if your dataset is large, you will need to **repartition** it.

* In PySpark and SparkR recipes, you need to use the SparkSQL API to repartition a dataframe (generally ``df.repartition(X)`` where X is a number of partitions)
* In SparkSQL, Visual preparation, MLLib and VisualSQL recipes, repartitioning is automatic (in 10 partitions by default). You can configure the repartitioning and the target number of partitions in the various Advanced tabs.

A good rule of thumb is to ensure that each partition will correspond to 100-200 MB of data. Therefore, if your input dataset (on a non-HDFS non-S3 dataset) is 10 GB, you might want to repartition it in 50-100 (remember that for HDFS or S3 datasets, partitioning is automatically done at the source).
