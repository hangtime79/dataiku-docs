dsscli tool
#############

.. contents::
	:local:
	:depth: 1

.. note::

    These instructions do not apply to Dataiku Cloud

``dsscli`` is a command-line tool that can perform a variety of runtime administration tasks on DSS. It can be used directly by a DSS administrator, or incorporated into automation scripts.

Most dsscli operations are performed through the DSS public API and can thus also be performed using the :doc:`DSS public API Python client <devguide:api-reference/python/index>`. You can also directly query the :doc:`DSS REST API </publicapi/index>`.

Running dsscli
================

dsscli is made of a large number of commands. Each command performs a single administration task. Each command takes arguments and options

From the DSS data directory, run ``./bin/dsscli <command> <arguments>``

* Running ``./bin/dsscli -h`` will list the available commands.
* Running ``./bin/dsscli <command> -h`` will show the detailed help of the selected command.

For example, to list jobs history in project MYPROJECT, use ``./bin/dsscli jobs-list MYPROJECT``


dsscli vs dssadmin
====================

Another command-line tool is available in the DSS data directory for performing management tasks on DSS: ``./bin/dssadmin``

* dssadmin is mostly for "installation-kind" of commands (setting up R, Spark or Hadoop integration for example)
* dsscli is mostly for "day-to-day" routine operations (creating users, running jobs, ...)

Security-related commands
==========================

dsscli provides commands to:

* Create, delete, list and edit users
* Create, delete, list and edit groups
* Create, delete, list and edit API keys

user-create
------------

.. code-block:: bash

    dsscli user-create [-h] [--email EMAIL]
                               [--source-type SOURCE_TYPE]
                               [--display-name DISPLAY_NAME]
                               [--user-profile USER_PROFILE] [--group GROUP]
                               login password

* ``SOURCE_TYPE`` must be either ``LOCAL`` to create a regular user (in the DSS users database), ``LDAP`` to create a user that will authenticate through LDAP or ``LOCAL_NO_AUTH`` for authentication through SSO. See :doc:`/security/authentication/ldap` and :doc:`/security/sso` for more information. Note that even for LDAP and LOCAL_NO_AUTH, dsscli expects a "password" argument. Enter any random string, it will be ignored. The default is ``LOCAL``

* ``USER_PROFILE`` is one of the possible user profiles defined by your license. For most DSS licenses, it is one of ``READER``, ``DATA_ANALYST`` or ``DATA_SCIENTIST``. The default is specified by your configuration

* The ``--group GROUP`` argument can be specified multiple times to place the user in multiple groups

users-list
----------

.. code-block:: bash

	dsscli users-list

user-delete
------------

.. code-block:: bash

	dsscli user-delete [-h] login

	positional arguments:
  		login       Login to delete

user-edit
----------

Modifies the settings of an existing user.

.. code-block:: bash

    dsscli user-edit [-h] [--password PASSWORD]
                             [--display-name DISPLAY_NAME] [--email EMAIL]
                             [--user-profile USER_PROFILE] [--group GROUP]
                             login


Each of password, display name, email, user-profile and groups can be modified independently.

For example, running ``dsscli user-edit --email mynewemail@company.com user`` will only modify the email address, and leave all other fields unmodified.

All groups are modified at once: thus to modify groups, you need to pass a new list of groups, which will be the new complete list.

It is not possible to modify password for a LDAP or LOCAL_NO_AUTH user

groups-list
------------

Lists all groups in DSS

.. code-block:: bash

	dsscli groups-list [-h] [--with-permissions] [--output OUTPUT]
                               [--no-header]

If ``--with-permissions`` is specified, additional columns are added to the output with global permissions, as detailed in  :doc:`/security/permissions`


group-create
--------------

Creates a group by name

