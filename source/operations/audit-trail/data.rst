Audit data
############

.. contents::
	:local:

Each audit event is a JSON message. You can parse DSS audit events using the "JSON" file format in DSS. We recommend setting a "max depth" of 2, 1 for the envelope and 1 for the actual data fields

Events envelopes
=================

Each audit event is a JSON message. Depending on how it was written, its form can be a bit different, as it can be wrapped in a different envelope.

In standard audit log files
-----------------------------

In standard audit log files (produced through log4j), events look like:

.. code-block:: json

    {
        "severity": "INFO",
        "logger": "dku.audit.generic",
        "message": { "... The actual JSON message ..."},
        "mdc": {
            "apiCall": "/api/projects/get-summary",
            "user": "admin"
        },
        "callTime": 9,
        "timestamp": "2020-02-19T16:05:02.441+0100"
    }


* severity can be ignored
* logger will indicate the topic 
* mdc contains additional context information that will usually be repeated in the message
* callTime indicates, for events sent during processing of a query, how long the current query had been running
* timestamp is the ISO-8601-formatted timestamp at which it was processed

In Event Server data files
---------------------------

Event Server data files are formulated like:

.. code-block:: json

    {
        "clientEvent": { "... The actual JSON message ..."},
        "origAddress": "127.0.0.1",
        "serverTimestamp": "2020-03-17T19:15:30.609+0100"
    }


* origAddress is the IP of the DSS node that sent the event to the Event Server

* serverTimestamp is the ISO-8601-formatted timestamp at which it was received on the Event Server

Event data
============

Each event is a single JSON object and will always contain at least a ``msgType`` indicating the precise message type. Additional fields depend on the msgType.

Most audit events will contain a ``authUser`` field indicating the user who performed the request

Some of the most important msgTypes are:

For "generic" topic
--------------------

 * application-open: DSS was open in a browser tab
 * login/logout: self-explanatory
 * dataset-read-data-sample: A dataset's Explore was open
 * dataset-read-data: Data was read for a dataset
 * flow-job-start / flow-job-done: A job was started/completed
 * flow-object-build-start / flow-object-build-failed / flow-object-build-success: Within a job, a dataset was built
 * scenario-run: A scenario was run manually
 * scenario-fire-trigger: A scenario was run automatically
 * project-export-download: A project was exported
 * dataset-export: A dataset was exported

For "apinode-query" topic
-------------------------

 * "prediction-query": a prediction endpoint was run
 * "sql-query": a SQL query endpoint was run
 * "dataset-lookup-query": a dataset lookup endpoint was run
 * "function-query": a function endpoint was run

For "compute-resource-usage" topic
-----------------------------------

 * "compute-resource-usage-start": a compute resource usage was started
 * "compute-resource-usage-update": a compute resource usage was updated
 * "compute-resource-usage-complete": a compute resource usage was completed
 * "compute-resource-usage-start": a compute resource usage was started
 * "kubernetes-cluster-usage-status": periodic report on the status and usage of a Kubernetes cluster
