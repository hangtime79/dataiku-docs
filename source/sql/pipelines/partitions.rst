Partitions and SQL pipelines
##############################

.. contents::
    :local:


Partitioning refers to the splitting of a dataset along meaningful dimensions, such that each partition contains a subset of the dataset. 

Dataiku DSS can provide partitioning support, both on SQL databases that have native partitioning support and on those that do not. However, performance will generally be better when the SQL database has native partitioning support. 

See :doc:`/partitions/sql_datasets` for more information.

.. _union-all-sql-partition:

Partitioned datasets in a SQL pipeline
==================================================

It is possible to go from a partitioned dataset to a non-partitioned dataset in your SQL pipeline. You can also go from one partitioned dataset to another, with both datasets having uneven partition dependencies. See :doc:`/partitions/dependencies` for more details.
