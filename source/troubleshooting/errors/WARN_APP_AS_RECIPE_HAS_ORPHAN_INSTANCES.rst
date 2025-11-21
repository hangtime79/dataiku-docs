WARN_APP_AS_RECIPE_HAS_ORPHAN_INSTANCES: Too many Application-As-Recipe instances
#################################################################################

When the `Keep Instance` option is enabled for a given Application-As-Recipe, everytime the recipe is run, the instance is kept for troubleshooting purposes. This option should only be used temporarily since these instances can add up to a lot of disk usage.

Remediation
===========

Disable the `Keep Instance` option and/or delete the instances that are no longer necessary for troubleshooting.
