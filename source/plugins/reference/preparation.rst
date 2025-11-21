Component: Preparation Processor
################################

Preparation processors are additional steps you can add to a Prepare recipe Script.

To create a new Preparation processor, we recommend that you use the plugin developer tools (see the tutorial for an introduction). In the Definition tab, click on “+ ADD COMPONENT”, choose ”PREPARATION PROCESSOR”, and enter the identifier for your new processor.
You’ll see a new folder named after your identifier containing 2 files: ``processor.json`` and ``processor.py``.

A basic processor definition looks like:

.. code-block:: json

    {
        "meta" : {
            "label" : "Custom processor",
            "description" : "",
            "icon" : "icon-puzzle-piece"
        },
        "mode": "CELL",
        "params" : [
            {
                "name": "param1",
                "label": "Parameter 1",
                "type": "STRING",
                "description": "Some documentation for parameter1",
                "mandatory": true
            }
        ]
    }

A basic implementation looks like:

.. code-block:: python

    def process(row):
        # row is a dict of the row on which the step is applied
        param1_value = params.get('param1')
        return param1_value



The "meta" field is similar to all other kinds of DSS components.

Output single column
===================================

When ``mode`` is set to ``CELL`` in the descriptor, the preparation processor outputs a single column.

To generate the values for this output column, DSS calls the ``process`` function of the processor for each rows of the dataset, and stores the returned value in the output column for the associated row.

The following implementation creates a new column containing a salutation message using the ``Name`` column in the input dataset.

.. code-block:: python

    def process(row):
        return "Dear " + row['Name']


To allow end-users to select an input column, you add a parameter of type COLUMN.

.. code-block:: json

    {
        "meta" : {
            "label" : "Custom processor (cell)",
            "description" : "",
            "icon" : "icon-puzzle-piece"
        },
        "mode": "CELL",
        "params" : [
            {
                "name": "input_column",
                "label": "Input column",
                "type": "COLUMN",
                "description": "Column containing the name of the person",
                "columnRole": "main",
                "mandatory": true
            }
        ]
    }

.. code-block:: python

    def process(row):
        input_column = params.get('input_column')
        return "Dear " + row[input_column]

Output multiple columns
===================================

To output or modify more than one column, ``mode`` must be set to ``ROW`` in the descriptor.

The implementation of your ``process`` function must return a ``dict`` where each key/value represent a cell in the row. You usually will return the ``row`` object received as argument after your modifications.

To configure the names of the output columns, you add one parameter per output column.

.. code-block:: json

    {
        "meta" : {
            "label" : "Custom processor (row)",
            "description" : "",
            "icon" : "icon-puzzle-piece"
        },
        "mode": "ROW",
        "params" : [
            {
                "name": "input_column",
                "label": "Input column",
                "type": "COLUMN",
                "description": "Column containing the name of the person",
                "columnRole": "main",
                "mandatory": true
            },
            {
                "name": "salutation_column",
                "label": "Salutation column",
                "type": "COLUMN",
                "description": "Output for salutation message",
                "columnRole": "output_salutation"
            },
            {
                "name": "greeting_column",
                "label": "Greeting column",
                "type": "COLUMN",
                "description": "Output column for greeting message",
                "columnRole": "output_greeting"
            }
        ]
    }

For example, to generate 2 additional columns containing a salutation and a greeting message for each person in the dataset, you would use the above descriptor and this implementation:

.. code-block:: python

    def process(row):
        input_column = params.get('input_column')

        salutation_column = params.get('salutation_column')
        if salutation_column is not None and salutation_column != "":
            row[salutation_column] = "Dear " + row[input_column]

        greeting_column = params.get('greeting_column')
        if greeting_column is not None and greeting_column != "":
            row[greeting_column] = "Hello " + row[input_column]

        return row

Using code environment for a processor
======================================
To use the :ref:`code environment <other_code_env>` defined for the processor, add an additional parameter "useKernel" within the ``processor.json``. 

The updated processor definition looks like:

.. code-block:: json

    {
        "meta" : {
            "label" : "Custom processor",
            "description" : "",
            "icon" : "icon-puzzle-piece"
        },
        "mode": "CELL",
        "params" : [
            {
                "name": "param1",
                "label": "Parameter 1",
                "type": "STRING",
                "description": "Some documentation for parameter1",
                "mandatory": true
            }
        ],
        "useKernel" : true
    }

The plugin will need to be reloaded after making the above change.
