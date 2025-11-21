ERR_RECIPE_SYNC_AWS_DIFFERENT_REGIONS: Error in recipe engine: Redshift and S3 are in different AWS regions
################################################################################################################

DSS attempted to sync a Redshift cluster with a S3 dataset from another AWS regions, using "Redshift to S3" or "S3 to Redshift" engine. AWS does not currently allow this operation.

Remediation
===========

* Use a S3 bucket in the same AWS region as the Redshift cluster, or
* Use the DSS engine instead of "Redshift to S3" / "S3 to Redshift".
