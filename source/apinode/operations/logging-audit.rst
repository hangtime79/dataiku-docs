Logging and auditing
######################

.. contents::
	:local:

The API node outputs three kinds of logs:

* Regular runtime logs (in the ``run/apimain.log`` file)
* Audit logs for the administration API
* Logs of queries

Logging of queries is especially important if you plan on implementing a feedback loop. Knowing what has been predicted for what records is important. You'll also need to have a way to retrieve "what finally happened" for each record that the API node predicted (did this customer convert? churn? was it a fraud? did the sensor fail? ...)

By default:

* Administration API audit logs are written to the same ``run/apimain.log`` file
* Queries are logged in the ``run/audit`` folder

How to configure audit and query logging
==========================================

Audit and query logging is done through the standard Java Log4J logging mechanism.

.. note::

	Dataiku DSS has been confirmed to be not vulnerable to the family of vulnerabilities regarding Log4J. No mitigation action nor upgrade is required. Dataiku does not use any affected version of Log4J, and keeps monitoring the security situation on all of its dependencies.

You can set the destination of these loggers by modifying the Log4J appenders in the ``bin/log4j.properties`` file

The loggers used for audit logging are:

* dku.apinode.audit.queries:

	* Logs all queries to prediction endpoints, in a JSON format. The log message includes the input features, the prediction results, and timing information

* dku.apinode.audit.auth

	* Logs authentication failures, both on Admin and User APIs

* dku.apinode.audit.admin

	* Logs all modifications done through the admin API. The log message includes details about the API key used to perform the call

* dku.apinode.audit.allcalls

	* Logs basic information for all API calls, both Admin and User APIs. It is generally not recommended to enable this logger

How to turn on query logging
=============================

In your API_DATA_DIRECTORY, create a directory and subdirectory called ``resources/logging``.

In the logging directory, add a file called ``dku-log4j.properties``.

Copy the following content into ``dku-log4j.properties``

.. code-block:: bash

	# By default, send audit logging to a specific file in run
	# For an inalterable audit log, this should be sent to an external system,
	# not controlled by the DSS user
	log4j.appender.AUDITFILE=org.apache.log4j.RollingFileAppender
	log4j.appender.AUDITFILE.File=${DIP_HOME}/run/audit/audit.log
	log4j.appender.AUDITFILE.MaxFileSize=100MB
	log4j.appender.AUDITFILE.MaxBackupIndex=20
	log4j.appender.AUDITFILE.layout=com.dataiku.dip.logging.JSONAuditLayout

	# Queries logging: use rolling files.
	log4j.appender.QUERIES_AUDIT_FILE=org.apache.log4j.RollingFileAppender
	log4j.appender.QUERIES_AUDIT_FILE.File=${DIP_HOME}/run/api-queries/queries.log
	log4j.appender.QUERIES_AUDIT_FILE.MaxFileSize=10MB
	log4j.appender.QUERIES_AUDIT_FILE.MaxBackupIndex=10
	log4j.appender.QUERIES_AUDIT_FILE.layout=org.apache.log4j.PatternLayout
	log4j.appender.QUERIES_AUDIT_FILE.layout.ConversionPattern={"timestamp" : "%d{yyyy/MM/dd-HH:mm:ss.SSS}Z", "logger": "%c", "severity" : "%p", "message" : %m}%n

	# Remove audit logs from regular CONSOLE logger
	log4j.additivity.dku.audit=false
	log4j.logger.dku.audit= INFO, AUDITFILE


	# And enable it
	log4j.additivity.dku.audit.generic=false
	log4j.logger.dku.audit.generic= INFO, QUERIES_AUDIT_FILE

Then, restart your API node (`./bin/dss restart`).

You should now see queries logged in the ``run/audit`` folder.


Logging queries to Kafka
==========================

Apache Kafka is a distributed message queue, which can be used to get query logs out of the API node.

To enable logging queries to Kafka:

* Add all jars from the Kafka distribution to the ``lib/java`` folder

* Replace the "Queries logging" part of ``bin/log4j.properties`` by the following snippet:

.. code-block:: bash

	log4j.appender.QUERIES_KAFKA=org.apache.kafka.log4jappender.KafkaLog4jAppender
	log4j.appender.QUERIES_KAFKA.BrokerList=kafka1:9092,kafk2:9092,kafka:9093
	log4j.appender.QUERIES_KAFKA.Topic=dku-apinode-audit
	log4j.appender.QUERIES_KAFKA.layout=com.dataiku.dip.logging.JSONAuditLayout

	log4j.additivity.dku.apinode.audit.queries=false
	log4j.logger.dku.apinode.audit.queries= INFO, QUERIES_KAFKA

.. note::

	You can also send administration and authentication audit logs to Kafka by setting appropriate configuration for the
	other audit loggers.
