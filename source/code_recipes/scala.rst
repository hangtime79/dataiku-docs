Spark-Scala recipes
###################

Data Science Studio gives you the ability to write Spark recipes using Scala, Spark's native
language. Spark-Scala recipes can read and write datasets, even when their storage backend is not
HDFS.

Spark-scala recipes can manipulate datasets by using
`SparkSQL's DataFrames <http://spark.apache.org/docs/latest/sql-programming-guide.html>`_.

Reference documentation for the DSS Scala API can be found at:
|scala_api_doc_url|

Prerequisites
================

Prior to writing Scala recipes, you need to ensure that DSS and Spark are properly configured together. See :doc:`/spark/installation`.

Creating a Spark-Scala recipe
=============================

* Create a new Spark-Scala recipe, either through a dataset's Actions menu or in *+Recipe > Hadoop & Spark > Spark-Scala*
* Add the input Datasets and/or Folders that will be used as source data in your recipes.
* Select or create the output Datasets and/or Folder that will be filled by your recipe.
* Click `Create recipe`.
* You can now write your Spark code in Scala. A sample code is provided to get you started.

.. note::

	If the Spark-Scala icon is not enabled (greyed out), it can be because:

	* Spark is not installed. See :doc:`/spark/installation` for more information
	* You don't have :doc:`write access </security/permissions>` on the project
	* You don't have the proper :doc:`user profile </security/user-profiles>`. Your administrator
	  needs to grant you an appropriate user profile

Basic Spark-Scala recipe
========================

First of all, you will need to load the Dataiku API and entry points:

.. code-block:: scala

	import com.dataiku.dss.spark._
	import org.apache.spark.SparkContext
	import org.apache.spark.sql.SQLContext
	import org.apache.spark.sql.functions._

	val sparkConf    = DataikuSparkContext.buildSparkConf()
	val sparkContext = new SparkContext(sparkConf)
	val sqlContext   = new SQLContext(sparkContext)
	val dkuContext   = DataikuSparkContext.getContext(sparkContext)

You will then need to obtain DataFrames for your input datasets and directory handles for your input folders:

.. code-block:: scala

	val inputDataset1 = dkuContext.getDataFrame(sqlContext, "KeyOfInputDataset")
	val inputFolder1 =  dkuContext.getManagedFolderRoot("IdOfInputFolder")

These return a SparkSQL DataFrame and a Java File (pointing to the Folder's root) respectively.
You can then apply your transformations to the DataFrame and do what you need in the Folder.

Finally you can save the transformed DataFrame into the output dataset. By default the ``save``
method overwrites the dataset schema with that of the DataFrame:

.. code-block:: scala

	dkuContext.save("KeyOfOutputDataset", transformedDataFrame)

If you declared the schema of the output dataset prior to running the Scala code, you can use
``save(…, writeSchema = false)``. However, it can be impractical to do so, especially if your code
generates many columns (or columns that change often).

If you run your recipe on partitioned datasets, the above code will automatically load/save the
partitions specified in the recipe parameters. You can forcibly load or save another partition (or
load all partitions) of a dataset:

.. code-block:: scala

	getDataFrame(sqlContext, "KeyOfInputDataset", partitions = Some(List("otherPartitionId")))
	getDataFrame(sqlContext, "KeyOfInputDataset", partitions = Some(null)) // whole dataset
	save("KeyOfOutputDataset", dataframe, targetPartition = Some("otherPartitionId"))

In the same vein, ``save`` will use the writing mode (append or overwrite) defined in the recipe's
configuration by default. You can also override this behavior, but please note that some dataset
types do not support Append mode (e.g. HDFS):

.. code-block:: scala

	save("KeyOfOutputDataset", dataframe, writeMode = Some(WriteMode.Append))

