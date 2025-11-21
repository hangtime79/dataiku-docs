Metric
########

The metric insight allows you to publish a :doc:`metric </metrics-check-data-quality/metrics>` about any supported object (dataset, saved model, managed folder or model evaluation store).

Publishing a metric insight
===========================

You can publish a metric insight from several locations:

From the metrics view
-----------------------

.. note::

	This method is only possible if you have at least the "Read project content" permission.

From the metrics view, either in a dataset, saved model or managed folder, you can click on the caret next to each metric, and click Publish

.. image:: /dashboards/img/publish-metric.png

From the dashboard
-------------------

Click on the + button to add tiles. Select metric, then select the data source for which you want to display a metric. If you only have dashboard access, you will only see the datasets, models and folders that have previously been :doc:`dashboard-authorized </security/authorized-objects>`.

Choose the metric to display. You can only add metrics which have already been computed.

Tile display
=============

The tile can display either:

* The current value of the metric as a large display (either a number, a histogram or a list of values).
* The history values

.. image:: /dashboards/img/metric-display.png

View insight
========================

The full-size view of the insight always displays the history value of the metric.

No edition is possible on the metric insight.