WARN_RECIPE_SPARK_INDIRECT_S3: No direct access to read/write S3 dataset
########################################################################

You are running a recipe that uses Spark (either a Spark code recipe, or a visual recipe using the Spark engine). This recipe either reads or writes a S3 dataset.

However, your administrator has not granted you the "Read connection details" permission on the connection in which the S3 dataset lies.

Without this permission, your Spark job will not be able to read (or write) the S3 dataset directly, and will indeed need to go through a slow path. This will very strongly degrade the performance of your Spark job.

Remediation
===========

Your administrator needs to grant the "Details readable by" permission on the S3 connection to one of the groups you belong to.

More details on this permission can be found in :doc:`/security/connections`