Component: Macros
####################

.. contents::
   :depth: 1
   :local:
   :backlinks: none


    
Description
==================

A macro is a Dataiku component used to automatize tasks or to extend the capability of Dataiku.
It can be used in several places in Dataiku DSS, depending on the role of the macro.
By default, macros are accessible from the "Macros" menu of each project.
In addition, macro can be made accessible in other places, depending on the ``macroRoles`` field.
For example, if the ``macroRoles`` is:

* ``DATASETS`` the macro will be available when selecting on or more Datasets in the Flow.
* ``PROJECT_MACROS`` is about running code on the project in order to achieve global processing on a project (it can
  be used, to automatically kill running processing, like notebooks).
* ``PROJECT_CREATOR`` will allow (administrators) to create a project template with some default configurations.
  
A macro is not limited to only one kind of role, allowing it to appear in several places if it makes sense.


For more information about macros, see :doc:`/operations/macros`.

.. seealso::

    Multiple tutorials on this subject are found in the Developer Guide :doc:`devguide:tutorials/plugins/macros/index`.

Creation
==================

To start creating a macro,  we recommend that you use the plugin developer tools (see the tutorial for an introduction). In the Definition tab, click on "Add Python macro", and enter the identifier for your new macro. You'll see a new folder ``python-runnables`` and will have to edit the ``runnable.py`` and ``runnable.json`` files

A macro is essentially a Python function, wrapped in a class, written in a ``runnable.py`` file in the macro's folder.

A basic macro's code looks like

.. code-block:: python

    from dataiku.runnables import Runnable

    class MyMacro(Runnable):
        def __init__(self, project_key, config, plugin_config):
            self.project_key = project_key
            self.config = config

        def get_progress_target(self):
            return None

        def run(self, progress_callback):
            # Do some things. You can use the dataiku package here

            result = "It worked"
            return result

The associated ``runnable.json`` file looks like:

.. code-block:: json

    {
        "meta" : {
            "label" : "A great macros",
            "description" : "It does stuff",
            "icon" : "icon-trash"
        },

        "impersonate" : false,
        "permissions" : ["READ_CONF"],
        "resultType" : "HTML",
        "resultLabel" : "The output",

        "params": [
            {
                "name": "param_name",
                "label" : "The parameter",
                "type": "INT",
                "description":"Delete logs for jobs older than this",
                "mandatory" : true,
                "defaultValue" : 15
            }
        ]
    }

The "meta" and "params" fields are similar to all other kinds of DSS components.

Macro roles
==================

Macro roles define where this macro will appear in DSS GUI. They are used to pre-fill a macro parameter with context.

E.g,: if a macro has a role of type DATASET that points to an ``input_dataset`` parameter, the dataset's action menu will show this macro and clicking on it will prefill the ``input_dataset`` parameter will the selected dataset.

Each role consists of:

* type: where the macro will be shown

    * when selecting DSS object(s): DATASET, DATASETS, API_SERVICE, API_SERVICE_VERSION, BUNDLE, VISUAL_ANALYSIS, SAVED_MODEL, MANAGED_FOLDER
    * in the project list: PROJECT_MACROS
* targetParamsKey(s): name of the parameter(s) that will be filled with the selected object
* applicableToForeign (boolean, default false): can this role be applied to foreign elements (such as foreign datasets, folders or models)?

For example, a ``runnable.json`` file with macro roles could look like that:

.. code-block:: json

    {
        "meta" : {
            "label" : "A great macros",
            "description" : "It does stuff",
            "icon" : "icon-trash"
        },

        "impersonate" : false,
        "permissions" : ["READ_CONF"],
        "resultType" : "HTML",
        "resultLabel" : "The output",

        "macroRoles": [
            {
               "type": "DATASET",
               "targetParamsKey": "input_dataset",
               "applicableToForeign": true
            },
            {
               "type": "API_SERVICE_PACKAGE",
               "targetParamsKeys": ["input_api_service", "input_api_service_package"]
            }
        ],

        "params": [
            {
                "name": "input_dataset",
                "type": "DATASET",
                "label": "Input dataset"
            },
            {
                "name": "input_api_service",
                "type": "API_SERVICE",
                "label": "API Service"
            },
            {
                "name": "input_api_service_version",
                "type": "API_SERVICE_VERSION",
                "apiServiceParamName": "input_api_service",
                "label": "API Service version package",
                "description": "retrieved from the API Service stated above"
            }
        ]
    }

