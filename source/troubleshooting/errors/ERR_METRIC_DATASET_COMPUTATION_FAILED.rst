ERR_METRIC_DATASET_COMPUTATION_FAILED: Metrics computation completely failed
############################################################################

DSS tried refresh the basic metrics on a dataset, but failed. 


Remediation
===========

The causes for not being able to compute a metric can be:

* invalid dataset setup, resulting in unreadable data files or unreadable SQL tables
* unavailability of the engine selected for the computations (Hiveserver2 or Impala server down, invalid connection parameters for Hadoop or the SQL connection)

The error message should give more context about what part of the metric computations can have failed, and should direct attempts to fix the problem. If the engine seems available, the settings of which engine to use are accessible on the dataset's Status > Edit tab.