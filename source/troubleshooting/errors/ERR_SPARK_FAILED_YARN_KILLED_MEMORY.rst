ERR_SPARK_FAILED_YARN_KILLED_MEMORY: Spark failure: killed by YARN (excessive memory usage)
##############################################################################################

Description
============

This error can happen when running any Spark-enabled recipe, when Spark is running in "YARN" deployment mode.

This error indicates that YARN (the resource manager) has forcefully killed the Spark components, because they ran above their allocated memory allocation.

When a Spark application starts on YARN, it tells YARN how much memory it will use at maximum. YARN accordingly reserves this amount of memory. If, during runtime, the memory usage (per container) goes above this limit, YARN kills the process for breaching its promise.

Remediation
============

When a Spark application runs on YARN, it requests YARN containers with an amount of memory computed as: ``spark.executor.memory + spark.yarn.executor.memoryOverhead``

``spark.executor.memory`` is the amount of Java memory (Xmx) that Spark executors will get. However, Java processes always consume a bit more memory, which is accounted for by ``spark.yarn.executor.memoryOverhead``

By default, the memory overhead is 10% of executor memory (with a minimum of 384 MB). This value is often not enough.

The remediation is to increase the value of ``spark.yarn.executor.memoryOverhead`` Spark setting. For more information about how to set Spark settings, please see :doc:`/spark/configuration`. Note that your administrator may need to perform this change.

Beware: unlike ``spark.executor.memory`` where values like ``3g`` are permitted, the value for ``spark.yarn.executor.memoryOverhead`` must always be an integer, in megabytes.

We generally recommend setting a value between ``500`` and ``1000``.
