Concepts
########

Streaming endpoints
===================

A streaming endpoint is a message source or sink. It can be

* a topic in a Kafka cluster
* a queue in SQS
* a HTTP SSE endpoint (read only)


Continuous recipe
==================

Recipes taking streaming endpoints as input are continuous recipes.

The distinction between regular and continuous recipes comes from the fact that runs of regular recipes are finite: their input data consists of datasets and the recipe is done when all the input data is read. However, streaming endpoints can provide data indefinitely, so continuous recipes can work without ever stopping on their own.


Continuous activity
===================

A continuous activity is a controller that oversees one continuous recipe and ensures it runs well, potentially restarting it if it fails.
