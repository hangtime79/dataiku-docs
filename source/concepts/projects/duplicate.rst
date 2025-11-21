How to Copy a Dataiku Project
=============================

An existing project can make a useful template for a new project so that you don't have to manually replicate the Flow.  How to copy a project depends upon whether you want to:

- Make a copy on the current instance
- Make a copy on another instance

Technical Requirements
-----------------------

- Dataiku user with the Create projects global permission
- Admin rights on the project you want to copy

Make a Copy on the Current Dataiku Instance
--------------------------------------------

- From the homepage of the project you want to copy, choose Actions > Duplicate project.

Alternatively:

- From the Projects page, right-click on the tile of the project you want to copy and choose Duplicate project.

Duplicate Project Options
~~~~~~~~~~~~~~~~~~~~~~~~~~

When duplicating a project:

- It must have a unique project ID.  Dataiku provides a default name and ID, or you can choose your own.
- You have the option to choose what data is included in the export.  Be sure that your connections to any databases use the ``${projectKey}_`` prefix to ensure that there is no conflict over database tables between the original and duplicated projects.

Make a Copy on Another Dataiku Instance
-----------------------------------------

- From the homepage of the project you want to copy, choose Actions > Export.
- Download the project export .zip file.
- From the user homepage of another instance, choose +New project > Import and select the .zip file.

Alternatively:

- Use the command-line export and import scripts available on the DSS server:

.. code-block:: bash

  DATA_DIR/bin/dsscli project-export project_key foo.zip
  DATA_DIR/bin/dsscli project-import foo.zip

- Use ``dsscli project-export -h`` for a short help.

Export/Import Project Options
-----------------------------

When exporting a project, you have the option to choose what data is included in the export.  This can be useful if the bandwidth between the Dataiku instances is slow:

- Deselect the export of non-input data.  Once the project is imported on the second Dataiku instance, rebuild the downstream datasets.

When importing a project:

- It must have a unique project ID.  You'll be prompted if there is a conflict with an existing project on the instance.
- The new instance must have connections configured for the imported project to use.  Do not create a connection to the same location (e.g. the same database) on the second instance: both projects would then write to the same tables (in SQL, Hive, etc.). The last dataset to be computed would overwrite the other dataset stored in the same table.
- The new instance must have any necessary code environments for the imported project to use.  If the names of the code environments on the new instance are different from those on the original instance, you can "remap" the old names to the new names.
