ERR_PLUGIN_MISSING_IN_CONTAINER_IMAGE: Plugin is missing in container image
###########################################################################

DSS is trying to run a recipe in a container, but one of the inputs or outputs or a step in the Prepare recipe's script is provided by a plugin that has not been installed in the container image. 

Remediation
===========

If the plugin has been removed completely from the DSS instance, the DSS administrator need to re-install it. If the plugin is installed in DSS, then the DSS administrator needs to ensure the plugin is selected to be included in the container image, and rebuild the container image

* on the plugin page, make sure ``Containerized visual recipes`` is "Enabled". If not, use "include in image"
