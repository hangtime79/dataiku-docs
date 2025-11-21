(recipes)=

```{eval-rst}
..
  this code samples has been verified on DSS: 13.2.0
  Date of check: 23/09/2024
  
  this code samples has been verified on DSS: 14.1.0
  Date of check: 29/08/2025
```

# Recipes

This page lists usage examples for performing various operations with recipes through Dataiku Python API.
In all examples, `project` is a {py:class}`dataikuapi.dss.project.DSSProject` handle, 
obtained using {meth}`~dataikuapi.DSSClient.get_project()` or {meth}`~dataikuapi.DSSClient.get_default_project()`

## Basic operations

### Listing recipes

```python
recipes = project.list_recipes()
# Returns a list of DSSRecipeListItem

for recipe in recipes:
        # Quick access to main information in the recipe list item
        print("Name: %s" % recipe.name)
        print("Type: %s" % recipe.type)
        print("Tags: %s" % recipe.tags) # Returns a list of strings

        # You can also use the list item as a dict of all available recipe information
        print("Raw: %s" % recipe)
```

### Deleting a recipe

```python
recipe = project.get_recipe('myrecipe')
recipe.delete()
```

### Modifying tags for a recipe

```python
recipe = project.get_recipe('myrecipe')
settings = recipe.get_settings()

print("Current tags are %s" % settings.tags)

# Change the tags
settings.tags = ["newtag1", "newtag2"]

# If we changed the settings, we must save
settings.save()
```

## Recipe creation

Please see {doc}`flow`

## Recipe status

You can compute the status of the recipe, which also provides you with the engine information.

### Find the engine used to run a recipe

```python
recipe = project.get_recipe("myrecipe")
status = recipe.get_status()
print(status.get_selected_engine_details())
```

### Check if a recipe is valid

{py:meth}`~dataikuapi.dss.recipe.DSSRecipe.get_status` calls the validation code of the recipe

```python
recipe = project.get_recipe("myrecipe")
status = recipe.get_status()
print(status.get_selected_engine_details())
```

### Find the engines for all recipes of a certain type

This example shows how to filter a list, obtain {py:class}`~dataikuapi.dss.recipe.DSSRecipe` objects for the list items, and getting their status

```python
for list_item in project.list_recipes():
        if list_item.type == "grouping":
                recipe = list_item.to_recipe()
                engine = recipe.get_status().get_selected_engine_details()["type"]
                print("Recipe %s uses engine %s" % (recipe.name, engine))
```

## Recipe settings

When you use {py:meth}`~dataikuapi.dss.recipe.DSSRecipe.get_settings` on a recipe, you receive a settings object whose class depends on the recipe type. Please see below for the possible types.

### Checking if a recipe uses a particular dataset as input

```python
recipe = project.get_recipe("myrecipe")
settings = recipe.get_settings()
print("Recipe %s uses input:%s" % (recipe.name, settings.has_input("mydataset")))
```

### Replacing an input of a recipe

```python
recipe = project.get_recipe("myrecipe")
settings = recipe.get_settings()

settings.replace_input("old_input", "new_input")
settings.save()
```

### Setting the code env of a code recipe

```python
recipe = project.get_recipe("myrecipe")
settings = recipe.get_settings()

# Use this to set the recipe to inherit the project's code env
settings.set_code_env(inherit=True)

# Use this to set the recipe to use a specific code env
settings.set_code_env(code_env="myenv")

settings.save()
```

## Reference documentation

### List and status

```{eval-rst}
.. autosummary::
        dataikuapi.dss.recipe.DSSRecipe
        dataikuapi.dss.recipe.DSSRecipeListItem
        dataikuapi.dss.recipe.DSSRecipeStatus
        dataikuapi.dss.recipe.RequiredSchemaUpdates
``` 

### Settings

```{eval-rst}
.. autosummary::
        dataikuapi.dss.recipe.DSSRecipeSettings
        dataikuapi.dss.recipe.CodeRecipeSettings
        dataikuapi.dss.recipe.SyncRecipeSettings
        dataikuapi.dss.recipe.PrepareRecipeSettings
        dataikuapi.dss.recipe.SamplingRecipeSettings
        dataikuapi.dss.recipe.GroupingRecipeSettings
        dataikuapi.dss.recipe.SortRecipeSettings
        dataikuapi.dss.recipe.TopNRecipeSettings
        dataikuapi.dss.recipe.DistinctRecipeSettings
        dataikuapi.dss.recipe.PivotRecipeSettings
        dataikuapi.dss.recipe.WindowRecipeSettings
        dataikuapi.dss.recipe.JoinRecipeSettings
        dataikuapi.dss.recipe.DownloadRecipeSettings
        dataikuapi.dss.recipe.SplitRecipeSettings
        dataikuapi.dss.recipe.StackRecipeSettings
```

### Creation

```{eval-rst}
.. autosummary::
        dataikuapi.dss.recipe.DSSRecipeCreator
        dataikuapi.dss.recipe.SingleOutputRecipeCreator
        dataikuapi.dss.recipe.VirtualInputsSingleOutputRecipeCreator
        dataikuapi.dss.recipe.CodeRecipeCreator
        dataikuapi.dss.recipe.PythonRecipeCreator
        dataikuapi.dss.recipe.SQLQueryRecipeCreator
        dataikuapi.dss.recipe.PrepareRecipeCreator
        dataikuapi.dss.recipe.SyncRecipeCreator
        dataikuapi.dss.recipe.SamplingRecipeCreator
        dataikuapi.dss.recipe.DistinctRecipeCreator
        dataikuapi.dss.recipe.GroupingRecipeCreator
        dataikuapi.dss.recipe.PivotRecipeCreator
        dataikuapi.dss.recipe.SortRecipeCreator
        dataikuapi.dss.recipe.TopNRecipeCreator
        dataikuapi.dss.recipe.WindowRecipeCreator
        dataikuapi.dss.recipe.JoinRecipeCreator
        dataikuapi.dss.recipe.FuzzyJoinRecipeCreator
        dataikuapi.dss.recipe.GeoJoinRecipeCreator
        dataikuapi.dss.recipe.SplitRecipeCreator
        dataikuapi.dss.recipe.StackRecipeCreator
        dataikuapi.dss.recipe.DownloadRecipeCreator
        dataikuapi.dss.recipe.PredictionScoringRecipeCreator
        dataikuapi.dss.recipe.ClusteringScoringRecipeCreator
        dataikuapi.dss.recipe.EvaluationRecipeCreator
        dataikuapi.dss.recipe.StandaloneEvaluationRecipeCreator
        dataikuapi.dss.recipe.ContinuousSyncRecipeCreator
```

### Utilities

```{eval-rst}
.. autosummary::
        dataikuapi.dss.utils.DSSComputedColumn
        dataikuapi.dss.utils.DSSFilter
        dataikuapi.dss.utils.DSSFilterOperator
```