WARN_MISC_BASE_IMAGE_FROM_OLDER_DSS_IMAGE: Custom Base Image was built with an older DSS Version.
#################################################################################################

Building of Custom Base Images is a manual process and should be repeated every time DSS is upgraded, otherwise they might not be compatible with the new DSS Version.

Remediation
===========

Rebuild all Custom Base Images that are being used in the `Containerized execution` settings, using the Base Image from the new DSS Version.

