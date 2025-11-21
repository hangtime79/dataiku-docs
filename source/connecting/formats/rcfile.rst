:orphan:

Hive RCFile
###########


.. warning::

  **Deprecated**: Support for RCFiles is :doc:`Deprecated </troubleshooting/support-tiers>` and will be removed in a future DSS version

RCFiles, short of Record Columnar File, are flat files consisting of binary key/value pairs, which shares much similarity with SequenceFile.
RCFile stores columns of a table in a record columnar way.

Compatibility
-------------

Data Science Studio can read & write RCFiles using either :code:`ColumnarSerDe` or :code:`LazyBinaryColumnarSerDe`.
Most Hive data types are supported, including complex types (object, map & array).

The following Hive types are not supported:

* DATE
* UNION

Limitations
-----------

- The RCFile format can only be used on HDFS connections.

- Impala < 1.3 doesn't correctly support LazyBinaryColumnarSerDe.
  For more information, see https://issues.cloudera.org/browse/IMPALA-781.

- Hive < 0.12 only : in some cases involving parallel processing, writing a RCFile from DSS may be slower than usual.
  This is a direct consequence of another Hive issue. For more information, see https://issues.apache.org/jira/browse/HIVE-3772.
