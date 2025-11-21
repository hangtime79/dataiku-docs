A job fails
############

When a job fails, go to the page of the failed job. This page gives a lot of information about why jobs did not succeed.

Source dataset is not ready
============================

If this error appears, it means that one of the source datasets required for running this job was not usable, which can mean:

* For a database dataset, it was not possible to connect to the database
* For a SQL dataset, the source SQL table did not exist (or could not be accessed)
* For a filesystem (or HDFS, S3, Azure Blob, FTP, ...) dataset, the input data file or folder did not exist

The error message contains the name of the dataset having issues (as well as the partition, in the case of partitioned dataset). Explore this dataset, and fix the issues with the source data.

Dataset is already being built
===============================

One of the datasets (including intermediate datasets) that needed to be built is already being built by another job which is currently running. 

Wait for this other job to complete and retry.

One of the recipes failed
=========================

If you see the two-columns layout, with recipes on the left, and logs on the right, and one of the recipes is in "failed" state, click on it to see the logs of the recipe. Read carefully both the error message and the logs, which generally contain information about the cause of the failure.

In particular, in the case of code recipes, if your code failed, the error message will often be pretty generic like "Code failed, check the logs". You need to peruse through the log files to find the original failure in your code (it will generally be highlighted red).

Getting a job diagnosis
========================

When you encounter a job failure and can't find a reason in the error details or log files, Dataiku Support will ask you to provide a *Job diagnosis*

The job diagnosis is a Zip file that contains a lot of information about the job and some information about the current DSS instance, configuration information, system information, environment data, ...

To generate a job diagnosis:

* Go to the page of the affected job (whether the job failed or not)
* Click on Actions > Download job diagnosis
* This will download the job diagnosis to your local machine, that you can then send to Dataiku Support

Note that Dataiku Support does not accept files larger than 15 MB. If your job diagnosis Zip is bigger than that, you can use a file transfer service to get the diagnosis to us. We recommend using *WeTransfer*, but any similar service (or internal service provided by your IT) can work.