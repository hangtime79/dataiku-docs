Version control of projects
############################

.. contents::
	:local:

DSS comes builtin with Git-based version control. Each project is backed by a regular Git repository. Each change that you make in the DSS UI (modify the settings of a dataset, edit a recipe, modify a dashboard, ...) is automatically recorded in the Git repository

This gives you:

* Traceability into all actions performed in DSS
* The ability to understand the history of each object
* The ability to revert changes
* The ability to work with multiple branches

You don't need to configure anything to benefit from version control. However, by switching to explicit commit modes, you can get more control.

Viewing history
=================

On the project menu, click on "Version Control". The project's history browser appears. You can view all commits made on the project. Scroll to the bottom to load more commits.

You can click on any commit to view the details and browse the changed files on this commit. By clicking on the "Compare" button, you can compare the state of the whole project between two revisions.

In addition, when you are in an object (dataset, recipe or web app), you can click on the History tab to view the history of only this specific object.

Manual or automatic commits
============================

In a project "Change Management" settings (Project Settings > Change management), the "Commit Mode"
option defines how changes are committed to your project Git repository. You can select between "Auto" or
"Explicit" commit modes, based on your workflow preferences.

By default, a Dataiku project uses the "Auto" commit mode where changes are automatically
committed whenever you save recipes or other items within the project. In this mode, every time you make a change and
save it, a new commit is created in the project Git repository and history.

If you select the "Explicit" commit mode, all changes will still be saved to the project, but you will
need to explicitly commit your changes using the "Commit" button that will appear in the top menu on different pages. 
In this mode, you have more control over when your changes are committed to the Git repository, for example you can choose 
to commit multiple changes together in a single commit or make individual commits for each modification.

Reverting
==========

Revert a project to a revision
--------------------------------

On the project's Version Control page, you can revert your project to a specific revision.

.. warning::

	Reverting a project to an older revision will discard all work performed in all aspects of the project since that revision, by all users of a project.

	Reverting only affects the configuration of the project (datasets, recipes, web apps, dashboards...).
	It does not affect data. Thus, after revert, some data might be missing and might need to be rebuilt

Click on the revision you want to revert to, and click on "Revert to this revision".


Revert an object to a revision
--------------------------------

From an object's history tab, you can revert only this object (recipes only for now) to a specific revision. Other objects in the project are not affected.

.. warning::

	Reverting a single object is a dangerous operation, since it might make the reverted object inconsistent with the rest of the project. Various issues may appear.

	Reverting a single object may cause Git conflicts. In that case, DSS will not perform the revert. You will need to perform it manually using the Git command line.

	We advise that you only use this option to revert to previous revisions only in presence of "simple" changes like changes in code rather than "structural" changes (changing inputs of a recipe, ...)

Revert a single commit from a project
--------------------------------------

On the project's Version Control page, you can revert a single previous commit. A "reverse" commit will be added to the history of the project.

.. warning::

	Reverting a single revision is a dangerous operation, since it might make the reverted object inconsistent with the rest of the project. Various issues may appear.

	Reverting a single revision may cause Git conflicts. In that case, DSS will not perform the revert. You will need to perform it manually using the Git command line.

	We advise that you only use this option to cancel previous commits that only contain "simple" changes like changes in code rather than "structural" changes (changing inputs of a recipe, ...)

Working with branches
======================

.. warning::

	It is strongly recommended to have a good understanding of the Git model and wording before using this feature.

.. warning::

	Merge commits make it impossible to revert a project into an anterior state from the DSS UI. To ensure projects can be reverted, prefer using squash merging, which is only available using an external tool (Github, Bitbucket, Gitlab, ...).

From the project's Version Control page, click on the branch indicator to create a new branch or switch to an existing branch.

If you have enabled a remote, this will show both local and remote branches.

Using projects per branch
--------------------------

When creating a new branch or switching to a branch, you have the option to either:

* Switch the current project to the branch
* Duplicate the current project to a new project that will be initialized on the branch

We strongly recommend using duplicated projects. It is important to understand that a given DSS project can only be on one branch at any given time. If you switch the branch of the current project, this will affect all collaborators, and you can't work on multiple branches at once.
In addition, when using the governance capabilities, not using the recommended duplicated projects may lead to the loss of some governance data (ex: workflows attached to Saved Model Versions or Bundles).

* If you have a remote repository and you create a duplicated project, you'll be able to commit and push your changes in the branch from the duplicated project, merge them outside of DSS and then pull the changes in the "main" project. See `Working with a remote`_
* If you don't have a remote repository, you'll be able to commit and merge the branch into the "main" project by using merge requests. See `Working with no remote`_

If you have already created a duplicated project for a given branch, DSS will propose to go to this duplicated project if you try to switch to this branch.

Working with a remote
======================

The version control in DSS is a regular Git repository (which can be managed with the ``git`` command line tool).

It is possible to connect the repository of each project to a Git remote.  This will allow you to pull new updates and branches from the remote, and to push your changes to the remote.

.. warning::

	**Tier 2 support**: Support for pushing to Git remotes is covered by :doc:`Tier 2 support </troubleshooting/support-tiers>`

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
* In another Git tool (not DSS), merge the pushed local branch into the original branch, resolving conflicts
* In DSS, switch back to the original branch and drop local changes
* Pull
* You will now have your merged changes

Merging branches (outside of DSS)
----------------------------------

Let's say you have a project on branch "main" and want to develop a new feature.

* In DSS, switch to a new branch "myfeature". This will by default create a new project
* When you are happy with the new feature, push it
* In your Git UI (Github, Bitbucket, Gitlab, ...), open a pull request from myfeature to main
* Merge the pull request (prefer squash merging to avoid the limitations on project revert)
* In DSS, go back to the original project (on the "main" branch)
* Pull it, you will now have your merged changes

Working with no remote
=======================

.. note::

	Although it is possible to merge branches directly in DSS, we recommend working with a remote whenever possible, as it offers more options for managing merge commits and better collaboration capabilities.

Merging branches (within DSS)
------------------------------

.. note::

	To create a merge request, the user must be granted the permission to edit the destination project and must be allowed to "Write unisolated code".

Let's say you have a project on branch "main" and want to develop a new feature.

* In DSS, switch to a new branch "myfeature". Choose to duplicate the project
* When you are happy with the new feature, go back to the main project and create a merge request
* Select the duplicated project associated with the "myfeature" branch
* Review the changes and resolve the conflicts if any
* Merge the merge request.

Per-project vs global Git
==========================

When you install DSS, it is by default configured to have one Git repository per project, plus a global Git repository for "global" configuration elements (Administration settings, connections, users and groups, ...)

.. note::
	DSS overrides the Git ``excludesFile`` configuration property in each project. This property references a global ``.dku-projects-gitignore`` file that centralizes all DSS internal project files that must be git-ignored.

DSS can also be configured to have a single Git repository for the whole configuration of all projects.

.. warning::

    We don't advise changing this setting. Using global repository makes it impossible to work with Git remotes.

To change this setting:

* Stop DSS

* Edit ``install.ini``, and in the ``[git]`` section, set ``mode = global``

* Start DSS
