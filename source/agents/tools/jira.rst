Jira
#######

Create Jira Issue
==================

This tool is provided by the "Jira" plugin, which needs to be installed.

In the plugin Settings -> Jira connection, create a new preset to connect to a Jira instance (cloud or on premise) using a username and API token.

When configuring a tool instance in a project, choose a Jira connection preset and enter the Jira project key where new issues will be added.

The tool can populate an issue summary and description.

Test your Create Jira Issue tool in the "Quick test" tab:

.. code-block:: json

    {
        "input": {
            "summary": "Your issue summary",
            "description": "Longer description"
        },
        "context": {}
    }
