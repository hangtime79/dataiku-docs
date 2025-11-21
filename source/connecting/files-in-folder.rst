"Files in folder" dataset
##########################

A :doc:`managed folder <managed_folders>` is a generic object in the DSS flow that contains files. It can be read and written by Python or R recipes, and files can be added to it either manually or via an API.

In some setups, it is useful to recreate a dataset from such a managed folder.  To do this use the *Create Dataset* action for a manager folder, or 
use the *Files in folder* dataset.  This is accessed visually via the menu *+DATASET / Internal / Files from Folder*.

* Select the folder to read from
* If needed, select a pattern to select the files to read from the folder. If you don't select a pattern, all files in the folder are read.



This enables advanced setups like:

* Having a Python recipe download files from a files-oriented data store that DSS cannot read. The Python recipe downloads the files to a managed folder. This way, it does not have to deal with parsing the files.
* Having a files-in-folder dataset do the parsing and extraction from the intermediate folder.

.. note::

	Even when the folder backing the "Files in folder" dataset is on HDFS, the dataset can't be used as Hive table. Use a normal HDFS dataset pointing at the same location as the folder instead.
