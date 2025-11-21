Dataiku Projects
################

The *Dataiku Projects* screen lists all deployed projects, i.e. project bundles that are deployed and active on an automation node.

By default, all project infrastructures are monitored. You can exclude an infrastructure from Unified Monitoring by going to *Settings* (only available to administrators). Also see :doc:`unified-monitoring-settings`

Every project has a *Deployment Status*, *Model Status*, *Execution Status* and *Global Status*

Deployment Status
=================

This is the health status of the deployment, as reported by the Deployer.


Model Status
============

The Model Status of a project represents the worst model status aggregated from all models in this project.

Please see :doc:`model-status` for more details.


Execution Status
=================

The Execution Status of a project represents the worst execution status of all **enabled** scenarios in this project.


Data Status
===========

The Data Status of a project provides a condensed view of the most recent **Data Quality** rules execution. It reflects the worst outcome among all **active** rules.

For more details, please refer to the :doc:`/metrics-check-data-quality/data-quality-rules` documentation.


Global Status
=============

In addition to the three statuses detailed in the previous sections, every project has a "Global status",
which is computed by taking the worst of "Deployment Status", "Model Status" and "Execution Status".
