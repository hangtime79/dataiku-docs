Streaming Spark Scala
#####################

DSS uses wrappers around Spark's `structured streaming <https://archive.apache.org/dist/spark/docs/2.4.0/structured-streaming-programming-guide.html>`_ to manipulate streaming endpoints. This implies using a micro-batch approach and manipulating Spark dataframes.

.. note:

	Streaming dataframes do not offer the full range of capabilities of Spark. Notably, they don't provide access to a RDD, which implies manipulating them with SparkSQL primitives and UDFs.

Data from streaming endpoints is accessed via `getStream()`:

.. code-block:: scala

	val dkuContext   = DataikuSparkContext.getContext(sparkContext)
	val df = dkuContext.getStream("wikipedia")
	// manipulate df like a regular dataframe

DSS will automatically use Spark's native Kafka integration, and stream the data via the backend for other endpoint types.

Writing a streaming dataframe to a dataset is:

.. code-block:: scala

	val q = dkuContext.saveStreamingQueryToDataset("dataset", df)
	q.awaitTermination() // waits for the sources to stop

Writing to a streaming endpoint is equally simple:

.. code-block:: scala

	val q = dkuContext.saveStreamingQueryToStreamingEndpoint("endpoint", df)
	q.awaitTermination() // waits for the sources to stop

The `awaitTermination()` call is needed, otherwise the recipe will exit right away.
