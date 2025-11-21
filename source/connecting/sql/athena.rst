AWS Athena
##########

DSS can connect to AWS Athena.

.. warning::

	**Tier 2 support**: Connection to AWS Athena is covered by :doc:`Tier 2 support </troubleshooting/support-tiers>`

.. warning::

	Athena is not a standalone SQL database. Instead, it is an interactive query layer on top on Amazon S3 data.
	The integration of Athena in DSS is designed primarily for querying S3 datasets built in DSS.


Supported
===========

* Running interactive SQL notebooks on Athena based on previously-built S3 datasets
* Using Athena as charts engine for S3 datasets (partial support)
* Running SQL queries on Athena based on previously-built S3 datasets (execution and data read through Athena, write through DSS)

Not supported
===============

* Any form of write to Athena (writes should be made to a S3 dataset)

Installing the JDBC driver
===========================

The JDBC Driver can be downloaded from https://docs.aws.amazon.com/athena/latest/ug/connect-with-jdbc.html

* Select the "Driver version" field according to the Athena driver version you chose (2.X or 3.X)
* In the “Driver jars directory”, enter the path of the directory where you put the downloaded driver

.. note::

    Unzip the Athena driver if downloaded as a ZIP file

.. warning::

    Do not place the Athena JAR file directly in the ``lib/jdbc`` folder as it may conflict with DSS libraries


Connecting to Athena
=====================

The recommended way to connect to Athena is to:

* Setup a S3 connection, including all potential advanced security options
* Create an Athena connection
* Select "From S3 connection" as the Credentials mode
* Enter the name of your S3 connection

The Athena connection will automatically use the same credentials as the S3 connection. Note that the credentials used for the S3 connection thus need Athena-related IAM permissions. The S3 connection must have either the Credentials mode "AWS Keypair" or "STS with AssumeRole".
