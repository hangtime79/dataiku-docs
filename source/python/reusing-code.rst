Reusing Python code
####################

.. contents::
	:local:

When you write a lot of Python code in a project, or across projects, you will often want to make reusable parts of code.

DSS provides several mechanisms for reusing Python code:

* Packaging your code as functions or modules, and making them available in a specific project
* Importing code that has been made available from one project to another
* Packaging your code as functions or modules, and making them available in all projects
* Packaging your code as a reusable plugin, and making it available for coder and non-coder users alike

.. _project-lib:

Sharing Python code within a project
=====================================

In each project, you can write Python modules in the **Library editor**. The project's library editor is available by going into the "Code" universe (orange), and selecting the "Libraries" tab.

.. image:: img/project-lib-editor-python.png

You can then write code under a "Python source" folder, i.e. a folder that has the "Python" icon associated to it.


Modules that are written here are automatically available in all Python code in the same project. Import rules are the regular Python rules.

For example, to use the function shown in the above image, use:

.. code-block:: python

	from analyticfunctions import build_custom_keras_model
	model = build_custom_keras_model()

or:

.. code-block:: python

	import analyticfunctions
	model = analyticfunctions.build_custom_keras_model()

.. note::

	Don't forget that if you create subfolders in a Python source folder, each folder must have a ``__init__.py`` file in order to be a valid Python module

For a file at the root of the library editor:

.. image:: img/project-lib-editor-python-2.png

Use:


.. code-block:: python

	from misccustom import get_now
	the_time = get_now()

or:

.. code-block:: python

	import misccustom
	the_time = misccustom.get_now()

Working with multiple source folders
--------------------------------------

By default, the Library editor contains two top-level folders, "python" and "R", which are respectively the root folder for Python and R code.

You can create other folders that will also act as Python source folders, i.e. that will be added to the ``PYTHONPATH`` (or ``sys.path``) of the Python processes of the project.

Working with multiple source folders is mainly useful when :doc:`importing code from external Git repositories </collaboration/import-code-from-git>`. When using this, addition of the new folders is automatic.

To manually edit the list and order of the Python source folders, open the ``external-libraries.json`` file in the library editor and edit the ``pythonPath`` list. All paths must be relative to the root of the library editor.

Importing libraries from other projects
=========================================

If you have created libraries in a project A, you can import them in project B. The libraries of project A will be added to the source path of all code running in project B.

* Go to the library editor of project B
* Open the ``external-libraries.json`` file
* Edit the ``importLibrariesFromProjects`` list and add the project key (which appears in the URL, i.e. not the project display name) to it
* Save the ``external-libraries.json`` file

You need to have "Read project content" permission on A and "write project content" on B.

.. _global-lib:

Sharing Python code globally
=============================

In addition to the per-project Python library editor, there is another global Python library editor for the whole instance.
The global Python library editor is available from the **Application menu > Global Shared Code**.

.. image:: img/global-shared-code.png

Modules that are written here are automatically available in all Python code in all projects.
Import rules follow the regular Python rules (see above for more information).

Permissions
------------

You need the "Edit lib folders" global (group-level) permission to use the global Python library editor.

.. caution::

    Putting code in the global library increases the risk of having clashes or conflicts.
    Generally speaking, it is preferable to use per-project libraries.

    Libraries in the global folder will be importable in all Python code,
    regardless of the active :doc:`code environment </code-envs/index>`.
    You should ensure that your code is compatible with Python 3.

.. warning::

    Although global libraries are included in :doc:`API node service packages </apinode/concepts>`,
    they are not included in  :doc:`project bundles </deployment/creating-bundles>`.

Manual editing of code library folders
=========================================

Although not recommended, if you have shell access to the DSS machine, you can modify the library folders directly:

* Per-project library folder is in ``DATA_DIR/config/projects/PROJECT_KEY/lib``
* Global library folder is in ``DATA_DIR/lib/python``

Packaging code as plugins
==========================

See :doc:`/plugins/index`
