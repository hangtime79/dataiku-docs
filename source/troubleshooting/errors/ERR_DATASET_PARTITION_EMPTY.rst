ERR_DATASET_PARTITION_EMPTY: Input partition is empty
######################################################

An input partition (or unpartitioned dataset) is empty.
This partition or dataset may not have been built yet.
The error message should contain the particular dataset
and partition ID.

This error can happen:

* When exploring a dataset
* When running a recipe
* When otherwise using a dataset

Some common reasons for a partition to be empty are:

* The partition or dataset was never built
* The partition or dataset was cleared
* A third-party system or person erased the partition or dataset
* The dataset's settings are incorrect (wrong path, wrong table name…)


Remediation
===========

* Try rebuilding the partition or dataset
* If the dataset is external, check the dataset's settings and check the source of that dataset,
  exploring that dataset from outside DSS.
* Make sure that the dataset's partitioning settings are correct
