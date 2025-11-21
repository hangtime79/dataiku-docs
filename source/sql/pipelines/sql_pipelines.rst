Using SQL pipelines
#####################

.. contents::
    :local:


In DSS, each recipe reads some datasets and writes some datasets. For example:

* A grouping recipe will read the input dataset from the storage, perform the grouping, and write the grouped dataset to its storage.
* A SQL recipe will read input(s), perform the whole SQL computation defined by the SQL recipe, and then direct SQL to write the output(s)

Given this read-write behavior of recipes:

* When writing a coding SQL recipe, you can write complex data processing steps with an arbitrary number of SQL operations, and DSS will send these pipelines to SQL as one single activity.
* When using a chain of visual and/or code recipes, however, DSS executes each recipe independently. For example, if you have a grouping recipe followed by a prepare recipe then a join recipe then a grouping recipe, and so forth, each recipe will be executed independently, and the SQL engine would read and write the datasets in each recipe.

For a Dataiku DSS flow that uses a SQL engine and consists of consecutive recipes sharing the same connection, *SQL pipelines* can minimize or avoid the dataset read-write cycle.


.. _enabling-sql-pipelines:

Enabling SQL pipelines
=======================

SQL pipelines are not enabled by default in DSS but can be enabled on a per-project basis.

* Go to the project **Settings**
* Go to **Pipelines**
* Select **Enable SQL pipelines**
* **Save** settings

.. _configure-datasets:

Configuring behavior for intermediate datasets
------------------------------------------------

A SQL pipeline covers one or more intermediate datasets that are part of the pipeline. For each of these intermediate datasets, you can configure the behavior of the pipeline by enabling or disabling virtualization. To enable virtualization for a dataset: 

* Open the dataset and go to the **Settings** tab at the top of the page
* Go to the **Advanced** tab
* Check "Virtualizable in build"

You can also enable virtualization for one or more datasets at once by performing these steps:

* Select one or more datasets in the **Flow**
* Locate the "Other actions" section in the right panel and select **Allow build virtualization (for pipelines)**

When you configure a dataset to be virtualizable, consider:

* whether the dataset is not useful by itself, but is only required as an intermediate step to feed recipes down the Flow. In this case, virtualization can be useful to prevent DSS from writing the data of this intermediate dataset when executing the SQL pipeline.
* whether the dataset is useful by itself. For example, if the dataset is used by charts, enabling virtualization can prevent DSS from creating required charts, as the data needed to create the charts would not be available. 

.. note::
    In some cases, you can configure a dataset to be virtualizable, but DSS would still write the dataset during the execution of the SQL pipeline. This happens when there are some technical constraints on the dataset that prevent the dataset from being virtualized.

Although writing intermediate datasets reduces the performance gain of using a SQL pipeline, the pipeline still provides the benefit that the datasets do not have to be read again once they've been written. A SQL pipeline can also help to avoid SQL startup overheads.

.. _configure-recipes:

Configuring behavior for recipes 
---------------------------------

A SQL pipeline also covers multiple recipes, and you can configure the behavior of the pipeline for each recipe.

* Open the recipe and go to the **Advanced** tab at the top of the page
* Check the options for "Pipelining":

    * "Can this recipe be merged in an existing recipes pipeline?" 
    * "Can this recipe be the target of a recipes pipeline?"

The first setting determines whether a recipe can be concatenated inside an existing SQL pipeline. The second setting determines whether running the recipe can trigger a new SQL pipeline.

.. _creating-sql-recipes:

Creating SQL pipelines
=======================

When you run a build job, the Dataiku flow dependencies engine automatically detects if there are SQL pipelines based on the :ref:`settings of the datasets <configure-datasets>` and the :ref:`recipe settings <configure-recipes>`. The engine will then create separate job activities for each of them. 

The details of the SQL pipelines that have run can be visualized in the job results page. On the left part of the screen, "SQL pipeline (xx activities)" will appear and mention how many recipes or recipe executions were merged together.

.. _sql-pipelines-supported-databases:

Supported databases
====================

The SQL pipelines feature is supported for databases that are compatible with SQL views. These include:

- Snowflake
- Databricks
- Redshift
- BigQuery
- Synapse
- SQL Server
- PostgreSQL
- MySQL
- Oracle
- Greenplum
- Teradata
- Vertica

Limitations
===========

Additional limitations when running a SQL pipeline:

* The SQL datasets must be part of the same database connection
* The following are not supported:

  * SQL script recipes
  * SQL query recipes with :ref:`multiple statements <code-recipes.sql.multiple-statements-handling>`
  * TopN visual recipes with a "Remaining rows" output dataset
  * Pivot visual recipes with the "Recompute schema at each run" option enabled
  * Split visual recipes using "Dispatch percentiles of sorted data" or "Full random" mode
  * :doc:`/other_recipes/generate-features` visual recipes

Related Pages
===============

* :doc:`/connecting/sql/index`
* :doc:`/spark/pipelines`
