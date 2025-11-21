The DSS Event Server
##########################

.. contents::
	:local:

The DSS Event Server is a very simple HTTP server that runs alongside a DSS node.

The Event Server receives events as HTTP queries and dispatches them to *targets*.

The primary use case of the Event Server is to receive audit trail messages from multiple DSS nodes and to centralize them. In this kind of setup:

* You install the event server on a single DSS node
* You configure an audit target on each DSS node that sends to this single event server
* The event server on the "auditing node" writes the events it receives to a local target (for example, local files)
* The managers can then parse these local files to grab centralized audit information

Installing the event server
==============================


The event server is a new process in a design or automation node.

To install the event server:

* Stop DSS

* Run ``./bin/dssadmin install-event-server``

* Start DSS

.. _event-server.configuration:

Configuration of the event server
=================================

The Event Server receives events that had been posted by the "EventServer target" of the audit dispatcher.

The Event Server dispatches events to destinations. There can be multiple destinations in an Event Server. The concepts for audit dispatch and Event Server are extremely similar.

Each event server destination defines:

 * What topics it accepts (or all)
 * What routing keys it accepts (or all)
 * Where it sends the events.

The Event Server is configured in Administration > Settings > Event Server

At the moment, the Event Server can only write events as files on a "filesystem-like" connection.

The Filesystem-like destination takes as parameters:

* a connection (Filesystem, S3, Azure Blob or Google Cloud Storage)
* a path within that connection.

It creates subfolders of this path like ``/topic/routing-key/YYYY/mm/dd/HH`` (configurable).

Importantly, it does not create a dataset, you still need to create the dataset targeting this connection

Security
==========

The Event Server takes optional authentication (and the audit target can set it of course)


Limitations
=============

The Event Server is not highly-available nor horizontally scalable. It should however adequately serve the needs of most customers, and can handle thousands of events per second.