ERR_RECIPE_CANNOT_USE_ENGINE: Cannot use the selected engine for this recipe
############################################################################

The selected execution engine / backend for this recipe cannot be used.
The specific error message should contain more details on the precise
cause of this error.

The input dataset, model, or other recipe settings are not compatible
with the selected engine for this recipe.

Some common examples include:

* Using the SQL engine with non-SQL input datasets
* Using SQL computed columns on DSS engine
* Changing the model (output of a training recipe or input of a scoring
  recipe) for one with a different backend.
* Using features not supported by the engine, like text features
  for ML in SQL.


Remediation
===========

Make sure that the recipe settings and inputs are compatible with the
selected engine. Change the engine if necessary.

If the recipe's inputs were recently changed, that is probably a good
place to start looking.
