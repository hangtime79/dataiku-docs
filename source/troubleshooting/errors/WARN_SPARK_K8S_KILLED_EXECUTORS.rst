WARN_SPARK_K8S_KILLED_EXECUTORS: Some Kubernetes executors were killed
######################################################################

When Spark runs on K8S, Spark executors are run in pods in the cluster. These pods are created by Spark with memory requests to the K8S cluster, based on the values passed in the properties ``spark.executor.memory`` and ``spark.kubernetes.memoryOverheadFactor``. But the processes running the Spark executor in the pod can end up requesting more memory than expected from the K8S node, in which case the node will forcefully terminate the pod, and along with it, the Spark executor. This happens sometimes when the memory overhead factor is underestimated, or when the executor spawns subprocesses (for example: Python processes to compute UDFs).

Remediation
===========

- increase ``spark.kubernetes.memoryOverheadFactor`` 
- increase ``spark.executor.memory``
