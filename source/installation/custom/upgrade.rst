Upgrading a DSS instance
########################

.. contents::
	:local:

.. note::

	On macOS, upgrade your instance by following the instructions on https://www.dataiku.com/product/get-started/mac/, and install directly over the existing application.  It's still a good idea to make a backup of the data directory first.


In the rest of this procedure, DATA_DIR denotes the location of the DSS Data directory.

Notes and limitations
=======================

For each version of DSS, we publish :doc:`/release_notes/index`, which indicate the detailed limitations, attention points and notes about release. We strongly advise that you read all release notes for the new DSS version before starting the upgrade.

Notably, some machine learning models often need to be retrained when upgrading between major DSS upgrades.

Ways to upgrade a DSS instance
================================

Upgrading an instance in-place
-------------------------------

This documentation explains how to upgrade a single DSS instance. After the upgrade completes, it is not possible to rollback the upgrade. We therefore strongly advise that you take a backup of the whole DATA_DIR prior to starting the upgrade procedure


Upgrading by project import/export
-----------------------------------

Some people perform upgrades by:

* Creating a new DSS instance
* Exporting projects from the old instance
* Importing the projects into the new instance
* Then only shutting down the old DSS instance

We *do not* recommend that you use this approach for the following reasons:

* It is much slower and requires much more operations than an instance clone

* While a project export carries all important parts of the projects, some things are NOT part of a project export and will be lost. This includes files written from Jupyter notebooks, SQL notebooks results, and the whole "state" of the Flow. In other words, all incremental computation state will be lost and all datasets / partitions will need to be recomputed.

If you want to keep the original instance up and running while trying the migration, please see the following procedure.

Upgrading by cloning the instance
----------------------------------

Some people prefer to keep an old instance running and to clone it to a new DSS instance that will be upgraded to the new version.

This requires a few additional migration operations and care:

* If you are going to run it on the same machine, keep in mind that each instance needs its own block of 10 consecutive TCP ports. Thus, the new instance needs to be installed on a different port range

* Changing the ``installid`` flag of the new instance is recommended to avoid conflicts.

* The new instance will run all scenarios just like the old one. This could lead to corrupted data

* If Graphite reporting is enabled, you need to change the prefix for the new instance in order not to corrupt the metrics.

We recommend that you get in touch with your Dataiku Customer Success Manager before such a procedure.

In any case, the path would be “duplicate the instance, migrate ports and DATA\_DIR, upgrade the new instance” (copying DATA\_DIR between DSS instances of distinct versions is not supported).

Pre-upgrade tasks
===================

.. warning::

	Before upgrading, it is very highly recommended to backup the whole content of the data directory.

Stop the old version of DSS

.. code-block:: bash

	DATA_DIR/bin/dss stop

Unpack the new software
=========================

Unpack the distribution tarball in the location you have chosen for the new installation directory.

.. code-block:: bash

	cd SOMEDIR
	tar xzf /PATH/TO/dataiku-dss-NEWVERSION.tar.gz
	# This creates installation directory SOMEDIR/dataiku-dss-NEWVERSION for the new version

Perform the upgrade
=========================

.. code-block:: bash

	dataiku-dss-NEWVERSION/installer.sh -d DATA_DIR -u

Like for normal install, DSS will check for missing system dependencies, and ask you to run a dependencies installation command with superuser privileges if needed.

DSS will ask you to confirm migration of the existing data directory

Post-upgrade tasks (before startup)
====================================

Update R installation
----------------------

If R installation has been performed (see: :doc:`r`), you must perform again the "install-R-integration" step after upgrade.

.. code-block:: bash

	DATA_DIR/bin/dssadmin install-R-integration

Reinstall graphics exports
---------------------------

If :doc:`graphics exports have been enabled </installation/custom/graphics-export>`, you must replay the same installation procedure

Reinstall standalone Hadoop and Spark
----------------------------------------

If you used standalone libraries for Hadoop and/or Spark, you need to rerun the corresponding install procedure.

User-isolation framework instances only: secure the new installation
----------------------------------------------------------------------

If :doc:`User Isolation Framework </user-isolation/index>` is enabled, you must rerun the
:ref:`install-impersonation <install.impersonation>` step (as root) to secure the new installation.

.. _upgrade.base-images:

Rebuild base images
--------------------

If :doc:`containerized execution has been enabled </containers/setup-k8s>`, you will need to :ref:`rebuild all base images <rebuild.base-images>`.

Start the new version of DSS
============================

To start DSS, run the following command:

.. code-block:: bash

	DATA_DIR/bin/dss start

Post-upgrade tasks (after startup)
====================================

Rebuild code envs
-----------------

For some major upgrades, you may need to rebuild the code environments that you already have. The reason is that core dependencies may have been updated, and DSS may not be compatible with the old core dependencies anymore.

If you are using code environments with containerized execution, make sure that all your :doc:`code env images have been rebuilt </containers/code-envs>` and you will need to update all your code environments accordingly (for the appropriate selected container configurations).

For more details, please check the release notes of your version

Retrain machine learning models
-------------------------------

For some major upgrades, you may need to retrain some of the machine learning models.

Note that in these cases, the packages deployed in an API node also need to be regenerated on DSS and redeployed on the API node.

For more details, please check the release notes of your version.

Rebuild code studio templates
-----------------------------

If :doc:`containerized execution has been enabled </containers/setup-k8s>`, and you have already :ref:`rebuilt your base images <upgrade.base-images>`, you will also need to rebuild all your code studio templates.

To rebuild these, there are two options:

* Run the following command:

.. code-block:: bash

	DATA_DIR/bin/dsscli code-studio-templates-build

* Or rebuild them via the Dataiku DSS interface. Go to Administration > Code Studios, select all the templates, and choose **Build** from the selection drop-down menu.
