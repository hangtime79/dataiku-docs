Managed folders
#######################

.. contents::
	:local:

DSS comes with a large number of supported formats, machine learning engines, ... But sometimes you want to do more. If you need to store and manipulate data in a format not supported natively by DSS, or to use training algorithms without a scikit-learn interface, then DSS offers unstructured storage handles in the form of "Managed Folders". In there, you can read and write any kind of data, and you can do so on any filesystem-like connection (local filesystem of course, but also HDFS, S3, FTP...).

DSS does not try to read or write structured data from managed folders, but they appear in Flow and can be used for dependencies computation. Furthermore, you can upload and download files from the managed folder using the :doc:`/publicapi/index`.


Here are some example use cases:

* You have some files that DSS cannot read, but you have a Python library which can read them: upload the files to a manged folder, and use your Python library in a Python recipe to create a regular dataset

* You want to use Vowpal Wabbit to create a model. DSS does not have full-fledged integration in VW. Write a first Python recipe that has a managed folder as output, and write the saved VW model in it. Write another recipe that reads from the same managed folder to make a prediction recipe

* Anything else you might think of. Thanks to managed folders, DSS can help you even when it does not know about your data.


Creating a managed folder
=========================

Managed folders creation is available in the flow from the `New dataset` menu (under the name 'Folder'). To create a managed folder, you need to select an existing connection that supports folders:

* either a FS-like connection (filesystem, HDFS, S3, Azure, GCS, FTP, SSH) that has the `Allow managed folders` set
* or a custom FS provider (see :doc:`/plugins/reference/fsproviders`)

The default connection to create managed folders on is named ``managed_folders`` and corresponds to the `managed_folders` directory in DSS data directory, ie. resides on the filesystem of the DSS server.

.. note::

	If a connection allows managed folders, it is strongly recommended to setup naming rules for new datasets/folders, and default path/bucket if relevant, to prevent different managed folders/datasets from different projects from overlapping.


Using a managed folder
======================

Managed folders are primarily intended to be used as input or output for code recipes (Python, R, Scala), though some visual recipes dealing with unstructured data also use managed folders as output (Export, :doc:`Download </other_recipes/download>`, Merge Folder).

A managed folder can be used both as input or output of Python, R, PySpark and SparkR recipes.

* To use a managed folder as input, select it in the inputs selector
* To use a managed folder as output, click on the "Add" button of outputs, and select "Create folder" at the bottom. Enter a label for the managed folder.

Managed folders can also be used in Python and R notebooks, and in webapps.

The managed folder follows the usual conventions pertaining to file-like objects:

* objects inside the managed folder are identified by a "path" corresponding to their position w.r.t. the folder's root.
* objects have a size and can have a modification time (if the underlying storage system permits it)
* objects can be "files" or "directories". The latter has a size of 0, contains no data in itself, but contains other files or directories

.. note::

    Not all storage systems have a native concept of "directory", in which case directories are merely a logical structure inferred from the actual objects' paths (ie. the files' paths)

* when reading from a file, DSS returns a non-seekable stream of data
* when writing to a file, DSS doesn't support positioning, so the entire file is written from the beginning

Merge Folder Recipe
-------------------

The "merge folder" recipe allows you to copy all the files from one or multiple managed folders to another DSS managed folder from the same or from another connection that accepts managed folders.

Note that this recipe can be used to copy a managed folder from a connection to another, similarly to the "sync recipe", but with managed folders.



Local vs non-local 
===================

When a managed folder is "local", it is hosted on the filesystem on the DSS machine, where your code runs. This means that it is possible to interact with it directly, by retrieving its path from the Dataiku API.

In most cases, however, managed folder are "not local":

* Either because the data is actually hosted in another location (S3, HDFS, Azure Blob, ...)
* Or because your code is not running on the DSS machine (Kubernetes execution for instance), and thus cannot directly access its filesystem

In these cases, you can't retrieve the path, and must use the various APIs of DSS to download and upload files to the managed folder.


.. _usage-in-python:

Usage in Python
===============

To use a managed folder, retrieve its handle from the Python Dataiku API:

.. code-block:: python

	import dataiku

	handle = dataiku.Folder("folder_name")

You can then list the contents of the folder, as paths relative to its root.

.. code-block:: python

	import dataiku

	handle = dataiku.Folder("folder_name")
	# pass a partition identifier if the folder is partitioned
	paths = handle.list_paths_in_partition()

To read a file from the folder:

.. code-block:: python

    with handle.get_download_stream("myinputfile.txt") as f:
        data = f.read()

The `get_download_stream` method returns a Python "file-like" object, which can be used to other Python functions that support non-seekable file-like objects.

To read an image from the folder:

.. code-block:: python

    from PIL import Image

    images_folder = dataiku.Folder(FOLDER_ID)
    for img in [item["fullPath"] for item in images_folder.get_path_details()["children"]]:
        with images_folder.get_download_stream(path=img) as stream:
            im = Image.open(stream)

To write a file in the folder:

.. code-block:: python

    with handle.get_writer("myoutputfile.txt") as w:
        w.write("some data")

The Dataiku API also provides additional functions to interact with managed folders. See :doc:`devguide:concepts-and-examples/managed-folders`

In the specific case of local folders (i.e. hosted on the filesystem and you are not running in a container), you can use the `get_path` function to retrieve the path of the managed folder, and then read and write data directly (with the regular Python API for a local filesystem)

.. code-block:: python

    import dataiku, os.path

    handle = dataiku.Folder("folder_name")
    path = handle.get_path()

    with open(os.path.join(path, "myinputfile.txt")) as f:
        data = f.read()

Copy the contents of one folder to another folder: 

.. code-block:: python 

    import dataiku

    client = dataiku.api_client()
    project = client.get_project('PROJECT_KEY')

    source_folder = project.get_managed_folder("source_folder_id")
    target_folder = project.get_managed_folder("target_folder_id")
    
    # target_folder will now contain a copy of all files that were in source_folder
    future = source_folder.copy_to(target_folder)
    future.wait_for_result()


Usage in R
============

To list files in a managed folder:

.. code-block:: R

    library(dataiku)
    paths <- dkuManagedFolderPartitionPaths("folder_name")

To read a file from the folder:

.. code-block:: R

    data <- dkuManagedFolderDownloadPath("folder_name", "path_in_folder")

This method will try to parse the content. Please see ``dkuManagedFolderDownloadPath`` in the reference documentation for details: |R_dataiku_api_doc_url|.

To write a file to the folder:

.. code-block:: R
    
    # data must be a connection providing the data to upload
    dkuManagedFolderUploadPath("folder_name", "path_in_folder", data)

In the specific case of local folders (i.e. hosted on the filesystem and you are not running in a container), you can use the `dkuManagedFolderPath` function to retrieve the path of the managed folder, and then read and write data directly (with the regular R API for a local filesystem)

.. code-block:: R

    path <- dkuManagedFolderPath("folder_name")


Usage of a folder as a dataset
================================

The contents of a managed folder can be used to construct a filesystem dataset. This is done using the :doc:`/connecting/files-in-folder`.

This enables advanced setups like:

* Having a Python dataset download files from a files-oriented data store that DSS cannot read. The Python recipe downloads the files to a managed folder. This way, it does not have to deal with parsing the files.
* Having a files-in-folder dataset do the parsing and extraction from the intermediate folder.


Clearing
========

When a managed folder is built, DSS does not perform any cleaning of the folder's contents. The code of the recipe having the folder as output is responsible for performing any necessary cleanup.
