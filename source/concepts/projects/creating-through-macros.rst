Creating projects through macros
#################################

Many administrators wish to have more control on how projects are created. Examples of use cases include forcing a default code env, container runtime config, automatically creating a new code env, setting up authorizations, setting up UIF settings, creating a Hive database, ...

This led many administrators to deny project creation to users, leading to higher administrative burden for administrators.

With project creation macros, administrators can delegate the creation of projects to users, but the project will be created using administrator-controlled code, in order to perform additional actions or setup.

For users
==========

Once your administrator has created a project creation macro, and granted you the appropriate :ref:`permission <projects-creation>`, you'll see new options appear in the "New project" button

For administrators
===================

You need to create a dev plugin and create a project creation macro in it.

Please see :doc:`/plugins/reference/project-creation-macros` for more details