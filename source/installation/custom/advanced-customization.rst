Customizing DSS installation
############################

.. toctree::

.. contents::
    :local:

.. _install.ini:

Installation configuration file
===============================

The installation process for Data Science Studio can be customized through the ``DATADIR/install.ini`` configuration file.

This file is initialized with default values when the data directory is first created. It can be edited to specify
a number of non-default installation options, which are then preserved upon upgrades.

Modifying this file requires running a post-installation command to propagate the changes, and restarting DSS, as follows:

.. code-block:: bash
  
  # Stop DSS
  DATADIR/bin/dss stop
  # Edit installation options
  vi DATADIR/install.ini
  # Regenerate DSS configuration according to the new settings
  DATADIR/bin/dssadmin regenerate-config
  # Restart DSS
  DATADIR/bin/dss start

The ``install.ini`` installation configuration file is a standard INI-style `Python configuration file
<https://docs.python.org/2/library/configparser.html>`_ with ``[section]`` headers followed by ``key = value`` entries.
The following entries are set up by the initial installation and are mandatory:

.. code-block:: ini
  
  [general]
  # DSS node type (design node, api node...)
  nodetype = design

  [server]
  # DSS base port
  port = 11200

Additional installation options are described throughout this manual.

.. _config.https:

Configuring HTTPS
=================

By default, DSS listens to HTTP connections on the given base port, i.e. is accessible at address ``http://DSS_HOST:DSS_PORT``. Using installation
configuration directives, you can switch DSS to accepting HTTPS connection instead, i.e. answering ``https://DSS_HOST:DSS_PORT``.

You will need to generate and provide a SSL server certificate and private key file matching the domain name used by end users to reach DSS. You can
then configure DSS to switch to HTTPS by adding the following entries to the ``[server]`` section of the ``install.ini`` installation configuration
file:

.. code-block:: ini

  [server]
  ssl = true
  ssl_certificate = PATH_TO_CERTIFICATE_FILE
  ssl_certificate_key = PATH_TO_PRIVATE_KEY_FILE
  ssl_ciphers = recommended

You should then regenerate DSS configuration and restart DSS, as described in :ref:`install.ini`.

.. note::
  The optional ``ssl_ciphers = recommended`` configuration key restricts the set of SSL ciphers accepted by DSS to a safe subset, for better protection
  against known attacks, while staying compatible with most recent browsers and DSS-supported Linux platforms.

  Setting this key to ``default`` (or omitting it altogether) does not configure any restriction on the accepted SSL ciphers, which then fall back to the default list built into the nginx server.

.. note::
  You can also expose DSS to users over HTTPS by interposing a :doc:`reverse proxy <./reverse-proxy>`. This option is mandatory if you want
  to use default HTTPS port 443, as DSS cannot run with the superuser privileges necessary to listen on this port.

.. note::
  If all DSS users access it over HTTPS, you can enforce session cookies security as described in :doc:`/security/advanced-options`.


Configuring IPv6 support
========================

By default, DSS listens to IPv4 connections only. Using the following installation configuration directive, you can configure DSS to listen to IPv6
connections to its base port, in addition to IPv4 connections.

.. code-block:: ini
  
  [server]
  ipv6 = true

You should then regenerate DSS configuration and restart DSS, as described in :ref:`install.ini`.


Configuring log file rotation
=============================

Main DSS processes log files
----------------------------

DSS processes write their log files to directory ``DATADIR/run``:

+-----------------+------------------------------------------------+
|   backend.log   |           Main DSS process (backend)           |
+-----------------+------------------------------------------------+
| hproxy.log      | Hadoop connectivity process (hproxy, optional) |
+-----------------+------------------------------------------------+
| nginx.log       | HTTP server (nginx)                            |
+-----------------+------------------------------------------------+
| ipython.log     | Python / R notebook server (ipython)           |
+-----------------+------------------------------------------------+
| supervisord.log | Process control and supervision                |
+-----------------+------------------------------------------------+

By default, these log files are rotated when they reach a given size, and purged after a given number of rotations. The following installation
configuration directives can be used to customize this behavior:

.. code-block:: ini

  [logs]
  # Maximum file size, default 100MB.
  # Suffix multipliers "KB", "MB" and "GB" can be used in this value.
  logfiles_maxbytes = SIZE
  # Number of retained files, default 10.
  logfiles_backups = NUMBER_OF_FILES

You should then regenerate DSS configuration and restart DSS, as described in :ref:`install.ini`.


Additional DSS log files
------------------------

In addition to the main log files described above, DSS generates two additional log files in directory ``DATADIR/run``, which are handled differently:

* ``nginx/access.log`` :
  This is the access log for DSS HTTP server. Under normal utilization this file grows only slowly compared to the previous ones. It is not rotated automatically, but can be rotated manually through the standard nginx procedure, or using the manual log file rotation command described below.

* ``frontend.log`` :
  This is a low-level log for debug purposes only. It is rotated independently of the others, on a non-configurable schedule.


Manual log file rotation
------------------------

The following command forces DSS to close and reopen its log files (main DSS processes log files and nginx access log). Combined with standard tools
like ``logrotate(8)``, and the possibility to disable automatic log rotation as described above, this lets you take full control over the DSS log
rotation process, and integrate it in your log file handling framework.

.. code-block:: bash

  # Use standard Unix commands to rename DSS current log files
  ...
  # Force DSS to reopen new log files
  DATADIR/bin/dss reopenlogs

