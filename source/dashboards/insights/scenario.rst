Scenarios
###############

DSS provides two very different kinds of insights about :doc:`scenarios </scenarios/index>`.

Scenario runs report
=======================

This insight displays a timeline of the last runs of a specific scenario, on a configurable time period. It is very similar to the view available per scenario in View > Last runs, or for multiple scenarios in Automation

* Display the listing of the files in the folder (with preview). This gives the ability to download each file or the whole folder content, as a .zip file
* Display the preview of a single file. This gives the ability to download the file. Note that downloading other files is not exposed but still technically feasible: the permissions granularity is the managed folder, not the file.

Publish
--------

You can publish a scenario runs report insight from several locations:

From the scenario
%%%%%%%%%%%%%%%%%%%%%

.. note::

	This method is only possible if you have at least the "Read project content" permission.

From the scenario's action menu, click Publish. This creates a new runs report insight.

From the dashboard
%%%%%%%%%%%%%%%%%%%%%%


Click on the + button to add tiles. Select scenario, then select "Last runs" and the scenario for which you want to display the timeline. If you only have dashboard access, you will only see the datasets, models and folders that have previously been :doc:`dashboard-authorized </security/authorized-objects>`.


Tile display
--------------

In the tile display, you can configure between various display modes for the timeline of past runs, and select a predefined time range over which scenario runs should be displayed.

Insight view
-------------

The insight full view gives you more advanced browsing capabilities in the scenario history. It is not possible to edit anything for a scenarios runs report insight.

Changing time range in the full view does not reflect on the tile.



Run a scenario button
========================

You can also create a "Run scenario" insight. This insight displays a button that allows dashboard-only users to run a scenario.

This insight gives some form of write access to people who don't normally have this kind of access, so you want to carefully evaluate the security implications of this insight.

A scenario whose run button is exposed on the dashboard always runs as the "Run as" user of the scenario (see :doc:`/scenarios/index` for more information). It does not run as the user who clicked the button (since the user who clicked the button might not have requested permissions on the data sources). However, the :doc:`DSS audit log </security/audit-trail>` will include information about the user who clicked the button.

Publish
---------

.. note::

	You can only publish a "Scenario run" button if you have the "Read project content" permission.


Click on the + button to add tiles. Select scenario, then select "Run button" and the scenario for which you want to create a run button

Dashboard authorization
--------------------------

Like for all other types of insights, a dashboard authorization. The "Scenario run" button needs a special "Run" permission on the dashboard authorization. This can be configured in the Dashboard authorizations page in the project settings.

If, when you create the Scenario run button,  you have the "Manage dashboard authorizations" permissions, the run dashboard authorization is automatically granted.

Tile display
--------------

The tile displays a big "Run" button, which turns into a "Running" info while the scenario is running. You can also click to Abort while the scenario is running.

There are no tile display specific options for the Scenario run button insight.

View and edit insight
------------------------

There is no full-size view for this insight