WARN_SPARK_TASK_OOM: Some Spark tasks encountered out of memory
###############################################################

Spark executors run in containers (in Yarn or Kubernetes), wich impose constraints on the memory of the processes running in them. A task dispatched by Spark to one of its executors can make the executor trip over the limit enforced by the container, in which case the container will be forcefully terminated by its manager, thus killing the task in the Spark job. This is not necessarily a non-recoverable error for Spark, and Spark will attempt a task that failed several times before completely giving up on the job.

Remediation
===========

- ensure the memory overhead property for the relevant Spark master is set to a meaningful value. For Yarn this is ``spark.executor.memoryOverhead`` (value in MB), for K8S this is ``spark.kubernetes.memoryOverheadFactor`` (value in fraction of ``spark.executor.memory``)
- ensure the ``spark.executor.memory`` is set to a meaningful value (at least 2g)
- increase the value for the memory overhead property and/or the memory property