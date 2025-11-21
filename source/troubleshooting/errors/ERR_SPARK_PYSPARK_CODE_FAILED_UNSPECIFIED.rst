ERR_SPARK_PYSPARK_CODE_FAILED_UNSPECIFIED: Pyspark code failed
##########################################################################

Description
============

This error can happen when:

* Running a Pyspark recipe
* Running a plugin recipe that uses Pyspark

This error indicates that the Pyspark execution failed, and threw a Python exception.

* The message of the error contains the full error message from Spark
* Additional details, including the Python stack, are available in the job log


Remediation
============

You need to carefully read both the error message, and the logs of the job that failed. Between them, they contain all information which is available to understand why the Pyspark code threw an exception.