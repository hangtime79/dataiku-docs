Upgrading FM
############

Description
===========

This guided setup allows you to upgrade an existing Dataiku Cloud Stacks for Google Cloud.
It assumes you had followed :doc:`the guided setup example <guided-setup-new-vpc-elastic-compute>` to build
your initial setup.

Steps
=====

.. warning::

  For any upgrade to Fleet Manager version 12.6.0 or higher, it is required to previously stop the virtual
  machine hosting Fleet Manager, or the upgrade process could fail.


Stop Fleet Manager server
-------------------------

* In the deployment manager, click on your deployment. We call it ``<deployment>``
* Unwind the list of resources then click on ``instance-<deployment>``
* Click on *Manage resource* at the top right
* In section *Network interfaces*, find the *Primary internal IP address* and make a note of it. We call it ``<fm-ip-address>``
* Then, click on the vertical dots *More actions* menu at the top right, then click on *Stop*
* Wait for the instance the reach the state *Stopped*

Backup Fleet Manager's data disk
--------------------------------

* Go back to the list of resources in the deployment manager
* Click on ``data-<deployment>``
* Click on *Manage resource* at the top right
* Click on *Create snapshot*
* Give it an identifiable name, for instance ``fm-backup-YYYYMMDD``, make a note of it, then click on *Create*
* Wait for the snapshot to reach status *Ready for use*

Delete the existing deployment
------------------------------

* Go back to the deployment in the Deployment Manager
* Click on *Delete*
* Keep option *Delete <deployment> and all resources created by it* selected
* Click on *Delete All*

Create the new stack
--------------------

* Follow :doc:`the guided setup example <guided-setup-new-vpc-elastic-compute>` to deploy the new version of Fleet Manager, but add new elements to the *properties* section:

  * ``privateIpAddress:<fm-private-ip>``

  * ``snapshot:global/snapshots/<snapshot-name>`` or ``snapshot:projects/<project-name>/global/snapshots/<snapshot-name>`` if the snapshot is in a different project


Troubleshooting
===============

PostgreSQL related error messages
---------------------------------

If you are troubleshooting a non-responsive Fleet Manager after an upgrade, you might want to observe the logs
displayed by ``sudo journalctl -u fm-setup``.

If you see the message ``Postgres server cannot be upgraded because it was not stopped properly. Please consult documentation.``
or ``PostgreSQL upgrade failed``, it is likely the machine hosting Fleet Manager was not properly
stopped before the upgrade. You can fix it by **upgrading** to an intermediate version first.

Follow these instructions:

* Replay step *Stop Fleet Manager server* above
* Make sure you still have the snapshot ID of the last working version of Fleet Manager
* Replay step *Delete the existing deployment* above
* Replay step *Create the new stack* above but use the following template URLs instead

.. code-block::

    gsutil cp gs://dataiku-cloudstacks/templates/fleet-manager/12.5.2/fleet-manager-instance.jinja .
    gsutil cp gs://dataiku-cloudstacks/templates/fleet-manager/12.5.2/fleet-manager-instance.jinja.schema .

* Restart the upgrade process

DSS machines seem unresponsive
------------------------------

In case the DSS machines seem unresponsive in the FM UI following the upgrade, reprovision the different DSS machines for them to be able to communicate again with FM.
