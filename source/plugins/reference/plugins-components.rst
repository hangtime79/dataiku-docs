Plugin Components
########################

.. toctree::
    :maxdepth: 1
    :hidden:

    recipes
    preparation
    macros
    project-creation-macros
    webapps
    file-format
    samples
    fsproviders
    custom-fields
    prediction-algorithms
    charts-elements


Existing components
===================

A plugin is made of a number of **components**. Each component is a single kind of object in Dataiku DSS, such as a dataset, recipe, or webapp.  Each component adds functionality to a plugin. A plugin bundles components together as a single consistent whole.

The (non-exhaustive) list of plugin components includes:

* Dataset
* :doc:`Recipe <recipes>`
* :doc:`Macros <macros>`
* :doc:`File Format <file-format>`
* :doc:`Sample Dataset <samples>`
* Format extractors/exporters
* Format exporters
* :doc:`Filesystem providers <fsproviders>`
* Metric probes and checks
* Scenario triggers and steps
* Preparation processor steps
* Shared code to import into recipes or notebooks
* :doc:`Webapps <webapps>`
* :doc:`Prediction algorithm <prediction-algorithms>`
* :doc:`Custom Fields <custom-fields>`
* Parameter set
* Custom Policy Hooks

.. seealso::

    Multiple tutorials on this subject are found in the Developer Guide :doc:`devguide:tutorials/plugins/index`.


The most up-to-date list of possible components can be found in the product.  In the plugin editor, click **+ Add > Create component**.  The resulting dialog shows the list of possible components.  When you add a component, Dataiku DSS automatically makes the appropriate additions to the plugin directory structure and adds some starter code to help you get started.

.. image:: img/components-list.png


Structure of a plugin
========================

The elements of a plugin are contained within a top-level directory that identifies the plugin.  When you create a plugin from scratch (called, for example, ``myplugin``), that top-level directory contains:

* A ``python-lib`` subdirectory with a ``myplugin`` subdirectory that has an ``__init__.py`` file that is empty of code.  The ``python-lib`` directory is a good place to put functions that will be reused throughout the plugin.
* A ``plugin.json`` file that describes the plugin as a whole.
    
    * As a best practice, the ``id`` element of this JSON file should be the same as the name of the top-level directory.

For example, the ``plugin.json`` shown below leads to the Fig. 1.

.. code-block:: javascript

    {
        // Plugin identifiers are globally unique and only contain A-Za-z0-9_-
        "id": "timeseries-preparation",

        // It is highly recommended to use Semantic Versioning
        "version": "2.0.1",

        // Meta data for display purposes:
        "meta": {
            // label: name of the plugin as displayed, should be short
            "label": "Time Series Preparation",
            // description: longer string to help end users understand what this plugin does
            "description": "Perform resampling, windowing operations, interval extraction, extrema extraction, and decomposition on time series data (one row per time stamp).",

            "author": "Dataiku (Du PHAN and Marine SOBAS)",

            // icon: must be one of the FontAwesome 3.2.1 icons, complete list here at https://fontawesome.com/v3.2.1/icons/
            "icon": "icon-time",

            "licenseInfo": "Apache Software License",

            // URL where the user can learn more about the plugin
            "url": "https://www.dataiku.com/dss/plugins/info/time-series-preparation.html",

            // List of tags for filtering the list of plugin
            "tags": [
                "Time Series"
            ]
        }
    }


.. figure:: ./img/plugin-structure-plugin-time-serie.png
    :align: center
    :class: with-shadow
    :alt: Description of a plugin.

    Description of a plugin.


Generic information about the Components of a plugin
====================================================

Components
----------

As you add components to the plugin, this adds to the plugin folder structure.  Each type of component has a subdirectory under the top-level directory.  Each component has a directory that contains a JSON file that describes the component as a whole, and code files that define what the component does.

Parameters
----------
Each component generally has some :doc:`configuration parameters <params>` and has a metadata section.

.. _plugin_metadata_section:

Metadata section
----------------

Metadata is used for display purposes. You can configure the name of the component as well as its description
and the icon used to represent the component, by filling out the "meta" field as shown below.

.. code-block:: javascript

    "meta": {
        // label: name of the component as displayed, should be short
        "label": "Short title",

        // description: longer string to help end users understand what this component does
        "description": "A longer description that helps the user understand the purpose of the component",

        // icon: must be one of the FontAwesome 3.2.1 icons, complete list here at https://fontawesome.com/v3.2.1/icons/
        "icon": "icon-puzzle-piece"
    },