.. note::

    Only the ``API_SERVICE_VERSION`` type needs an array specified through ``targetParamsKeys``, as it has to fill two related parameters: the API service and the API service package.

    All the other types only need to specify one ``targetParamsKey``.

Result of a macro
==================

In addition to performing its action, a macro can return a result, which will be displayed by the user. In many cases, the main job of a macro is to output some kind of report. In that case, the result is actually the main function of the macro.

To return a result from your macro, you must first define the ``resultType`` field in the ``runnable.json`` file.

Valid result types are defined below

HTML
----

In ``runnable.json``, set ``"resultType" : "HTML"``

Your macro's ``run`` function must return a HTML string, which will be displayed inline in the result's page. Users will have the option to download the HTML. You may use CSS declarations in your HTML code but please make sure to properly scope them so that they cannot interfere with DSS.

URL
----

In ``runnable.json``, set ``"resultType" : "URL"``

Your macro's ``run`` function must return an URL as a string. Users will be presented with a link.

RESULT_TABLE
--------------

In ``runnable.json``, set ``"resultType" : "RESULT_TABLE"``.

This allows you to build a table view which will be properly formatted for display. We recommend that you use RESULT_TABLE rather than HTML if the output of your macro is a simple table, as you won't have to handle styling and formatting.

In your macro's run function, create and fill your result table as follows

.. code-block:: python

    from dataiku.runnables import Runnable, ResultTable

    rt = ResultTable()

    # First, declare the columns of the output
    # Parameters to add_Column are: id, label, type
    rt.add_column("dataset", "Dataset", "STRING")

    rt.add_column("table", "Table", "STRING")

    # Then, add records, as lists, in the same order as the columns
    record = []
    record.append("dataset_name")
    record.append("table_name")
    rt.add_record(record)

    # Return the result table as the return value of the macro's run function
    return rt

Valid types for columns are:

* STRING: A regular string
* STRING_LIST: Add a list of strings in the ``record`` array. It will be formatted comma-separated

Interacting with DSS in macros
===============================

The recommended way to interact with DSS in the code of a macro is either the internal Python API or the public API.

For internal API, for example, this includes ``dataiku.Dataset()``. Interaction with the public API is made easy by ``dataiku.api_client()`` which gives you a public API client handle, automatically configured with the permissions of the user running the macro.

Progress reporting
===================

You have the possibility to monitor the progress status of your macro during its execution by leveraging the ``progress_callback()`` function.

The first step is to make the ``get_progress_target()`` function return a `(target, unit)` tuple where:

* `target` is the "final value" your progress bar will have to reach

* `unit` defines which measure of scale the progress bar is assessing (for example `SIZE` if you are uploading/downloading a file, `FILES` if you are processing a list of files, `RECORDS` if you are processing a list of records, `NONE` if the unit is arbitrary, e.g. using a percentage).


.. code-block:: python

  def get_progress_target(self):
    return (3, 'NONE')


The next step is then to invoke ``progress_callback()`` within the ``run()`` function with a "current progress" value to update the status of the progress bar every time it's necessary.

.. code-block:: python

  def run(self, progress_callback):
    # Write code for part 1/3 of your macro here
    progress_callback(1)
    # Write code for part 2/3 of your macro here
    progress_callback(2)
    # Write code for part 3/3 of your macro here
    progress_callback(3)


Security of macros
====================

Impersonation
--------------

You need to configure whether this macro will run with UNIX identity of the user running DSS, or with the identity of the final user. Note that this is only relevant for the users of your plugin if :doc:`User Isolation Framework </user-isolation/index>` is enabled, but since your plugin might be used in both cases, you still need to take care of this.

Generally speaking, we recommend that your macros run with ``"impersonate" : true``. This means that they may not access the filesystem outside of their working directory and should only use DSS APIs for their operations.

If your macro runs with ``"impersonate": false``, it can access the filesystem, notably the DSS datadir.

Permissions
------------

A macro always runs in the context of a project (which is passed to the macro's constructor).

Your macro can define the project permissions that users must have to be able to run the macro. This is done in the ``permissions`` field of the ``runnable.json`` file.

Valid permission identifiers are:

* ADMIN
* READ_CONF
* WRITE_CONF

For more information about the meaning of these permissions, see :doc:`/security/permissions`

In addition, if the users running the macro need to have global DSS administrator rights, set the ``"requiresGlobalAdmin"`` field of ``runnable.json`` to ``true``
