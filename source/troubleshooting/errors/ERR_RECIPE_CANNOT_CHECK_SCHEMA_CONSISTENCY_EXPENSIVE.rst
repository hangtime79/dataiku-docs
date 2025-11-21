ERR_RECIPE_CANNOT_CHECK_SCHEMA_CONSISTENCY_EXPENSIVE: Cannot check schema consistency: expensive checks disabled
################################################################################################################

DSS has detected that the schema is expensive to compute for the
specified dataset(s).

This error can happen when trying to run a schema check or propagate
schema changes from a dataset.


Remediation
===========

The "Check consistency" and "Propagate schema" tools in the flow
have a "Perform potentially slow checks" option.
Make sure this option is enabled.

