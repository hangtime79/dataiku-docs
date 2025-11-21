:tocdepth: 2

Recipes
########

For usage information and examples, see :doc:`/concepts-and-examples/recipes`

.. autoclass:: dataikuapi.dss.recipe.DSSRecipe
.. autoclass:: dataikuapi.dss.recipe.DSSRecipeListItem
	:inherited-members: dict
.. autoclass:: dataikuapi.dss.recipe.DSSRecipeStatus
.. autoclass:: dataikuapi.dss.recipe.RequiredSchemaUpdates

Settings
--------
.. autoclass:: dataikuapi.dss.recipe.DSSRecipeSettings
	:inherited-members:
.. autoclass:: dataikuapi.dss.recipe.DSSRecipeDefinitionAndPayload
	:noindex:
.. autoclass:: dataikuapi.dss.recipe.CodeRecipeSettings
.. autoclass:: dataikuapi.dss.recipe.SyncRecipeSettings
.. autoclass:: dataikuapi.dss.recipe.PrepareRecipeSettings
.. autoclass:: dataikuapi.dss.recipe.SamplingRecipeSettings
.. autoclass:: dataikuapi.dss.recipe.GroupingRecipeSettings
.. autoclass:: dataikuapi.dss.recipe.SortRecipeSettings
.. autoclass:: dataikuapi.dss.recipe.TopNRecipeSettings
.. autoclass:: dataikuapi.dss.recipe.DistinctRecipeSettings
.. autoclass:: dataikuapi.dss.recipe.PivotRecipeSettings
.. autoclass:: dataikuapi.dss.recipe.WindowRecipeSettings
.. autoclass:: dataikuapi.dss.recipe.JoinRecipeSettings
.. autoclass:: dataikuapi.dss.recipe.DownloadRecipeSettings
.. autoclass:: dataikuapi.dss.recipe.SplitRecipeSettings
.. autoclass:: dataikuapi.dss.recipe.StackRecipeSettings

Creation
--------
.. autoclass:: dataikuapi.dss.recipe.DSSRecipeCreator
.. autoclass:: dataikuapi.dss.recipe.SingleOutputRecipeCreator
.. autoclass:: dataikuapi.dss.recipe.VirtualInputsSingleOutputRecipeCreator
.. autoclass:: dataikuapi.dss.recipe.CodeRecipeCreator
.. autoclass:: dataikuapi.dss.recipe.PythonRecipeCreator
.. autoclass:: dataikuapi.dss.recipe.SQLQueryRecipeCreator
.. autoclass:: dataikuapi.dss.recipe.PrepareRecipeCreator
.. autoclass:: dataikuapi.dss.recipe.SyncRecipeCreator
.. autoclass:: dataikuapi.dss.recipe.SamplingRecipeCreator
.. autoclass:: dataikuapi.dss.recipe.DistinctRecipeCreator
.. autoclass:: dataikuapi.dss.recipe.GroupingRecipeCreator
.. autoclass:: dataikuapi.dss.recipe.PivotRecipeCreator
.. autoclass:: dataikuapi.dss.recipe.SortRecipeCreator
.. autoclass:: dataikuapi.dss.recipe.TopNRecipeCreator
.. autoclass:: dataikuapi.dss.recipe.WindowRecipeCreator
.. autoclass:: dataikuapi.dss.recipe.JoinRecipeCreator
.. autoclass:: dataikuapi.dss.recipe.FuzzyJoinRecipeCreator
.. autoclass:: dataikuapi.dss.recipe.GeoJoinRecipeCreator
.. autoclass:: dataikuapi.dss.recipe.SplitRecipeCreator
.. autoclass:: dataikuapi.dss.recipe.StackRecipeCreator
.. autoclass:: dataikuapi.dss.recipe.DownloadRecipeCreator
.. autoclass:: dataikuapi.dss.recipe.PredictionScoringRecipeCreator
.. autoclass:: dataikuapi.dss.recipe.ClusteringScoringRecipeCreator
.. autoclass:: dataikuapi.dss.recipe.EvaluationRecipeCreator
.. autoclass:: dataikuapi.dss.recipe.StandaloneEvaluationRecipeCreator
.. autoclass:: dataikuapi.dss.recipe.ContinuousSyncRecipeCreator

Utilities
---------
.. autoclass:: dataikuapi.dss.utils.DSSComputedColumn
.. autoclass:: dataikuapi.dss.utils.DSSFilter
.. autoclass:: dataikuapi.dss.utils.DSSFilterOperator