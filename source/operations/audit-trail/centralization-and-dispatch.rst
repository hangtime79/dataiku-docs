Audit centralization and dispatch
###########################################

.. contents::
	:local:

In order to provide non-repudiation characteristics, it is important that the audit events are sent outside of the DSS machine, on a remote system that cannot be accessed and tampered with from the DSS machine.

Furthermore, there are multiple use cases for *centralizing* audit logs from multiple DSS nodes in a single system.

Some of these use cases include:

* Customers with multiple instances want a centralized audit log in order to grab information like "when did each user last do something".
* Customers with multiple instances want a centralized audit log in order to have a global view on the usage of their different audit nodes, and compliance with license
* Compute Resource Usage reporting capabilities use the audit trail, and make more sense if fully centralized. You may want to cross that information with HR resources, department assignments, ...
* Most MLOps use case require centralized analysis of API node audit logs

DSS features a complete routing *dispatch* mechanism for these use cases.

Audit dispatching
==================

Each message sent through the audit system carries a mandatory "topic" and an optional "routing key".

The topic is given by the DSS code and cannot be controlled by the user. It is akin to a "category". At the moment, the following topics exist:

 * generic: Applicative audit of most events in DSS
 * generic-failure: Applicative audit of most failures in DSS
 * authfail: All authentication and authorization failure events
 * apinode-query: Applicative audit of API node queries and replies
 * compute-resource-usage: Audit of usage of compute resources
 * apicalls: Raw logging of API calls on private and public API (for debugging purposes mostly)


The routing key is optional, and allows more advanced dispatching. The routing key is also written in the audit message, for processing at destination. The main use case for routing keys is for apinode-query messages. Each apinode-query audit message is optionally emitted with a routing key specified in the service's configuration. This allows differentiating and/or routing differently the apinode-query audit messages of each API node service.

Each time a DSS node creates an audit message, the message goes through the audit dispatcher to be sent to *audit targets*

Each target defines:

 * What topics it accepts (or all)
 * What routing keys it accepts (or all)
 * Where it sends the events.

.. _audit-trail.log4j-target:

Log4J target
=============

This target sends data using the log4j library. By default, this library is preconfigured to generate the files mentioned in :doc:`default-storage`.

.. note::

	Dataiku DSS has been confirmed to be not vulnerable to the family of vulnerabilities regarding Log4J. No mitigation action nor upgrade is required. Dataiku does not use any affected version of Log4J, and keeps monitoring the security situation on all of its dependencies.

However, all log4j appenders can be used to get audit out of the DSS machine. Configuring log4j is done by editing the ``resources/logging/dku-log4j.properties`` file. (See :doc:`/operations/logging` for more information)

EventServer target
===================

Most use cases of centralizing audit logs from multiple machines can be handled using the DSS Event Server.

For more details on how to install and configure the event server can be found in :doc:`eventserver`

Kafka target
=============

.. warning::

    **Tier 2 support**: Kafka target is experimental and covered by :doc:`Tier 2 support </troubleshooting/support-tiers>`


If you have a Kafka connection defined in your node, you can configure a Kafka target.
