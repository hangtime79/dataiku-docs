Default storage of audit trail
################################

By default, the audit trail is logged in the ``run/audit`` folder of the DSS data directory.

This folder is made of several log files, rotated automatically. Each file is rotated when it reaches 100 MB, and up to 20 history files are kept

Each audit log files is made of one JSON record per line.