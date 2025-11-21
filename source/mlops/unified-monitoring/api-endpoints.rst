API Endpoints
#############

The *API Endpoints* screen lists all endpoints that Unified Monitoring can detect.

Unified Monitoring can monitor:

* **Endpoints of API Services**: API Services deployed to an infrastructure defined in the Deployer, including third-party infrastructures (Amazon SageMaker, Google Vertex AI, Microsoft Azure Machine Learning, Databricks or Snowflake Snowpark Container Services). Also see  :doc:`/apinode/first-service-apideployer`.
* **External Endpoints**: Endpoints deployed to third-party infrastructures, not managed by Dataiku. In order to see those endpoints, you need to declare additional "Monitoring Scopes" (only available to administrators) as detailed in :doc:`unified-monitoring-settings`.

Every API Endpoint has a "Global Status", a "Deployment Status" and may have a "Model Status", if Unified Monitoring was able to link this endpoint to a DSS Saved Model.

Unified Monitoring may also be able to display "Response time", "Volume" and "Activity", if available for the endpoint.

Deployment Status
=================

The Deployment Status of an API Endpoint is the health status of the endpoint, as reported by the underlying infrastructure.


Model Status
============

The Model Status of an API Endpoint is the worst model status from all models
that could be matched to this API Endpoint.

Please see :doc:`model-status` for more details.


.. note::
    
    For External Endpoints, the Model Status can be computed only if this endpoint has a corresponding :doc:`External Model </mlops/external-models/index>`


Global Status
=============

In addition to the two statuses detailed in the previous sections, every API Endpoint has a "Global status",
which is computed by taking the worst of "Deployment Status" and "Model Status".


Activity Metrics
================

For every API Endpoint, Unified Monitoring will display activity metrics, if available.

.. note::

    Activity metrics are retrieved on a best-effort basis, as there are a number of scenarios where DSS might
    not be able to retrieve anything, including (but not limited to):

    * Permission issues with the monitoring solution of the third-party cloud provider.
    * For Dataiku endpoints, disabling or not correctly configuring the "Monitoring" section of the infrastructure.
    * For External endpoints, disabling or not correctly configuring the monitoring solution of the third-party cloud provider.


No longer available External Endpoints
======================================

If an External Endpoint, once monitored, is no longer detectable by Unified
Monitoring (possibly due to its deletion from the cloud provider), it will be
displayed in an error state.

To remove such API Endpoints from Unified Monitoring, click on the relevant row
and click on the "Remove" button in the modal window that appears (only
available to administrators).

