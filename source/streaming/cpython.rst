Continuous Python
#################

Just like a regular Python recipe, a continuous Python recipe runs user-provided Python code. The difference is that it accepts streaming endpoints as inputs and outputs, and when running, will restart if needed and requested. The Python code has to loop or wait indefinitely, in order to continuously handle the input and produce output.

Reading from streaming endpoints
================================

It is advised to read from streaming endpoints using native access, ie to have the Python process connect directly to the message source and handle the messages and offsets directly.

Alternatively, a simpler method to read from a streaming endpoint is to have DSS read the messages and forward them to the Python process.

.. code-block:: python

	endpoint = dataiku.StreamingEndpoint("wikipedia")

	message_iterator = endpoint.get_message_iterator()
	for msg in message_iterator:
		# use the message ... (msg is a json-encoded object)
		state = message_iterator.get_state() # a string
		# if/when needed, do something with state


Reading from Kafka endpoints
----------------------------

The StreamingEndpoint class offers a helper to consume from a Kafka topic using the `pykafka <https://github.com/Parsely/pykafka>`_ package

.. code-block:: python

	endpoint = dataiku.StreamingEndpoint("wikipedia_kafka")
	message_iterator = endpoint.get_native_kafka_consumer()

	for msg in message_iterator:
	    # use the pykafka message object

Messages returned by pykafka have the following fields usable in your code:

	* timestamp is a unix timestamp in milliseconds
	* offset is the message offset in the topic
	* partition_key is the key of the message, as a byte array
	* value is the value of the message, as a byte array

.. note::

	The builtin Python environment does not include the pykafka package. To use the helper methods, you need to use a custom code-env that includes this package.

.. note::

	Only PLAINTEXT Kafka listeners (ie without SSL encryption) are handled by the helper. For SSL support, you need to use pykafka directly and pass the relevant parameters to setup the encryption logic.

.. note::

	The helper returns simple consumers. If you want balanced consumers, you need to use pykafka directly.


Reading from SQS endpoints
----------------------------

The StreamingEndpoint class offers a helper to consume from a SQS queue using the `boto3 <https://github.com/boto/boto3>`_ package

.. code-block:: python

	endpoint = dataiku.StreamingEndpoint("wikipedia_sqs") 
	message_iterator = endpoint.get_native_sqs_consumer()

	for msg in message_iterator:
	    # use the message (it's a string)

The messages returned by the iterator are acknowledged one by one on SQS side when they are retrieved from the iterator. To acknowledge messages only after they've been processed, use boto3 directly

.. note::

	The builtin Python environment does not include the boto3 package. To use the helper methods, you need to use a custom code-env including this package.


Reading from HTTP SSE endpoints
-------------------------------

The StreamingEndpoint class offers a helper to consume from a HTTP SSE endpoint using the `sseclient <https://github.com/btubbs/sseclient>`_ package

.. code-block:: python

	endpoint = dataiku.StreamingEndpoint("wikipedia") 
	message_iterator = endpoint.get_native_httpsse_consumer()

	for msg in message_iterator:
	    # use the sseclient message object

Messages returned by pykafka have these fields:

	* id is a message identifier (often equivalent to the offset)
	* event is the event type
	* data is the message data (can be None depending on the event)

.. note::

	The builtin Python environment does not include the sseclient package. To use the helper methods, you need to use a custom code-env including this package.




Writing to streaming endpoints
==============================

It is advised to write to streaming endpoints using native access, ie to have the Python process connect directly to the message source and handle the messages and offsets directly.

Alternatively, a simpler method to write to a streaming endpoint is to have the Python process send the messages to DSS and let DSS handle the writing.

.. code-block:: python

	endpoint = dataiku.StreamingEndpoint("wikipedia_kafka")
	# setting a schema is strongly advised before using get_writer()
	endpoint.set_schema([{"name":"data", "type":"string", ...}])
	with endpoint.get_writer() as writer:
	    for msg in message_iterator:
	        writer.write_row_dict({"data":msg.data, ...})
	        writer.flush()

The call to `flush()` ensures the messages are sent to DSS for writing. It is not mandatory after each and every message written, but need to be used regularly nonetheless.

Writing to Kafka endpoints
----------------------------

The StreamingEndpoint class offers a helper to produce to a Kafka topic using the `pykafka <https://github.com/Parsely/pykafka>`_ package

.. code-block:: python

	endpoint = dataiku.StreamingEndpoint("wikipedia_kafka")
    with endpoint.get_native_kafka_producer(sync=True) as writer:
		for msg in message_iterator:
        	writer.produce(msg.data.encode('utf8'), partition_key='my_key'.encode('utf8'), timestamp=datetime.now())


The `partition_key` and `timestamp` params are optional.

.. note::

	The builtin Python environment doesn't include the pykafka package. To use the helper methods, the code needs to be run on a code env providing the pykafka package.

.. note::

	Only PLAINTEXT Kafka listeners (ie without SSL encryption) are handled by the helper. For SSL support, you need to use pykafka directly and pass the relevant parameters to setup the encryption logic.


Writing to datasets
===================

Writing the output dataset is done via a writer object returned by Dataset.get_continuous_writer, using the standard methods write_row_dict, write_dataframe or write_tuple.

.. warning::

	When writing to datasets, it is crucial to regularly checkpoint the data. The reason being that rows written to the dataset are first staged to a temporary file and only become fully part of the dataset when a checkpoint is done.


.. code-block:: python

	dataset = dataiku.Dataset("wikipedia_dataset")
	dataset.write_schema([{"name":"data", "type":"string"}, ...])
	with dataset.get_continuous_writer() as writer:
	    for msg in message_iterator:
	        writer.write_row_dict({"data":msg.data, ...})
	        writer.checkpoint("this_recipe", "some state")



Offset management
=================

Most streaming sources have a notion of offset, to keep track of where in the message queue the reader is. The recipe is responsible for managing its offsets, and particularly for storing the current offset and retrieving the last offset upon starting.

When writing to datasets with a continuous writer (from a `get_continuous_writer()` call), and if the dataset is a file-based dataset, the recipe can rely on the last state saved via a call to `checkpoint()` and retrieve that last state with `get_state()` on the continuous writer. When writing to streaming endpoints, the recipe has to manage the storage of the offsets.
