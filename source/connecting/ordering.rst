Data ordering
#############

In some cases, you must order the rows in a dataset. Depending on the type of the dataset and your use case, you may choose between two types of ordering: write ordering and read-time ordering.

.. _write-ordering:

Write ordering
==============

Write ordering is used to store the rows physically in the same order as they are pushed into the dataset.
Enabling write ordering implies using a single thread for writing data and thus it may decrease performance.
This option can be enabled in the dataset settings. This setting is compatible with most storage types that act like file systems:

 - :doc:`/connecting/upload`
 - :doc:`/connecting/filesystem`
 - :doc:`/connecting/hdfs`
 - :doc:`/connecting/s3`
 - :doc:`/connecting/gcs`
 - :doc:`/connecting/azure-blob`
 - :doc:`/connecting/ftp`
 - :doc:`/connecting/scp-sftp`

Read-time ordering
==================

Read-time ordering means that the rows of the dataset will be ordered when they are read from the source.
Enabling read-time ordering may decrease read performance. Read-time ordering is compatible with
most SQL databases. This option is available in the dataset settings and can be superseded with
different values for two distinguish uses:

 - Configuring a sample in explore view
 - Exporting a dataset in action menu
