ERR_ML_MODEL_DETAILS_OVERFLOW: Model details exceed size limit
##############################################################

Some details of this model require more memory than allowed, so DSS stopped reading those details to prevent
a large memory consumption by the backend.

This happens when the files containing details about the model are bigger than the allowed quota.
There are two usual underlying causes to this:

* This model is computed on a dataset with a very large number of columns
* This model is tree-based, has a very large number of nodes (numerous and/or very deep trees)

Remediation
===========

As a user, you can try reducing the size of the model (less columns, less trees, shallower trees).

A DSS administrator can also change the quota for this error, by setting the value of
``dku.fileSizeLimit.modelDetailJson`` in ``config/dip.properties`` in the data directory.
Specify the quota in bytes, defaults to 52428800 (i.e. 50 MB).

If this does not solve your issue, please report the issue to Dataiku support.
