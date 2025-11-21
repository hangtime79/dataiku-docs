ERR_RECIPE_CANNOT_CHECK_SCHEMA_CONSISTENCY_WITH_RECIPE_CONFIG: Cannot check schema consistency because of recipe configuration
##############################################################################################################################

DSS cannot check the schema consistency on this recipe's output dataset,
because this recipe's configuration prevents the deterministic
computation of the schema.

This error can happen when trying to run a schema check or propagate
schema changes from a dataset.

The common causes for this error happening are:

* A Pivot recipe is configured to always recompute output schema
* The modality list of a Pivot recipe is not up-to-date,
  e.g. because the input dataset or the recipe settings were change
* A SparkSQL recipe is using global metastore mode, which disables
  validation and schema computation
* A Sync recipe is configured in "free output schema" mode, meaning
  that you set the schema of the output dataset and the recipe will
  perform name-based matching to fill the columns from the input
  dataset.


Remediation
===========

* For the Pivot recipe, you can disable the schema re-computation,
  and run it so that the output dataset is computed and its schema
  is up-to-date.
* For the SparkSQL recipe, you can either disable the global metastore
  if you don;t need it or run the recipe to compute the output dataset.
* For the Sync recipe, you can switch it to Strict schema mode to update
  the output schema (this will erase any customization that you made
  like column reordering), then put it back in free schema mode for
  customization.

In all cases, you can also manually (or programmatically using the
:doc:`Public API </publicapi/index>`) set the schema on the output dataset.

Learn more about:

* :doc:`/other_recipes/pivot`
* :doc:`/code_recipes/sparksql`
* :doc:`/other_recipes/sync`
