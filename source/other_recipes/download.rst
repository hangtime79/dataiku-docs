Download recipe
#################

.. contents::
	:local:

The "download" recipe allows you to download files from files-based connections, and store them in a DSS managed folder. The managed folder itself can be stored in any files-based connection that accepts managed folders.

Files-based connections mean the following:

* Filesystem
* HDFS
* S3
* GCS
* Azure Blob Storage
* FTP
* SFTP
* SSH
* HTTP (read-only, cannot write)

The download recipe only deals with files: it does not interpret the files, and does not create a directly usable dataset. It only creates a managed folder. Once you have created the download recipe and its associated output managed folder, you can create a "Files in folder" dataset based on the output managed folder. This "Files in folder" dataset deals with parsing the files in the managed folder, handling format, settings and schema.

Creating a download recipe
============================

From the Flow, click the "+Recipe" button, and select Visual > Download

Give a name to the output managed folder, and choose in which connection to store it.

Create the recipe. You can now add sources, and then "Run" the recipe to perform the initial download.

Selecting files from the sources
=================================

The download recipe gets files from a number of "sources" and mirrors them to the output folder.

You can use as source of download:

* A HTTP(s) URL (which can contain authentication)
* A FTP URL (which can contain authentication)
* A path within a Filesystem, HDFS, S3, GCS, Azure Blob, FTP, SFTP or SSH connection

The "Path in connection" text input defines the set of files to download from
the source. Standard globbing expansion patterns are supported, where a
question mark character ``?`` matches any character in a remote file or
directory name, and a star character ``*`` matches any sequence of characters
in a remote file or directory name. To match all files and subfolders in the
connection's startup directory, specify ``*`` as path.

Patterns can be absolute (with a leading ``/`` character) or relative, in which
case they are interpreted according to the default remote directory for this
connection.

Remote file names matching the given pattern are directly downloaded at the
top-level of the output folder. Remote directory names matching the
given pattern are downloaded as sub-directories of the output folder.
along with all their contents.

Only regular files and directory are considered when enumerating sources.
In particular, symbolic links are ignored.

Note that in order to avoid name collisions between downloaded files, renaming
rules may be applied during the mirroring process:

* When multiple data sources are defined for a single download recipe,
  individual file names are prefixed with the data source index and an underscore
  ``_`` character.
* When wildcard expansion patterns appear in source directory specifications,
  downloaded file or directory names are prefixed with enclosing directory names
  and an underscore ``_`` character.

Mirroring rules
----------------

Source files mirroring is performed according to file size and last modification
time. If a remote file is created or updated on the remote host, it will be
downloaded by the next output folder build operation. If a remote file
disappears from the remote host, its local mirror will be deleted by the next
output folder build operation.

This synchronization behavior can be customized with the two options:

* Delete extra files (true by default)
* Download up-to-date files (false by default)


Examples
---------

+-------------------+----------------------+---------------------+-----------------------+-------------------------+
| Path in           | Matched remote files | Downloaded files    | Downloaded files      |     Notes               |
| connection        |                      | (single source)     | (multi sources)       |                         |
+===================+======================+=====================+=======================+=========================+
| ``/stats/\*.log`` | /stats/20140102.log  | 20140102.log        | 1_20140102.log        | Pattern matches files   |
|                   | /stats/20140103.log  | 20140103.log        | 1_20140103.log        | in single directory     |
+-------------------+----------------------+---------------------+-----------------------+-------------------------+
| ``/stats*/*.log`` | /stats.2013/0101.log | stats.2013_0101.log | 1_stats.2013_0101.log | Pattern matches files   |
|                   | /stats.2013/0102.log | stats.2013_0102.log | 1_stats.2013_0102.log | in multiple directories |
|                   | /stats.2014/0101.log | stats.2014_0101.log | 1_stats.2014_0101.log |                         |
+-------------------+----------------------+---------------------+-----------------------+-------------------------+
| ``/stats\*``      | /stats.2013/0101.log | stats.2013/0101.log | stats.2013/1_0101.log | Pattern matches         |
|                   | /stats.2013/0102.log | stats.2013/0102.log | stats.2013/1_0102.log | directories             |
|                   | /stats.2014/0101.log | stats.2014/0101.log | stats.2014/1_0101.log |                         |
+-------------------+----------------------+---------------------+-----------------------+-------------------------+


Partitioned download recipes
=============================

The output folder of a download recipe can be partitioned like any other DSS managed folder. See :doc:`/partitions/index` for more information about partitioning.

When partitioning is activated for the output folder of a download recipe:

* Remote files are downloaded from origin servers one partition at a time, for
  each "build" of each partition of the output folder
* A set of expansion variables are available to include in the URL and remote path
  definitions, to choose remote file names from partition values.
* The source definition screen contains an additional input field "Partition to
  download for preview" - this value is used when individual data sources are checked through
  the "Check source" buttons.

The variable expansion patterns that can be used in URLs and remote paths to
define the set of files to download for a given dataset partition can be found
at :doc:`/partitions/variables`.

Example
---------

The following defines a download recipe from a directory of web server log files
accessible through a FTP server (similar instructions apply for any downloaded data):

* Create a download recipe. At that point, the output folder is not partitioned.

* Go to the output folder, then in Settings > Partitioning

* Add a time dimension named "date", period "DAY",
  pattern ``%Y/%M/%D/.*``. This defines the naming pattern for **downloaded
  files** (ie, in the managed folder storage).

* Save and go back to the download recipe definition

* Add a source to download from, and enter
  ``ftp://MYWEBSERVER/var/log/apache2/$DKU_DST_YEAR/$DKU_DST_MONTH/$DKU_DST_DAY/*.log``.
  This defines the naming pattern for **remote source** files.

* If you want to check that the details are correct, you need to provide a partition identifier. DSS
  will replace the ``DKU_DST_`` variables by the ones from the partition identifier

Given the above definitions, whenever you try to build partition "2017-02-05", the download recipe
will mirror all files named ``\*.log`` in
subdirectory ``/var/log/apache2/2017/02/05`` of the FTP server, and store them
in subdirectory ``2017/02/05`` of the managed folder

