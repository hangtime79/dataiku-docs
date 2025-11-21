WARN_MISC_ENVVAR_SPECIAL_CHAR: Environment variables with special characters
############################################################################

Some of the environment variables in your DSS instance do not adhere to Kubernetes restrictions and will therefore not be propagated to containerized jobs.
For Kubernetes, a valid environment variable name must consist of alphabetic characters, digits, ``_``, ``-``, or ``.``, and must not start with a digit. The regular expression used for validation is ``[-._a-zA-Z][-._a-zA-Z0-9]*``.

Remediation
===========

If you need these environment variables to be propagated to containerized jobs, you must rename them to match the validation pattern used by Kubernetes.