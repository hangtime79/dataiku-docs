Installing an automation node
###############################

.. contents::
	:local:

You need to manually install an automation node if you plan to deploy projects to automation. See :doc:`/deployment/index` for more information.
 

The process of installing a DSS automation node instance is very similar to a regular DSS installation. :doc:`requirements` and :doc:`initial-install` thus remain mostly valid.

Installation
==============

Unpack the kit like for a design node.

Then from the user account which will be used to run the DSS automation node, enter the following command:

.. code-block:: bash

	dataiku-dss-VERSION/installer.sh -t automation -d DATA_DIR -p PORT -l LICENSE_FILE

Where:

* DATA_DIR is the location of the data directory that you want to use. If the directory already exists, it must be empty.
* PORT is the base TCP port.
* LICENSE_FILE is your DSS license file.

In short, all installation steps are the same as for a design node, you simply need to add ``-t automation`` to the ``installer.sh`` command-line.

.. note::

	Using the automation node requires a specific DSS license. Please contact Dataiku for more information.

Dependencies handling, enabling startup at boot time, and starting the automation node, work exactly as for the DSS design node.