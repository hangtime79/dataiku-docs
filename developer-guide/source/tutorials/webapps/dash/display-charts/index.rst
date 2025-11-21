Display a Bar chart using Dash
******************************

.. meta::
    :title: Display a Bar chart using Dash
    :description: This tutorial will introduce the development of a Dash application for extracting sales data from Dataiku.
      You can select countries from a dropdown menu, and the bar plot will dynamically update to display the total sales for the chosen countries.
    :tag: webapps
    :tag: dash
    :tag: dataset


This tutorial will introduce the development of a Dash application for extracting sales data from Dataiku.
You can select countries from a dropdown menu,
and the bar plot will dynamically update to display the total sales for the chosen countries.

You should know how to create an empty Dash web application.
If you don't, please refer to :doc:`this tutorial<../common-parts/create-the-webapp-empty-template>`.

Prerequisites
#############

* Dataiku >= 12.0
* A code environment with ``dash`` and ``plotly``

.. note::

    We have tested this tutorial using a Python 3.9 code environment with ``dash==2.18.0`` and ``plotly==5.13.1``.
    Other Python versions may be compatible.
    Check the webapp logs for potential incompatibilities.

Data preparation
################

Start by downloading the source data following
`this link <https://cdn.downloads.dataiku.com/public/website-additional-assets/data/Orders_by_Country_sorted.csv>`__
and make it available in your Dataiku project, for example, by uploading the *.csv* file. Name the resulting
Dataiku dataset ``Orders_by_Country_sorted``.

Creating the webapp
###################

The webapp will consist of a title, a text (to explain the purpose of the webapp),
a multi-select object (for selecting the countries), and a plot.

Importing the libraries
^^^^^^^^^^^^^^^^^^^^^^^
First, you need to create an empty Dash web application and import the required libraries,
as shown in :ref:`Code 1<webapps-dash-display-charts-code-import-libs>`.

.. literalinclude:: ./assets/dash.py
    :lines: 1-5
    :language: python
    :name: webapps-dash-display-charts-code-import-libs
    :caption: Code 1: Importing the required libraries.

Providing data
^^^^^^^^^^^^^^
To use the dataset, you must read ``Orders_by_Country_sorted`` with the ``dataiku`` package,
as shown in :ref:`Code 2<webapps-dash-display-charts-code-read-data>`.

.. literalinclude:: ./assets/dash.py
    :lines: 6-10
    :language: python
    :name: webapps-dash-display-charts-code-read-data
    :caption: Code 2: Reading the data.


Creating the layout
^^^^^^^^^^^^^^^^^^^
:ref:`Code 3<webapps-dash-display-charts-code-layout>` defines the web application's layout,
as defined at the beginning of this section.
You must plug a callback to update the bar chart, so you don't need to create it in the layout.
The callback will be called when the application will start.

.. literalinclude:: ./assets/dash.py
    :lines: 11-26
    :language: python
    :name: webapps-dash-display-charts-code-layout
    :caption: Code 3: Creating the layout.

Updating the bar chart
^^^^^^^^^^^^^^^^^^^^^^
:ref:`Code 4<webapps-dash-display-charts-code-callback>`
is responsible for creating/updating the bar chart whenever the user changes the selected countries.
For the Dash application, if you don't use ``prevent_initial_call=True`` in the parameter of a callback,
the callback is called when the application starts.
So, we can use the same callback to create or update the bar chart.

.. literalinclude:: ./assets/dash.py
    :lines: 27-
    :language: python
    :name: webapps-dash-display-charts-code-callback
    :caption: Code 4: Updating the bar chart.

Going further
#############
You can test different charts, change the column used to display the information and  adapt this tutorial to your needs.

Here are the complete versions of the code presented in this tutorial:

.. dropdown:: :download:`app.py<./assets/dash.py>`

    .. literalinclude:: ./assets/dash.py
        :language: python

