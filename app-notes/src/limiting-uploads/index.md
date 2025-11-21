# Howto: Limit uploads for some users

  * [1. Overview](#1-overview)
  * [2. Prevent uploads in the data directory](#2-data-dir)
  * [3. Prevent all uploads](#3-all)


<a name="1-overview"></a>

## 1. Overview

This document provides a set of recommended steps when you, as a DSS administrator, want to restrict some users' ability to upload arbitrary datasets/files to DSS.

There are two main ways of uploading a dataset / file to DSS:

- Creating an [Uploaded dataset](https://doc.dataiku.com/dss/latest/connecting/upload.html)
- Creating a [Managed Folder](https://doc.dataiku.com/dss/latest/connecting/managed_folders.html) and uploading into it

Please note that of course even with those steps, a motivated user with some kind of write access would still be able to put some data that you cannot automatically control,
e.g. via a code recipe, or copy-pasting the into an inline dataset, etc.


<a name="2-data-dir"></a>

## 2. Prevent uploads in the data directory

By default, DSS has a built-in destination for Uploaded datasets, which is the `uploads` subdirectory inside the data directory.
You can disable uploads to this folder in Administration > Settings > Engines and Connection, by unchecking “Uploads in default location”.


<a name="3-all"></a>

## 3. Prevent all uploads

Even with the option above disabled, users may still create an Uploaded dataset or a Managed Folder
as long as they store them into any file-based Connection that allows it.

To prevent this:

- Prevent those users from creating connections (in the permissions of all the groups they belong to)
- Restrict existing file-based connections (any connection that can receive files like HDFS, FTP, S3, etc.), deleting them or making them either:
    - Not accessible to those users
    - Accessible but not writable
    - Writable (can rebuild external datasets on them) but not accepting managed folders nor managed datasets

You may want to create such a user and try it yourself while logged as this user to make sure you've closed all the easy accesses.

