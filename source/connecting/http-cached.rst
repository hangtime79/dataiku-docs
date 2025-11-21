HTTP (with cache)
##################

.. contents::
  :local:

DSS can directly read data stored on HTTP or HTTPS servers using the :doc:`HTTP dataset <http>`. This "remote" dataset can only be used as input in DSS.

However, this often has bad performance characteristics because DSS needs to redownload the data each time it needs it. To handle this case, DSS provides the :doc:`/other_recipes/download`.

Creating a cached version of a HTTP source with the download recipe implies:

* Creating a download recipe, and its associated output managed folder
* Creating a :doc:`files-in-folder` based on the previous output managed folder

Since this process can be cumbersome, DSS provides a shortcut that automatically performs the previous actions.

* From the flow or the datasets list, click on "New dataset", then "Network > HTTP (with cache)"
* Enter the HTTP, HTTPS or FTP URL, and click on Check
* Choose the location where to store the downloaded data folder, a name for the folder, then click on "Create folder and download"
* DSS downloads the files, please wait
* Once download is done, click on "Create dataset on folder"
* You are taken to the definition of the "Files-in-folder" dataset
* Click on "Test" so that DSS automatically parses the data
* Create the dataset

Notes:

* You can only enter a single URL in the creation wizard, but you can add other later on in the definition of the download recipe.
* This wizard does not handle partitioned cases. If you want to manage partitioning, you need to manually create your download recipe.

