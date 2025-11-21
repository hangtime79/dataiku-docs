Initial Setup
###############

.. contents::
	:local:

.. warning::

    This document only covers the initial setup of the local code isolation capability of the User Isolation Framework. Additional components will generally be required. Please refer to the adequate reference deployments and capabilities details.

In the rest of this document:

* ``dssuser`` means the UNIX user which runs the DSS software
* ``DATADIR`` means the directory in which DSS is running


Prerequisites and required information
----------------------------------------

Please read carefully the :doc:`prerequisites-limitations` documentation and check that you have all required information.

The most important parts here are:

* Having a keytab for the ``dssuser``
* Having administrator access to the Hadoop cluster
* Having root access to the local machine
* Having an initial list of end-user groups allowed to use the impersonation mechanisms.

Perform a regular DSS installation
------------------------------------

* Perform a regular DSS installation. See :doc:`/installation/custom/initial-install`.

* If needed, setup integration with your secure Hadoop cluster. See  :doc:`/hadoop/installation` and :doc:`/hadoop/secure-clusters`.

* If needed, setup integration with Spark. See :doc:`/spark/installation`.

.. note::

	It is possible to setup Spark integration after setting up UIF, but this require more manual work so we strongly recommend that you start by setting up Spark integration.


.. _install.impersonation:

Initialize UIF
--------------

* As ``dssuser``, stop DSS

.. code:: bash

	% cd DATADIR
	% ./bin/dss stop

* As ``root``, run, from ``DATADIR``

.. code:: bash

	./bin/dssadmin install-impersonation dssuser

Please pay attention to the messages emitted by this procedure. In particular, you might need to manually add a snippet to your ``sudoers`` configuration.

As ``root``, edit the ``/etc/dataiku-security/INSTALL_ID/security-config.ini`` file. In the ``[users]`` section, fill in the ``allowed_user_groups`` settings with the list of UNIX groups that your end users belong to. Only users belonging to these groups will be allowed to use the local code impersonation mechanism.

INSTALL_ID is a long string of random characters. One INSTALL_ID is created for each installation of DSS, so if you have several installations of DSS on the machine, you may have several folders in ``/etc/dataiku-security``. To find out the INSTALL_ID of your DSS instance, look into the ``DATADIR/install.ini`` file. You'll find a ``installid`` line which is your INSTALL_ID.

Additional setup for local filesystem access
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

The ``/etc/dataiku-security/INSTALL_ID/security-config.ini`` contains configuration keys in section ``[dirs]`` to ensure that
only those subdirectories of the local host which pertain to the DSS installation can be modified by the
DSS subprocesses which run with elevated privileges:

* ``dss_datadir`` : should contain the absolute path to the DSS data directory. This key is automatically set
  by the install-impersonation step.
* ``additional_allowed_file_dirs`` : this key is initially empty. It should be set to the list of local
  subdirectories which DSS is allowed to access *outside* the DSS data directory, including:

  * any local subdirectory configured as a local filesystem connection
  * any cgroup subdirectory configured for DSS resource control management (see :doc:`/operations/cgroups`).

Configure filesystem access on the DSS folders
-----------------------------------------------

You need to ensure that all end-user groups have read-only access to:

* The DSS datadir (including all parent folders)
* The DSS installation directory (including all parent folders)

``dssadmin install-impersonation`` automatically sets up 711 permission on the DSS datadir, but you might need to ensure proper access to parent folders.

Configure identity mapping
---------------------------

* As ``dssuser``, start DSS.

* Log in as a DSS administrator, and go to Administration > Settings > Security & Audit > Other security settings.

* DSS has been preconfigured with simple identity mapping rules (one-to-one both on users and groups).

* You can choose to configure this with different rule types:

  * One-to-one mapping
  * Single user mapping
  * Pattern mapping

    The matching pattern is a standard search-and-replace Java regular expression. ``(...)`` can be used to capture a substring in the DSS username, and ``$1``, ``$2``... mark the place where to insert these captured substrings in the UNIX username.
    
    For example, configuring the following rule:

      * Matching pattern: ``([^@]*)@mydomain.com``
      * Replacement (UNIX): ``$1``

    would map the DSS user ``first.last@mydomain.com`` to the UNIX user ``first.last``.
    
    For more information, see :doc:`concepts`.
* Save settings if needed.

