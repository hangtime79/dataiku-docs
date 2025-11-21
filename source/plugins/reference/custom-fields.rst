Component: Custom Fields
#########################

Custom Fields are additional metadata fields that are added to Dataiku DSS objects such as datasets, recipes, etc.

To start adding Custom Fields, we recommend that you use the plugin developer tools (see the tutorial for an introduction). In the Definition tab, click on “+ ADD COMPONENT”, choose ”Custom Fields”, and enter the identifier for your new Custom Fields. You’ll see a new folder ``custom-fields`` and will have to edit the ``custom-fields.json`` file.

A basic Custom Fields's definition looks like

.. code-block:: json

    {
        "meta" : {
            "label" : "Custom fields test",
            "description" : "Custom Fields",
            "icon" : "icon-puzzle-piece"
        },
        "customFields" : [
            {
                "applyToObjects" : {
                    "mode": "SOME",
                    "includedObjectTypes": ["PROJECT", "DATASET"]
                },
                "field": {
                    "name": "custom_field_1",
                    "type": "SELECT",
                    "defaultValue": "UNSURE",
                    "selectChoices": [
                        {
                            "value": "YES",
                            "label": "Yes"
                        },
                        {
                            "value": "UNSURE",
                            "label": "Not sure"
                        },
                        {
                            "value": "NO",
                            "label": "No"
                        }
                    ]
                }
            }
        ]
    }


The "meta" field is similar to all other kinds of DSS components.

Defining a set of Custom Fields
===================================

The "customFields" field is an array listing all the Custom Fields you want to add. The definition of one Custom Fields is composed of two main fields that are mandatory: "applyToObjects" and "field".

Objects definition
---------------------

A Custom Field can be applied to several types of object in Dataiku DSS among:

* PROJECT
* DATASET
* RECIPE (including visual and code recipes)
* SQL_NOTEBOOK
* JUPYTER_NOTEBOOK
* ANALYSIS
* SAVED_MODEL
* INSIGHT
* MANAGED_FOLDER
* LAMBDA_SERVICE (an API Designer service)
* SCENARIO
* DASHBOARD
* WEB_APP
* REPORT (a Rmarkdown report)
* ARTICLE (a wiki article)
* CONNECTION (a Dataiku DSS connection)
* COLUMN (a column within a dataset)

There are 3 modes on how to assign a Custom Field to Dataiku DSS object:

* ALL : include all types of objects
* SOME : include the types of objects listed in the ``includedObjectTypes`` field
* EXCLUDING : include all types of objects except the ones listed in the ``excludedObjectTypes`` field

For instance:

.. code-block:: javascript

        "applyToObjects" : {
            "mode": "ALL"
        }

.. code-block:: javascript

        "applyToObjects" : {
            "mode": "SOME",
            "includedObjectTypes": ["PROJECT", "DATASET"]
        }

.. code-block:: javascript

        "applyToObjects" : {
            "mode": "EXCLUDING",
            "excludedObjectTypes": ["PROJECT", "DATASET"]
        }

Custom Field definition
-------------------------

The fields defining a Custom Field are the following:

* name : the unique name of the field
* type : the type of the field among:

    * STRING : a single-line text
    * INT : an integer number
    * DOUBLE : a floating-point number
    * BOOLEAN : a binary (yes/no) choice
    * PASSWORD : a hidden single-line text
    * SELECT : a selection between multiple choices
    * COLUMN : a selection of a column from an input schema (in a recipe context)
    * COLUMNS : a multiple selection of columns from an input schema (in a recipe context)
    * MAP : a complex object
    * KEY_VALUE_LIST : a key/value pair list
    * TEXTAREA : a multiple-line text
    * ARRAY : a complex objects list
    * PROJECT : a selection of a project
    * DATASET : a selection of a dataset
    * DATASETS : a multiple selection of datasets
    * DATASET_COLUMN : a selection of a column from a specific dataset
    * DATASET_COLUMNS : a multiple selection of columns from a specific dataset
    * CONNECTIONS : a multiple selection of connections
    * FOLDER : a selection of a managed folder
    * MODEL : a selection of a saved model
    * SCENARIO : a selection of a scenario
    * API_SERVICE : a selection of an API service
    * API_SERVICE_VERSION : a selection of a version of a specific API service
    * BUNDLE : a selection of a bundle
    * VISUAL_ANALYSIS : a selection of an analysis
    * CLUSTER : a selection of a cluster
    * SEPARATOR : an horizontal line that is used to separate a list of fields that has no input value

* label : a short label of the field
* description : a longer description of the field
* defaultValue : the default value of the field
* mandatory : true or false whether the field should be mandatory
* canSelectForeign : true of false whether suggested datasets include foreign datasets (for DATASET and DATASETS types)
* minD : the minimum possible value (for DOUBLE type)
* maxD : the maximum possible value (for DOUBLE type)
* minI : the minimum possible value (for INTEGER type)
* maxI : the maximum possible value (for INTEGER type)
* columnRole : the input role of a recipe that is used to retrieve the columns of the corresponding input dataset (for COLUMN and COLUMNS types)
* visibilityCondition : a condition run in the UI that can be used to hide or display the field
* datasetParamName : the Custom Field name which contains the dataset from which columns are suggested (for DATASET_COLUMN and DATASET_COLUMNS types)
* apiServiceParamName : the Custom Field name which contains the API service from which API service version are suggested (for API_SERVICE_VERSION type)
* iconInDatasetPreview : the CSS icon class that is displayed next to the dataset name in the dataset UI (for SELECT type)
* selectChoices : a list of possible choices composed of the following fields (for SELECT type)

    * value : the value of the choice
    * label : a short label of the choice
    * icon : an icon for the choice
    * color : a color for the choice
    * showInColumnPreview : true or false whether to display the field value in the explore UI if the field has this value

* clusterPermissions : a list of permissions among (USE, UPDATE, MANAGE_USERS) (for CLUSTER type)

For instance:

.. code-block:: json

    {
        "field" : {
            "name": "number_of_models",
            "type": "INT",
            "label": "Enter the number of models",
            "description": "Enter the number of models",
            "defaultValue": 0,
            "minI": 0,
            "maxI": 10
        }
    }

.. code-block:: json

    {
        "field" : {
            "name": "project_state",
            "type": "SELECT",
            "label": "Project state",
            "description": "Which state in the lifecycle is the project?",
            "defaultValue": "BEGINNING",
            "selectChoices": [
                {
                    "value": "BEGINNING",
                    "label": "Beginning!"
                },
                {
                    "value": "WORK_IN_PROGRESS",
                    "label": "Work in progress..."
                },
                {
                    "value": "FINISHED",
                    "label": "Finished :)"
                }
            ]
        }
    }

.. code-block:: json

    {
        "field" : {
            "name": "main_project",
            "type": "PROJECT",
            "label": "Main project",
            "description": "Which project is the main project of the instance?"
        }
    }
