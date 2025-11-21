WARN_SPARK_TASK_DISKFULL: Some Spark tasks encountered disk space issues
########################################################################

Spark executors of Spark-over-Kuberenetes setups run in pods in the clusters, and pods get as ``/tmp`` a portion of the actual cluster node's disk, which implies that the size of ``/tmp`` in the pods is constrained by the node's disk size, and the usage that other pods of the same node make of their ``/tmp``.

Since Spark spills data on disk when data doesn't fit in memory anymore, and since Spark can run subprocesses that also take disk space, like Python UDFs, this ``/tmp`` can be overused, and in such cases either the processes in the pod will crash because they cannot get the disk space they need, or the Kubernetes cluster itself will notice the excessive usage of disk space and forcefully terminate the pod, thus killing the task in the Spark job. This is not necessarily a non-recoverable error for Spark, and Spark will attempt a task that failed several times before completely giving up on the job.

Remediation
===========

- reduce the number of tasks each executor handles concurrently, by setting ``spark.executor.cores`` to 1
- split the workload of Spark executors by increasing parallelism. This can mean for example repartitioning the input data, or increasing ``spark.sql.shuffle.partitions``
- provision nodes with larger disks for the Kubernetes cluster