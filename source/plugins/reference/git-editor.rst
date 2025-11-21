Git integration in the plugin editor
#####################################

When you create a plugin in the plugin editor, a Git repository is associated to the plugin. Each change you make in the editor (saving a file, adding a new component, ...) is automatically committed in the Git repository.

This gives you:

* Traceability into all actions
* The ability to view the history
* The ability to revert changes

For more details on fetching from Git remotes and working with Git remotes in Dataiku, see :doc:`/collaboration/git`.

Viewing history
================

On the plugin development page, click on "History". The plugin's history browser appears. You can view all commits made on the plugin. Scroll to the bottom to load more commits.

You can click on any commit to view the details and browse the changed files on this commit. By clicking on the "Compare" button, you can compare the state of the plugin between two revisions.

Reverting
==========

From the plugin's History, you can revert your plugin to a specific revision. Click on the revision you want to revert to, and click on "Revert to this revision".

Working with branches
=====================

Click on the branch indicator to create a new branch or switch to an existing branch.

If you have enabled a remote, this will show both local and remote branches.

Merging branches is not available directly in DSS. Instead, use a remote (see below).

A single plugin in a single DSS instance can only have a single branch active at the moment. To work on several branches at the same time, you need to develop in isolated DSS instances.

Working with a remote
======================

You can optionally associate a Git remote repository to your plugin. This will allow you to pull new updates and branches from the remote, and to push your changes to the remote.

.. warning::

	It is strongly recommended to have a good understanding of the Git model and wording before using this feature.

To associate a remote, click on the change tracking indicator, select "Add a remote", and enter the URL of the remote. For more details on working with Git remotes, see :doc:`/collaboration/git`. 

Once the remote is associated, new options become available:

* Fetch fetches the latest changes and branches from the remote (but does not touch the local copy)

* Push pushes the current active branch to the remote. Push will fail if the remote has been updated first. In that case, start by pulling.

* Pull does a "pull --rebase" action: it fetches the latest changes from the remote and attempts to rebase your local changes on top of the remote changes. In case of a conflict, pull aborts. It is not possible to edit conflicts directly in DSS. See below for help on handling conflicts

* Drop changes allows you to drop all commits you made on the local branch, and to move back the local branch to the HEAD of the remote branch

Handling conflicts
-------------------

If pull fails because of a conflict, do the following:

* Create a new local branch
* Push it
* In another Git tool (not DSS), merge the original branch into the pushed local branch, resolving conflicts
* In DSS, switch back to the original branch and drop local changes
* Pull
* You will now have your merged changes

Merging branches
-----------------

Let's say you have a plugin on branch "master" and want to develop a new feature.

* In DSS, switch to a new branch "myfeature".
* When you are happy with the new feature, push it
* In your Git UI (Github, Bitbucket, Gitlab, ...), open a pull request from myfeature to master
* Merge the pull request
* In DSS, switch back to the "master" branch
* Pull it, you will now have your merged changes
