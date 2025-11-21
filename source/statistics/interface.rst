.. _statistics-interface:

The Worksheet Interface
#########################

The **Worksheet** is a visual summary of exploratory data analysis (EDA) tasks, and Dataiku DSS allows you to create multiple worksheets for a given dataset. To access the worksheets, click the **Statistics** tab of a dataset.

.. _worksheet_elements:

Elements of a worksheet
===============================
A worksheet header consists of elements described as follows.

.. image:: img/worksheet-interface.png

* The **Worksheet** menu allows you to create a new worksheet, or rename, duplicate, delete, and switch from one worksheet to another in the current dataset.
* The **New Card** button creates a new card and adds it to the current worksheet. You can create multiple cards within a worksheet, with each card performing a specific EDA task. Cards in a worksheet appear below the worksheet header. See :ref:`card_elements` for more details.
* The **Sampling & filtering** menu allows you to configure the sample on which to perform EDA tasks in cards. You can also choose to compute cards on the whole data (no sampling). The specified sample is used to compute all the cards in a worksheet.
* The **Confidence level** menu allows you to define the global confidence level of statistical tests in the worksheet. Certain statistical tasks use this value to produce `confidence intervals <http://www.stat.yale.edu/Courses/1997-98/101/confint.htm>`_ or to highlight *p*-values according to the significance level.
* The **Selection** button represents the active data selection (corresponding to a subset of the data). A stripe pattern is used to highlight this selection across all charts in the worksheet. You can remove the active selection at any time by clicking the **Selection** button.

   .. note::
      This button does not appear by default in the worksheet header. To display it, define the active data selection by clicking on a bar of a histogram plot or a cell of a mosaic plot.
* The gear icon |gear-icon| provides the option of running the worksheet in a container, for instance, to compute the results on a bigger sample that the DSS server cannot accommodate in memory. See :doc:`Running in containers </containers/concepts>` for more information.

.. |gear-icon| image:: img/gear_icon.png

The different :ref:`types of cards<types_of_cards>` in a worksheet depend on the particular EDA task that you choose to perform. Cards consist of elements that are described as follows.

.. _card_elements:

Elements of a card
===============================

.. image:: img/card-interface.png

* The **configuration menu** (✎) allows you to edit the settings of a card.
* The **deletion button** (🗑) allows you to delete a card.
* The **general menu** (⋮) allows you to publish a card, duplicate a card or view its JSON representation.
* The **Split by** menu allows you to select a variable to use for splitting the data into subsets. The card then performs statistical computations on each subset. This feature is useful for comparing the same statistics across multiple groups.
* The section below the card header contains the results of the EDA task.

.. _types_of_cards:

Types of cards
---------------

* :doc:`Univariate analysis <univariate>`
* :doc:`Bivariate analysis <bivariate>`
* :doc:`Fit curves and distributions <fit>`
* :doc:`Statistical tests <tests>`
* :doc:`Multivariate analysis <multivariate>`
