.. _visual-recipes-distinct:

Distinct: get unique rows
##########################

.. contents::
	:local:


The "distinct" recipe allows you to deduplicate rows in a dataset by retrieving unique rows. The rows are compared using the columns you specify. You can also choose to get the number of duplicates for each combination. It can be performed on any dataset in DSS, whether it's a SQL dataset or not. The recipe offers visual tools to setup the specifications and aliases.

The "distinct" recipe can have pre-filters and post-filters. The filters documentation is available :doc:`here  <../other_recipes/sampling>`.

.. seealso::
    For more information, see also the following articles in the Knowledge Base:
    
    - `Concept | Distinct recipe <https://knowledge.dataiku.com/latest/data-preparation/visual-recipes/concept-distinct-recipe.html>`_
    - `Tutorial | Distinct recipe <https://knowledge.dataiku.com/latest/data-preparation/visual-recipes/tutorial-distinct-recipe.html>`_

Engines
=======

Depending on the input dataset types, DSS will adjust the engine it uses to execute the recipe, and choose between Hive, Impala, SparkSQL, plain SQL, and internal DSS. The available engines can be seen and selected by clicking on the cog below the "Run" button.
