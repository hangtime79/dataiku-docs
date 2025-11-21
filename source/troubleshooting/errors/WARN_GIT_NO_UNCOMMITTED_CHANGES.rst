WARN_GIT_NO_UNCOMMITTED_CHANGES: Projects - Uncommitted Git changes
####################################################################

Some projects in your Dataiku instance have uncommitted changes in their Git repository, even though they are configured in **Auto** commit mode. This situation is not expected and may indicate an internal issue or an edge case during project activity.

These uncommitted changes can lead to inconsistencies when switching branches or during collaborative work.

Remediation
===========

Open the affected project(s) in Dataiku and go to the **Version Control** page:

- Click on the **Force Commit** button to review the uncommitted changes.
- If the changes are valid, commit them using the dialog.

There is currently no way to discard uncommitted changes from the UI. 