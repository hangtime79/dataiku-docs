Model report
###############

A "model report" insight shows the result screens of the active version of a saved model (deployed in Flow).

A model report insight cannot show a model which is still living in a visual analysis. Only models that have been deployed to the Flow can be put in a model report insight. For more information, see :doc:`/machine-learning/index`

Publishing a model report insight
====================================

You can publish a chart insight from several locations:

From the model version
------------------------

.. note::

	This method is only possible if you have at least the "Read project content" permission.

Go to the saved model in the Flow and open the active version. From here, click on the "Publish" button.

This creates a new insight pointing to the saved model.

From the dashboard
-------------------

Click on the + button to add tiles. Select "model report", then select the model for which you want to show the data. If you only have dashboard access, you will only see the models that have previously been :doc:`dashboard-authorized </security/authorized-objects>`.

Tile display
=============

The tile display of a "model report" shows a single report page (summary, variables importance, decision chart, confusion matrix, ...). In the tile settings, you can select which page to show.

If you want to show multiple pages, you can create several tiles based on the model report insight. To do that, click on the + button, select "Pick existing", and pick the model report insight that you previously created. The new tile can show a different page of the same insight.

View insight
========================

The View page of the saved model report insight shows all the pages, in an interface similar to the regular models result page of DSS.

Note that you cannot edit anything in that insight view (threshold, cost matrix gain, cluster hierarchy, ...), even if you have write access to the project.

All modifications must be done in the original model.