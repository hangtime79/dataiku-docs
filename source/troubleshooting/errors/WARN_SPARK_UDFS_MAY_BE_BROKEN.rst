WARN_SPARK_UDFS_MAY_BE_BROKEN: Python UDFs may fail
###################################################

Pyspark serializes UDFs (user defined functions) from the Spark driver, typically running locally on the DSS VM in some code env, then transfers them in their serialized form to the Spark executors, where they're deserialized and run. Use of Python serialization entails that the python process doing the deserialization must have the exact same packages as the one doing the serialization (as well as the same Python version). If the packages of the code environment on the executor side differ, deserialization may fail, or the python code may fail at runtime.

Remediation
===========

- go to the code environment used by the recipe in ``Administration``
- ensure that the Spark config used by the recipe is among the Spark configs in the ``Containerized execution`` tab of the code environment
- ``Update`` the code environment to force a rebuild of the images
