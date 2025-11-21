Chart
#####

A chart insight shows a chart from the :doc:`data visualization </visualization/index>` component of DSS.

A chart insight shows a chart based on a dataset. Charts built in a visual analysis cannot be published to the Dashboard.

Publishing a chart insight
===========================

You can publish a chart insight from several locations:

From a dataset
----------------

.. note::

	This method is only possible if you have at least the "Read project content" permission.

When you are designing charts in the "Charts" tab of a dataset, once you are satisfied you can click on the "Publish" button.

This will copy the current chart to a new insight and publish it on a dashboard. Further modifications in the insight will not be reflected in the dataset chart, and further modifications in the dataset chart will not be reflected in the insight.

From the dashboard
-------------------

Click on the + button to add tiles. Select chart, then select the dataset on which you want to create a chart. If you only have dashboard access, you will only see the datasets that have previously been :doc:`dashboard-authorized </security/authorized-objects>`.

You are redirected to the "Edit" view of the insight, which is similar to the regular DSS charts editor. See :doc:`/visualization/index` for more information. Design your chart and save it.

When you go back to the dashboard, the tile shows your newly created chart.

Tile display
=============

The tile display of a chart only displays the chart itself. It does not display filters. You can choose whether you want to display the axis, legends and tooltips.

View and edit insights
========================

If you have write access to the chart insight, you can modify all settings (axis, legends, filters, ...) in the Edit view of the insight.

If you only have read access, you can only see the chart and cannot modify the axis and displayed data in the "View" display. You can modify the filters but your changes to filters will not be persisted.

Changes to filters are only persisted if they are done in the "Edit" view by someone who has write access to the insight (and the insight is then saved)
