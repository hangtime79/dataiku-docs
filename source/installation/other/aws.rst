AWS "Sandbox" marketplace image
#################################

Dataiku provides a pre-built Marketplace AMI for running DSS on AWS EC2.

.. note::

	Of course, you can use the regular Linux installation procedure (:doc:`/installation/custom/initial-install`) on any compatible EC2 instance.

	The AMI provides a shorter path to having a working standalone DSS instance
	with default options.

.. warning::

	This AMI is provided as a way to quick start a DSS instance, mainly for testing purposes.
	It comes with several "pre-made" choices (accounts, disks, installation directories, ...) and installed packages and may not be suitable for all purposes.

	For production purposes, we strongly recommend using :doc:`/installation/cloudstacks-aws/index` instead

	This AMI does not come with any specific upgrade features. Use the regular DSS upgrade mechanisms.

	This AMI is generally not suitable for use as edge node of an existing Hadoop cluster. See :doc:`/hadoop/index` for more information. For these cases, we recommend you install a new instance of DSS on a manually installed Linux EC2 instance.
	Note that edge nodes for Hadoop clusters (except EMR) must generally not use AmazonLinux.

	This AMI is not usable out of the box with EMR. Additional setup is required. Alternatively, you can use
	our EMR-ready AMI. See :doc:`/hadoop/distributions/emr` for more information.

.. contents::
	:local:

Prerequisites
================

You need an AWS account to proceed. You will be billed only for the EC2 instance, the Marketplace AMI itself is free.

Installation
==============

See https://www.dataiku.com/dss/trynow/aws/

Manual launch details
----------------------

If you go with the Manual Launch, you should:

* In instance details, **enable the auto-assign public IP**.
* In security groups, **expose the standard HTTP and/or HTTPS ports and SSH port** for administration.
* At the launch, **select or create a public key** to be able to administrate the instance via SSH.

How to
=======

How do I use DSS?
------------------

DSS is available:

* As regular HTTP, on the port 80 of the EC2 instance.
* As HTTPS, on the port 443 of the EC2 instance - DSS is preloaded with a self-signed certificate, so you will get a security error. You can replace this with a real certificate afterwards.

At first launch, you will have to prove that you are the owner of the instance. Authenticate with:

* the instance id (i-xxxxxxxx) as login
* an empty password.

When first accessing the DSS UI, you will be prompted to register for the DSS free edition, or enter your DSS enterprise license.

How do I log into the EC2 instance?
-------------------------------------

You can log into the instance using the ``ec2-user`` account and the keypair that you
specified during setup of the instance.

Beware: DSS does not run under the ``ec2-user`` account, but under the ``dataiku`` account.
The ``ec2-user`` is sudoer, so from the ``ec2-user`` shell, you can use ``sudo su dataiku`` to get a shell as the ``dataiku`` user.

Out of the box, you cannot login as the ``dataiku`` user, and the ``dataiku`` user is not sudoer.
(you can add your SSH key to the authorized keys of dataiku, though).

Where is the DSS data directory?
----------------------------------

The DSS data directory on the EC2 instance is ``/home/dataiku/dss``. All operations on this data directory (like installing R, JDBC drivers, ...) must be performed as the ``dataiku`` user (see above).

What is installed by default?
------------------------------

The Dataiku AMI is based on AlmaLinux 8. It contains:

* A standard installation of Dataiku DSS running under Linux user account "dataiku".
* A local PostgreSQL database, with a connection to it pre-configured in DSS.
* A standard installation of R, also pre-configured in DSS.
* A nginx reverse proxy exposing DSS onto the standard HTTP port 80, and the standard HTTPS port 443 using a self-signed certificate. For better security, you can provide your own certificate in directory /etc/nginx/ssl.


How do I install JDBC drivers?
-------------------------------

JDBC drivers must be installed by copying the relevant files in the "lib/jdbc" folder of the DSS data directory (See :doc:`/installation/custom/jdbc`).

You can either download files from the instance or upload them using SSH. Copy into the ``/home/dataiku/dss/lib/jdbc`` folder must be done as the ``dataiku`` user (see above).