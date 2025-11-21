Usage of Spark in DSS
######################

When Spark support is enabled in DSS, a large number of components feature additional
options to run jobs on Spark.

SparkSQL recipes
====================

SparkSQL recipes globally work like :doc:`SQL Recipes </code_recipes/sql>` but
are not limited to SQL datasets. DSS will fetch the data and
pass it on to Spark.

You can set the Spark configuration in the `Advanced` tab.

See :doc:`/code_recipes/sparksql`


Visual recipes
===============

You can run :doc:`Preparation </preparation/index>` and some :doc:`Visual
Recipes </other_recipes/index>` on Spark. To do so, select `Spark` as the
execution engine and select the appropriate Spark configuration.

For each visual recipe that supports a Spark engine, you can select
the engine under the "Run" button in the recipe's main tab, and set the Spark
configuration in the "Advanced" tab.

All visual data-transformation recipes support running on Spark, including:

* Prepare
* Sync
* Sample / Filter
* Group
* Disinct
* Join
* Pivot
* Sort
* Split
* Top N
* Window
* Stack

Python code
==================

You can write Spark code using Python:

* In a :doc:`Pyspark recipe </code_recipes/pyspark>`
* In a :doc:`Python notebook </notebooks/python>`

Note about Spark code in Python notebooks
--------------------------------------------

All Python notebooks use the same named Spark configuration. See :doc:`/spark/configuration` for more information about named Spark configurations.

When you change the named Spark configuration used by notebooks, you need to restart DSS afterwards.

R code
========

.. warning::

	**Tier 2 support**: Support for SparkR and sparklyr is covered by :doc:`Tier 2 support </troubleshooting/support-tiers>`

You can write Spark code using R:

* In a :doc:`Spark R recipe </code_recipes/sparkr>`
* In a R notebook

Both the recipe and the notebook support two different APIs for accessing Spark:

* The "SparkR" API, ie. the native API bundled with Spark
* The "sparklyr" API

Note about Spark code in R notebooks
--------------------------------------------

All R notebooks use the same named Spark configuration. See :doc:`/spark/configuration` for more information about named Spark configurations.

When you change the named Spark configuration used by notebooks, you need to restart DSS afterwards.


Scala code
===========

You can use :doc:`Scala </code_recipes/scala>`, spark's native language, to implement your custom logic. The Spark configuration is set in the recipe's `Advanced` tab.

Interaction with DSS datasets is provided through a dedicated DSS Spark API, that makes it easy to read and write SparkSQL dataframes from datasets.


.. warning::

  The Spark-Scala notebook is deprecated and will soon be removed


Machine Learning with MLLib - Deprecated
========================================

See the dedicated :doc:`MLLib page </machine-learning/algorithms/mllib>`.
