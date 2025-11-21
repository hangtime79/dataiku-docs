WARN_GIT_EXCLUDES_FILE_NOT_SET: Projects - Git excludesFile not set correctly
##############################################################################

Some Git projects in your Dataiku instance do not have the `core.excludesFile` option correctly configured in their Git settings. This setting ensures that project-specific directory, such as `.dss-meta`, are excluded from version control.

Remediation
===========

To avoid accidental commits of internal files, ensure that each Git repository is configured with the following:

.. code-block:: ini

    [core]
    excludesFile = $DSS_HOME/config/.dku-projects-gitignore

This file should also contain `.dss-meta` as an ignored pattern.