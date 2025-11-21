Installing a new DSS instance
#############################

.. contents::
    :local:

.. note::

	This is the documentation to perform a Custom Dataiku install of a new Dataiku DSS instance on a Linux server

	Other installation options are available (Dataiku Cloud Stacks, macOS, Windows, AWS sandbox, Azure sandbox, or Virtual Machine).
	Please see :doc:`/installation/index`.

Pre-requisites
===============

To install Dataiku DSS, you need:

* the installation tar.gz file
* to make sure that you meet the installation :doc:`requirements`.


Installation folders
======================

A Dataiku DSS installation spans over two folders:

* The installation directory, which contains the code of Dataiku DSS. This is the directory where the Dataiku DSS tarball is unzipped (denoted as "INSTALL_DIR")
* The data directory (which will later be named "DATA_DIR").

The data directory contains :

* The configuration of Dataiku DSS, including all user-generated configuration (datasets, recipes, insights, models, ...)
* Log files for the server components
* Log files of job executions
* Various caches and temporary files
* A Python virtual environment dedicated to running the Python components of Dataiku DSS, including any user-installed
  supplementary packages
* Dataiku DSS startup and shutdown scripts and command-line tools

Depending on your configuration, the data directory can also contain some managed datasets. Managed datasets can also be created outside of the data directory with some additional configuration.

It is highly recommended that you reserve at least 100 GB of space for the data directory.

The data directory should be entirely contained within a single mount and be a regular folder. Having foreign mounts within the data directory, or symlinking parts of the data directory to foreign mounts is not supported.

Installation
==============

Unpack
-------

Unpack the tar.gz in the location you have chosen for the installation directory.

.. code-block:: bash

	cd SOMEDIR
	tar xzf /PATH/TO/dataiku-dss-VERSION.tar.gz
	# This creates a directory named dataiku-dss-VERSION in the current directory
	# which contains DSS code for this version (no user file is written to it by DSS).
	# This directory is referred to as INSTALL_DIR in this document.


Install Dataiku DSS
-----------------------------

From the user account which will be used to run Dataiku DSS, enter the following command:

.. code-block:: bash

	dataiku-dss-VERSION/installer.sh -d /path/to/DATA_DIR -p PORT [-l LICENSE_FILE]

Where:

* DATA_DIR is the location of the data directory that you want to use. If the directory already exists, it must be empty.
* PORT is the base TCP port. Dataiku DSS will use several ports between PORT and PORT+10
* LICENSE_FILE is your Dataiku DSS license file.

.. warning::

	DATA_DIR must be outside of the install dir (i.e. DATA_DIR must not be within dataiku-dss-VERSION)

.. note::

	If you don't enter a license file at this point, DSS will start as a Free Edition. You can enter a license file at any time.

The installer automatically checks for any missing system dependencies. If any is missing, it will give you the command to run to install them with superuser privileges. After installation of dependencies is complete, you can start the Dataiku DSS installer again, using the same command as above.

.. _boot.startup:

(Optional) Enable startup at boot time
------------------------------------------

At the end of installation, Dataiku DSS will show you the optional command to run with superuser privileges to configure automatic boot-time startup:

.. code-block:: bash

	sudo INSTALL_DIR/scripts/install/install-boot.sh [-n INSTANCE_NAME] DSS_DATADIR DSS_USER

This configures a systemd-based system service with a default name of "dataiku" (in ``/etc/systemd/system/dataiku.service``), and enables it to automatically start at boot. You can then use standard service management commands to control this DSS instance, as in:

.. code-block:: bash

	# Start the DSS service
	sudo systemctl start dataiku
	# Stop the DSS service
	sudo systemctl stop dataiku
	# Get service status
	sudo systemctl status dataiku
	# Get service log
	sudo journalctl -u dataiku
	# Disable boot-time startup
	sudo systemctl disable dataiku

.. note::

    If you have several instances of DSS installed on the same host, and want more than one to automatically start at boot time, you need to provide different, non-default names for them so as to configure independent boot-time system services, as follows:

    .. code-block:: bash

        # Defines system service "dataiku.dev" for DSS design instance
        sudo DESIGN_INSTALL_DIR/scripts/install/install-boot.sh -n dev DESIGN_DATA_DIR DESIGN_USER_ACCOUNT
        # Defines system service "dataiku.prod" for DSS automation instance
        sudo AUTOMATION_INSTALL_DIR/scripts/install/install-boot.sh -n prod AUTOMATION_DATA_DIR AUTOMATION_USER_ACCOUNT

