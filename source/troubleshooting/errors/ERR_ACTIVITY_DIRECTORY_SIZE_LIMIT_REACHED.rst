ERR_ACTIVITY_DIRECTORY_SIZE_LIMIT_REACHED: Job activity directory size limit reached
####################################################################################

The file system directory dedicated to a currently running job activity reached its size limit,
so DSS automatically killed the job to avoid consuming too much disk space on the server.


This error can be triggered when running a Join or Group recipe using the internal DSS engine.
While executing these recipes, the internal DSS engine will potentially have to spill a large amount of data to the disk, for example, when doing a cross join.

Remediation
===========

When executing a Join recipe, use the SQL or Spark engine if available. If all input datasets are on the same SQL connection, DSS will automatically select the SQL engine.

A DSS administrator can also change the limit for this error, by setting the value of
``dku.recipes.visual.h2based.directorySize.maxMB`` in ``config/dip.properties`` in the data directory.
Specify the limit in megabytes, defaults to 20000 (i.e. 20 GB).