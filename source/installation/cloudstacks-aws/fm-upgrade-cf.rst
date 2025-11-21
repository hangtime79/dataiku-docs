Upgrading FM
############


Description
===========

This guided setup allows you to upgrade an existing Dataiku Cloud Stacks for AWS.
It assumes you had followed :doc:`the guided setup example <guided-setup-new-vpc-elastic-compute>` to build
your initial setup.

**Prerequisites**

You need to have administrative access to an existing AWS subscription

Steps
=====

.. warning::

  For any upgrade to Fleet Manager version 12.6.0 or higher, it is required to previously stop the virtual
  machine hosting Fleet Manager, or the upgrade process could fail.


Stop Fleet Manager server
-------------------------

* Under *Cloud Formation*, find your already created stack and click on it
* Go to the *Resources* tab
* Copy the *Instance ID* (do not click on it)
* Go to the *EC2 console*, in the *Instances list*
* Add a filter ``Instance ID = <instance id>``, a single running instance shows up
* Click on the instance ID to open instance page
* Find FM private IP in *Private IPv4 addresses* and copy it
* Then, click on *Instance State > Stop instance*
* Wait for the instance to reach the state *Stopped*

Backup Fleet Manager's data disk
--------------------------------

* Under *Cloud Formation*, find your already created stack and click on it
* Go to the *Resources* tab
* Copy your data volume ID
* In *EC2 > Elastic Block Store > Volumes*, search using your volume ID
* Select your volume and click on *Actions > Create snapshot*
* Enter a description and click on *Create snapshot*
* Copy the snapshot ID

Delete your existing stack
--------------------------

* Under Cloud Formation, find your stack and click on *Resources*
* Click on the instance
* Note its IAM Role
* Go back in *Cloud Formation* and delete your stack
* Wait for the stack to be fully deleted

Create the new stack
--------------------

* Click on 'Create stack' > 'With new resources'
* In "Amazon S3 URL", enter ``https://dataiku-cloudstacks.s3.amazonaws.com/templates/fleet-manager/14.2.2/fleet-manager-instance.yml``
* Click on Next
* Enter the stack name
* Put the same basic settings as in the original setup including FM role / VPC and subnet
* Under *Advanced settings*, put the FM private IP you copied before and the snapshot ID
* If you have used a KMS key, specify it
* Click on *Next*
* Click on *Next* again
* Acknowledge the resources creation and submit


Troubleshooting
===============

PostgreSQL related error messages
---------------------------------

If you are troubleshooting a non-responsive Fleet Manager after an upgrade, you might want to observe the logs
displayed by ``sudo journalctl -u fm-setup``.

If you see the message ``Postgres server cannot be upgraded because it was not stopped properly. Please consult documentation.``
or ``PostgreSQL upgrade failed``, it is likely the machine hosting Fleet Manager was not properly
stopped before the upgrade. You can fix it by upgrading to an intermediate version first.

Follow these instructions:

* Replay step *Stop Fleet Manager server* above
* Make sure you still have the snapshot ID of the last working version of Fleet Manager
* Replay step *Delete your existing stack* above
* Replay step *Create the new stack* above but change the documented S3 URL to ``https://dataiku-cloudstacks.s3.amazonaws.com/templates/fleet-manager/12.5.2/fleet-manager-instance.yml``
* Resume the upgrade process

DSS machines seem unresponsive
------------------------------

In case the DSS machines seem unresponsive in the FM UI following the upgrade, reprovision the different DSS machines for them to be able to communicate again with FM.