This system service is implemented by a helper script installed at ``/etc/dataiku/INSTANCE_ID/dataiku-boot``, where ``INSTANCE_ID`` is the unique id of this DSS instance (generated at installation time in ``DATA_DIR/install.ini``).

This script has an associated configuration file ``dataiku-boot.conf`` in the same directory (``/etc/dataiku/INSTANCE_ID/dataiku-boot.conf``).
This file can be used to configure the optional creation of resource control cgroups for use by this DSS instance, as described :doc:`here </operations/cgroups>`.

.. warning::

    Versions of Dataiku DSS prior to 13.x were using legacy systemv-based init scripts in ``/etc/init.d/dataiku[.NAME]`` for boot-time startup.

    In order to migrate an instance to the new systemd-based setup, you need to first remove its legacy startup script if any.

    Note that any customization for the legacy script (in ``/etc/default/dataiku`` or ``/etc/sysconfig/dataiku``) would have to be reinstalled in the new service configuration file at ``/etc/dataiku/INSTANCE_ID/dataiku-boot.conf``.

    Note also that service configuration keys have been renamed from ``DIP_xxx`` (legacy syntax) to ``DSS_xxx`` (new syntax).


Start Dataiku DSS
--------------------------

To directly start Dataiku DSS, run the following command:

.. code-block:: bash

	DATA_DIR/bin/dss start

To start the Dataiku DSS system service, run the following command:

.. code-block:: bash

    # Default DSS service
    sudo systemctl start dataiku

    # Named DSS service
    sudo systemctl start dataiku.INSTANCE_NAME

.. warning::

	Do not mix manual- and system-service-based startup and shutdown. A DSS instance started through systemctl (or at boot) should only be stopped or restarted through systemctl, so the operating system service manager can correctly keep track of the Dataiku DSS service status.


Complete installation example
================================

The following shows a transcript from a complete installation sequence:

.. code-block:: bash

	# Start from the home directory of user account "dataiku"
	# which will be used to run the Dataiku DSS
	# We will install DSS using data directory: /home/dataiku/dss_data
	$ pwd
	/home/dataiku
	$ ls -l
	-rw-rw-r-- 1 dataiku dataiku 159284660 Feb  4 15:20 dataiku-dss-VERSION.tar.gz
	-r-------- 1 dataiku dataiku       786 Jan 31 07:42 license.json

	# Unpack the distribution kit
	$ tar xzf dataiku-dss-VERSION.tar.gz

	# If the User Isolation Framework is to be configured on this instance,
	# make sure all user accounts have read-execute permission to the installation directory
	$ chmod a+x .
	$ umask 22

	# Run installer, with data directory $HOME/dss_data and base port 10000
	# This fails because of missing system dependencies
	$ dataiku-dss-VERSION/installer.sh -d /home/dataiku/dss_data -l /home/dataiku/license.json -p 10000

	# Install dependencies with elevated privileges, using the command shown by the previous step
	$ sudo -i "/home/dataiku/dataiku-dss-VERSION/scripts/install/install-deps.sh"

	# Rerun installer script, which will succeed this time
	$ dataiku-dss-VERSION/installer.sh -d /home/dataiku/dss_data -l /home/dataiku/license.json -p 10000

	# Manually start DSS, using the command shown by the installer step
	$ /home/dataiku/dss_data/bin/dss start

	# Connect to Dataiku DSS by opening the following URL in a web browser:
	#    http://HOSTNAME:10000
	# Initial credentials : username = "admin" / password = "admin"

	# [Optional] To finalize the installation, restart as a system-managed service:
	#
	# Stop the manually-started instance
	$ /home/dataiku/dss_data/bin/dss stop
	#
	# Create a system service, using the command shown by the previous step
	$ sudo "/home/dataiku/dataiku-dss-VERSION/scripts/install/install-boot.sh" "/home/dataiku/dss_data" dataiku
	#
	# Start the system service
	$ sudo systemctl start dataiku


Manual dependency installation
==============================

The Dataiku DSS installer includes a dependency management script, to be run with superuser privileges,
which automatically installs the additional Linux packages required for your particular configuration.

In some cases however, it might be necessary to manually install these dependencies, for instance when the person installing
DSS does not have access to administrative privileges, or when the server does not have access to the required package
repositories.

You can check for missing packages by running the dependency installer script with option ``-check``. This does not require superuser privileges:

.. code-block:: bash

	$ dataiku-dss-VERSION/scripts/install/install-deps.sh -check [-with-r]

