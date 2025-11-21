Partitioned SQL recipes
#########################

This page deals with the specific case of partitioned datasets in SQL recipes. For general information about SQL recipes, see :doc:`/code_recipes/sql`


Reading from partitioned datasets
====================================

In SQL recipes (both "query" and "script"), reading partitioned datasets requires that you manually restrict what is being read in your query.

For example, if you have a dataset "inp1" partitioned by "country" (a "discrete values" partitioning dimension), you want to write a query like that:

.. code-block:: sql

	SELECT col1, COUNT(*) AS count FROM inp1
		WHERE country = 'the partition I want to read'
		GROUP BY col1;

The partition(s) that you want to read is determined by the partition dependencies system and should not be hard-coded in your recipe. Instead, you should use :doc:`variables`. In our previous example, you would actually write your query as:

.. code-block:: sql

	SELECT col1, COUNT(*) AS count FROM inp1
		WHERE country = '$DKU_SRC_country'
		GROUP BY col1;


Writing into partitioned datasets (SQL query, writing to column-based partitioned)
==================================================================================

This case applies if:

* You are using an SQL Query recipe
* You are writing to an SQL table dataset (or another column-based-partitioning dataset, like Cassandra or MongoDB)

In this case, the partitioning columns *must* appear in the output data.
Note that it must appear in the SQL query at the correct position wrt. the output schema and with the correct name.

For example, reusing our previous example, we are going to write the result of the query to a dataset "out1",
which is partitioned by "country2".

The schema of out1 looks like:

* country2
* col1
* count

The query could look like:

.. code-block:: sql

	SELECT country as country2, col1, COUNT(*) as count FROM inp1
		WHERE country = '$DKU_SRC_country'
		GROUP BY col1;

However, this only works in the case where we have a "equals" dependency, because we are actually writing the country of the *input* dataset as the country2 of the *output* dataset.

If we wanted to write in another partition, it would not work. In the more general case, we need to write the following:

.. code-block:: sql

	SELECT '$DKU_DST_country2' as country2, col1, COUNT(*) as count FROM inp1
		WHERE country = '$DKU_SRC_country'
		GROUP BY col1;

The DKU_DST variable is replaced by the value of the "country2" dimension for the output dataset. For more information, see :doc:`variables`.


Writing into partitioned datasets (SQL query, writing to file-based partitioned)
==================================================================================

This case applies if:

* You are using an SQL Query recipe.
* You are NOT writing to an SQL table dataset in the same connection

Remember (as explained in :doc:`/code_recipes/sql`) that in that specific case, DSS retrieves the rows from the query and writes them in the output dataset. In that case, DSS "controls" how data is written and handles all partitioning issues. (see :doc:`/partitions/recipes` for more details).

As you are writing to a files-based partitioned dataset, you *do not need to do anything specific* in the SQL query about the output partitioning values. DSS will write to the correct folder automatically.


Writing into partitioned datasets (SQL script)
==============================================

When you write with an SQL script recipe, you are responsible for:

* ensuring idempotence (running the script several times produces the same output as running it once)
* inserting records with the correct partitioning values.

This generally involves:

* Performing a DELETE query with a restriction on the target partitioning value (or, if you are using native partitioning, using the correct database-specific commands to drop a partition)

* Making sure that inserted records have their partitioning columns values set to the target partitioning value.

To help you, Dataiku DSS provides you with many variables that you can substitute in your SQL scripts.  See :doc:`variables`.

