Jupyter Notebook
#################

A "Jupyter notebook" insight shows a snapshot (called an export) of the content of a Jupyter (Python, R, Scala) notebook. For more information, see :doc:`/notebooks/index`.

The insight only shows a static snapshot, it does not show the "current" version of the notebook. The insight does not give the possibility to modify or run the notebook.

.. note::

	Unlike most other insights, a Jupyter notebook must first be published at least once by a user with "Write project content" permission on the project and "Write safe code" global permission.

	Once this user has published a first time the notebook, other users can create insights pointing to it and add them on their dashboards

There can be several exports of the same Jupyter notebook. In the insight, you can choose between the different versions. This allows you to show the notebook at different points in time.

Publishing a Jupyter notebook insight
=======================================

You can publish a Jupyter notebook insight from several locations:

From the notebook
------------------------

.. note::

	This method is only possible if you have at least the "Write project content" permission, and the permission to create Jupyter notebook

Go to the Jupyter notebook. From the Actions menu, click on the "Publish" button. This action is also possible from the notebooks list.

This actually does three actions:

	* Create a snapshot (an export) of the Jupyter notebook
	* Create an insight pointing to the notebook. The insight will display the latest snapshot
	* Add the insight to the specified dashboard

From the dashboard
-------------------

Click on the + button to add tiles. Select "Jupyter notebook", then select the notebook for which you want to show the export.

If you only have dashboard access, you will only see the notebooks that have previously been :doc:`dashboard-authorized </security/authorized-objects>`.

Tile display
=============

The tile display of a "Jupyter notebook" insight shows the content of the notebook. In the tile settings, you can select whether the code should be shown or not.

View and edit insight
========================

The View page of the Jupyter notebook insight shows the content of the notebook.

If you have write access to the insight, you can go to the Edit tab, where you can select between the different exports.

If you have "Write project content" access to the project and the permission to write code, you'll be able to create a new export.