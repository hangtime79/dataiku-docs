ERR_CONTAINER_IMAGE_PUSH_FAILED: Container image push failed
############################################################

When creating or updating a code environment, DSS tried to push the corresponding container
image(s) for containerized execution configuration(s) but one such push failed.

Most frequent causes are:

* The repository URL is incorrect
* The authentication mechanisms have not been properly setup (the ``docker push`` command must be already be fully functional for this repository)
* TLS security is required but has not been properly setup on that containerized execution configuration
* When using Amazon AWS EKS / ECR, the pre-push script is incorrect or not working

You can still use the code environment when running on the DSS backend and on containerized execution
configurations that do not need to pull the image from the registry (typically local Docker),
but won't be able to use the code environment on containerized execution configurations that need to
pull this image.

Remediation
===========

You can find the logs of the ``docker push`` command either in the code environment creation/update
window, or in the code environment logs. Also try (or ask your IT administrator to try) manually
pushing a dummy image to the same repository directly from the command line.
If you or your IT administrator cannot resolve the error from the logs, you can send those logs to Dataiku support.

