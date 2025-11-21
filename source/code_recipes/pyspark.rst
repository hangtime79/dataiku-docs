PySpark recipes
###################

DSS lets you write recipes using Spark in Python, using the PySpark API.

As with all Spark integrations in DSS, PySPark recipes can read and write datasets,
whatever their storage backends.

Pyspark recipes manipulate datasets using the PySpark / SparkSQL "DataFrame" API.

.. contents::
	:local:


Creating a PySpark recipe
=============================

* First make sure that :doc:`Spark is enabled </spark/installation>`
* Create a Pyspark recipe by clicking the corresponding icon
* Add the input Datasets and/or Folders that will be used as source data in your recipes.
* Select or create the output Datasets and/or Folder that will be filled by your recipe.
* Click `Create recipe`.
* You can now write your Spark code in Python. A sample code is provided to get you started.

.. note::

	If the Pyspark icon is not enabled (greyed out), it can be because:

	* Spark is not installed. See :doc:`/spark/installation` for more information
	* You don't have :doc:`write access </security/permissions>` on the project
	* You don't have the proper :doc:`user profile </security/user-profiles>`. Your administrator
	  needs to grant you an appropriate user profile


Anatomy of a basic Pyspark recipe
===================================

First of all, you will need to load the Dataiku API and Spark APIs, and create the Spark context

.. code-block:: python

	# -*- coding: utf-8 -*-

	# Import Dataiku APIs, including the PySpark layer
	import dataiku
	from dataiku import spark as dkuspark
	# Import Spark APIs, both the base SparkContext and higher level SQLContext
	from pyspark import SparkContext
	from pyspark.sql import SQLContext

	sc = SparkContext()
	sqlContext = SQLContext(sc)

You will then need to obtain DataFrames for your input datasets and directory handles for your input folders:

.. code-block:: python

	dataset = dataiku.Dataset("name_of_the_dataset")
	df = dkuspark.get_dataframe(sqlContext, dataset)


These return a SparkSQL DataFrame
You can then apply your transformations to the DataFrame.

Finally you can save the transformed DataFrame into the output dataset. By default this
method overwrites the dataset schema with that of the DataFrame:

.. code-block:: scala

	out = dataiku.Dataset("out")
	dkuspark.write_with_schema(out, the_resulting_spark_dataframe)

If you run your recipe on partitioned datasets, the above code will automatically load/save the
partitions specified in the recipe parameters.