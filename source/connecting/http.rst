HTTP
#####

.. contents::
  :local:

DSS can read data stored on HTTP or HTTPS servers. This "remote" dataset can only be used as input in DSS.

.. warning::

	When using a HTTP dataset "as-is", data will be fetched from the HTTP source each time you access this dataset in Explore
	or Charts and the sample needs to be refreshed.

	Quite often, you'll want to use the :doc:`/other_recipes/download` to cache the contents from the HTTP server.

	The :doc:`/connecting/http-cached` dataset is a shortcut that allows you to quickly create a download recipe and its associated
	"files in folder" output dataset

	By default, the download recipe will still check the HTTP server for updates when its
	output folder is rebuilt. This behavior can be disabled.

Creating a HTTP dataset
==========================

* From the Flow or datasets list,  click the "New dataset" button and select "Network > HTTP"
* Enter the URL(s) to download, one per line.
* Click on Test to download the first URL and detect format and schema
  

Remote URL definition
------------------------

A remote source can be defined by a HTTP or HTTPS URL. HTTP/HTTPS URL may only
reference a single remote file, and wildcard expansion patterns are not
recognized in them.

Remote URL definitions can contain optional inline authentication credentials
and non-default network ports.

+-------------------------------------------------------+---------------------+
|                          URL                          | Downloaded files    |
|                                                       | (single source)     |
+=======================================================+=====================+
| ``http://HOST/stats/20140102.log``                    | 20140102.log        |
+-------------------------------------------------------+---------------------+
| ``http://USER:PASSWORD@HOST:8080/stats/20140102.log`` | 20140102.log        |
+-------------------------------------------------------+---------------------+


Partitioned HTTP dataset
=========================

It is possible to partition a HTTP dataset. Unlike with other kinds of files-based datasets, you do not partition a HTTP dataset by specifying folder patterns. That is because a HTTP dataset is not enumerable.

When partitioning is enabled for a HTTP dataset:

* Remote files are downloaded from origin servers one partition at a time, each time a sample is computed, or a recipe based
  on this dataset is run
* A set of expansion variables are available to include in the URL to choose remote file names from partition values.
* The source definition screen contains an additional input field "Preview partition" to define which partition is used when "Testing" the dataset in the dataset definition screen
* The source definition screen contains an additional input field "Partitions list" to manually set the list of possible partitions. This is used when trying to list partitions from the sample screen, from the metrics screen, or when using the "All available" partition dependency.

The expansion variables are the regular ``%Y, %M, %D, %H`` and ``%{dimension_name}`` that you use in other partitioned datasets.

.. warning::

	Expansion variables in download recipes are different

Example
---------

The following defines a HTTP dataset based on a web server that contains a file for each US state:

* Create a new HTTP dataset

* Click on activate partitioning, add a discrete partition dimension named "state"
* Set https://my-website/data/%{state}.csv as the URL
* Set "AZ" as the preview partition
* Optional: Set "AL,AZ ..... WY" as the partitions list
* Test and create

Given the above definitions, whenever you access partition ``NJ``, the HTTP dataset will only fetch the URL ``https://my-website/data/NJ.csv``.
