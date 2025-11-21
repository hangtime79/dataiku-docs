Dynamic dataset repeat
######################
Any external SQL table or non-partitioned file-based dataset (except if it's a
Delta Lake or an HDFS dataset) can be configured to be repeating. Such a
dataset takes a secondary "parameters" dataset as a setting and when read a
partial data extraction takes place as many times as there are rows in the
parameters dataset. Each time data is extracted, variables are expanded in
certain fields of the dataset settings based on the current row of the
parameters dataset. The content of the dataset is the concatenation of the
individual data extraction results.

SQL table dataset
=================

Variables can be used in the Connection tab of the dataset settings which
identify the table to read from, e.g. the **Database**, **Schema** and
**Table** settings in case of a Snowflake dataset.

Example use case
----------------

There are many similar tables, e.g. there is one table per movie distributor,
and there is also a dataset containing the names of those tables. In order to
have a single dataset reading from all those tables, again, assuming the same
or similar schema across the tables, you can build a Flow like this:

* Create an editable dataset containing table names
* Create a SQL dataset, enable the repeating feature picking the editable
  dataset as the repeating parameters dataset
* The table name format in the Connection tab of the SQL dataset settings could
  be something like this:
  ::

      MOVIES_${distributor}

File-based dataset
==================

Variables can be used in the file selection rules, i.e. in the explicit list of
**Files to include**, in the **Exclusion rules**, or in the
**Inclusion rules**.

Example use case
----------------

There is a folder with many files which get updated daily. In order to have a
dataset with only the most recently updated file, you can build a Flow like
this:

* Have a folder
* Create a list contents recipe to list files from this folder in order to get
  the files' paths and their last modification information
* Create a top N recipe to get the most recently updated file
* Create a files in folder dataset from the folder, enable the repeating
  feature picking the output dataset of the top N recipe as the repeating
  parameters dataset
* Set **Files selection** to "Explicitly select files" and add an item to the
  **Files to include** list using a variable referring to the repeating
  parameters dataset configuration

Configuring
===========

To enable a repeating dataset:

* Go to the settings of the dataset
* Go to the Advanced tab
* Within the **Dynamic dataset repeat** section, make sure **Enable** is
  checked and a dataset is selected in the **Parameters dataset** dropdown

Once enabled, you’ll notice a repeat icon on the dataset in the Flow.

By default a variable is created for each column of the parameters dataset
however it is also possible to create a mapping of column names to variable
names. Only the variables specified by the mapping will then be created. This
is useful to avoid variable shadowing.