If you manually pre-installed all the dependencies that would have been selected by the automated script, you can
continue installing Dataiku DSS using standard procedures. If that is not the case (because you explicitly chose to leave
a component missing, or you installed some component from an alternate source) you must then run the DSS installer
with the "-n" flag, to disable the default dependency checks.

.. code-block:: bash

	# Python 3 has been installed from a custom source instead of the standard system RPM
	# Force the DSS installer to run without checking for missing dependencies (option "-n")
	$ dataiku-dss-VERSION/installer.sh -n -d /home/dataiku/dss_data -l /home/dataiku/license.json -p 10000

RHEL-compatible distributions
-----------------------------

You may need to configure the EPEL additional repository, for R support (and for nginx, on version 7.x systems).

You may need to enable the "CodeReady", "PowerTools" or "Optional" repositories, for indirect dependencies required by R.

Dataiku DSS depends on the following packages:

+---------------------------------------------------------------------+------------------------------------------------------------------------------+
|                                 Name                                |                                    Notes                                     |
+=====================================================================+==============================================================================+
| acl                                                                 | For User Isolation Framework support                                         |
+---------------------------------------------------------------------+------------------------------------------------------------------------------+
| expat git nginx unzip zip                                           | Mandatory                                                                    |
+---------------------------------------------------------------------+------------------------------------------------------------------------------+
| java-17-openjdk-headless                                            | See "Java" note below                                                        |
+---------------------------------------------------------------------+------------------------------------------------------------------------------+
| python3 *or* python39 *or* python3.10 *or* python3.11               | For built-in Python packages. See "Python" note below                        |
+---------------------------------------------------------------------+------------------------------------------------------------------------------+
| freetype libgfortran libgomp                                        | Built-in Python packages dependencies                                        |
+---------------------------------------------------------------------+------------------------------------------------------------------------------+
| policycoreutils policycoreutils-python-utils                        | For SELinux support                                                          |
+---------------------------------------------------------------------+------------------------------------------------------------------------------+
| R-core-devel libicu-devel libcurl-devel openssl-devel libxml2-devel | For R support. See "R" note below                                            |
+---------------------------------------------------------------------+------------------------------------------------------------------------------+
| fontconfig dejavu-sans-fonts                                        | For font support                                                             |
+---------------------------------------------------------------------+------------------------------------------------------------------------------+
| glibc-langpack-en                                                   | For localization support                                                     |
+---------------------------------------------------------------------+------------------------------------------------------------------------------+
| procps-ng                                                           | For process management tools                                                 |
+---------------------------------------------------------------------+------------------------------------------------------------------------------+

Debian / Ubuntu Linux distributions
-----------------------------------

