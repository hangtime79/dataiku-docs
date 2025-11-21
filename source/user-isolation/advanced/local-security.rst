Configuration of the local security
#####################################

What are the sudo authorizations?
==================================

When you install impersonation, DSS adds a sudoers rule in ``/etc/sudoers.d/dataiku-dss-THE_DSS_USER-RANDOM_STRING``

.. note::

	If DSS could not install this sudoers rule, the impersonation setup asks
	you to do it manually

This rule allows DSS to run, as root, a small wrapper which is used:

* To execute user-submitted code as the end-user UNIX accounts
* To change permissions and ownerships on various files required by user-submitted code

No user-submitted code runs as root. The wrapper (also called the security module) has a specific configuration to limit which users it may run as.

Configuration of the local security module
============================================

When DSS runs a command on behalf of an end-user, it consults the security module configuration in ``/etc/dataiku-security/INSTALL_ID/security/security-config.ini``.

This ini file contains two important information:

* Which user groups it may change identity to. This is configured in ``[users]``, in the ``allowed_user_groups`` settings.
* Where DSS is located. DSS will not change any file permissions outside of this directory, unless explicitly allowed as stated below.

Splitted DSS datadirs
----------------------

In some configurations, you might have "splitted" your DSS datadir, by using symbolic links.

To allow the security module to change file permissions in the additional locations, fill in the ``additional_allowed_file_dirs`` in the ``dirs`` section.
