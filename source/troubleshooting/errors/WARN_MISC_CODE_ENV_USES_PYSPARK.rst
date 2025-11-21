WARN_MISC_CODE_ENV_USES_PYSPARK: pyspark installed in a code environment
########################################################################

The package `pyspark` has been manually installed in a code environment. It is not recommended to install `pyspark` manually.

Remediation
===========

Remove `pyspark` from the list of required packages of the code env.

.. note::

	Please refer to :doc:`the documentation</spark/index>` to find out how to install and interact with Spark in the recommended way. 
	Running the Spark integration in DSS automatically adds pyspark to code envs.
