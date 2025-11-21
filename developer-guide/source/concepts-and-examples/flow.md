(flow)=

```{eval-rst}
..
  this code samples has been verified on DSS: 13.2.0
  Date of check: 23/09/2024
  
  this code samples has been verified on DSS: 14.2.0
  Date of check: 08/09/2025
```

# Flow creation and management

## Programmatically building a Flow

The flow, including datasets, recipes, ... can be fully managed and created programmatically.

Datasets can be created and managed using the methods detailed in {doc}`datasets/datasets-other`.

Recipes can be created using the {meth}`~dataikuapi.dss.project.DSSProject.new_recipe` method. This follows a builder pattern: {meth}`~dataikuapi.dss.project.DSSProject.new_recipe` returns you a recipe creator object, on which you add settings, and then call the {py:meth}`~dataikuapi.dss.recipe.DSSRecipeCreator.create()` method to actually create the recipe object.

The builder objects reproduce the functionality available in the recipe creation modals in the UI, so for more control on the recipe's setup, it is often necessary to get its settings after creation, modify it, and save it again.

### Creating a Python recipe

```python
builder = project.new_recipe("python")

# Set the input
builder.with_input("myinputdataset")
# Create a new managed dataset for the output in the filesystem_managed connection
builder.with_new_output_dataset("grouped_dataset", "filesystem_managed")

# Set the code - builder is a PythonRecipeCreator, and has a ``with_script`` method
builder.with_script("""
import dataiku
from dataiku import recipe
input_dataset = recipe.get_inputs_as_datasets()[0]
output_dataset = recipe.get_outputs_as_datasets()[0]

df = input_dataset.get_dataframe()
df = df.groupby("something").count()
output_dataset.write_with_schema(df)
""")

recipe = builder.create()

# recipe is now a ``DSSRecipe`` representing the new recipe, and we can now run it
job = recipe.run()
```

### Creating a Sync recipe

```python
builder = project.new_recipe("sync")
builder = builder.with_input("input_dataset_name")
builder = builder.with_new_output("output_dataset_name", "filesystem_managed")

recipe = builder.create()
job = recipe.run()
```

### Creating and modifying a grouping recipe

The recipe creation mostly handles setting up the inputs and outputs of the recipes, so most of the setup of the recipe has to be done by retrieving its settings, altering and saving them, then applying schema changes to the output

> ```python
> builder = project.new_recipe("grouping")
> builder.with_input("dataset_to_group_on")
> # Create a new managed dataset for the output in the "filesystem_managed" connection
> builder.with_new_output("grouped_dataset", "filesystem_managed")
> builder.with_group_key("column")
> recipe = builder.build()
>
> # After the recipe is created, you can edit its settings
> recipe_settings = recipe.get_settings()
> recipe_settings.set_column_aggregations("myvaluecolumn", sum=True)
> recipe_settings.save()
>
> # And you may need to apply new schemas to the outputs
> # This will add the myvaluecolumn_sum to the "grouped_dataset" dataset
> recipe.compute_schema_updates().apply()
>
> # It should be noted that running a recipe is equivalent to building its output(s)
> job = recipe.run()
> ```

### A complete example

This examples shows a complete chain:

- Creating an external dataset
- Automatically detecting the settings of the dataset (see {doc}`datasets/datasets-other` for details)
- Creating a prepare recipe to cleanup the dataset
- Then chaining a grouping recipe, setting an aggregation on it
- Running the entire chain

```python
dataset = project.create_sql_table_dataset("mydataset", "PostgreSQL", "my_sql_connection", "mytable", "myschema")

dataset_settings = dataset.autodetect_settings()
dataset_settings.save()

# As a shortcut, we can call new_recipe on the DSSDataset object. This way, we don't need to call "with_input"

prepare_builder = dataset.new_recipe("prepare")
prepare_builder.with_new_output("mydataset_cleaned", "filesystem_managed")

prepare_recipe = prepare_builder.create()

# Add a step to clean values in "nb_colis" that are not valid Double
prepare_settings = prepare_recipe.get_settings()
prepare_settings.add_processor_step("FilterOnBadType", {
    "action":"REMOVE_ROW","booleanMode":"AND",
    "appliesTo":"SINGLE_COLUMN",
    "columns":["nb_colis"],"type":"Double"})
prepare_settings.save()

prepare_recipe.compute_schema_updates().apply()
prepare_recipe.run()

# Grouping recipe

grouping_builder = project.new_recipe("grouping")
grouping_builder.with_input("mydataset_cleaned")
grouping_builder.with_new_output("mydataset_cleaned_grouped", "filesystem_managed")
grouping_builder.with_group_key("week")
grouping_recipe = grouping_builder.build()

grouping_recipe_settings = grouping_recipe.get_settings()
grouping_recipe_settings.set_column_aggregations("month", min=True)
grouping_recipe_settings.save()

grouping_recipe.compute_schema_updates().apply()
grouping_recipe.run()
```

