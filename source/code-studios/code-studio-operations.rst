Operations
###############################

.. contents::
	:local:

.. _synchronized_files:

Editing files with Code Studio
==============================

The Code Studios run separately from DSS, in the Kubernetes cluster.

Some files are then synchronized between DSS and the Code Studio, in order for recipes / project libraries / ... to be available within each Code Studio.

Files are:

* synchronized from DSS to Code Studio when the Code Studio starts
* synchronized from Code Studio to DSS when the Code Studio stops
* synchronized both ways (with conflict detection) when clicking the "Synchronize files" button in the UI of the Code Studio

Each type of file is synchronized to a particular location in the Code Studio, which is overridable in the template settings.

All versioned files are under control of the DSS instance's *git*, so it's recommended to avoid putting large files or binary files in versioned areas. Instead, large files should preferably go into non-versioned (resources) areas

Project libraries
-----------------

The usual Project libraries (see :doc:`Reusing Python Code </python/reusing-code>` and :doc:`Reusing R Code </R/reusing-code>`) are available to all Code Studios of the project. Project libraries are versioned in the version control of the project.

Project libraries can be edited outside of a Code Studio through the "Code > Libraries" menu

Project libraries are available at ``/home/dataiku/workspace/project-lib-versioned`` in the Code Studio by default.

.. note::

	Project libraries can also have non-Python and non-R files, such as stylesheets, small static files, ... For large files, use Project resources instead.

Project resources
-----------------

Project resources are:
    - non-versioned files that are global to a project, and available to all Code Studios of the project. 
    - useful for storing artifacts that may be used by several Code Studios in the project, and that should not be versioned (usually because they are large), such as images.
    - available at `/home/dataiku/workspace/project-lib-resources` in the Code Studio by default. 

Code Recipes
------------

The code of code recipes (Python, R, SQL, Scala) is available to all Code Studios of the project, with one file per recipe.

The code is exactly what you see when editing a given recipe in the DSS UI, for example after opening it from the Flow.

Code Recipes are available at ``/home/dataiku/workspace/recipes`` in the Code Studio by default.

Code Notebooks
--------------

The source of code recipes (Python, R, SQL, Scala) is available to all Code Studios of the project, with one file per notebook.

The code is exactly what you see when editing a given recipe in the DSS UI, for example after opening it from the notebook menu.

Notebooks are available at ``/home/dataiku/workspace/notebooks`` in the Code Studio by default.

Code Studio versioned files
---------------------------

These files are specific to each Code Studio and are not shared between Code Studios. 

These files should be used for Code Studios that define an application (such as a Streamlit Application), for the code of the application itself. For example, the default "Streamlit" block for templates puts the code of the application there.

Code Studio versioned files can be edited in DSS, in "Files > Versioned" in the UI of the Code Studio.

Code Studio versioned files are available at `/home/dataiku/workspace/code_studio-versioned` in the Code Studio by default.

Code Studio resource files
--------------------------

These files are specific to each Code Studio and are not shared between Code Studios. 

These files should be used for Code Studios that define an application (such as a Streamlit Application), for storing artefacts that are needed by the Code Studio and that should not be versioned (usually because they are large), such as images.

Code Studio resource files can be edited in DSS, in "Files > Resources" in the UI of the Code Studio.

Code Studio resource files are available at ``/home/dataiku/workspace/code_studio-resources`` in the Code Studio by default.


User config files
-----------------

These files are shared across all Code Studios of a user and are not shared between users.

They are useful to store user settings.

In the built-in blocks for Visual Studio Code, RStudio Server and JupyterLab, this folder is used to store the IDE configuration.

User config files are available at ``/home/dataiku/workspace/user-versioned`` in the Code Studio by default

User resource files
-------------------

These files are shared across all Code Studios of an user, and are not shared between users. They are not versioned.

They are useful to store user artifacts that should not be versioned, such as plugins, tools, ...

User resource files are available at ``/home/dataiku/workspace/user-resources`` in the Code Studio by default.
