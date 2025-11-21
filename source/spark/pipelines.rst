Spark pipelines
################

.. contents::
    :local:

.. warning::

	**Tier 2 support**: Spark pipelines are covered by :doc:`Tier 2 support </troubleshooting/support-tiers>`

	In case of issues, you always have the option to disable Spark pipelines on a per-project basis.

One of the greatest strengths of Spark is its ability to execute long data pipelines with multiple steps without always having to write the intermediate data and re-read it at the next step.

In DSS, each recipe reads some datasets and writes some datasets. For example:

* A grouping recipe will read from the storage the input dataset, perform the grouping and write the grouped dataset to its storage.
* A PySpark recipe will direct Spark to read the input(s), perform the whole Spark computation defined by the PySpark recipe and then direct Spark to write the output(s)

With this behavior:

* When writing a coding Spark recipe (PySpark, SparkR, Spark-Scala or SparkSQL), you can write complex data processing steps with an arbitrary number of Spark operations, and DSS will send this to Spark as one single activity.
* However, when having a chain of visual and/or code recipes (a grouping then a prepare then a join then a grouping ...), each recipe is executed independently, and the data is materialized in each dataset.

If all of these visual recipes are Spark-enabled, it is possible to avoid the read-write-read-write cycle using *Spark pipelines*. When several consecutive recipes in a DSS Flow (including with branches or splits) use the Spark engine, DSS can automatically merge all of these recipes and run them as a single Spark job, called a Spark pipeline. This strongly boosts performance by avoiding needless writes and reads of intermediate datasets, and also alleviates Spark startup overheads.

A Spark pipeline covers multiple recipes, and thus one or more intermediate datasets which are part of the pipeline. You can configure the behavior of the pipeline for each of these intermediate datasets:

* Either this dataset is not meaningful nor useful by itself: it is only required as an intermediate step to feed recipes down the Flow. In that case, DSS will not at all write the data of this intermediate dataset when executing the Spark pipeline.
* Or the data in this dataset is actually useful (maybe because you have charts or notebooks using it). In that case, during the execution of the pipeline, DSS will still write the intermediate dataset.

Writing intermediate datasets reduces the performance gain of using a Spark pipeline, but does not negate it since the burden of re-reading the dataset afterwards is still alleviated. It also mutualizes startup overheads.



Enabling Spark pipelines
============================

Merging of Spark pipelines is not enabled by default in DSS. It must be enabled on a per-project basis.

* Go to the project **Settings**
* Go to **Pipelines**
* Select **Enable Spark pipelines**
* **Save** settings

Creating a Spark pipeline
============================

You don't need to do anything special to get Spark pipelines. Each time you run a build job, DSS will evaluate whether one or several Spark pipelines can be created and will run them automatically.

You can check whether a Spark pipeline has been created in the job's results page. On the left part of the screen, "Spark pipeline (xx activities)" will appear and mention how many recipe or recipe executions were merged together.

Configuring behavior for intermediate datasets
================================================

The behavior of intermediate datasets can be configured by the user: write them or not (only the final datasets are written in that case).

This behavior is configured per dataset.

* Go to the dataset's settings page
* Go to Advanced
* Check "Virtualizable in build" if you don't require this dataset to be built when a Spark pipeline includes it.

Limitations
===========

The following are not supported in Spark pipelines:

* PySpark and SparkR code recipes
* Spark Scala code recipes in "Free-form" code mode
* SparkSQL query recipes with :ref:`multiple statements <code-recipes.sql.multiple-statements-handling>`
* TopN visual recipes with a "Remaining rows" output dataset
* Pivot visual recipes with the "Recompute schema at each run" option enabled
* Split visual recipes using "Dispatch percentiles of sorted data" mode
* :doc:`/other_recipes/generate-features` visual recipes

The Spark Scala recipe has additional limitations when running in a Spark Pipeline:

* ``dkuContext.flowVariables`` are not provided
* ``dkuContext.customVariables`` remains the same through the entire job, including the entire pipeline.
  This is not specific to the Spark pipeline, but can be counter-intuitive when some upstream recipe modifies it.
