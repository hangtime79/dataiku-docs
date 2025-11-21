DSS Macros
###########

Macros are predefined actions that allow you to automate a variety of tasks, like:

* Maintenance and diagnostic tasks
* Specific connectivity tasks for import of data
* Generation of various reports, either about your data or DSS

Macros can either be:

* Run manually, from a Project's "Macros" screen.
* Run automatically from a scenario step
* Made available for running to dashboard users by adding them on a dashboard.

Macros can be:

* Provided as part of DSS
* In a plugin
* Developed by you

For example, the following macros are provided as part of DSS:

* Generate an audit report of which connections are used
* List and mass-delete datasets by tag filters
* Clear internal DSS databases
* Clear old DSS job logs
* Kill Jupyter sessions that have either been running or idle for too long

Macros are designed to make repetitive tasks or tasks that would require to write code each time easier. Other examples could be:

* Creating a project, adding a set of groups to it and performing various other settings (if you need to create a large number of projects)
* Importing a folder full of files and creating one dataset for each

Some macros can be used by all DSS users (like data-import-related macros) or only by administrators (like clearing internal databases)

You can write your own macros in Python. For more information, see :doc:`/plugins/reference/macros`
