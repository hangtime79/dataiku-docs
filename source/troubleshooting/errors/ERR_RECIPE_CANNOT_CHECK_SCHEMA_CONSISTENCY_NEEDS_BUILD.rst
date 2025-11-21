ERR_RECIPE_CANNOT_CHECK_SCHEMA_CONSISTENCY_NEEDS_BUILD: Cannot compute output schema with an empty input dataset. Build the input dataset first.
################################################################################################################################################

This error happens when trying to propagate a schema change in a dataset
that is not yet built.

Some schema propagation require the dataset to be built, because the
schema of the output dataset depends on the data of the input dataset.
This is for example the case for some prepare recipes.


Remediation
===========

Build an input dataset in order to propagate the schema changes or check the
schema consistency of downstream datasets.