## Working with flow zones

### Listing and getting zones

```python
# List zones

for zone in flow.list_zones():
    print("Zone id=%s name=%s" % (zone.id, zone.name))

    print("Zone has the following items:")
    for item in zone.items:
        print("Zone item: %s" % item)

# Get a zone by id - beware, id not name
zone = flow.get_zone("21344ZsQZ")

# Get the "Default" zone
zone = flow.get_default_zone()
```

### Creating a zone and adding items in it

```python
flow = project.get_flow()
zone = flow.create_zone("zone1")

# First way of adding an item to a zone
dataset = project.get_dataset("mydataset")
zone.add_item(dataset)

# Second way of adding an item to a zone
dataset = project.get_dataset("mydataset")
dataset.move_to_zone(zone)

# Third way of adding an item to a zone
zones = flow.list_zones()
zone = "zone1"
zoneId = [z.id for z in zones if z.name==zone][0]

dataset = project.get_dataset("mydataset")
dataset.move_to_zone(zoneId)
```

### Changing the settings of a zone

```python
flow = project.get_flow()
zone = flow.get_zone("21344ZsQZ")

settings = zone.get_settings()
settings.name = "New name"

settings.save()
```

### Getting the zone of a dataset

```python
dataset = project.get_dataset("mydataset")

zone = dataset.get_zone()
print("Dataset is in zone %s" % zone.id)
```

## Navigating the flow graph

DSS builds the Flow graph dynamically by enumerating datasets, folders, models and recipes and linking all together through the inputs and outputs of the recipes. Since navigating this can be complex, the {class}`dataikuapi.dss.flow.DSSProjectFlow` class gives you access to helpers for this

### Finding sources of the Flow

```python
flow = project.get_flow()
graph = flow.get_graph()

for source in graph.get_source_computables(as_type="object"):
    print("Flow graph has source: %s" % source)
```

### Enumerating the graph in order

This method will return all items in the graph, "from left to right". Each item is returned as a {class}`~dataikuapi.dss.dataset.DSSDataset`, {class}`~dataikuapi.dss.managedfolder.DSSManagedFolder`, {class}`~dataikuapi.dss.savedmodel.DSSSavedModel`, {class}`~dataikuapi.dss.streaming_endpoint.DSSStreamingEndpoint` or {class}`~dataikuapi.dss.recipe.DSSRecipe`

```python
flow = project.get_flow()
graph = flow.get_graph()

for item in graph.get_items_in_traversal_order(as_type="object"):
    print("Next item in the graph is %s" % item)
```

### Replacing an input everywhere in the graph

This method allows you to replace an input (dataset for example) in every recipe where it appears as a input

```python
flow = project.get_flow()
flow.replace_input_computable("old_dataset", "new_dataset")

# Or to replace a managed folder
flow.replace_input_computable("oldid", "newid", type="MANAGED_FOLDER")
```

## Schema propagation

When the schema of an input dataset is modified, or when the settings of a recipe are modified, you need to propagate this schema change across the flow.

This can be done from the UI, but can also be automated through the API

```python
flow = project.get_flow()

# A propagation always starts from a source dataset and will move from left to right till the end of the Flow

propagation = flow.new_schema_propagation("sourcedataset")

future = propagation.start()
future.wait_for_result()
```

There are many options for propagation, see {py:class}`dataikuapi.dss.flow.DSSSchemaPropagationRunBuilder`

## Exporting a flow documentation

This sample shows how to generate and download a flow documentation from a template.

