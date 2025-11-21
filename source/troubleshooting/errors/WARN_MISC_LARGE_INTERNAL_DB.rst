WARN_MISC_LARGE_INTERNAL_DB: internal runtime database is too large
###################################################################

The internal runtime database exceeds the recommended size of 5GB. This threshold can be modified with the `dku.sanitycheck.runtimedb.internal_db_threshold_gb` dip property.

Remediation
===========

It is recommended to switch to external runtime database by following :ref:`these instructions<runtime_db.external>`.