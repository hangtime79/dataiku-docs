ERR_MISC_DISK_FULL: Disk is almost full
#######################################

The file system mentioned in the error is almost full. This error is triggered when a file system is over 90% full. This threshold can be modified with the `dku.sanitycheck.diskusage.threshold` dip property.
Note that the value must be a percentage (i.e. `dku.sanitycheck.diskusage.threshold=85` for 85%).

Remediation
===========

Various subsystems of DSS consume disk space in the DSS data directory, see :doc:`/operations/disk-usage` for more details.