.. code-block:: bash

 	dsscli group-create [-h] [--description DESCRIPTION]
                              [--source-type SOURCETYPE] [--admin ADMIN]
                              [--may-manage-code-envs MAYMANAGECODEENVS]
                              [--may-create-code-envs MAYCREATECODEENVS]
                              [--may-write-unsafe-code MAYWRITEUNSAFECODE]
                              [--may-write-safe-code MAYWRITESAFECODE]
                              [--may-create-projects MAYCREATEPROJECTS]
                              [--may-manage-udm MAYMANAGEUDM]
                              [--may-edit-lib-folders MAYEDITLIBFOLDERS]
                              [--may-develop-plugins MAYDEVELOPPLUGINS]
                              [--may-create-authenticated-connections MAYCREATEAUTHENTICATEDCONNECTIONS]
                              name

All of the ``--may-xxx`` flags take "true" or "false" as argument, and refer to one of the global permissions as detailed in :doc:`/security/permissions`

SOURCETYPE can be either LDAP or LOCAL. Note that LDAP groups need to declare mappings to LDAP groups to be functional, but this feature is not currently in dsscli. You need to use the DSS API clients.

Adding users in groups is done by editing these users.

group-edit
-----------

Edits the settings of a group by name

.. code-block:: bash

 	dsscli group-edit [-h] [--description DESCRIPTION]
                              [--source-type SOURCETYPE] [--admin ADMIN]
                              [--may-manage-code-envs MAYMANAGECODEENVS]
                              [--may-create-code-envs MAYCREATECODEENVS]
                              [--may-write-unsafe-code MAYWRITEUNSAFECODE]
                              [--may-write-safe-code MAYWRITESAFECODE]
                              [--may-create-projects MAYCREATEPROJECTS]
                              [--may-manage-udm MAYMANAGEUDM]
                              [--may-edit-lib-folders MAYEDITLIBFOLDERS]
                              [--may-develop-plugins MAYDEVELOPPLUGINS]
                              [--may-create-authenticated-connections MAYCREATEAUTHENTICATEDCONNECTIONS]
                              name

All of the ``--may-xxx`` flags take "true" or "false" as argument, and refer to one of the global permissions as detailed in :doc:`/security/permissions`

SOURCETYPE can be either LDAP or LOCAL. Note that LDAP groups need to declare mappings to LDAP groups to be functional, but this feature is not currently in dsscli. You need to use the DSS API clients.

Adding users in groups is done by editing these users.

api-keys-list
--------------

Lists global API keys

api-key-create
---------------

Creates a global API key

.. code-block:: bash

	dsscli api-key-create [-h] [--output OUTPUT] [--no-header]
                                  [--description DESCRIPTION] [--label LABEL]
                                  [--admin ADMIN]
                                  [--may-manage-code-envs MAYMANAGECODEENVS]
                                  [--may-create-code-envs MAYCREATECODEENVS]
                                  [--may-write-unsafe-code MAYWRITEUNSAFECODE]
                                  [--may-write-safe-code MAYWRITESAFECODE]
                                  [--may-create-projects MAYCREATEPROJECTS]
                                  [--may-manage-udm MAYMANAGEUDM]
                                  [--may-edit-lib-folders MAYEDITLIBFOLDERS]
                                  [--may-develop-plugins MAYDEVELOPPLUGINS]
                                  [--may-create-authenticated-connections MAYCREATEAUTHENTICATEDCONNECTIONS]

The ``--admin`` flag and all of the ``--may-xxx`` flags take "true" or "false" as argument, and refer to one of the global permissions as detailed in :doc:`/security/permissions`

api-key-edit
---------------

Edits a global API key

.. code-block:: bash

	dsscli api-key-edit [-h] [--output OUTPUT] [--no-header]
                                  [--description DESCRIPTION] [--label LABEL]
                                  [--admin ADMIN]
                                  [--may-manage-code-envs MAYMANAGECODEENVS]
                                  [--may-create-code-envs MAYCREATECODEENVS]
                                  [--may-write-unsafe-code MAYWRITEUNSAFECODE]
                                  [--may-write-safe-code MAYWRITESAFECODE]
                                  [--may-create-projects MAYCREATEPROJECTS]
                                  [--may-manage-udm MAYMANAGEUDM]
                                  [--may-edit-lib-folders MAYEDITLIBFOLDERS]
                                  [--may-develop-plugins MAYDEVELOPPLUGINS]
                                  [--may-create-authenticated-connections MAYCREATEAUTHENTICATEDCONNECTIONS]
                                  key

