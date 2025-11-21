ERR_SPARK_FAILED_TASK_OOM: Spark failure: out of memory in task
##########################################################################

Description
============

This error can happen when running any Spark-enabled recipe

This error indicates that the Spark processing failed because one of the executors encountered a Java out of memory situation.

Remediation
============

Specific case of code recipes
-------------------------------

If the failure comes from a Spark code recipe (Spark-Scala, Pyspark or SparkR), check your code for large allocations performed in the executors.

General case
-------------

This error generally does not indicate that the DSS machine or the cluster is out of memory, but that the configuration for executing the Spark code is too restrictive.

You generally need to increase the ``spark.executor.memory`` Spark setting. For more information about how to set Spark settings, please see :doc:`/spark/configuration`. Note that your administrator may need to perform this change.

If not set, the default value of ``spark.executor.memory`` is 1 gigabyte (``1g``).

If your Spark is running in ``local`` master mode, note that the value of ``spark.executor.memory`` is not used. Instead, you must increase ``spark.driver.memory`` to increase the shared memory allocation to both driver and executor.