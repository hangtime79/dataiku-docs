Kafka
#####

DSS can leverage `Kafka <https://kafka.apache.org>`_ topics as streaming endpoints.

Connection setup
================

To read or write from Kafka topics, a connection to a Kafka cluster is required. The connection is defined by a list of bootstrap servers, and security settings. DSS supports the PLAINTEXT and SASL protocols for communicating with the brokers, and Kerberos authentication which is a special case of SASL. Since both protocols are not natively encrypted, they usually require to activate SSL. When this is the case, the truststore and keystore holding the certificates are also set in the connection (see the `ssl.*` properties in `Kafka's doc <https://kafka.apache.org/documentation/#consumerconfigs>`_)

.. warning::

	Using Kerberos and/or SSL precludes using the helper methods to access the streaming endpoints in Python recipes, as the python libraries do not handle Kerberos and/or require the certificates in a form that is not a keystore/truststore


Message format
==============

Kafka messages comprise a key, a value and a timestamp. Both key and value are treated by the Kafka brokers as binary data, and it is the message producer and consumer's duty to read and write this binary data.

When converting a message to a row, DSS reads the key first (if a format is set), then the value. Columns present in the key take precedence over columns present in the value. Similarly, the timestamp column (if defined) takes precedence over the columns present in key or value.

.. warning::

	Streaming endpoints have a schema, like datasets, which describes its content as a set of columns with types. When DSS reads from a Kafka topic, the most important part of the schema is the set of column names, while the types are only informative. However, if you are using Spark to process the data, the types have to properly match the types of the data in the Kafka message since Spark is more strict with typing.


Single-value
------------

This format maps to the base SerDes classes of Kafka. It treats the binary value as the binary representation of a single value: a string or an integer or a long integer or a double or a byte array. DSS reads or writes the value in a given column. If the column name is not specified, nothing is read or written.


JSON
----

The binary value is a UTF8 JSON string. DSS parses the entire value or a subset of its fields.


Avro
----

The flavor of Avro used in the Kafka world is actually not a pure Avro message, but a composite of a schema identifier and an Avro message. DSS uses the SerDes from Confluent to read Avro messages (see the `SerDes' doc <https://docs.confluent.io/current/schema-registry/serdes-develop/serdes-avro.html#>`_), which makes it mandatory to define the `schema.registry.url` property in some way: either on the Kafka connection properties, or in the streaming endpoint properties.


Timestamp handling
==================

All messages in a Kafka topic have a timestamp, usually set by the broker when the message is added to the topic. When a timestamp column name is set in the streaming endpoint's settings, upon reading in DSS, the value of the timestamp is fetched in that column. Conversely, if the `provide timestamp` checkbox is ticked, upon writing by DSS the value of the timestamp column is used for the message timestamp (if the broker permits setting the timestamp)
