ERR_RECIPE_CANNOT_CHECK_SCHEMA_CONSISTENCY_ON_RECIPE_TYPE: Cannot check schema consistency on this kind of recipe
#################################################################################################################

DSS cannot check the schema consistency on this kind recipe, because
this recipe contains arbitrary code that can set the output schema
at runtime.

This error can happen when trying to run a schema check or propagate
schema changes from a dataset.


Remediation
===========

If you are trying to propagate the changes made on an upstream schema,
you should rebuild this recipe's output dataset (in recursive mode)
to get the updated schema for this dataset and continue propagating
downstream.
