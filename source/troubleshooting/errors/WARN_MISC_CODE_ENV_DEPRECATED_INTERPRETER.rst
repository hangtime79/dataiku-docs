WARN_MISC_CODE_ENV_DEPRECATED_INTERPRETER: Deprecated Python interpreter
########################################################################

The code environment use a deprecated Python interpreter.

Remediation
===========

Update the Python interpreter used by the code environment in the code environment settings.

As for the built-in environment, it can be updated in a few steps:

1. Delete the current built-in environment (``<DSS_HOME>/pyenv``)
2. run ``<INSTALL_DIR>/installer.sh -u -d <DSS_HOME> -P <Python interpreter>``