The ``--admin`` flag and all of the ``--may-xxx`` flags take "true" or "false" as argument, and refer to one of the global permissions as detailed in :doc:`/security/permissions`

api-key-delete
----------------

Deletes a global API key

.. code-block:: bash 
    
    api-key-delete [-h] key

Jobs-related commands
======================

These commands are used to trigger, list and abort jobs and scenarios

jobs-list
----------

Lists jobs for a given project, both running ones and past ones

.. code-block:: bash

	dsscli jobs-list [-h] [--output OUTPUT] [--no-header] project_key

Returns a list like:

=========================================                 =======  ==============
Job id                                                    State    From scenario
=========================================                 =======  ==============
Build_dataset1_2017-10-25T13-05-23.615                    RUNNING
Build_dataset1_2017-10-25T13-05-23.615                    FAILED
Build_dataset1_2017-10-25T12-45-32.864                    FAILED
Build_Other_2017-10-25T12-43-31.463                       DONE
=========================================                 =======  ==============

build
------

Runs a DSS job to build one or several datasets, saved models or managed folders

.. code-block:: bash

    build [-h] [--output OUTPUT] [--no-header] [--wait]
                         [--mode MODE] [--dataset DATASET [DATASET ...]]
                         [--folder FOLDER] [--model MODEL]
                         project_key

Specifying outputs to build
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

To build "dataset1" and "dataset2" in project "PROJECT1", run: ``dsscli build PROJECT1 --dataset dataset1 --dataset dataset2``

* For partitioned datasets, use the following syntax: ``dsscli build PROJECT1 --dataset dataset1 partition1``
* For multiple partitions, use the regular partition specification syntax:

	* ``dsscli build PROJECT1 --dataset dataset1 FR,EN``
	* ``dsscli build PROJECT1 --dataset dataset1 2017-01-02/2017-01-14``
	* ``dsscli build PROJECT1 --dataset dataset1 2017-01-02/2017-01-14|FR,2017-01-02/2017-01-30|EN``

Build modes
%%%%%%%%%%%%

Use --mode to switch between the different build modes of the DSS flow. The argument must be one of:

* RECURSIVE_BUILD,
* NON_RECURSIVE_FORCED_BUILD
* RECURSIVE_FORCED_BUILD
* RECURSIVE_MISSING_ONLY_BUILD

Other
%%%%%%

The --wait argument makes dsscli wait for the end of the job (either success or failure) before returning. If the job fails or is aborted, dsscli returns with a non-zero exit code.

If not waiting, dsscli prints the new job id

job-abort
----------

Aborts a running job

.. code-block:: bash 

	dsscli job-abort [-h] project_key job_id

The job_id is the first column returned by the ``dsscli jobs-list`` command

job-status
-----------

Gets the status of a job

.. code-block:: bash

    dsscli job-status [-h] [--output OUTPUT] [--no-header]
                              project_key job_id


Scenarios-related commands
===========================

scenarios-list
---------------

Lists scenarios of a project

.. code-block:: bash

    dsscli scenarios-list [-h] [--output OUTPUT] [--no-header]
                                  project_key

scenario-runs-list
-------------------

Lists previous and current runs of a scenario

.. code-block:: bash

    dsscli scenario-runs-list [-h] [--output OUTPUT] [--no-header]
                                      [--limit LIMIT] [--only-finished-runs]
                                      project_key scenario_id

* ``--only-finished-runs`` limits output to runs that are finished (either succeeded, failed or was aborted)
* ``--limit`` limits the number of returned runs. Default is 10

scenario-run
------------

Runs a scenario

.. code-block:: bash

    dsscli scenario-run [-h] [--output OUTPUT] [--no-header] [--wait]
                                [--no-fail] [--params RUN_PARAMS]
                                project_key scenario_id

