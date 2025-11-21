Monitoring DSS
###############

Monitoring the behaviour and proper function of DSS is essential to production readiness and evaluating sizing.

.. contents::
	:local:

Concepts
=========

Monitoring DSS is essentially based on three topics:

* Raising alerts when some services are not working properly
* Storing and plotting immediate and historical data of host-level statistics (CPU, memory, IO, disk space, ...)
* Storing and plotting immediate and historical data of application-level statistics (users logged in, number of jobs, number of scenarios, ...)

DSS itself does not include a monitoring infrastructure (alerting or historical graphs) but provides many APIs and monitoring points that allow you to plug your own monitoring infrastructure onto it.

Any monitoring software that has the ability to run scripts or call HTTP APIs can be used to monitor DSS.

However, Dataiku provides a **non-supported** open source tool called **dkumonitor** that bundles together the common "Graphite / Grafana" stack for easy setup. Usage of dkumonitor is completely optional, it simply provides you with a quick way to deploy this monitoring stack.

Historizing metrics
====================

Historizing metrics can be done in two main ways:

* DSS pushes metrics to an historization system
* An historization system regularly pulls metrics from DSS

Install the dkumonitor service (optional)
------------------------------------------

dkumonitor is useful if you don't already have a Graphite / Grafana stack

Go to https://github.com/dataiku/dkumonitor and follow the instructions

Configure DSS to push metrics
-----------------------------

DSS can be configured to send internal and system metrics about the studio to a metrics server. DSS currently supports Graphite (Carbon) servers.

When the monitoring integration is installed:

* DSS will automatically install and configure a collectd agent. This agent collects host-level statistics and sends them to the Carbon server
* The DSS backend will start reporting its own application-level metrics to the same Carbon server

You can install the monitoring integration at any time.

Prerequisites
%%%%%%%%%%%%%%

The DSS monitoring integration is only supported on Linux platforms.

.. _monitoring_integration.online:

Case 1: Automatic installation, if your DSS server has Internet access
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

This procedure installs the required binaries and configures the monitoring integration for DSS.

* Go to the DSS data dir

  .. code-block:: bash

    cd DATADIR

* Stop DSS

  .. code-block:: bash

    ./bin/dss stop

* Run the installation script

  .. code-block:: bash

    ./bin/dssadmin install-monitoring-integration -graphiteServer GRAPHITE_HOST:GRAPHITE_PORT

.. note::

	If you already set up a Graphite server into the DSS Administration panel, this step will not override your current settings.
	To let the setup change these fields too, empty them beforehand.

.. note::

	If you have installed dkumonitor, you need to enter the "base port" of dkumonitor + 1. If you installed dkumonitor on port 27600, then use 27601 as -graphiteServer option

* Start DSS

  .. code-block:: bash

    ./bin/dss start

.. note::

  A prefix for the metrics is automatically computed. If your host is called `host.domain.ext`, 
  the prefix will be `dss.ext.domain.host.DSS_PORT`. You can override this prefix by using 
  the `-prefix` option when running the integration.


Case 2: If your DSS server does not have Internet access
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

To help with the monitoring installation when the DSS server does not have Internet access (directly nor through a proxy), the DSS installation kit includes a standalone script which may be used to download the required binaries and store them to a directory suitable for offline installation on the DSS server.

* First, download and unpack DSS on a machine with an internet access, then run the following command.

  .. code-block:: bash

    dataiku-dss-VERSION/scripts/install/download-monitoring-packages.sh

* Transport the directory ``dataiku-dss-VERSION/tools/collectd`` to the DSS server and drop it in ``dataiku-dss-VERSION/tools/``.

* Run the monitoring integration as in :ref:`case 1 <monitoring_integration.online>`.

Raising alerts
===============

DSS does not provide any builtin alerting mechanism. Zabbix is a common choice for monitoring DSS and raising alerts.

There are a number of ways to do "immediate monitoring" of DSS to raise alerts as soon as an abnormal condition is detected.

Monitoring the "get-configuration" API endpoint (without authentication)
-------------------------------------------------------------------------

Configure your monitoring agent to regularly query the `/dip/api/get-configuration` endpoint on the DSS server. This endpoint is used to bootstrap the UI and does not require authentication.

If this endpoint returns 200, it gives a first indication that DSS is properly responding

Monitoring any public API endpoint (with authentication)
---------------------------------------------------------

You can regularly query any "read-only" public API endpoint. For example `/public/api/projects/` which lists the projects. This requires authenticating with an API key.

See :doc:`/publicapi/index` for more information

Running "canary" jobs
----------------------

One of the most complete ways to regularly test DSS is to:

* Create a dedicated monitoring project that has a very small and quick Flow
* Use the Python API to regularly run a small job and wait for it to complete successfully

Uninstall monitoring integration 
================================

If you installed the monitoring integration and wish to remove the integration, you can do so by removing the ``collectd`` section of your ``install.ini`` file through the following process: 

  .. code-block:: bash 

   # Stop DSS
   DATADIR/bin/dss stop
   # Edit installation options and remove the "collectd" section
   vi DATADIR/install.ini
   # Regenerate DSS configuration according to the new settings
   DATADIR/bin/dssadmin regenerate-config
   # Restart DSS
   DATADIR/bin/dss start

