Migration operations
####################

.. contents::
    :local:

Migrating the base port
=======================

It is possible to change the base port of an existing Data Science Studio instance, by editing the
:ref:`installation configuration file <install.ini>`:

* Stop DSS

  .. code-block:: bash

    DATADIR/bin/dss stop

* Edit the ``DATADIR/install.ini`` installation configuration file

  .. code-block:: ini

    [server]
    port = NEW_BASE_PORT

* Regenerate DSS configuration

  .. code-block:: bash

    DATADIR/bin/dssadmin regenerate-config

* Restart DSS

  .. code-block:: bash

    DATADIR/bin/dss start


Migrating the installation directory
====================================

It is possible to change the installation directory of an existing Data Science Studio instance, by replaying the installer in "upgrade" mode:

* Stop DSS

  .. code-block:: bash

    DATADIR/bin/dss stop

* Move the installed kit to its new location (or unpack the .tar.gz distribution archive to a new location)

  .. code-block:: bash

    mv OLD_DIR/dataiku-dss-VERSION NEW_DIR/
    # or
    cd NEW_DIR
    tar xf /PATH/TO/dataiku-dss-VERSION.tar.gz

* Run the installer in upgrade mode

  .. code-block:: bash

    NEW_DIR/dataiku-dss-VERSION/installer.sh -d DATA_DIR -u

* If you have configured DSS with :doc:`User Isolation Framework </user-isolation/index>`, run the impersonation installation
  step as ``root`` from ``DATADIR``

  .. code-block:: bash

    ./bin/dssadmin install-impersonation DSSUSER

* Restart DSS

  .. code-block:: bash

    DATADIR/bin/dss start


Migrating the data directory
============================

It is possible to change the path of the data directory of an existing Data Science Studio instance, by replaying the installer in "upgrade" mode.
Note that the Python virtual environment has to be rebuilt after migration. This is because Python virtual
environments embed their installation path in various places.

* Stop DSS

  .. code-block:: bash

    DATADIR/bin/dss stop

* Save the list of locally-installed Python packages

  .. code-block:: bash

    DATADIR/bin/pip freeze -l >local-python-packages.txt

* Move the data directory to its new location

  .. code-block:: bash

    mv DATADIR NEWDATADIR

* Remove the Python virtualenv, keeping a backup copy

  .. code-block:: bash

    mv NEWDATADIR/pyenv NEWDATADIR/pyenv.backup

* Run the installer in upgrade mode. This recreates the Python virtualenv

  .. code-block:: bash

    dataiku-dss-VERSION/installer.sh -d NEWDATADIR -u

* Reinstall locally-installed Python packages (if any)

  .. code-block:: bash

    NEWDATADIR/bin/pip install -r local-python-packages.txt

* If you have configured DSS with :doc:`User Isolation Framework </user-isolation/index>`:

    * As ``root``, edit the file ``/etc/dataiku-security/INSTALL_ID/security/security-config.ini`` to update, in section ``dirs``, the path under ``dss_data_dir``. For information on finding INSTALL_ID, see :doc:`/user-isolation/initial-setup`.
    * Still as ``root``, update the paths in sudoers file ``/etc/sudoers.d/dataiku-dss-<dss_user>-<dss_instance_id>`` to point to ``NEWDATADIR``
    * Still as ``root``, either:
      
      * Run ``NEWDATADIR/bin/dssadmin install-impersonation DSSUSER`` to update ``NEWDATADIR/security/execwrapper.sh``
      * Or, edit ``NEWDATADIR/security/execwrapper.sh`` and update the path to ``CONFIGDIR`` to point to ``NEWDATADIR``

* Restart DSS

  .. code-block:: bash

    NEWDATADIR/bin/dss start

* If you have configured DSS to :ref:`start automatically on server boot <boot.startup>`:
  
  * Re-run the ``install-boot.sh`` command (as root), or
  * Directly adjust the data directory path in the service configuration file, which you can locate with:
    ``ls -l /etc/default/dataiku* /etc/sysconfig/dataiku*``

* When everything is considered stable, remove the backup

  .. code-block:: bash

    rm -rf NEWDATADIR/pyenv.backup

.. note::

  If you could not save the list of locally-installed Python packages before migration (step 2 above), it is possible to reconstitute it
  by looking at the package installation directory:

  .. code-block:: bash

    ls -l NEWDATADIR/pyenv.backup/lib/python?.?/site-packages
    

Migrating DSS to start with a new user 
======================================

To switch the user that runs DSS or to switch DSS to run with a service account, you will perform a migration operation. In this section:

 * ``olddssuser`` is the original UNIX user which runs the DSS software
 * ``newdssuser`` is the new UNIX user to run the DSS software 

Before you start, make sure you have a :doc:`backup </operations/backups>` of your data directory. If you don't have one, create one now. 

* As the user ``olddssuser``, stop DSS:

  .. code-block:: bash 

      DATADIR/bin/dss stop

* Update the ownership of your install directory and data directory so that the new UNIX user ``newdssuser`` has proper access/permissions:

  .. code-block:: bash 

      sudo chown -Rh NEW_USER:NEW_GROUP INSTALLDIR DATADIR
    
* As the new ``newdssuser``, re-run installer in upgrade mode:
    
  .. code-block:: bash 

      INSTALLDIR/installer.sh -d DATADIR -u

* If you have UIF configured in your environment, re-run the :doc:`install-impersonation script </user-isolation/initial-setup>` as root, to point to the new ``newdssuser``:

  .. code-block:: bash
 
    ./DATADIR/bin/dssadmin install-impersonation newdssuser

* As the new ``newdssuser`` unix user, restart DSS: 

  .. code-block:: bash

      DATADIR/bin/dss start

* If you have a boot-up script installed, set start on boot to the new ``newdssuser``. Note that INSTALLDIR and DATADIR must be referenced by their full paths:

  .. code-block:: bash

      sudo -i INSTALLDIR/scripts/install/install-boot.sh DATADIR newdssuser 

