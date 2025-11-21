Troubleshooting
###############

sudo failed (exit code 1) when UIF is enabled and devtoolset-8 is installed
---------------------------------------------------------------------------

If devtoolset-8 is installed on your instance and you are using UIF, devtoolset-8 will include a non-compatible sudo in the default PATH. Note that if you recently installed :doc:`prophet</R/prophet>` you may encounter this error due to upgrading to devtoolset-8 in order to install the package. If you are using UIF and devtoolset-8 and receive a sudo error, you can force the use of the default sudo with the following steps:

Stop DSS: 

.. code-block:: bash 

    ./DATADIR/bin/dss stop 


Edit your ``DATADIR/install.ini`` file and add the entry: 

.. code-block:: bash 

    [mus]
    custom_root_sudo = ["/usr/bin/sudo"]

Start DSS: 

.. code-block:: bash 

    ./DATADIR/bin/dss start 