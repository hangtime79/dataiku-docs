Teradata Connector For Hadoop
#############################

`Teradata Connector for Hadoop` (TDCH) can be used in DSS as an additional execution engine which allows scalable parallel data transfers between Teradata and HDFS.


Installation and configuration
==============================

The Teradata Hadoop appliance already embeds TDCH. On the Hadoop side, many Hadoop enterprise vendors embed a TDCH library in their product, otherwise you can install it by:

* downloading the `Teradata Connector for Hadoop <https://downloads.teradata.com/download/connectivity/teradata-connector-for-hadoop-command-line-edition>`_
  installation archive (you need a Teradata account)
* unzipping it somewhere on the machine that runs DSS.

Once you have downloaded (or already know the location of) TDCH you can enable its support in DSS by adding the following properties to
configuration file ``DATADIR/config/dip.properties``, and restarting DSS (you may have to adjust file version numbers according to your distribution):

.. code-block:: sh

    tdch.enabled = true
    tdch.jar = /PATH/TO/TDCH/LIB/teradata-connector-1.5.1.jar
    tdch.includes = /PATH/TO/TDCH/LIB/tdgssconfig.jar,/PATH/TO/TDCH/LIB/terajdbc4.jar


Usage and Guidelines
====================

For any `Sync` recipe between a HDFS dataset and a Teradata dataset, the TDCH engine will be available (both directions).

Some settings are available in the "Advanced" tab of the recipe to define the distribution method and number of mappers.

Refer to Teradata documentation for tuning the engine according to your Teradata characteristics and YARN capabilities. 

The following distribution methods are available:

* For Teradata -> HDFS sync:
  
  * split.by.hash
  * split.by.value
  * split.by.partition
  * split.by.amp

* For HDFS -> Teradata sync
  
  * batch.insert
  * internal.fastload

Limitations
============

* Partitioned datasets are not supported
* Only the CSV format is supported for the HDFS dataset
* SQL "query" datasets are not supported. Only SQL "table" datasets are supported
* Properties defined at the HDFS connection level are not taken into account. Therefore, it is generally not possible to sync with cloud storages (S3, GCS, WASB, ADLS) - since these connections generally require properties for credentials