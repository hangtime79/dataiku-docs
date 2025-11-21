Diagnosing and debugging issues
#################################

The first step in diagnosing issues with DSS is to identify what kinds of issue you are having:

* A job fails
* A scenario fails
* A machine learning model fails
* Other issues

Initial investigation
=======================

* In case of job failure, follow the steps in :doc:`problems/job-fails`.
* In case of scenario failure, follow the steps in :doc:`problems/scenario-fails`.
* In case of machine learning model training failure, follow the steps in :doc:`problems/ml-train-fails`.

For other steps, if you see an error message in the DSS UI and cannot make sense of it, the first step is to study the log files of DSS.

Log files are stored in the ``run`` folder of the DSS data directory. For example, if you used ``/opt/dataiku/data`` as the data directory, the logs will be in ``/opt/dataiku/data/run``

You will find there the following files:

* ``backend.log``: Log file for the main backend server
* ``ipython.log``: Log file of the Jupyter notebook server
* ``hproxy.log``: Log file for the Hadoop validation engine (validating Hive recipes)
* ``nginx.log``: Log file for the web server serving the public port of DSS
* ``governserver.log``: (Applicable only to Govern node) Log file of the main Govern server

For design, automation and deployer nodes, the main log file is ``backend.log``. Look at this file for errors. You can also view the log files directly from DSS UI: go to Administration > Maintenance > Log files.

For govern nodes, the main log file is ``governserver.log``. Look at this file for errors.


Getting an instance diagnosis
==============================

When you encounter "global" issues in DSS (i.e., issues other than a job failure), and can't find a reason in the error details or log files, Dataiku Support will ask you to provide a *DSS instance diagnosis*

The instance diagnosis is a Zip file that contains a lot of information about the current DSS instance, its log files, configuration information, system information, environment data, ...

To generate a diagnosis:

* Go to Administration > Maintenance > Diagnostic tool.
* Click on "Run diagnostic tool"
* Once the tool is done, download the file and send it to Dataiku Support

Note that Dataiku Support does not accept files larger than 15 MB. If your diagnosis Zip is bigger than that, you can use a file transfer service to get the diagnosis to us. We recommend using *WeTransfer*, but any similar service (or internal service provided by your IT) can work.

What does the instance diagnosis contain
-----------------------------------------

* Information about the machine running DSS
* Log files of DSS 
* (Can be disabled) Configuration of DSS, which includes information about projects, datasets, recipes, connections, ...
* (Can be disabled) Listing of all files in the DSS data directory
* (Can be disabled) Information about what actions DSS is currently processing
* If applicable, information about your Hadoop and Spark setup

What doesn't the instance diagnosis contain
---------------------------------------------

The instance diagnosis does not contain any of your datasets or managed folders data.

How to check the content of the instance diagnosis ?
-----------------------------------------------------

The instance diagnosis is a simple Zip file, which you can open to check the contents before sending to Dataiku.