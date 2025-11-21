Limiting Concurrent Executions
##############################

When a recipe is run to build a dataset (and its descendants if required or requested), DSS creates and executes a job to perform the work.
This job is itself composed of one or more activities. DSS creates an activity per dataset per partition.

To prevent jobs from consuming too many resources when they run, DSS limits the number of activities that are executed simultaneously.

.. contents::
	:local:

---------------------------------
Global and per-job limits
---------------------------------
By default, only 5 activities can be executed simultaneously on a DSS instance. Administrators can change this value in the *Administration > Settings > Resource control > Concurrent jobs and activities* screen.

Administrators can also limit the number of max jobs executed simultaneously on an instance.

* The number of running jobs will use the lowest value between *max activities* and *max jobs*.
* Use ``0`` to fallback to the max activities limit.

Administrators can also limit the number of activities simultaneously executed by a single job.

---------------------------------
Per-recipe limits
---------------------------------
Users creating recipes can also limit the number of activities simultaneously executed by a recipe.

To set a limit, users must edit the recipe, go to the Advanced tab and change the recipe limit from zero (unlimited) to the desired value.

---------------------------------
Additional limits
---------------------------------
Administrators can tune DSS even further regarding concurrent activities executions and add additional limits. They can limit the number of activities simultaneously executed:

* for a given project.
* for a given recipe type.
* by a given user.
* by recipes with a given tag.
* by a plugin recipe.

These additional limits are defined using a key/value syntax.

To define a **limit for a given project**, the key must follow the pattern "project/XXXX" (where XXXX is the key of the project, as seen in the URL). For example, to limit the number of concurrent activities executed for the project TEST1 to 2, add a new key 'project/TEST1' with a corresponding value of 2.

To define a **limit for a given user**, the key must follow the pattern "user/XXXX" (where XXXX is the username of a user).

To define a **limit for a given tag**, the key must follow the pattern "tag/XXXX" (where XXXX is the name of a tag).

To define a **limit for a given recipe type**, the key must follow the pattern "recipeType/XXXX" (where XXXX is a type of recipe such as 'shaker').

To define a **limit for a plugin recipe**, the key must be one of the values of the :code:`resourceKeys` field defined in the descriptor for the plugin recipe.

For example, to limit the number of concurrent activities executed by some CPU hungry plugin recipe to 1, edit the :code:`recipe.json` file corresponding to the plugin recipe and add **cpu_hungry** in the :code:`resourceKeys` field.

.. code-block:: json

    {
        "meta" : {
            "label" : "...",
            "description" : "...",
            "icon" : "..."
        },
        "kind" : "...",
        "inputRoles" : [ "..." ],
        "outputRoles" : [ "..." ],
        "params" : [ "..." ],
        "resourceKeys" : [ "cpu_hungry" ]
    }

.. note::
    The field "resourceKeys" holds a list of keys that allows to limit the number
    of concurrent executions and activities triggered by this recipe.

    Administrators can configure the limit per resource key in the *Administration > Settings > Resources control > Concurrent jobs and activities*
    screen.

Then go back to the *Administration > Settings > Resources control > Concurrent jobs and activities* and add a limit using **cpu_hungry** as key and 1 as value.
