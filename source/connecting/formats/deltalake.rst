Delta Lake
###########

Delta Lake is a file storage format on top of Parquet, that augments Parquet with the ability to perform updates and removals, and other database-oriented features.

Dataiku can read Delta Lake files and process them, either using Spark or any recipe.

.. warning::

  **Experimental**: Support for Delta Lake is :doc:`Experimental </troubleshooting/support-tiers>`


Support for Delta Lake requires Spark integration to be done on the DSS instance. Delta Lake then appears as a file format.

Datasets in Delta Lake format can be stored on S3, Azure Blob Storage, Google Cloud Storage or HDFS

While Delta Lake datasets can be processed with any recipe, we strongly recommend processing them with Spark recipes

Delta Lake datasets that have underlying partitioning will be read unpartitioned.
