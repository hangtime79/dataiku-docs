.. _visual-recipes-upsert:

Upsert: Consolidate data
########################

.. contents::
	:local:


Upsert is a term coined by blending "update" and "insert", and the operation is often handled in SQL databases by a "MERGE INTO" verb. The operation's goal is to take rows in, and perform two different operations at the same time:

- if the row already exists in the output, update the values of the row in the output with the values of the incoming row (UPDATE mode)
- if the row doesn't yet exists in the output, add the incoming row to the output (INSERT mode)

Since no row deletion occurs in the output, the net effect of an upsert is that you consolidate incoming rows into one single output dataset. 

.. note::

    This capability is provided by the "upsert-recipe" plugin, which you need to install. Please see :doc:`/plugins/installing`.

    This plugin is :doc:`not supported </troubleshooting/support-tiers>`.


Upsert keys
-----------

The upsert operation needs to map each row in the input and output dataset to some unique entity. This is done by specifying a subset of the columns to act as a unique key.


Example
-------

Let's say you regularly have data files for customers, one row per customer, but only for customers that were added or for which some piece of information was modified since last time. Each customer is identified by some `customer_id` key. Starting from an empty output dataset, an upsert recipe would then behave like:

1. First run (add customer 1 and 2), with input:


.. list-table:: 
   :widths: 50 50 50
   :header-rows: 1

   * - customer_id
     - name
     - rating
   * - 1
     - Bob
     - 3
   * - 2
     - Alice
     - 1


The output after run is:


.. list-table:: 
   :widths: 50 50 50
   :header-rows: 1

   * - customer_id
     - name
     - rating
   * - 1
     - Bob
     - 3
   * - 2
     - Alice
     - 1


2. Second run (modify customer 2, add customer 3), with input:


.. list-table:: 
   :widths: 50 50 50
   :header-rows: 1

   * - customer_id
     - name
     - rating
   * - 2
     - Alicia
     - 1
   * - 3
     - Daphne
     - 2


The output after run is:


.. list-table:: 
   :widths: 50 50 50
   :header-rows: 1

   * - customer_id
     - name
     - rating
   * - 1
     - Bob
     - 3
   * - 2
     - Alicia
     - 1
   * - 3
     - Daphne
     - 2


3. Third run (modify customer 1) with input:


.. list-table:: 
   :widths: 50 50 50
   :header-rows: 1

   * - customer_id
     - name
     - rating
   * - 1
     - Bob
     - 999


The output after run is:


.. list-table:: 
   :widths: 50 50 50
   :header-rows: 1

   * - customer_id
     - name
     - rating
   * - 1
     - Bob
     - 999
   * - 2
     - Alicia
     - 1
   * - 3
     - Daphne
     - 2



Engines
=======

Depending on the input dataset types, DSS will adjust the engine it uses to execute the recipe, and choose between Hive, Impala, SparkSQL, plain SQL, and internal DSS. The available engines can be seen and selected by clicking on the cog below the "Run" button.

When the engine is SQL, DSS can offer several modes of operation depending on the type of underlying database:

- "direct upsert statement": many SQL databases can handle upsert recipes "natively", usually with a MERGE INTO verb, sometimes with a special handling of rejections to an INSERT INTO because of a unique constraint
- "update then insert": issue 2 SQL statements to the database, one to update rows already present in the output dataset, then one to add new rows. This mode doesn't use a temporary table
- "prepare upserted then replace output": a temporary table is prepared, with existing rows and new rows, and the output dataset is cleared then replaced by this temporary table. This is the most generic mode, but also the slowest, and it requires being able to make a temporary table


Notes
=====

- at least one upsert key is required to identify rows
- DSS does not enforce or control the unicity of rows in the input or output dataset. If several rows have the same combination of values for the upsert keys, the behavior is undefined

