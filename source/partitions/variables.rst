Partitioning variables substitutions
#######################################

When a recipe involves partitioned datasets, some variables are made available to the code that you write for this recipe, to help you manage partitions.

Substituting variables
========================

SQL
-------------

Variables are replaced in your code using the $VARIABLE_NAME syntax. For example, if you have the following code:

.. code-block:: sql

	SELECT * from mytable WHERE condition='$DKU_DST_country';

with a variable DKU_DST_country which has value France, the following query will actually be executed:

.. code-block:: sql

	SELECT * from mytable WHERE condition='France';

Hive
-----

Variables are replaced in your code using the ${hiveconf:VARIABLE_NAME} syntax. For example, if you have the following code:


.. code-block:: sql

	SELECT * from mytable WHERE condition='${hiveconf:DKU_DST_date}';

with a variable DKU_DST_date which has value 2020-12-21, the following query will actually be executed:

.. code-block:: sql

	SELECT * from mytable WHERE condition='2020-12-21';

Python
-------

Since read and write is done through Dataiku DSS, you don't need to specify the source or destination partitions in your code for that, using "get_dataframe()" will automatically give you only the relevant partitions.

For other purposes than reading/writing dataframes, all variables are available in a dictionary called dku_flow_variables in the dataiku module. Example:

.. code-block:: py

	import dataiku
	print("I am working for year %s" % (dataiku.dku_flow_variables["DKU_DST_YEAR"]))

R
--

Flow variables are retrieved using the ``dkuFlowVariable(variableName)`` function

.. code-block:: R

	library(dataiku)
	dkuFlowVariable("DKU_DST_country")


Available variables
=====================

Related to the target datasets
--------------------------------

+-------------------------+---------------+--------------------------------------------+--------------+
|      Variable name      |  Available if |                   Value                    |   Examples   |
+=========================+===============+============================================+==============+
| DKU_DST_dimensionName   | For each      | Value of the dimension "dimensionName"     | * France     |
|                         | dimension     | for the current activity.                  | * 2020-01-22 |
|                         |               |                                            |              |
|                         |               | For time dimensions,                       |              |
|                         |               | given using time partition                 |              |
|                         |               | identifier syntax.                         |              |
+-------------------------+---------------+--------------------------------------------+--------------+
| DKU_DST_YEAR            | time          | Value of the year (4 digits) for the       | 2020         |
|                         | partitioned   | time dimension.                            |              |
+-------------------------+---------------+--------------------------------------------+--------------+
| DKU_DST_MONTH           | time          | Value of the month (2 digits, from)        | 01           |
|                         | partitioned   | 01 to 12) for the time dimension           |              |
|                         | (month, day   |                                            |              |
|                         | or hour)      |                                            |              |
+-------------------------+---------------+--------------------------------------------+--------------+
| DKU_DST_DAY             | time          | Value of the day of month (2 digits,       | 22           |
|                         | partitioned   | from 01 to 31) for the time                |              |
|                         | (day or hour) | dimension                                  |              |
+-------------------------+---------------+--------------------------------------------+--------------+
| DKU_DST_DATE            | time          | Date for the time dimension, in            | 2020-01-22   |
|                         | partitioned   | yyyy-MM-dd format                          |              |
|                         | (day or hour) |                                            |              |
+-------------------------+---------------+--------------------------------------------+--------------+
| DKU_DST_HOUR            | time          | Value of the hour of day (2 digits, from)  | 21           |
|                         | partitioned   | 00 to 23) for the time dimension.          |              |
|                         | (hour)        |                                            |              |
+-------------------------+---------------+--------------------------------------------+--------------+
| DKU_DST_YEAR_1DAYAFTER  | the same      | Value of the various date components       | 2020-01-23   |
| ...                     | variable is   | variables for the day FOLLOWING the        |              |
|                         | available     | dimension value.                           |              |
+-------------------------+---------------+--------------------------------------------+--------------+
| DKU_DST_YEAR_1DAYBEFORE | the same      | Value of the various date components       | 2020-01-21   |
|                         | variable is   | for the day PRECEDING the dimension value  |              |
|                         | available     |                                            |              |
+-------------------------+---------------+--------------------------------------------+--------------+
| ... _7DAYSBEFORE        | Idem          | Value of the various date components       | 2020-01-15   |
| ... _7DAYSAFTER         |               | for the date 7 days PRECEDING or FOLLOWING |              |
|                         |               | the dimension value                        |              |
+-------------------------+---------------+--------------------------------------------+--------------+
| ... _1HOURBEFORE        | Idem          | Idem                                       |              |
| ... _1HOURAFTER         |               |                                            |              |
+-------------------------+---------------+--------------------------------------------+--------------+

