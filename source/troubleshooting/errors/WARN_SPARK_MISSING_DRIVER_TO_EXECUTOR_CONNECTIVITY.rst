WARN_SPARK_MISSING_DRIVER_TO_EXECUTOR_CONNECTIVITY: The Spark driver cannot call into the executors
####################################################################################################

Spark executors run in containers in the cluster, so on different machines than the Spark driver. While most communication between executors and driver happens in the executor-to-driver direction, some few operations make the Spark driver call the executors directly, mostly when it needs to collect back data on the driver side. Typical cases include usage of ``collect()`` or ``toPandas()`` in Pyspark, and joins for which Spark decides to use the "broadcast join" method over the usual shuffle join.

When the driver has to contact the executors directly, it can end up being at odds with the networking setup of the VM it's running on and/or of the cluster: it is indeed not uncommon to not be able to access the IPs of the pods in the cluster, because of firewall rules for example. The Spark job will then fail with exceptions related to network connections.

Remediation
===========

- avoid using ``collect()`` or ``toPandas()``, because they load all the data on the DSS VM and won't parallelize subsequent workloads
- ensure that the DSS VM can reach the IPs of the pods. Note that depending on the type of Kubernetes cluster, the range of IPs used by the pods can live outside the main range of IPs of the VPC. For example, in GKE, pods use a secondary IP range  
- if the recipe is a join, or is a Pyspark recipe doing a join, then add the Spark property `spark.sql.autoBroadcastJoinThreshold -> -1` to the recipe settings
