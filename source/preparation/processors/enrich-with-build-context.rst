Enrich with build context
#############################################

This processor adds columns containing information about the current build context, when available.

The following information can be added:

* Build date: date when the job started
* Job ID: ID of the job that ran the Prepare recipe

Additionally, this processor will not output any valid data when designing the preparation. The data
will only be filled when actually running the recipe.


.. pristine
