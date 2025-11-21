Component: Sample Dataset
*************************

.. contents::
   :depth: 1
   :local:
   :backlinks: none

Description
###########
Dataiku DSS gives the ability to kickstart a project by adding ready-to-use datasets, called sample datasets.

Some sample datasets are installed by default. In case you need to add your own sample datasets, you can develop a
sample dataset plugin.

.. seealso::

    A tutorial on this plugin component is available in the Developer Guide: :doc:`devguide:tutorials/plugins/sample-dataset/index`.


Creation
########

To develop a new sample dataset plugin, go to a development plugin page, click on "+New Component", then
choose "Sample Dataset" from the list of components. Choose a name for your component, and click on "Add".

.. note::
    Once this is done Dataiku DSS opens the code editor, allowing you to update the metadata of you plugin, as well the sample's content and resource files.

Configuration
#############

A sample dataset plugin is configurable in the associated JSON file (automatically created by Dataiku DSS),
in the folder ``sample-datasets/{<sample-dataset-id>}/dataset.json``.

This JSON configuration file comprises different parts as shown in the code below.

.. code-block:: javascript
    :caption: Configuration file of a sample dataset plugin

    {
        // Metadata section.
        "meta": {
            // Metadata used for display purposes.
        },

        // Global configuration about the sample data plugin.
        // See below for more information.
        "columns": [...]
    }


Metadata configuration
^^^^^^^^^^^^^^^^^^^^^^

For the metadata section, the usual configuration applies. Please refer to :ref:`plugin_metadata_section`.

There are some additional optional parameters that you may want to fill depending on your needs

.. code-block:: javascript
    :caption: Additional optional metadata parameters of a sample dataset

    /* The number of rows in your sample, will be displayed when listing the dataset samples */
    "rowCount": 100,

    /* Logo used on the Sample Dataset modal to represent your sample */
    "logo": "logo-name.png",

    /* Number used to sort the dataset samples by descending order when listed */
    "displayOrderRank": 10

If you want to specify a logo for your sample, place the image inside a shared `resource` folder in root of your plugin,
and can only contain letters, digits, dots, underscores, hyphens and spaces.
Your logo should ideally be an image of 280x200 pixels.

The available extensions for a logo are the following: ``.apng``, ``.png``, ``.avif``, ``.gif``, ``.jpg``, ``.jpeg``, ``.jfif``, ``.svg``, ``.webp``, ``.bmp``, ``.ico``, ``.cur``

Sample data
^^^^^^^^^^^

Your sample data must be comprised of one or several ``.csv`` file or ``.csv.gz`` file
located here : ``sample-datasets/{<sample-dataset-id>}/data/{<sample-file>}``.
By default your sample dataset component will be created with a small sample example named ``sample.csv``

Each sample file consists in a CSV file where the separator is a comma ``,`` and the quote character is a double quote ``"``.
Ensure that the input CSV files adhere to this format for correct parsing and processing.
Each sample file should not contain any header row, as the column names are defined in the JSON configuration file.

You will need at least one sample file to save your plugin.

Global configuration
^^^^^^^^^^^^^^^^^^^^

For the global configuration, a sample dataset has to define the following:

.. code-block:: javascript
    :caption: Global configuration of a sample dataset

    /* Description of the schema of your dataset */
    "columns": [...],

The ``"columns"`` field is the place where you can specify the schema of your sample dataset, it contains as many columns as your dataset has.
Your column should be ordered in the same order than the one in your csv file.

Each column is structured with the following fields :

* name: unique identifier of the column
* type: storage type of the column
* comment (optional): description of the column
* meaning (optional): “high-level” definition of the column, used to validate the cell. If not set, the meaning will be deduced from the sample content.

For the list of columns types, please refer to :ref:`storage_types`

For the list of available meanings, please refer to :doc:`/schemas/meanings-list`

.. code-block:: javascript
    :caption: Structure of a column

    {
        /* Unique identifier for your column */
        "name": "columns-name",
        /* Type of the column */
        "type": "double",
        /* Optional description of the column, that will be displayed in the dataset's explore view */
        "comment": "This is the description of my column",
        /* Optional meaning of the column */
        "meaning": "DoubleMeaning"
    }



Complete example
################

.. code-block:: javascript
    :caption: Complete example of the ``dataset.json``

    /* This file is the descriptor for the sample dataset template my-sample-dataset */
    {
        "meta": {
            "label": "Temperature Time Series",
            "description": "This dataset contains daily temperature data over a multi-year period",
            "icon": "fas fa-thermometer",
            "rowCount": 100,
            "logo": "thermometer-logo.png",
            "displayOrderRank": 100
        },
        "columns": [
            {
                "name": "date",
                "type": "dateonly",
                "comment": "The date of the temperature observation in the format YYYY-MM-DD",
                "meaning": "DateOnly"
            },
            {
                "name": "temperature",
                "type": "float",
                "comment": "The recorded temperature value for the given date"
            },
            {
                "name": "temperature_trend",
                "type": "float",
                "comment": "A calculated trend value representing the smoothed or averaged temperature over a specific period"
            }
        ]
    }

