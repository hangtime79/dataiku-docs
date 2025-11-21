Component: Project creation macros
###################################

Project creation build upon macros. You should thus be familiar with macros. For more information, please see :doc:`macros`

Please see :doc:`/concepts/projects/creating-through-macros` for details on why you would use project creation macros. A user needs to be granted the :ref:`Create projects using macros <projects-creation>` permission to use a project macro.

To start creating a project creation macro,  we recommend that you use the plugin developer tools (see the tutorial for an introduction). In the Definition tab, click on "Add Python macro", and enter the identifier for your new macro. You'll see a new folder ``python-runnables`` and will have to edit the ``runnable.py`` and ``runnable.json`` files

A project macro is essentially a macro that will run *non-impersonated*, which allows it to have full control over DSS. It receives the identity of the end-user request Python function, thus allowing to perform logic based on this identity.

The project creation macro is responsible for actually creating the project, and setting up permissions.

In order to perform privileged operations, the project creation macro must obtain a privileged API key as shown in the example below.

.. attention::

    The ``resultType`` must be set to ``JSON_OBJECT`` for this specific macro component,
    and the macro should return a JSON object containing a ``projectKey``.

.. seealso::

    A tutorial on this plugin component is available in the Developer Guide: :doc:`devguide:tutorials/plugins/macros/project-creation/index`.

Example: Create project with a default code env
================================================

The ``runnable.json`` file looks like:

.. code-block:: json

    {
        "meta": {
            "label": "New project with code env",
            "description": "Blabla",
            "icon": "icon-puzzle-piece"
        },

        "impersonate": false,

        "params": [
            {
                "name": "projectName",
                "label": "Project name",
                "type": "STRING",
                "mandatory": true
            },
            {
                "name": "pyCodeEnvName",
                "label": "Python Code env name",
                "type": "STRING",
                "defaultValue": "python3"
            }
        ],

        "resultType": "JSON_OBJECT",

        "macroRoles": [
            {"type": "PROJECT_CREATOR"}
        ]
    }

The two important parts here are:

* The `macroRoles` field defines this as a project creation macro
* The `impersonate` field makes the macro privileged

The "meta" and "params" fields are similar to all other kinds of DSS components.

The associated Python code is:

.. code-block:: python

    import dataiku
    from dataiku.runnables import Runnable
    from dataiku.runnables import utils
    import json

    class MyRunnable(Runnable):

        def __init__(self, unused, config, plugin_config):
            # Note that, as all macros, it receives a first argument
            # which is normally the project key, but which is irrelevant for project creation macros
            self.config = config
            
        def get_progress_target(self):
            return None

        def run(self, progress_callback):
            # Get the identity of the end DSS user
            user_client = dataiku.api_client()
            user_auth_info = user_client.get_auth_info()

            # Automatically create a privileged API key and obtain a privileged API client
            # that has administrator privileges.
            admin_client = utils.get_admin_dss_client("creation1", user_auth_info)

            # The project creation macro must create the project. Therefore, it must first assign
            # a unique project key. This helper makes this easy
            project_key = utils.make_unique_project_key(admin_client, self.config["projectName"])
            
            # The macro must first perform the actual project creation.
            # We pass the end-user identity as the owner of the newly-created project
            print("Creating project")
            admin_client.create_project(project_key, self.config["projectName"], user_auth_info["authIdentifier"])

            # Now, this macro sets up the default Python code environment, using the one specified by the user
            print("Configuring project")
            project = user_client.get_project(project_key)
            
            # Move the project to the current project folder, passed in the config as _projectFolderId
            project.move_to_folder(user_client.get_project_folder(self.config['_projectFolderId']))
            
            settings = project.get_settings()
            settings.set_python_code_env(self.config["pyCodeEnvName"])
            settings.save()

            # A project creation macro must return a JSON object containing a `projectKey` field with the newly-created
            # project key
            return json.dumps({"projectKey": project_key})
