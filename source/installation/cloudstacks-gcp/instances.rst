Instances
###########

Fleet Manager manages three kinds of DSS instances:

* Design nodes
* Execution (aka automation) nodes
* Deployer nodes (usually you only have a single deployer node in your fleet)

Dashboard
==========

The main screen through which you will get information about your instance is the dashboard. It is refreshed automatically
and displays basic network information, data disk usage as well as the :ref:`agent <gcp-cloudstacks-concept-agent>` logs.

.. _gcp-cloudstacks-instance-lifecycle:

Lifecycle
===========

Provisioning
--------------

The provisioning is the sequence of operations required to have a running DSS reachable by users. Provisioning an instance
has two main stages:

- The provisioning of cloud resources required for the instance to run. It is mostly a virtual machine and a data disk.
- A software startup sequence run by the :ref:`agent <gcp-cloudstacks-concept-agent>` which runs internal setup tasks, the setup actions you
  defined in your instance template, and installs and upgrades DSS if required.

Some settings changes require that you deprovision an instance an provision it again, which is denoted as *reprovisioning*.

Deprovisioning
----------------

Deprovisioning an instance consists of terminating the cloud virtual machine. The Persistent Disk is kept. A deprovisioned instance costs the Persistent Disk storage fee.

Data management
================

When an instance is created, a data disk distinct from the OS disk is created, attached and mounted to store all the persistent
data. The persistent data on an instance includes, but is not limited to:

- The DSS data directory
- The docker daemon data directory
- The certificates generated if self-signed certificates or Let's Encrypt certificates are in use.

Settings
==========

An instance has various settings that can be set at different point of its lifecycle.

General settings
-----------------

Not documented yet

HTTPS settings
----------------

Not documented yet

Operations
============

Not documented yet
