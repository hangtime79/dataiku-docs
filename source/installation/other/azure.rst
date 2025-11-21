Azure "Sandbox" marketplace image
##################################

Dataiku provides a pre-built image for running DSS on Azure


.. note::

	Of course, you can use the regular Linux installation procedure (:doc:`/installation/custom/initial-install`) on any compatible Azure Linux instance.

	The image provides a shorter path to having a working standalone DSS instance
	with default options.


.. warning::

	This image is provided as a way to quick start a DSS instance, mainly for testing purposes.
	It comes with several "pre-made" choices (accounts, disks, installation directories, ...) and installed packages and may not be suitable for all purposes.

	For production purposes, we strongly recommend using :doc:`/installation/cloudstacks-azure/index` instead

	This image does not come with any specific upgrade features. Use the regular DSS upgrade mechanisms.

	This image is generally not suitable for use as edge node of an existing Hadoop cluster. See :doc:`/hadoop/index` for more information. For these cases, we recommend you install a new instance of DSS on a manually installed Linux Azure instance.

.. contents::
	:local:

Prerequisites
================

You need an Azure account to proceed. You will be billed only for the virtual machine instance, the image itself is free.

Installation
==============

See https://www.dataiku.com/dss/trynow/azure/

How to
=======

How do I use DSS?
------------------

DSS is available:

* As regular HTTP, on the port 80 of the Azure VM instance.
* As HTTPS, on the port 443 of the Azure VM instance - DSS is preloaded with a self-signed certificate, so you will get a security error. You can replace this with a real certificate afterwards.

When first accessing the DSS UI, you will be prompted to register for the DSS free edition, or enter your DSS enterprise license.

How do I log into the virtual machine instance?
--------------------------------------------------

Administrative (command-line) access can be obtained by logging-in through SSH using the credentials specified when creating the machine.

Beware: DSS does not run under this account, but under the ``dataiku`` account.
The administrative account is sudoer, so from its shell, you can use ``sudo su dataiku`` to get a shell as the ``dataiku`` user.

Out of the box, you cannot login as the ``dataiku`` user, and the ``dataiku`` user is not sudoer (you can add your SSH key to the authorized keys of dataiku, though).

Where is the DSS data directory?
----------------------------------

The DSS data directory on the Azure VM instance is ``/home/dataiku/dss``. All operations on this data directory (like installing JDBC drivers, ...) must be performed as the ``dataiku`` user (see above).

What is installed by default?
------------------------------

The Dataiku image is based on on CentOS 7. It contains:

* A standard installation of Dataiku DSS running under Linux user account "dataiku".
* A local PostgreSQL database, with a connection to it pre-configured in DSS.
* A standard installation of R, also pre-configured in DSS.
* A nginx reverse proxy exposing DSS onto the standard HTTP port 80, and the standard HTTPS port 443 using a self-signed certificate. For better security, you can provide your own certificate in directory /etc/nginx/ssl.

How do I install JDBC drivers?
-------------------------------

JDBC drivers must be installed by copying the relevant files in the "lib/jdbc" folder of the DSS data directory (See :doc:`/installation/custom/jdbc`).

You can either download files from the instance or upload them using SSH. Copy into the ``/home/dataiku/dss/lib/jdbc`` folder must be done as the ``dataiku`` user (see above).
