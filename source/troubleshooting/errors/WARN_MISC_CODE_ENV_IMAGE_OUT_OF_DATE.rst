WARN_MISC_CODE_ENV_IMAGE_OUT_OF_DATE: Code Environment images out of date
#########################################################################

Code Environment Images are built when Containerized Execution is enabled for a Code Environment. These Code Environment Images are built on top of Base Images (configured in the Containerized Execution Settings).
Because Code Environment Images are not automatically rebuilt when the Base Images are rebuilt, it is necessary to trigger this process manually.

Remediation
===========

Navigate to the affect Code Environment's `Containerized execution` settings and click the `Update` button. This will rebuild all Code Environment Images using the latest Base Images.