Installing an API node
########################

.. contents::
	:local:

You need to manually install one or several API Nodes:
 * If you want to create a static infrastructure in the API Deployer. See :doc:`/apinode/concepts` for more information.
 * If you don't plan on using API Deployer

If you plan to use Kubernetes-based infrastructures in the API Deployer, you do not need to install any API node. Installation will be fully managed.

The process of installing a DSS API node instance is very similar to a regular DSS installation. :doc:`requirements` and :doc:`initial-install` thus remain mostly valid.

Installation
==============

Unpack the kit like for a design node.

Then from the user account which will be used to run the DSS API node, enter the following command:

.. code-block:: bash

	dataiku-dss-VERSION/installer.sh -t api -d DATA_DIR -p PORT -l LICENSE_FILE

Where:

* DATA_DIR is the location of the data directory that you want to use. If the directory already exists, it must be empty.
* PORT is the base TCP port.
* LICENSE_FILE is your DSS license file.

In short, all installation steps are the same as for a design node, you simply need to add ``-t api`` to the ``installer.sh`` command-line.

.. note::

	Using the API node requires a specific DSS license. Please contact Dataiku for more information.

Dependencies handling, enabling startup at boot time, and starting the API node, work exactly as for the DSS design node.