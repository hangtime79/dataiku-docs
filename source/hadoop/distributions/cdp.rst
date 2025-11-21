Cloudera CDP
#############

Dataiku supports

* Cloudera Data Platform - CDP Private Cloud Base:

  * 7.1.7 (aka 7.1.7.p0)
  * 7.1.7 SP1 (aka 7.1.7.p1000 and above)
  * 7.1.7 SP2 (aka 7.1.7.p2000 and above)
  * 7.1.8
  * 7.1.9
  * 7.1.9 SP1


* Cloudera Base on Premises

  * 7.3.1

Spark support
==============

* Dataiku supports the Spark 3 version provided by CDP
* The Spark 2 version provided by CDP is not supported anymore
* Connection to Azure Blob (abfs:// URLs) with Spark 3 is not supported

Security
=========

* Connecting to secure clusters is supported
* User isolation is supported with Ranger
* Using Knox is not supported. DSS must be deployed within the zone protected by Knox

Known issues
============

* DSS 14 requires at least Java 17 to run. If the Java version used for Spark is lower, it should be updated via the properties ``spark.executorEnv.JAVA_HOME`` and ``spark.yarn.appMasterEnv.JAVA_HOME`` in the Spark Settings to point to a suitable JDK (Java 17)
* The Hive version deployed by CDP 7.1.9 and 7.3.1 doesn't support unbounded ranges (https://issues.apache.org/jira/browse/HIVE-24905) in analytical function, which impacts Window recipes in DSS if they use an unbounded window frame. It can be worked around by setting the following Hive property:

.. code-block:: bash

    set hive.vectorized.execution.reduce.enabled=false