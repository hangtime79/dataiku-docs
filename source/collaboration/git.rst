Working with Git
##################

.. contents::
	:local:

Overview
==========

DSS provides native integration with Git. Several parts of DSS can work with Git

Version control of projects
----------------------------

Each change that you make in the DSS UI (modify the settings of a dataset, edit a recipe, modify a dashboard, ...) is automatically recorded in the version control system.

This gives you:

* Traceability into all actions performed in DSS
* The ability to understand the history of each object
* The ability to revert changes

For more details, see :doc:`version-control`

Importing Python and R code
-----------------------------

If you have code that has been developed outside of DSS and is available in a Git repository (for example, a library created by another team), you can import this repository (or a part of it) in the project libraries, and use it in any code capability of DSS (recipes, notebooks, webapps, ...)

For more details, see :doc:`import-code-from-git`

Importing Jupyter Notebooks
-----------------------------

If you have Notebooks that have been developed outside of DSS and are available in a Git repository, you can import these Notebooks in a DSS project. You can modify them inside DSS and push back the changes to the remote repository.

For more details, see :doc:`import-notebooks-from-git`

Developing plugins
-------------------

When developing plugins, each plugin is a Git repository. You can view the history, revert changes, use branches, and push/pull changes from remote repositories.

For more details, see :doc:`/plugins/reference/git-editor`.

Importing plugins
------------------

If you have developed a plugin on a DSS instance and have pushed your plugin to a Git repository, you can import this plugin on another DSS instance directly from the Git repository.

For more details, see :doc:`/plugins/installing`

.. _ref-devguide-working-with-remotes:

Working with remotes
=====================

All integration points explained above include the ability to interact with remote repositories (either pull-only or pull-and-push depending on the cases).

This section explains how you can work with remote repositories.

DSS always uses the "git" command-line client to work with remote repositories, in non-interactive mode.

* Interaction with SSH-based remotes requires that the UNIX account running DSS (the `dssuser`) can connect to the repository without any prompt, i.e.

   * It must either have a passwordless SSH key, or uses a SSH agent or Kerberos authentication)
   * The SSH host key for the remote host must already be validated - this can be done by logging in as the `dssuser` and running manually a Git clone/fetch command to the remote Git host
* Interaction with HTTPS-based remotes requires that the UNIX account running DSS (the `dssuser`) has credentials stored in the Git credentials cache for this particular repository


.. _git.setup:

Setup
----------------------------

To connect from DSS to an external git repository, you must copy your DSS user's public SSH key and add it to the list of accepted SSH keys in your GitHub account.

To copy the public key, from the terminal of your DSS user's account, run: `pbcopy < ~/.ssh/id_rsa.pub`

If you have not yet generated needed SSH keys, you will need to run `ssh-keygen` and follow corresponding prompts.

To generate your public key on Dataiku Cloud:

* go to your launchpad > extension tab > add an extension,
* select the SSH integration feature,
* enter the hostname of the repository,
* click to validate and generate the key.

Dataiku Cloud will then automatically generate the key and run a command to the origin to get (and verify) the SSH host key of this server. You can now copy the generated key and add it to your GitHub account. To find this key in the future or generate a new one go to the extension tab and edit the SSH Integration feature.

For more assistance, see GitHub's `documentation <https://help.github.com/articles/adding-a-new-ssh-key-to-your-github-account/>`_.

Configuration and security
----------------------------

Interaction with the remote repositories are always performed by the `dssuser`. In other words, even if your DSS instance is running :doc:`User Isolation Framework </user-isolation/index>`, Git accesses are not impersonated.

If you want to offer different levels of authorizations to your different user groups on the remote repositories, you need to setup multiple per-group Git configuration rules.

Per-group Git configuration rules are configured in Administration > Settings > Git.

Rules are evaluated on a "first-match" basis, the first rule that matches both the user's groups and the remote URL will be applied. Each rule applies either to a single group of users, or (if the group is left empty), to all users.
Multiple rules targeting different remote URLs can be defined for the same group (for example, to use different SSH keys depending on the remote URLs).

Each rule is used to define:

* Which remote URL(s) are allowed for this particular user group
* Additional Git configuration options. This is mostly used to configure the ``core.sshCommand`` option, in order to specify a specific SSH key
* Ability to override the "$HOME" environment variable. This allows you to use a ".gitconfig" file per group, notably used to specify alternative cached credentials file

If no rule matches for a given group, access to Git remotes is denied to this group. It is sometimes desirable to have a "catch-all" rule as the last rule, i.e. a rule without a "group name" specified that will catch all users not handled by other rules.


.. note::

	On Dataiku Cloud, the path to the generated SSH key is available in the SSH integration extension.


.. warning::

	Never use ``.*`` as a whitelisted URL, because that allows the user to clone local repositories as the ``dssuser``, which can be
	abused to read folders (as the ``dssuser``) that a user shouldn't be allowed to read.

	The default value when adding a new rule prevents this.

Example 1: Allow repository URLs explicitly per group
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

If you want:

* "group1" to be able to work with remotes "remote1a" and "remote1b"
* "group2" to be able to work with remote "remote2"
* All other groups to be denied access to any remote

Configure two rules:

* Group=group1, URLs whitelist = 2 entries, "remote1a" and "remote1b"
* Group=group2, URLs whitelist = 1 entry, "remote2"


If you want:

* "group1" to be able to work only with remote "remote1"
* All other groups to be able to work with remote "remote2"

Configure two rules:

* Group=group1, URLs whitelist = 1 entry, "remote1"
* Group=<empty>, URLs whitelist = 1 entry, "remote2"


Example 2: Use a SSH key per group
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

This is useful if your remote repository performs access control based on which SSH key is used to push.

If you want:

* "group1" to be able to work with any remote, but with SSH key "/home/dataiku/.ssh/group1-key"
* "group2" to be able to work with any remote, but with SSH key "/home/dataiku/.ssh/group2-key"
* All other groups to be denied access to any remote

Configure two rules:

* Group=group1, URLs whitelist = default value, add a configuration option ``"core.sshCommand" = "ssh -i /home/dataiku/.ssh/group1-key -o StrictHostKeyChecking=yes"``
* Group=group2, URLs whitelist = default value, add a configuration option ``"core.sshCommand" = "ssh -i /home/dataiku/.ssh/group2-key -o StrictHostKeyChecking=yes"``


.. note::

	On Dataiku Cloud, SSH keys created via the SSH extension are available by default to the DSS instance.
	To specify a custom SSH key, you must also add the ``-F none`` option so that SSH will not load the default configuration file, otherwise SSH keys listed by default will also be used.
	So a full configuration would look like: ``"ssh -i /home/dataiku/.ssh/group1-key -o StrictHostKeyChecking=yes -F none"``.


Troubleshooting
-----------------

"Unknown Host Key" issues
%%%%%%%%%%%%%%%%%%%%%%%%%%%

The first time you push to a remote, you might encounter a "UnknownHostKey" error. You need to first login in shell to the DSS server and run a single "ssh" or remote git command to the origin you want to talk with in order to get (and verify) the SSH host key of this server. The key will be added to your ".ssh/known_hosts" file and DSS can then connect.

For example if you want to push to ``git@myserver.com:myrepo`` and get a UnknownHostKey error, login to the server and run ``ssh git@myserver.com``. You will get a prompt to accept the host key. Accept it and you can then work with this remote.
