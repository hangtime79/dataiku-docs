Unified Monitoring Alerting
###########################

.. note::

    This screen is only available to administrators

**Unified Monitoring Alerting** allows administrators to create automated alert notifications when a deployed service, project, or endpoint status changes.

You can set up alerts for any item that is monitored by Unified Monitoring: deployed API services, projects, and external endpoints hosted by other cloud providers.

Alert scope
=================
Alerts are defined at the **infrastructure** level. You can further refine the scope of each alert by filtering based on deployments, endpoints, tags, or other available attributes that define the monitored elements.

Trigger conditions
===================
Administrators can configure alerts to be triggered based on the following status changes:

* **Any status change**
* **When status becomes unhealthy**
* **When status matches selected values**

Alert reporter
===============
To receive alerts when trigger conditions are met, you must assign a **reporter**, which defines how the alert is delivered. The following channels are supported:

* **Email**
* **Slack**
* **Microsoft Teams**
* **Webhook**

Each reporter type comes with a default alert template that highlights status changes for the monitored item.

.. note::

    You can use existing channels configured in the **Global Settings** of Dataiku DSS, or set up new ones.
