Dataset table
###############

A "dataset table" insight shows the dataset in a view fairly similar to the :doc:`Explore </explore/index>` view of a dataset.

Publishing a dataset table insight
====================================

You can publish a dataset table insight from several locations:

From a dataset
----------------

.. note::

	This method is only possible if you have at least the "Read project content" permission.

Either from the dataset's view, or from the Flow, click on the "Publish" button in the Actions column of the dataset.

This creates a new insight pointing to the dataset.

From the dashboard
-------------------

Click on the + button to add tiles. Select dataset table, then select the dataset for which you want to show the data. If you only have dashboard access, you will only see the datasets that have previously been :doc:`dashboard-authorized </security/authorized-objects>`.

You are redirected to the "Edit" view of the insight, which is similar to the Explore view of DSS.

When you go back to the dashboard, the tile shows the dataset

.. _Dataset table tile display:

Tile display
=============

The tile display of a "dataset table" displays the table. You can customize which elements are displayed. You cannot view or configure filters in the file.

For Elasticsearch datasets, the tile can also display the ":ref:`Search<Search view>`" tab, to allow users searching interactively in a dataset. Saved queries can be used but can not be created.

View and edit insight
========================

If you have write access to the chart insight, you can modify all settings, like in a regular dataset Explore (sampling, filters, displayed columns, sorting, coloring) in the Edit view of the insight.

If you only have read access, you can only see the table and cannot modify most elements. You can modify the filters but your changes to filters will not be persisted.

Changes to filters are only persisted if they are done in the "Edit" view by someone who has write access to the insight (and the insight is then saved).

The ":ref:`Search<Search view>`" tab is not available in insights for Elasticsearch datasets.
