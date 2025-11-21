HDFS datasets data structure
#############################

.. note::

	This only applies for HDFS datasets for which ACL synchronization is used.

When user isolation for Hadoop is disabled, datasets location is specified by a path in a connection.

When user isolation for Hadoop is enabled, DSS uses a different files pattern for managed datasets: if the dataset's configured location is ``/user/dataiku/datasets/MYPROJECT/mydataset``, then the actual data is written in ``/user/dataiku/datasets/MYPROJECT/mydataset/data``.

The "data" folder belongs to the last user who wrote the dataset (this might be "hive" or "impala"). The "mydataset" folder always belongs to the ``dssuser`` user.

ACLs preventing access are on the ``mydataset`` folder. Within that folder, it is normal for data files to have world-readable permissions. The restrictive "gateway" ACLs on ``mydataset`` prevent unauthorized users from accessing them.

This behavior is configured in the settings of the HDFS connection, in the "Write ACL synchronization mode" setting.
