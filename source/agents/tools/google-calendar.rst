Google Calendar
###########################

Create Google Calendar Event
============================

This tool is provided by the "Google Calendar" plugin, which needs to be installed.

First, login to the Google Developer Workspace, create a project, and enable the Google Calendar API. Then, create a Client in the Google Auth platform and retrieve a Client ID and Client secret. In the plugin Settings -> Google Single Sign On, create a new preset, enter the Client ID and Client secret, and grant access to user groups.

If you are an end user of the tool or a builder wanting to test the tool, go to your personal Profile & Settings -> Credentials -> Plugins -> Google Calendar -> your new preset, then authenticate to Google.

The Create Google Calendar Event tool will create an event in the calendar configured by the user running the agent.

When creating a tool instance in a project, choose an SSO preset from earlier, and optionally enter a calendar ID linked to your Google account (the default is the primary calendar).

The tool can add an event title, location, description, start time, end time, and add other attendees by email.

Test your Create Google Calendar Event tool in the "Quick test" tab:

.. code-block:: json

    {
        "input": {
            "summary": "Your title",
            "location": "Your location",
            "description": "Longer description",
            "start": "2025-05-06T19:00:00Z",
            "end": "2025-05-06T20:00:00Z",
            "attendees": "coworker1@company.com,coworker2@company.com"
        },
        "context": {}
    }