You may need to configure the CRAN repository, for R support (https://cran.r-project.org/).

Dataiku DSS depends on the following packages:

+------------------------------------------------------------------------------+--------------------------------------------------------------+
|                                     Name                                     |                            Notes                             |
+==============================================================================+==============================================================+
| acl                                                                          | For User Isolation Framework support                         |
+------------------------------------------------------------------------------+--------------------------------------------------------------+
| curl git libexpat1 nginx unzip zip                                           | Mandatory                                                    |
+------------------------------------------------------------------------------+--------------------------------------------------------------+
| openjdk-17-jre-headless                                                      | See "Java" note below                                        |
+------------------------------------------------------------------------------+--------------------------------------------------------------+
| python3.9 *or* python3.10 *or* python3.11                                    | For built-in Python packages. See "Python" note below        |
+------------------------------------------------------------------------------+--------------------------------------------------------------+
| python3-distutils libfreetype6 libgomp1                                      | Built-in Python packages dependencies                        |
+------------------------------------------------------------------------------+--------------------------------------------------------------+
| r-base-dev libicu-dev libcurl4-openssl-dev libssl-dev libxml2-dev pkg-config | For R support. See "R" note below                            |
+------------------------------------------------------------------------------+--------------------------------------------------------------+
| fontconfig fonts-dejavu                                                      | For font support                                             |
+------------------------------------------------------------------------------+--------------------------------------------------------------+
| locales                                                                      | For localization support                                     |
+------------------------------------------------------------------------------+--------------------------------------------------------------+
| procps                                                                       | For process management tools                                 |
+------------------------------------------------------------------------------+--------------------------------------------------------------+

Amazon Linux distributions
--------------------------

On Amazon Linux 2, you may need to enable "extra" repositories for nginx and Java 17, and EPEL for R support.

Dataiku DSS depends on the following packages:

+---------------------------------------------------------------------+------------------------------------------------------------------------------+
|                                 Name                                |                                    Notes                                     |
+=====================================================================+==============================================================================+
| acl                                                                 | For User Isolation Framework support                                         |
+---------------------------------------------------------------------+------------------------------------------------------------------------------+
| expat git nginx unzip zip                                           | Mandatory                                                                    |
+---------------------------------------------------------------------+------------------------------------------------------------------------------+
| java-17-amazon-corretto-headless                                    | See "Java" note below                                                        |
+---------------------------------------------------------------------+------------------------------------------------------------------------------+
| python3                                                             | For built-in Python packages. See "Python" note below                        |
+---------------------------------------------------------------------+------------------------------------------------------------------------------+
| libgomp                                                             | Built-in Python packages dependencies                                        |
+---------------------------------------------------------------------+------------------------------------------------------------------------------+
| freetype compat-gcc-48-libgfortran                                  | [Amazon Linux 2] Built-in Python packages dependencies                       |
+---------------------------------------------------------------------+------------------------------------------------------------------------------+
| R-core-devel libicu-devel libcurl-devel openssl-devel libxml2-devel | For R support. See "R" note below                                            |
+---------------------------------------------------------------------+------------------------------------------------------------------------------+
| glibc-langpack-en                                                   | For localization support                                                     |
+---------------------------------------------------------------------+------------------------------------------------------------------------------+
| dejavu-sans-fonts fontconfig                                        | For font support                                                             |
+---------------------------------------------------------------------+------------------------------------------------------------------------------+
| procps-ng                                                           | For process management tools                                                 |
+---------------------------------------------------------------------+------------------------------------------------------------------------------+

SUSE Linux Enterprise Server distributions
------------------------------------------

You may need to configure the following additional repositories:

+-------+------------------------------------------------+-----------------------+
|  Name |             Address                            |   Notes               |
+=======+================================================+=======================+
| nginx | https://nginx.org/                             | [SLES 12.x] For nginx |
+-------+------------------------------------------------+-----------------------+
| R     | obs://devel:languages:R:patched/<SLES_VERSION> | For R support         |
+-------+------------------------------------------------+-----------------------+

Dataiku DSS depends on the following packages:

+------------------------------------------------------------------------------------+---------------------------------------------------------+
|                                        Name                                        |                          Notes                          |
+====================================================================================+=========================================================+
| acl                                                                                | For User Isolation Framework support                    |
+------------------------------------------------------------------------------------+---------------------------------------------------------+
| git-core libexpat1 nginx unzip zip gawk                                            | Mandatory                                               |
+------------------------------------------------------------------------------------+---------------------------------------------------------+
| java-17-openjdk-headless                                                           | See "Java" note below                                   |
+------------------------------------------------------------------------------------+---------------------------------------------------------+
| python3 *or* python39 *or* python310 *or* python311                                | For built-in Python packages. See "Python" note below   |
+------------------------------------------------------------------------------------+---------------------------------------------------------+
| libfreetype6 libgomp1                                                              | Built-in Python packages dependencies                   |
+------------------------------------------------------------------------------------+---------------------------------------------------------+
| libgfortran3                                                                       | \[SLES 12.x\] Built-in Python packages dependencies     |
+------------------------------------------------------------------------------------+---------------------------------------------------------+
| gcc-fortran R-core-devel libicu-devel libcurl-devel libopenssl-devel libxml2-devel | For R support. See "R" note below                       |
+------------------------------------------------------------------------------------+---------------------------------------------------------+
| Base development tools                                                             | For R support.                                          |
+------------------------------------------------------------------------------------+---------------------------------------------------------+
| dejavu-fonts fontconfig                                                            | For font support                                        |
+------------------------------------------------------------------------------------+---------------------------------------------------------+
| procps                                                                             | For process management tools                            |
+------------------------------------------------------------------------------------+---------------------------------------------------------+

Additional notes
----------------

Java
	DSS supports Java 17.
	
	The suggested dependency package is the platform default, but DSS can use other Java runtime environments.
	The Java version to use can be specified with the JAVA_HOME environment variable when running the DSS installer.

	See :doc:`/installation/custom/advanced-java-customization` for details.

Python
	DSS supports Python 3.9, 3.10 and 3.11 for its built-in environment.

	One of these versions must be installed on the host, and can be chosen with the ``-P PYTHONBIN`` option to the installer.

	Additional Python versions may be used for code environments.

Additional python packages
	Installing additional Python packages which include native code may require the system development tools to be installed
	(typically C/C++ compilers and headers), in addition to any package-specific system dependency.

R
	DSS requires R 4.x 

	The dependencies listed above as well as the system development tools are necessary to enable the initial R integration in DSS.
	Additional dependencies are usually needed in order to build additional R packages.
