ERR_FSPROVIDER_TOO_MANY_FILES: Attempted to enumerate too many files
####################################################################

While attempting to enumerate a large number of files in a file system-like connection, DSS reached a safety limit and automatically aborted the operation in order to not disrupt the DSS backend.

Some of the actions that can trigger this error include:

* trying to read from a dataset that is made up of a very large number of files
* clicking on the "List files" button before setting the root path of a dataset (listing all the files in a connection)
* trying to browse a folder that contains a very large number of files

Remediation
===========

* Prefer creating a connection with a path restriction, rather than a connection pointing to the root of a bucket. You can use the "Path from" field under the "Path restrictions" section of the connection settings
* Avoid clicking on the "List files" button when pointing to a location that contains a large number of files, or before you have set a root path location for the dataset
