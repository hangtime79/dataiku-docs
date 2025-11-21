ServiceNow
#############

Create ServiceNow Issue
=======================

This tool is provided by the "ServiceNow" plugin, which needs to be installed.

In the plugin Settings -> Service accounts (or User accounts), create a new preset to connect to a ServiceNow instance and enter a single service account credential. In the case of a User account preset, you can require Dataiku users to enter their credentials individually.

When configuring a tool instance in a project, choose a Service account or User account authentication preset.

The tool can create and populate a new issue with a summary and description, and optionally an issue impact (between 1 and 3) and urgency (between 1 and 3).

Test your Create ServiceNow Issue tool in the "Quick test" tab:

.. code-block:: json

    {
        "input": {
            "summary": "Your issue summary",
            "description": "Longer description",
            "impact": 2,
            "urgency": 3
        },
        "context": {}
    }
