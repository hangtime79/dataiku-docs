AWS SQS
#######


Connection setup
================

SQS connections offer the same settings as :doc:`S3 connections <../connecting/s3>` to define AWS credentials


Message format
==============

SQS messages are text only. DSS offers to read or write them as simple text or as JSON

Single-value
------------

Upon reading, the message's text is put in the row under a column name, and upon writing, the value of the given column is taken from the row and used as message.

JSON
----

Upon reading, SQS messages are parsed from JSON to fill a row, and conversely, upon writing the fields of the row are grouped in a JSON object

