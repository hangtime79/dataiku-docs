.. _visual-recipes-window:

Window: analytics functions
###########################

.. contents::
	:local:


The "window" recipe allows you to perform analytics functions on any dataset in DSS, whether it's a SQL dataset or not. This is the equivalent of a SQL "over" statement. The recipe offers visual tools to setup the windows and aliases.
The "window" recipe can have pre-filters and post-filters. The filters documentation is available :doc:`here  <../other_recipes/sampling>`.

.. seealso::
    For more information, see also the following articles in the Knowledge Base:
    
    - `Concept | Window recipe <https://knowledge.dataiku.com/latest/data-preparation/visual-recipes/concept-window-recipe.html>`_
    - `Tutorial | Window recipe <https://knowledge.dataiku.com/latest/data-preparation/visual-recipes/tutorial-window-recipe.html>`_

Engines
=======

Depending on the input dataset types, DSS will adjust the engine it uses to execute the recipe, and choose between Hive, Impala, SparkSQL, plain SQL, and internal DSS. The available engines can be seen and selected by clicking on the cog below the "Run" button.

.. note:: 

    The DSS engine has different default window behavior than when using a SQL engine. When using the **DSS engine**, the window will default to the *whole* frame if no window is specified. As a result, you can see different window behavior when switching between the DSS engine and a SQL engine. In order to see the same result when using the DSS Engine as you would with the SQL engine, you can enable the Window Frame option with both the "Limit preceding rows" and "Limit following rows" options unchecked. 
    
Notes
=====

- Since DSS v4.1, null values are ordered in a specific way, take a look at :ref:`null-values-handling`
