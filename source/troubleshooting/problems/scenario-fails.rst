A scenario fails
#################

When a scenario fails, go to the page of the failed scenario runs. This page gives a lot of information about why scenarios did not succeed.

One "build" step failed
============================

The most common issue with scenario is that one of the "build" or "train" steps failed. In that case, please see :doc:`job-fails`.

Getting a scenario diagnosis
=============================

.. note::

	If the scenario failure is caused by the failure of one of the underlying jobs, please be sure to also get a job diagnosis for this particular job.

	See :doc:`job-fails` for more information on getting job diagnosis.


When you encounter a scenario failure and can't find a reason in the error details or log files, Dataiku Support will ask you to provide a *Scenario diagnosis*

The scenario diagnosis is a Zip file that contains a lot of information about the scenario and some information about the current DSS instance, configuration information, system information, environment data, ...

To generate a scenario diagnosis:

* Go to the page of the affected scenario run (whether the scenario failed or not)
* Click on "Download scenario diagnosis"
* This will download the scenario diagnosis to your local machine, that you can then send to Dataiku Support

Note that Dataiku Support does not accept files larger than 15 MB. If your scenario diagnosis Zip is bigger than that, you can use a file transfer service to get the diagnosis to us. We recommend using *WeTransfer*, but any similar service (or internal service provided by your IT) can work.