See [Flow Document Generator](https://doc.dataiku.com/dss/latest/flow/flow-document-generator.html) for more information.

```python
# project is a DSSProject object

flow = project.get_flow()

# Launch the flow document generation by either
# using the default template by calling without arguments
# or specifying a managed folder id and the path to the template to use in that folder
future = flow.generate_documentation(FOLDER_ID, "path/my_template.docx")

# Alternatively, use a custom uploaded template file
with open("my_template.docx", "rb") as f:
    future = flow.generate_documentation_from_custom_template(f)

# Wait for the generation to finish, retrieve the result and download the generated
# flow documentation to the specified file
result = future.wait_for_result()
export_id = result["exportId"]

flow.download_documentation_to_file(export_id, "path/my_flow_documentation.docx")
```

## Detailed examples

This section contains more advanced examples on Flow-based operations.

### Delete orphaned Datasets

It can happen that after some operations on a Flow one or more Datasets end up not being linked to any Recipe and thus become disconnected from the Flow branches. In order to programmatically remove those Datasets from the Flow, you can list nodes that have neither predecessor nor successor in the graph using the following function:

```{literalinclude} examples/flow/delete-orphaned-datasets.py
```

```{attention}
Note that the function has additional flags with default values set up to prevent accidental data deletion. Even so, we recommend you to remain extra cautious when clearing/deleting Datasets.
```

## Reference documentation

### Classes

```{eval-rst}
.. autosummary::
    dataikuapi.dss.recipe.CodeRecipeCreator
    dataikuapi.dss.dataset.DSSDataset
    dataikuapi.dss.flow.DSSFlowZone
    dataikuapi.dss.flow.DSSFlowZoneSettings
    dataikuapi.dss.future.DSSFuture
    dataikuapi.dss.job.DSSJob
    dataikuapi.dss.project.DSSProject
    dataikuapi.dss.flow.DSSProjectFlow
    dataikuapi.dss.flow.DSSProjectFlowGraph
    dataikuapi.dss.recipe.DSSRecipe
    dataikuapi.dss.recipe.DSSRecipeCreator
    dataikuapi.dss.recipe.DSSRecipeSettings
    dataikuapi.dss.flow.DSSSchemaPropagationRunBuilder
    dataikuapi.dss.recipe.GroupingRecipeCreator
    dataikuapi.dss.recipe.GroupingRecipeSettings
    dataikuapi.dss.recipe.PrepareRecipeSettings
    dataikuapi.dss.recipe.SingleOutputRecipeCreator
    dataikuapi.dss.flow.DSSSchemaPropagationRunBuilder
```

### Functions

```{eval-rst}
.. autosummary::
    ~dataikuapi.dss.recipe.PrepareRecipeSettings.add_processor_step
    ~dataikuapi.dss.flow.DSSFlowZone.add_item
    ~dataikuapi.dss.dataset.DSSDataset.autodetect_settings
    ~dataikuapi.dss.recipe.DSSRecipe.compute_schema_updates
    ~dataikuapi.dss.recipe.DSSRecipeCreator.create
    ~dataikuapi.dss.project.DSSProject.create_sql_table_dataset
    ~dataikuapi.dss.flow.DSSProjectFlow.download_documentation_to_file
    ~dataikuapi.dss.flow.DSSProjectFlow.generate_documentation
    ~dataikuapi.dss.flow.DSSProjectFlow.generate_documentation_from_custom_template
    ~dataikuapi.dss.flow.DSSProjectFlow.get_default_zone
    ~dataikuapi.dss.flow.DSSProjectFlow.get_graph
    ~dataikuapi.dss.flow.DSSProjectFlowGraph.get_items_in_traversal_order
    ~dataikuapi.dss.recipe.DSSRecipe.get_settings
    ~dataikuapi.dss.flow.DSSProjectFlowGraph.get_source_computables
    ~dataikuapi.dss.flow.DSSProjectFlow.get_zone
    ~dataikuapi.dss.flow.DSSFlowZone.id
    ~dataikuapi.dss.flow.DSSFlowZone.items
    ~dataikuapi.dss.flow.DSSProjectFlow.list_zones
    ~dataikuapi.dss.dataset.DSSDataset.move_to_zone
    ~dataikuapi.dss.dataset.DSSDataset.new_recipe
    ~dataikuapi.dss.project.DSSProject.new_recipe
    ~dataikuapi.dss.flow.DSSProjectFlow.new_schema_propagation
    ~dataikuapi.dss.flow.DSSProjectFlow.replace_input_computable
    ~dataikuapi.dss.recipe.DSSRecipe.run
    ~dataikuapi.dss.recipe.DSSRecipeSettings.save
    ~dataikuapi.dss.recipe.GroupingRecipeSettings.set_column_aggregations
    ~dataikuapi.dss.flow.DSSSchemaPropagationRunBuilder.start
    ~dataikuapi.dss.future.DSSFuture.wait_for_result
    ~dataikuapi.dss.recipe.GroupingRecipeCreator.with_group_key
    ~dataikuapi.dss.recipe.DSSRecipeCreator.with_input
    ~dataikuapi.dss.recipe.SingleOutputRecipeCreator.with_new_output
    ~dataikuapi.dss.recipe.CodeRecipeCreator.with_new_output_dataset
    ~dataikuapi.dss.recipe.CodeRecipeCreator.with_script
```