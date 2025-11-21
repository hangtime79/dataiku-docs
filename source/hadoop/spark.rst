Spark
######

.. contents::
	:local:

For an introduction to the support of Spark in DSS, see :doc:`/spark/index`

Dataiku DSS supports the version of Spark 3 provided by supported Hadoop distributions. Support for Spark 2 is deprecated.

.. _spark-setup:

* Go to the Dataiku DSS data directory

* Stop DSS

.. code-block:: bash

  ./bin/dss stop


* Run the setup

.. code-block:: bash

  # Path may differ
  ./bin/dssadmin install-spark-integration -sparkHome /opt/cloudera/parcels/SPARK3/lib/spark3

* Start DSS

.. code-block:: bash

  ./bin/dss start

Verify the installation
------------------------

Go to the Administration > Settings section of DSS. The Spark tab must be available.


Additional topics
===================

Metastore security
------------------

Spark requires a direct access to the Hive metastore, to run jobs using a HiveContext (as opposed to a SQLContext) and
to access table definitions in the global metastore from Spark SQL.

Some Hadoop installations restrict access to the Hive metastore to a limited set of Hadoop accounts (typically, 'hive', 'impala' and
'hue'). In order for SparkSQL to fully work from DSS, you have to make sure the DSS user account is authorized as well. This is
typically done by adding a group which contains the DSS user account to Hadoop key ``hadoop.proxyuser.hive.groups``.

.. note::

  On Cloudera Manager, this configuration is accessible through the ``Hive Metastore Access Control and Proxy User Groups Override``
  entry of the Hive configuration.


Configure Spark logging
-------------------------

Spark has DEBUG logging enabled by default; When reading non-HDFS datasets, this will lead Spark to log the whole datasets by default in the "org.apache.http.wire".

We strongly recommend that you modify Spark logging configuration to switch the org.apache.http.wire logger to INFO mode. Please refer to Spark documentation for information about how to do this.