If the scenario was already running, the run is cancelled, and a flag is returned in the output

If ``--wait`` is passed, command waits for the scenario to be complete and fails if the scenario fails, except if ``--no-fail`` is passed. It also fails if the run is cancelled because the scenario was already running

``--params`` is an optional file containing run parameters as a JSON dict. Use '-' for stdin

scenario-abort
---------------

.. code-block:: bash

    dsscli scenario-abort [-h] project_key scenario_id

Aborts the current run of a scenario, if any. Does not fail if the scenario was not running

Projects-related commands
===========================

projects-list
--------------

Lists all project keys and names. For example:

.. code-block:: bash 

    ./bin/dsscli projects-list

.. list-table::
   :widths: 20 20 
   :header-rows: 1

   * - Project key
     - Name
   * - DKU_HAIKU_STARTER
     - Haiku Starter for Administrator


project-export
--------------

Exports a project as zip archive to the specified path. Set the optional flags to modify export options.

.. code-block:: bash

    project-export [-h] [--uploads] [--no-uploads]
                                  [--managed-fs] [--no-managed-fs]
                                  [--managed-folders] [--no-managed-folders]
                                  [--input-managed-folders]
                                  [--no-input-managed-folders]
                                  [--input-datasets] [--no-input-datasets]
                                  [--all-datasets] [--no-all-datasets]
                                  [--analysis-models] [--no-analysis-models]
                                  [--saved-models] [--no-saved-models]
                                  project_key path

    positional arguments:
      project_key           Project key to export
      path                  Target archive path


Example:

.. code-block:: bash 

    ./bin/dsscli project-export DKU_HAIKU_STARTER DKU_HAIKU_STARTER.zip

    Exporting with options: {"exportManagedFolders": false, "exportAllDatasets": false, "exportManagedFS": false, "exportAllInputDatasets": false, "exportUploads": true, "exportAnalysisModels": true, "exportSavedModels": true, "exportAllInputManagedFolders": false} 


project-import
---------------

Import a project from project zip file.

.. code-block:: bash 

    project-import [-h] [--project-key PROJECT_KEY]  [--remap-connection OLD_CONNECTION=NEW_CONNECTION] path

        positional arguments:
          path                  Source archive path

        optional arguments:
          --project-key PROJECT_KEY
                                Override project key
          --remap-connection OLD_CONNECTION=NEW_CONNECTION
                                Remap a connection

In this example my imported project will have the project key ``IMPORTED_PROJECT``. Example:

.. code-block:: bash 

     ./bin/dsscli project-import --project-key=IMPORTED_PROJECT --remap-connection filesystem-managed=limited-filesystem MY_PROJECT.zip 
    Uploading archive ...
    Importing ...
    Import successful



project-delete
---------------

Delete a project. Returns nothing on success.

.. code-block:: bash 

    project-delete [-h] project_key

    positional arguments:
      project_key  Project key of project to delete
      
Example: 

.. code-block:: bash 

    ./bin/dsscli project-delete DKU_HAIKU_STARTER


bundle-export (Design node only)
----------------------------------------

Creates a new bundle for the specified project. If the ``bundle_id`` already exists for the project, you will receive an error. 

.. code-block:: bash 

    bundle-export [-h] project_key bundle_id

    positional arguments:
      project_key  Project key for which to export a bundle
      bundle_id    Identifier of the bundle to create

.. code-block:: bash 

    ./bin/dsscli bundle-export DKU_HAIKU_STARTER v1
    Start exporting bundle v1 ...
    Export completed


bundles-list-exported (Design node only)
------------------------------------------

Returns a table of bundle ids for the specified project.  If ``--with-data`` is specified, the full export manifest will be returned in JSON array format. 

.. code-block:: bash 

    bundles-list-exported [-h] [--with-data] project_key

    positional arguments:
      project_key           Project key for which to list bundles

    optional arguments:
      --with-data           Retrieve full information for each bundle

Example: 

