Making relocatable managed datasets
#####################################

When you create a :ref:`managed dataset <managed-datasets>`, you choose a connection in which to create this managed dataset.

DSS automatically chooses the settings of this new managed dataset within its connection. For example, by default, if you create a managed dataset ``ds1`` into a SQL connection ``myconn``, DSS will configure ``ds1`` with ``ds1`` (ie the dataset name) as table name. Similarly, DSS will use the name of the dataset in the path when creating a managed Filesystem or HDFS dataset.

It is a good practice to make sure that the settings of the managed datasets (SQL table names, paths) are *relocatable*. This means that we want them to have the following properties:

* If we create two datasets with the same name in different projects, their storage settings don't overlap.
* If we duplicate a project within a DSS instance, their storage settings don't overlap.
* If we import a project into an existing DSS instance, the storage settings of the new project don't overlap with existing projects.

The main instrument in ensuring relocatability of datasets is the usage of *variables* within storage settings. Variables are defined at the project level and can be defined such as having a different value for each project. In particular, the ``${projectKey}`` variable is automatically defined as the project key of the current project and is thus guaranteed to be different for each project.

For example, if the default path for a dataset named ``ds1`` is configured to be ``/${projectKey}_ds1``, it guarantees that if this dataset is copied to another project, its storage path won't overlap.

Relocatability settings are configured in each connection. These settings only apply to newly created HDFS datasets. Once a dataset has been created, relocatability settings don't apply anymore.

Relocation of SQL datasets
===========================

For SQL datasets, in the settings of the connection, you can configure (with variables):

* For the table name, a prefix and a suffix to the dataset name
* The database schema name

For example, with:

* Schema: ``${projectKey}`` (Please note: DSS can't create missing schema so make sure the schemas are created accordingly beforehand)
* Table name prefix: ``${myvar1}_``
* Table name suffix: ``_dss``

If you go to project ``P1`` (where ``myvar1 = a2``) and create a managed dataset called ``ds1`` in this connection, it will be stored in schema ``P1`` and the table will be called ``a2_ds1_dss``

Relocation of HDFS datasets
=============================

For HDFS datasets, in the settings of the connection, you can configure (with variables):

* For the path (within the connection), a prefix and a suffix to the dataset name
* For the associated Hive table (see :doc:`/hadoop/hive`):
	* for the table name, a prefix and a suffix to the dataset name
	* the Hive database

For example, with:

* Path prefix: ``${projectKey}/``
* Path suffix: ``test``
* Table name prefix: ``${myvar1}_``
* Table name suffix: ``_dss``
* Hive database ``${projectKey}_dss``

If you go to project ``P1`` (where ``myvar1 = a2``) and create a managed dataset called ``ds1`` in this connection, it will be stored in path ``P1/ds1`` and the associated Hive table will be in database ``P1_dss`` with table name ``a2_ds1_dss``
