WARN_SPARK_WITH_DATABRICKS_DATASET: Not leveraging Databricks compute
#####################################################################

You have selected a SparkSQL recipe or the Spark engine to execute a job on a Databricks dataset(s). This will not place the workload of the job in the Databricks cluster, but will instead put it wherever the Spark configuration points, for example "locally" on the DSS server or in your Kubernetes cluster.

Since the Databricks connection is a SQL connection, selecting a SQL recipe or the SQL engine will put the workload of the job in the Databricks cluster to leverage your Databricks compute resources.

Remediation
===========

When available, use a SQL recipe, or the SQL engine if in a visual recipe, when working with Databricks datasets.