.. code-block:: bash 

    ./bin/dsscli bundles-list-exported DKU_HAIKU_STARTER
    Bundle id
    -----------
    v1
    v2
    v3


bundle-download-archive (Design node only)
--------------------------------------------

Downloads a bundle as a zip file. 

.. code-block:: bash 

    bundle-download-archive [-h] project_key bundle_id path

    positional arguments:
      project_key  Project key for which to export a bundle
      bundle_id    Identifier of the bundle to create
      path         Target file (- for stdout)

Example: 

.. code-block:: bash 

    ./bin/dsscli bundle-download-archive DKU_HAIKU_STARTER v1 dku_haiku_bundle_v1.zip


project-create-from-bundle (Automation node only)
--------------------------------------------------

Creates a project on the Automation node based on a project bundle archive generated from the Design node. 

.. code-block:: bash 

    project-create-from-bundle archive_path

    positional arguments:
      archive_path          Archive path

Example: 

.. code-block:: bash 

    ./bin/dsscli project-create-from-bundle ../DESIGN_DATADIR/dku_haiku_bundle_v1.zip 
    
    Project key
    -----------------
    DKU_HAIKU_STARTER


bundles-list-imported (Automation node only)
--------------------------------------------------

Lists all bundles per project on the automation node. If ``--with-data`` is specified, the full export manifest in JSON array format for each bundle is returned.

.. code-block:: bash 

    bundles-list-imported [-h] project_key

    positional arguments:
      project_key           Project key for which to list bundles

Example:

.. code-block:: bash 

    ./bin/dsscli bundles-list-imported DKU_HAIKU_STARTER
    
    Bundle id
    -----------
    v1


bundle-import  (Automation node only)
--------------------------------------------------

Imports a bundle on the automation node from a zip file archive. If project does not already exist, use ``project-create-from-bundle``. 

.. code-block:: bash 

     bundle-import [-h] project_key archive_path

     positional arguments:
       project_key           Project key for which to import a bundle
       archive_path          Archive path

Example:

.. code-block:: bash 

    ./bin/dsscli bundle-import DKU_HAIKU_STARTER ~/DESIGN_DATADIR/dku_haiku_bundle_v1.zip
    
    Project key          Bundle id
    -------------------  -----------
    DKU_HAIKU_STARTER    v1

    
bundle-activate (Automation node only)
--------------------------------------------------

Activates a bundle on the automation node. Connection and code environment re-mappings should happen prior to activation. 

.. code-block:: bash 

    bundle-activate [-h] project_key bundle_id

    positional arguments:
      project_key  Project key for which to activate a bundle
      bundle_id    Identifier of the bundle to activate

Example: 

.. code-block:: bash 

    ./bin/dsscli bundle-activate DKU_HAIKU_STARTER v1
    {
      "aborted": false, 
      "unknown": false, 
      "alive": false, 
      "runningTime": 0, 
      "hasResult": true, 
      "result": {
        "neededAMigration": false, 
        "anyMessage": false, 
        "success": false, 
        "messages": [], 
        "warning": false, 
        "error": false, 
        "fatal": false
      }, 
      "startTime": 0
    }

Datasets related commands
==========================

datasets-list
--------------

Lists the Project key, Name and Type for all datasets in a specified project.

.. code-block:: bash

    datasets-list [-h] project_key

    positional arguments:
      project_key           Project key for which to list datasets


Example:

.. code-block:: bash 

    ./bin/dsscli datasets-list DKU_HAIKU_STARTER

.. list-table::
   :widths: 20 20 20
   :header-rows: 1

   * - Project key
     - Name
     - Type
   * - DKU_HAIKU_STARTER
     - Orders
     - FilesInFolder


dataset-schema-dump
--------------------

Outputs the Name, Type, Meaning and Max. length for all columns in a dataset schema. Meaning and Max. length will only be returned if they were modified from the default.

.. code-block:: bash 

    dataset-schema-dump [-h] project_key name

    positional arguments:
      project_key           Project key of the dataset
      name                  Dataset for which to dump the schema


