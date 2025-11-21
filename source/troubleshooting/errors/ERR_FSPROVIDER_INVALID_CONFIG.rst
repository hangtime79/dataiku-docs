ERR_FSPROVIDER_INVALID_CONFIG: Invalid configuration
############################################################

The configuration of a "Filesystem provider" is invalid.

Filesystem providers are used as the basis of:
 * All "files-based" datasets (Filesystem, HDFS, S3, GCS, Azure, FTP, SFTP, SCP, HTTP)
 * Managed folders

This error can happen:

 * When viewing or a using one of the above kinds of datasets
 * When running a job which involves one of the above kinds of datasets


Remediation
===========

Check the settings of the dataset or managed folder. The error message details what part of the configuration is invalid.

In some cases, the configuration issue can be at the connection level, in which case it must be fixed by your administrator.
