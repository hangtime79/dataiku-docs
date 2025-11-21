Component: Recipes
###################

.. contents::
    :local:
    :depth: 1

Description
===========
Dataiku DSS comes with some existing :doc:`/other_recipes/index` allowing the user to perform standard analytic
transformations. Visual recipes perform a transformation in the Flow, but they are not the only way to do it.

Coders can use :doc:`/code_recipes/index` to code additional transformations particularly when Dataiku DSS does
not cover their usage. Code recipes are a good way to extend Dataiku DSS's capabilities. These user-defined code recipes
can be converted to plugin recipes, allowing them to be distributed to non-coder users as a visual recipe.

To be able to convert a code recipe to a plugin recipe:

* Open the code recipe;
* Click on the "Action" button (or open the right panel);
* Click on the "Convert to plugin" button;
* Fill out the form.

There are two different ways to integrate a plugin recipe. You can choose to add the recipe plugin to an existing plugin.
Or, you can choose to create a new plugin, and then add the plugin recipe to this new plugin.


A plugin recipe is configurable in the associated JSON file (automatically created by Dataiku DSS during the
conversion process), in the folder ``custom-recipes/{<plugin-recipe-id>}/recipe.json``. This JSON configuration file
comprise different parts as shown in the code below.

.. code-block:: javascript

    {
        // Metadata section
        "meta": {
            //metadata used for display purpose
        },

        // Kind of the code recipe
        "kind": "PYTHON",

        // Input/Output section
        "inputRoles": [
            // DSS objects that can be used as input for the recipe
            // A recipe can have many different input objects
        ],
        "outputRoles": [
            // DSS objects that can be used as output for the recipe
            // A recipe can have many different output objects
        ],

        // Parameters section
        "params": [
            // Parameter definition usable for your recipe
        ],

        // Advanced configuration section
        // various configuration options.

    }

..
    COMMENTS / WARNING

    Different kinds of code recipes but for now nothing is documented
    It is undocumented for purposes for R, PYSPARK, SPARK_SCALA, JAVA
    So the only kind of recipe "documentable" is PYTHON

Write the plugin recipe code in the file ``recipe.py``. It should, at least, read the input parameter and produce
the dataset mentioned in the output section, like described below.

.. code-block:: python

    # To retrieve the datasets of an input role named 'input_A' as an array of dataset names:
    dataset_name = get_input_names_for_role('dataset_input')[0]

    # For outputs, the process is the same:
    output_name = get_output_names_for_role('dataset_output')[0]

    # Read recipe inputs
    df = dataiku.Dataset(dataset_name).get_dataframe()

    # In this example, we just copy the input to the output

    # Write recipe outputs
    output_dataset = dataiku.Dataset(output_name)
    output_dataset.write_with_schema(df)

Metadata
==================

Metadata is used for display purposes. You can configure the name of the recipe as well as its description, the icon
used to represent the recipe and also the color of this icon, by filling out the ``"meta"`` field as shown below.

.. seealso::

    Multiple tutorials on this subject are found in the Developer Guide :doc:`devguide:tutorials/plugins/recipes/index`.

Example
-------

.. code-block:: javascript

    "meta": {
        // label: name of the recipe as displayed, should be short
        "label": "Short title",

        // description: longer string to help end users understand what this recipe does
        "description": "A longer description that helps the user understand the purpose of the recipe",

        // icon: must be one of the FontAwesome 3.2.1 icons, complete list here at https://fontawesome.com/v3.2.1/icons/
        "icon": "icon-thumbs-up-alt",

        // DSS currently supports the following colors: red, pink, purple, blue, green, sky, yellow, orange, brown, and gray.
        "iconColor": "blue"
    },


Input/Output
====================

Each input/output role has the following structure:

* ``name``: Name of the role; this is how the role is referenced elsewhere in the code
* ``label``: A displayed name for this role
* ``description``: A description of what the role means
* ``arity``: UNARY or NARY (can accept one or multiple values?)
* ``required`` (boolean, default false): Does this role need to be filled?
* ``acceptsDataset`` (boolean, default true): Whether a dataset can be used for this role
* ``acceptsManagedFolder`` (boolean, default false): Whether a managed folder can be used for this role
* ``acceptsSavedModel`` (boolean, default false): Whether a saved model can be used for this role

Grouping input/output into roles enables the coder (and the user) to group their input/output into semantic groups of
data, rather than having all the input/output at the same level.

Example
-------

.. code-block::

    "inputRoles": [
        {
            "name": "dataset_names",
            "label": "input A displayed name",
            "description": "what input A means",
            "arity": "NARY",
            "required": true,
            "acceptsDataset": true
        },
        {
            "name": "managed_folder_name",
            "label": "input B displayed name",
            "description": "what input B means",
            "arity": "UNARY",
            "required": false,
            "acceptsDataset": false,
            "acceptsManagedFolder": true
        }

Parameters
==================

From a parameter perspective, a plugin code recipe is not different than other plugin components.
However, for the plugin code recipe, there are two types of parameters (**COLUMN** and **COLUMNS**). They allow the
user to select one (or more) column(s) in a dataset as parameter(s) for the plugin code recipe.
For more about parameters, please see :doc:`./params`.


Advanced configuration
===================================

Select from Flow view
---------------------

To make a new recipe directly available from the Flow view when selecting:

* a Dataset, add the field: ``"selectableFromDataset"``
* a Managed Folder, add the field: ``"selectableFromFolder"``
* a Saved Model, add the field: ``"selectableFromSavedModel"``

Each added field should target an existing inputRole, see below for the usage.

Complete example
================

.. code-block:: javascript

    {
        "meta": {
            "label": "Clip values",
            "description": "Allow clipping values on different columns",
            "icon": "icon-align-justify",
            "iconColor": "orange"
        },
        "kind": "PYTHON",
        "inputRoles": [
            {
                "name": "dataset_name",
                "label": "Datasets to clip",
                "description": "Automatically remove outliers from a dataset, by clipping the values",
                "arity": "UNARY",
                "required": true,
                "acceptsDataset": true
            },
            {
                "name": "managed_folder_name",
                "label": "dummy input",
                "description": "just here to demonstrate selection from the flow",
                "arity": "UNARY",
                "required": false,
                "acceptsDataset": false,
                "acceptsManagedFolder": true
            }
        ],
        "outputRoles": [
            {
                "name": "dataset_clipped",
                "label": "Clipped dataset",
                "description": "Result of the clipping",
                "arity": "UNARY",
                "required": true,
                "acceptsDataset": true
            }
        ],
        "params": [
            {
                "name": "IQR_coeff",
                "type": "DOUBLE",
                "defaultValue": 1.5,
                "label": "IQR coefficient",
                "mandatory": true
            }
        ],
        "selectableFromDataset": "dataset_name",
        //The next selectable is just for the example
        "selectableFromFolder": "managed_folder_name",

        // The field "resourceKeys" holds a list of keys that allows limiting the number
        // of concurrent executions and activities triggered by this recipe.
        //
        // Administrators can configure the limit per resource key in the Administration > Settings > Flow build
        // screen.
        "resourceKeys": []
    }
