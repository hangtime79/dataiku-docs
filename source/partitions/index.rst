.. _partitions-index:

Working with partitions
#######################

Partitioning refers to the splitting of a dataset along meaningful *dimensions*. Each partition contains a subset of the dataset that can be built independently.

For a general introduction to partitioning, see :doc:`/concepts/index`

.. toctree::
    :maxdepth: 1

    fs_datasets
    sql_datasets
    dependencies
    identifiers
    recipes
    hive
    sql_recipes
    variables
    models

The two partitioning models
============================

There are two models for partitioning datasets: files-based partitioning and column-based partitioning.

Files-based partitioning
-------------------------

This partitioning method is used for all datasets based on a filesystem hierarchy. This includes Filesystem, HDFS, Amazon S3, Azure Blob Storage, Google Cloud Storage and Network datasets.

In this method, partitioning is defined by the layout of the files on disk., so the data in the files is NOT used to decide which records belong to which partition.

For more information, see :doc:`fs_datasets`

Column-based partitioning
--------------------------

This partitioning method is used for datasets based on structured storage engines:

* All SQL databases
* NoSQL databases: MongoDB, Cassandra and Elasticsearch

In this method, the partitioning is derived from information (one or several columns) which is part of the data.

A very important point is that in this method, the schema of the dataset does contain the partitioning data.
