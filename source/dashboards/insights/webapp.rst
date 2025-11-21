Webapp
###############

A "webapp" insight displays the content of a :doc:`DSS webapp </webapps/index>`.

The insight is a read-only view of the webapp. For a webapp to be displayable in the dashboard, it must have been "run" at least once in the webapp editor.

Publishing a webapp insight
====================================

You can publish a webapp insight from several locations:

From the webapp
----------------

.. note::

	This method is only possible if you have at least the "Read project content" permission.


From the Webapp's view, click on Actions > Publish.

This creates a new insight pointing to the webapp.

From the dashboard
-------------------

Click on the + button to add tiles. Select "Webapp", then select the webapp that you want to display. If you only have dashboard access, you will only see the datasets that have previously been :doc:`dashboard-authorized </security/authorized-objects>`.

Tile and insight display
==========================

Both the tile view and the full insight view display the content of the webapp. It is not possible to modify anything in the insight. All editions must be done in the webapp editor.

.. include:: ../../webapps/dashboard-filters.rst
