Requirements
############

.. contents::
    :local:

Server
========

DSS must be installed on a Linux x86-64 server.

Linux distributions
-------------------

The following Linux distributions are fully supported, in 64-bit version only:

* Red Hat Enterprise Linux, version 8.10
* Red Hat Enterprise Linux, versions 9.x
* AlmaLinux, version 8.10
* AlmaLinux, versions 9.x
* Rocky Linux, version 8.10
* Rocky Linux, versions 9.x
* Oracle Linux, version 8.10
* Oracle Linux, versions 9.x
* Ubuntu Server, versions 20.04 LTS and 22.04 LTS
* Debian, versions 11 and 12
* Amazon Linux 2023
* SUSE Linux Enterprise Server 15 SP5 and SP6

These distributions should be up-to-date with respect to Linux patches and updates.

Support for the following Linux distributions is deprecated and will be removed in a future release:

* Amazon Linux 2

CPU
----

There are no specific CPU requirements. More cores will be required to maintain performance with larger DSS instances, or with more workloads.

RAM
-----

A minimum of 32 GB of RAM is required. More RAM will be required if you intend to load large datasets in memory (for example in the Jupyter notebook component), or for accomodating more users.

.. _requirements.disks:

Disks
------

It is highly recommended to run DSS on SSD drives.

While legacy rotational hard drives can be used, performance will be severely impacted, especially for larger instances, with many users. In these instances, rotational hard drives may lead to a non-workable experience.

Filesystem
-------------

**We strongly recommend only using XFS or ext4 as the filesystem on which DSS is installedd**

The filesystem on which DSS is installed must be POSIX compliant, case-sensitive, support POSIX file locks, POSIX ACLs and symbolic links.

.. warning::

	**Do NOT** install Dataiku DSS on a NFS filesystem (v3 or v4). This is known not to work, and will cause failures, hangs, and possible corruptions. This includes Amazon EFS.

	GlusterFS is known to cause instabilities and is not supported as the filesystem for installing DSS

Dataiku makes no particular recommendation as to the underlying block device. In particular, Dataiku does not have experience working with DRDB as the underlying block device and cannot provide recommendations about it.


System settings
----------------

* The hard limit on the maximum number of open files for the Unix user account running DSS must be at least 65536 (``ulimit -Hn``). For very large DSS instances, larger values may be required.

* The hard limit on the maximum number of user processes for the Unix user account running DSS must be at least 65536 (``ulimit -Hu``). For very large DSS instances, larger values may be required.

* The en_US.utf8 locale must be installed.

* Root access is not strictly required, but you might need it to install dependencies. If you want to start DSS at machine boot time, or use the :doc:`User Isolation Framework </user-isolation/index>`, root access is required.

* It is highly recommended to create an UNIX user dedicated to running the DSS. Running DSS as root is not supported.

* DSS has experimental support for running on Redhat 8 with FIPS-140-2 mode enabled. Please reach out to your Dataiku Customer Success Manager to learn more.

Networking
-----------

DSS may use up to 10 consecutive TCP ports. Only the first of these ports needs to be opened out of the machine. It is highly recommended to firewall the other ports.

Browser support
=================

Dataiku DSS is accessed over a Web browser.

The following browsers are supported:

* Google Chrome (latest version)
* Mozilla Firefox (latest ESR version)
* Microsoft Edge (latest version)

.. warning:: Proxy support

	DSS makes use of WebSockets technology. If a proxy is used between the user's browser and the DSS server, the proxy must support WebSockets.
	In case of doubt, it is recommended not to use any proxy between the browser and the DSS server.
