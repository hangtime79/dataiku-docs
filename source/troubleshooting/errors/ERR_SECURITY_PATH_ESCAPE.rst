ERR_SECURITY_PATH_ESCAPE: The requested file is not within any allowed directory
################################################################################

DSS enables the user with direct access to some files. Such shall stay into the allowed directories. This error can be triggered if:

- The filename provided in the folder editor is pointing to a file outside said folder
- A report template file is referred to with a name pointing outside the template directory

Remediation
===========

Do not use directory change patterns into filenames like ``../``. If you do see how you could have triggered this error, please contact the support.

