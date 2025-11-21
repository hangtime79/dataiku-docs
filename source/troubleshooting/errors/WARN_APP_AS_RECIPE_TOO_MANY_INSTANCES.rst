WARN_APP_AS_RECIPE_TOO_MANY_INSTANCES: Application-As-Recipe instance has orphan instances
###########################################################################################

When the `Keep Instance` option is enabled for a given Application-As-Recipe, everytime the recipe is run, the instance is kept for troubleshooting purposes. These instances are not automatically deleted when the Application-As-Recipe is deleted and use disk space unnecessarily.

Remediation
===========

Delete the orphan instances mentioned in the warning message. A link for each instance is provided in the warning message to facilitate the deletion.
