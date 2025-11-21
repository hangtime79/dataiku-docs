ERR_SQL_IMPALA_MEMORYLIMIT: Impala memory limit exceeded
##########################################################

Description
============

While executing a query, Impala encountered a memory limit exceeded situation.

This error can happen each time DSS interacts with Impala:

* When running an Impala code recipe
* When running a visual recipe with Impala engine
* When computing status of a HDFS dataset
* When computing charts on a HDFS dataset (including charts on a dashboard)

Remediation
============

This error is internal to Impala. Your administrator needs to change the configuration of the Hadoop cluster to increase the memory allocation to Impala.
