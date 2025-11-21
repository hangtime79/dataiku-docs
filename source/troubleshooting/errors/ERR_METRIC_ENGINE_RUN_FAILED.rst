ERR_METRIC_ENGINE_RUN_FAILED: One of the metrics engine failed to run
#############################################################################

DSS failed to compute a metric on an object (dataset or folder). 


Remediation
===========

The causes for not being able to compute a metric can be:

* generated SQL queries becoming too large for the computation engine. This happens when selecting too many metrics on a large number of columns; many databases have limits on the number of columns and aggregates a single statement can hold
* invalid dataset setup, resulting in unreadable data files or unreadable SQL tables
* unavailability of the engine selected for the computations (Hiveserver2 or Impala server down, invalid connection parameters for Hadoop or the SQL connection)

The error message should give more context about what part of the metric computations can have failed, and should direct attempts to fix the problem.
