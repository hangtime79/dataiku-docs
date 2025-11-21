Upload your files
####################

One of the easiest ways to create datasets in DSS is to upload your files to the DSS server.

From either the Flow or the datasets list, click on New dataset > Upload your files.

You can either drag-and-drop your files on the drop zone or click on the "Add file" button to select the file to upload.

After upload, DSS automatically parses and detect format, settings and schema for your new dataset.

.. _uploading-files-storage-location:

Storage location
==================

By default, when you upload files, they are stored within the DSS data directory, in the "uploads" folder.

Before clicking on "Create", you can select an alternative storage location for the uploaded files. You can store uploaded files in any "files-based" kind of DSS connection that has either the "Allow managed folders" flag or the "Allow managed datasets" flag set to true (Filesystem, HDFS, S3, GCS, Azure, FTP, SFTP, SSH).

.. note::

	Even when the uploaded files are put on HDFS, the dataset can't be used as Hive table. Use a normal HDFS dataset pointing at the same location as the dataset instead.


Size limitations
=================

There is no theoretical size limitation for uploading files to DSS.

You may encounter size issues related to the following:

* Whatever the storage location that you choose, DSS needs to store a temporary copy of the uploaded files on the DSS server before transferring them to the final storage location. You need to have at least twice the sum of the sizes to upload as free space on the partition where the DSS server is running.

* Reverse proxies or corporate firewalls running between DSS and your browser may impose size limitations. In that case, you will see a "413 error" in your browser. You need to ask your IT administrator to increase the upload size limitations, or use alternate ways to get your data to the DSS server.
