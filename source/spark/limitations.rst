Limitations and attention points
##################################

Spark is a fairly complex execution engine; tuning and troubleshooting Spark jobs require some experience.

Spark's additional possibilities come with a few limitations:

* Sampling with filter is not supported for input datasets; prefer a filtering
  recipe instead.

* HDFS datasets perform much better on Spark than other datasets, for both
  reading and writing.

* Sampling an HDFS dataset (except with a fixed ratio) can be slower than
  loading it unsampled.

.. warning::

  Spark's overhead is non-negligible and its support has some limitations (see above and
  :doc:`/spark/usage`).
  If your data fits in the memory of a single machine, other execution engines might be
  faster and easier to tune.
  It is recommended that you only use Spark for data that does not fit in the memory of a single
  machine.
