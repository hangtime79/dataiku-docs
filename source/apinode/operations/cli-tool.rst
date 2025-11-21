Using the apinode-admin tool
##############################

A DSS API node deployment includes a command-line tool to manage the API node: ``./bin/apinode-admin``

Almost all administration operations can be performed using this command-line tool running locally on the DSS API node server.

.. note::

	This method is not available on Dataiku Cloud.

.. note::

	API node administration can also be performed (including remotely) through the REST Admin API or its Python client.
	See :doc:`../api/admin-api` for more information.


The general syntax is:

.. code-block:: bash

	./bin/apinode-admin COMMAND COMMAND_ARGS

* Running ``./bin/apinode-admin -h`` lists the available commands
* Running ``./bin/apinode-admin COMMAND -h`` prints the help for COMMAND

The main commands of the apinode-admin tool are:

Commands to manage the list of services
========================================

* ``services-list``
* ``service-create``
* ``service-delete``

Commands to manage the on-disk generations of a service
=========================================================

* ``service-import-generation``
* ``service-list-generations``

Commands to manage the activation of generations
=========================================================

* ``service-switch-to-newest``
* ``service-switch-to-generation``
* ``service-set-mapping`` (Command to set a multi-version service. See :doc:`../managing_versions`)

* ``service-enable``
* ``service-disable``

Commands for administration API keys management
===================================================

* ``admin-keys-list``
* ``admin-key-create``
* ``admin-key-delete``

Other commands
=================

* ``metrics-get``
* ``predict``
