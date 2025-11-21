Spark configurations
#####################

Spark has many configuration options and you will probably need to use
several configurations according to what you do, which data you use, etc.
For instance you may want to use spark "locally" (on the DSS server) for some
jobs and on YARN on your Hadoop cluster for others, or specify the allocated
memory for each worker…

* As administrator, in the general settings (from the Administration menu), in
  the `Spark` section, you can add / remove / edit named "template"
  configurations, in which you can set Spark options by key/value pairs.
  See the `Spark configuration documentation
  <https://spark.apache.org/docs/latest/configuration.html#available-properties>`_

* At every place where you can prepare a Spark job, you will have to choose the
  base template configuration to use, and optionally additional / override
  configuration options for that specific job.

* In most recipes that can load non-HDFS datasets (or sampled HDFS datasets),
  datasets are loaded as a single partition. They must be repartitioned so that
  **every partition fits in a Spark worker's RAM**. There is a `Repartition
  non-HDFS inputs` settings to specify in how many partitions it should be
  split.
