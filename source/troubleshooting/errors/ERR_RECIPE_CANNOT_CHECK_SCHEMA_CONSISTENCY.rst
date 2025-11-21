ERR_RECIPE_CANNOT_CHECK_SCHEMA_CONSISTENCY: Cannot check schema consistency
###########################################################################

DSS could not check the schema consistency on this recipe. The specific error
message should contain more information about why this is the case.

This error can happen when trying to run a schema check or propagate
schema changes from a dataset.


Remediation
===========

Open the recipe and make sure it does not show any error. If the save button
is enabled, try saving it and re-performing the schema check.
Make sure that the output dataset(s) are correctly set, try to visit their
Settings > Schema screen and launch the consistency check from there.