Example:

.. code-block:: bash 
    
    ./bin/dsscli dataset-schema-dump DKU_HAIKU_STARTER Orders

The output would look like:

.. list-table::
   :widths: 30 20 20 20
   :header-rows: 1

   * - Name
     - Type
     - Meaning
     - Max. length
   * - tshirt_quantity
     - bigint
     - Integer
     - 200


dataset-list-partitions
------------------------

Lists all partition values for a specified dataset. 

.. code-block:: bash 
    
    dataset-list-partitions [-h] project_key name

    positional arguments:
      project_key           Project key of the dataset
      name                  Dataset for which to list partitions

For example, for a dataset with two partitions ``puchase_date`` and ``merchant_id``, the output would look like:

.. list-table::
   :widths: 30 20 
   :header-rows: 1

   * - purchase_date
     - merchant_id
   * - 2020-12-15
     - 437


dataset-clear
--------------

Clears the specified dataset and partition, if specified.

.. code-block:: bash 

    dataset-clear [-h] [--partitions PARTITIONS] project_key name

    positional arguments:
      project_key           Project key of the dataset
      name                  Dataset to clear

    optional arguments:
      --partitions PARTITIONS List of partitions to clear

Example:

.. code-block:: bash 
    
    ./bin/dsscli dataset-clear DKU_HAIKU_STARTER Orders_enriched


dataset-delete
------------------

Deletes the specified dataset.

.. code-block:: bash 

    dataset-delete [-h] project_key name

    positional arguments:
      project_key  Project key of the dataset
      name         Dataset to delete

Example: 

.. code-block:: bash 

    ./bin/dsscli dataset-delete DKU_HAIKU_STARTER Orders_enriched


Managed folders related commands
=================================

managed-folders-list
---------------------

Lists all managed folders for the specified project. 

.. code-block:: bash 
    
    managed-folders-list [-h] project_key

    positional arguments:
      project_key           Project key of the managed folders

Example:

.. code-block:: bash 

    ./bin/dsscli managed-folders-list DKU_HAIKU_STARTER

.. list-table::
   :widths: 20 20 30
   :header-rows: 1

   * - Name
     - Type
     - Id
   * - Orders
     - Filsystem
     - O2ue6CX3

managed-folder-list-contents
------------------------------

Lists the contents of a particular managed folder. ``managed_folder_id`` is the ``Id`` returned in a call to ``managed-folders-list``.

.. code-block:: bash 

    managed-folder-list-contents [-h] project_key managed_folder_id

    positional arguments:
      project_key           Project key of the managed folders
      managed_folder_id     Managed folder id

Example:

.. code-block:: bash 

    ./bin/dsscli managed-folder-list-contents DKU_HAIKU_STARTER O2ue6CX3

.. list-table::
   :widths: 30 20 40
   :header-rows: 1

   * - Path
     - Size
     - Last Modified
   * - /orders_2017-01.csv
     - 40981
     - 2021-01-25T18:49:48+00:00


managed-folder-get-file
------------------------------

Allows you to download a specified file from a managed folder to your server. If no ``--output-file`` is specified, the contents of the ``file_path`` file will be output to the console. 

.. code-block:: bash 

    managed-folder-get-file [-h] [--output-file OUTPUT_FILE] project_key managed_folder_id file_path

    positional arguments:
      project_key           Project key of the managed folders
      managed_folder_id     Managed folder id
      file_path             File path


    optional arguments:
      --output-file OUTPUT_FILE
                            Path to output file

Example: 

.. code-block:: bash 

    ./bin/dsscli managed-folder-get-file DKU_HAIKU_STARTER O2ue6CX3 orders_2017-01.csv --output-file my_local_orders.csv


Connections-related commands
=============================

connections-list
------------------

Lists all connections with their type and flags, like this: 

.. code-block:: bash 

    ./bin/dsscli connections-list

