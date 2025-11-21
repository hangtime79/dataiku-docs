:orphan:

Hive SequenceFile
#################

.. warning::

  **Deprecated**: Support for SequenceFile is :doc:`Deprecated </troubleshooting/support-tiers>` and will be removed in a future DSS version

SequenceFile is a flat file format consisting of binary key/value pairs.
It is extensively used in Hadoop MapReduce as input/output formats, since it is splittable.

Compatibility
-------------

Data Science Studio can read & write SequenceFiles using the Hive's default serializer/deserializer (:code:`LazySimpleSerDe`).
Most Hive data types are supported, including complex types (object, map & array).

The following Hive types are not supported:

* DATE
* UNION

Limitations
-----------

- The SequenceFile format can only be used on HDFS connections.
