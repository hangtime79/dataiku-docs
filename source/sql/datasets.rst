SQL datasets
##################

You can interact with SQL databases using:

.. contents::
    :local:

.. _external-table-datasets:

External table datasets
=========================

SQL table datasets are the simplest form of interaction with SQL databases. To create an external SQL table dataset, you simply need to choose the connection, the table, and you’re all set. The content of the table is now a dataset.

* Go to Datasets, click New > Your database type
* Select a connection.
* Make sure the « Read a database table » radio is selected.
* Click on "Get tables list"
* DSS connects to your database and retrieves the available tables.
* Select your table.
* Click the "Test table" button.
* DSS shows a preview of the contents.
* You can now save your dataset

.. warning::
	You cannot edit the schema of an external SQL table dataset. The names of the columns are provided by the database engine.

	On an external dataset, DSS chooses to preferably trust the content of the data.

	If you need to edit the names of the columns for further processing, you can for example use a data preparation recipe.

	When creating an external MySQL table dataset, upcast the types of the columns with unsigned integer types in the dataset schema, so that DSS's representation covers the full range of the values in these columns (use 'smallint' for 'tinyint unsigned', 'int' for 'smallint unsigned', 'bigint' for 'int unsigned'). As MySQL silently casts unsigned values to signed ones in queries, and DSS treats integer types as signed, it is advised to avoid unsigned integers.

.. _external-query-datasets:

External query datasets
========================

A SQL dataset can also be defined by a custom query. The results of the query become the rows of the dataset.
This allows you to create a virtual dataset, without having to materialize the rows (for example, if the query joins several tables).

A SQL query database is read-only. You cannot write to a SQL query.

.. note::
	Data Science Studio does not automatically test SQL queries, as they can be very expensive. You need to manually click the **Test query** button

.. _managed-sql-datasets:

Managed SQL datasets
=====================

Managed datasets can be created on SQL databases. Only "table" datasets can be managed (it makes no sense to write on a SQL query dataset).

You can create a managed SQL dataset:

* by clicking on the **Managed dataset** button in the New Dataset page
* by creating a new managed dataset as output of a recipe

When you create a managed SQL dataset, you start by selecting the connection in which it gets written. A table name is automatically selected based on the name of the SQL dataset. You can change it. A managed SQL dataset can target either an existing table or a non-existing one.

When you click the **Test** button, Dataiku DSS checks if the table exists in the database:

* If the table does not exist, then you have the ability to create it. You can choose not to create the table, and any recipe that requires it would automatically create the table.

* If the table exists, DSS automatically checks its schema. DSS warns you if the schema of the table and the dataset do not match, and suggests these fixes:
	* Drop the table (so it will be recreated with the dataset schema)
	* Override the dataset schema with the current schema of the table.

It is good practice to ensure that the settings of the managed datasets are relocatable. See :doc:`../connecting/relocation` for more details.
