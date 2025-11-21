Dynamic recipe repeat
#####################

Any SQL query recipe can be configured to be repeating. Such a recipe takes a
secondary "parameters" dataset as a setting and executes the query as many
times as there are rows in the parameters dataset. Each time the query is
executed, variables in the code are expanded based on the current row of the
parameters dataset. The output of the recipe is the concatenation of the
individual query results.

Example use case
================

In order to dynamically build an output dataset based on repeated expansions of
a SQL query, you can build a Flow like this:

* Have a large dataset with a column named ``title``
* Create an editable dataset with a column named ``title_to_match`` containing
  values which can be used in a ``WHERE`` clause of a SQL query
* Create a SQL query recipe, enable the repeating feature picking the editable
  dataset as the repeating parameters dataset
* The query could be something like this:
  ::

      SELECT *
      FROM "MOVIES"
      WHERE "title" ILIKE '%${title_to_match}%'

Configuring
===========

To enable a repeating recipe:

* Go to the Advanced tab of the recipe editor
* Within the **Dynamic recipe repeat** section, make sure **Enable** is checked
  and a dataset is selected in the **Parameters dataset** dropdown

Once enabled, you’ll notice a repeat icon on the recipe in the Flow.

By default a variable is created for each column of the parameters dataset
however it is also possible to create a mapping of column names to variable
names. Only the variables specified by the mapping will then be created. This
is useful to avoid variable shadowing.