.. list-table::
   :widths: 15 10 10 10 10 10 
   :header-rows: 1

   * - Name
     - Type
     - Allow write
     - Allow managed datasets
     - Usable by
     - Credentials mode
   * - filesystem_managed
     - Filsystem
     - True
     - True
     - ALLOWED
     - GLOBAL
     

Code env related commands
=============================

code-envs-list
------------------

Lists the Name, Language and Type of all code environments.

Example:

.. code-block:: bash 

    ./bin/dsscli code-envs-list

.. list-table::
   :widths: 20 20 30
   :header-rows: 1

   * - Name
     - Language
     - Type
   * - python36
     - PYTHON
     - DESIGN_MANAGED
     

code-env-update
------------------

Allows you to perform an "update" for a particular code environment. If the ``--force-rebuild-env`` flag is included, it will clear the code environment and rebuild it from scratch. Nothing is returned on success. 

.. code-block:: bash 

    code-env-update [-h] [--force-rebuild-env] lang name

    positional arguments:
      lang                 Language of code env to update
      name                 Name of code env to update

    optional arguments:
      --force-rebuild-env  Force rebuilding of the code env
      
In this example ``PYTHON`` is the language and ``python36`` is the code environment name. Example:

.. code-block:: bash 

    ./bin/dsscli code-env-update PYTHON python36 --force-rebuild-env


API services related commands
==============================

api-services-list
-----------------

Lists all API services per project. 

.. code-block:: bash 

    api-services-list [-h] project_key

Returns a list of service Ids, Endpoints and Public flags. Example:

.. code-block:: bash 

    ./bin/dsscli api-services-list DKU_HAIKU_STARTER

.. list-table::
   :widths: 30 20 50
   :header-rows: 1

   * - Id
     - Public?
     - Endpoints
   * - Tutorial_Deployment
     - Yes
     - High_Revenue_Customers (STD_PREDICTION)


api-service-package-create
---------------------------

Creates a package for an API service based on a project and service_id, which is the same as the ``Id`` returned from the ``api-services-list`` call. If no ``--name`` is specified, the version number will automatically be set to the next package version number available for the service.  If no ``--path`` is specified, the package will be downloaded to your current directory. 

.. code-block:: bash 

    api-service-package-create [-h] [--name NAME] [--path PATH]  project_key service_id

    positional arguments:
      project_key  Project key containing service
      service_id   API service to package

    optional arguments:
      --name NAME  Name for the package (default: auto-generated)
      --path PATH  Path to download the package to (default: current directory)

Examples:

.. code-block:: bash 

    ./bin/dsscli api-service-package-create DKU_HAIKU_STARTER Tutorial_Deployment
    Downloading package to v3.zip

    ./bin/dsscli api-service-package-create DKU_HAIKU_STARTER Tutorial_Deployment --name v7 --path /Users/ssinick/Documents/
    Downloading package to /Users/ssinick/Documents/v7.zip


Code studio templates related commands
======================================

code-studio-templates-list
--------------------------

Lists the ids and names of all code studio templates.

Example:

.. code-block:: bash 

    ./bin/dsscli code-studio-templates-list

.. list-table::
   :widths: 30 30
   :header-rows: 1

   * - Id
     - Label
   * - streamlit
     - Streamlit
     
code-studio-templates-build
---------------------------

Allows you to re-build images of your code studio templates. 

.. code-block:: bash 

    code-studio-templates-build [-h] [template_ids ...]

    optional argument:
      template_ids  The template ids, separated by a space, that you want to rebuild. By default, all templates are rebuilt.

In this example, we want to rebuild the code studio template with the id "streamlit":

.. code-block:: bash 

    ./bin/dsscli code-studio-templates-build streamlit
    > Building 1 code studio templates
    > Building streamlit ..... done
    > 1 successfully built, 0 failed


Controlling dsscli output
==========================

All dsscli commands that display results take two additional arguments:

* ``--no-header`` removes column headers from display to make them easier to parse (each line of the output directly corresponds to one data item)

* ``--output json`` to format output as JSON for machine consumption (the default is ``--output fancy``)