Related to the source datasets
-------------------------------

+-----------------------------------+-------------------------------------------------------+------------------+------------+
|           Variable name           |                      Available if                     |      Value       |  Examples  |
+===================================+=======================================================+==================+============+
| DKU_SRC_datasetName_dimensionName | * For each dimension of each dataset                  | The value of the | 2020-01-23 |
|                                   |                                                       | dimension        |            |
|                                   |                                                       | dimensionName    |            |
|                                   | * There is only one source partition for this dataset | for input        |            |
|                                   |                                                       | dataset          |            |
|                                   |                                                       | datasetName      |            |
+-----------------------------------+-------------------------------------------------------+------------------+------------+
| DKU_SRC_dimensionName             | * There is only one source dataset                    | The value of     | 2020-01-23 |
|                                   |                                                       | the dimension    |            |
|                                   |                                                       | dimensionName    |            |
|                                   | * There is only one source partition for this dataset | for the single   |            |
|                                   |                                                       | input dataset    |            |
|                                   |                                                       |                  |            |
|                                   |                                                       |                  |            |
+-----------------------------------+-------------------------------------------------------+------------------+------------+
| DKU_PARTITION_FILTER_datasetName  | * the recipe is an SQL recipe                         | filter for the   |            |
|                                   |                                                       | partitions used  |            |
|                                   |                                                       | by the recipe    |            |
|                                   |                                                       |                  |            |
+-----------------------------------+-------------------------------------------------------+------------------+------------+
| DKU_PARTITION_FILTER              | * the recipe is an SQL recipe                         | filter for the   |            |
|                                   |                                                       | partitions used  |            |
|                                   | * There is only one source dataset                    | by the recipe    |            |
|                                   |                                                       |                  |            |
+-----------------------------------+-------------------------------------------------------+------------------+------------+
| DKU_SRC_FIRST_DATE                | * There is only one source dataset                    | smallest         |            |
|                                   |                                                       | partition id     |            |
|                                   | * The dataset is time-partitioned                     |                  |            |
|                                   |                                                       |                  |            |
+-----------------------------------+-------------------------------------------------------+------------------+------------+
| DKU_SRC_LAST_DATE                 | * There is only one source dataset                    | biggest          |            |
|                                   |                                                       | partition id     |            |
|                                   | * The dataset is time-partitioned                     |                  |            |
|                                   |                                                       |                  |            |
+-----------------------------------+-------------------------------------------------------+------------------+------------+


Additionally, if the source dataset has time dimensions, all variables DKU_SRC_datasetName (date/year/month/day/hour), DKU_SRC_datasetName (DATE/YEAR/MONTH/DAY/HOUR)_(timeshift) will be available subject to the same rules as for DKU_DST _

If there is only one input dataset, all DKU_SRC_datasetName_variable variables are also available in the DKU_SRC_variable shortcut.

..  LocalWords:  sql mytable dataiku dimensionName yyyy DAYAFTER DAYBEFORE
..  LocalWords:  DAYSBEFORE DAYSAFTER HOURBEFORE HOURAFTER datasetName
