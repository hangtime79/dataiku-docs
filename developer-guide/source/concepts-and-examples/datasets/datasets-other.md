# Datasets (other operations)

```{eval-rst}
..
  this code samples has been verified on DSS: 13.2.0
  Date of check: 19/09/2024
  
  this code samples has been verified on DSS: 14.1.0
  Date of check: 06/08/2025

```

Please see {doc}`index` for an introduction about interacting with datasets in Dataiku Python API

This page lists many usage examples for performing various operations (listed below) with datasets through Dataiku Python API. It is designed to give an overview of the main capabilities but is not an exhaustive documentation.


In all examples, `project` is a {class}`dataikuapi.dss.project.DSSProject` handle, obtained using {meth}`~dataikuapi.DSSClient.get_project()` or {meth}`~dataikuapi.DSSClient.get_default_project()`

## Basic operations

### Listing datasets

```python
datasets = project.list_datasets()
# Returns a list of DSSDatasetListItem

for dataset in datasets:
        # Quick access to main information in the dataset list item
        print("Name: %s" % dataset.name)
        print("Type: %s" % dataset.type)
        print("Connection: %s" % dataset.connection)
        print("Tags: %s" % dataset.tags) # Returns a list of strings

        # You can also use the list item as a dict of all available dataset information
        print("Raw: %s" % dataset)
```

outputs

```
Name: train_set
Type: Filesystem
Connection: filesystem_managed
Tags: ["creator_admin"]
Raw: {  'checklists': {   'checklists': []},
        'customMeta': {   'kv': {   }},
        'flowOptions': {   'crossProjectBuildBehavior': 'DEFAULT',
                            'rebuildBehavior': 'NORMAL'},
        'formatParams': {  /* Parameters specific to each format type */ },
        'formatType': 'csv',
        'managed': False,
        'name': 'train_set',
        'tags' : ["mytag1"]
        'params': { /* Parameters specific to each dataset type */ "connection" : "filesystem_managed" },
        'partitioning': {   'dimensions': [], 'ignoreNonMatchingFile': False},
        'projectKey': 'TEST_PROJECT',
        'schema': {   'columns': [   {     'name': 'col0',
                                           'type': 'string'},
                                       {   'name': 'col1',
                                           'type': 'string'},
                                       /* Other columns ... */
                                       ],
                       'userModified': False},
        'tags': ['creator_admin'],
        'type': 'Filesystem'},
...
]
```

### Deleting a dataset

```python
dataset = project.get_dataset('TEST_DATASET')
dataset.delete(drop_data=True)
```

### Modifying tags for a dataset

```{code-block} python
:name: ce/datasets/datasets-other/modifying-tags-for-a-dataset
:caption: Modifying tags for a dataset

dataset = project.get_dataset("mydataset")
settings = dataset.get_settings()

print("Current tags are %s" % settings.tags)

# Change the tags
settings.tags = ["newtag1", "newtag2"]

# If we changed the settings, we must save
settings.save()
```


### Modifying the description for a dataset

```{code-block} python
:name: ce/datasets/datasets-other/modifying-the-description-for-a-dataset
:caption: Modifying the description for a dataset

dataset = project.get_dataset("mydataset")
settings = dataset.get_settings()

# To change the short description
settings.short_description = "Small description"

# To change the long description
settings.description = """Very long description
with multiline"""

settings.save()
```


### Reading and modifying the schema of a dataset

:::{warning}
Using {class}`~dataikuapi.dss.dataset.DSSDataset` to modify the schema from within a DSS job would not be taken into account for subsequent
activities in the job.
:::

```python
dataset = project.get_dataset("mydataset")
settings = dataset.get_settings()

for column in settings.get_raw().get('schema').get('columns'):
        print("Have column name=%s type=%s" % (column["name"], column["type"]))

# Now, let's add a new column in the schema
settings.add_raw_schema_column({"name" : "test", "type": "string"})

# If we changed the settings, we must save
settings.save()
```

### Modifying the meaning or comment of a column in a dataset

```{code-block} python
:name: ce/datasets/datasets-other/modifying-meaning-of-a-column
:caption: Modifying the meaning or comment of a column in a dataset

name_of_the_column = "example"
meaning_of_the_column = "Existing meaning"
comment_if_the_column = "My comment"


dataset = project.get_dataset("mydataset")
schema = dataset.get_schema()
for col in schema['columns']:
    if col['name'] == name_of_the_column:
        col['meaning'] = meaning_of_the_column
        col['comment'] = comment_if_the_column
        
dataset.set_schema(schema)

```
### Building a dataset

You can start a job in order to build the dataset

```python
dataset = project.get_dataset("mydataset")

# Build the dataset non recursively and waits for build to complete.
#Returns a :meth:`dataikuapi.dss.job.DSSJob`
job = dataset.build()

# Builds the dataset recursively
dataset.build(job_type="RECURSIVE_BUILD")

# Build a partition (for partitioned datasets)
dataset.build(partitions="partition1")
```

## Programmatic creation and setup (external datasets)

The API allows you to leverage Dataiku's automatic detection and configuration capabilities in order to programmatically create datasets or programmatically "autocomplete" the settings of a dataset.

### SQL dataset: Programmatic creation

```python
dataset = project.create_sql_table_dataset("mydataset", "PostgreSQL", "my_sql_connection", "database_table_name", "database_schema")

# At this point, the dataset object has been initialized, but the schema of the underlying table
# has not yet been fetched, so the schema of the table and the schema of the dataset are not yet consistent

# We run autodetection
settings = dataset.autodetect_settings()
# settings is now an object containing the "suggested" new dataset settings, including the completed schema
# We can just save the new settings in order to "accept the suggestion"
settings.save()
```

### SQL dataset: Modifying settings

The object returned by {meth}`dataikuapi.dss.dataset.DSSDataset.get_settings` depends on the kind of dataset.

For a SQL dataset, it will be a {class}`dataikuapi.dss.dataset.SQLDatasetSettings`.

```python
dataset = project.get_dataset("mydataset")
settings = dataset.get_settings()

# Set the table targeted by this SQL dataset
settings.set_table(connection="myconnection", schema="myschema", table="mytable")
settings.save()

# If we have changed the table, there is a good chance that the schema is not good anymore, so we must
# have DSS redetect it. `autodetect_settings` will however only detect if the schema is empty, so let's clear it.
del settings.schema_columns[:]
settings.save()

# Redetect and save the suggestion
settings = dataset.autodetect_settings()
settings.save()
```

### Files-based dataset: Programmatic creation

#### Generic method for most connections

This applies to all files-based datasets, but may require additional setup

```python
dataset = project.create_fslike_dataset("mydataset", "HDFS", "name_of_connection", "path_in_connection")

# At this point, the dataset object has been initialized, but the format is still unknown, and the
# schema is empty, so the dataset is not yet usable

# We run autodetection
settings = dataset.autodetect_settings()
# settings is now an object containing the "suggested" new dataset settings, including the detected format
# and completed schema
# We can just save the new settings in order to "accept the suggestion"
settings.save()
```

#### Quick helpers for some connections

```python
# For S3: allows you to specify the bucket (if the connection does not already force a bucket)
dataset = project.create_s3_dataset(dataset_name, connection, path_in_connection, bucket=None)
```

### Uploaded datasets: programmatic creation and upload

```python
dataset = project.create_upload_dataset("mydataset") # you can add connection= for the target connection

with open("localfiletoupload.csv", "rb") as f:
        dataset.uploaded_add_file(f, "localfiletoupload.csv")

# At this point, the dataset object has been initialized, but the format is still unknown, and the
# schema is empty, so the dataset is not yet usable

# We run autodetection
settings = dataset.autodetect_settings()
# settings is now an object containing the "suggested" new dataset settings, including the detected format
# andcompleted schema
# We can just save the new settings in order to "accept the suggestion"
settings.save()
```

### Manual creation

You can create and setup all parameters of a dataset yourself. We do not recommend using this method.

For example loading the csv files of a folder

```python
project = client.get_project('TEST_PROJECT')
folder_path = 'path/to/folder/'
for file in listdir(folder_path):
    if not file.endswith('.csv'):
        continue
    dataset = project.create_dataset(file[:-4]  # dot is not allowed in dataset names
        ,'Filesystem'
        , params={
            'connection': 'filesystem_root'
            ,'path': folder_path + file
        }, formatType='csv'
        , formatParams={
            'separator': ','
            ,'style': 'excel'  # excel-style quoting
            ,'parseHeaderRow': True
        })
    df = pandas.read_csv(folder_path + file)
    dataset.set_schema({'columns': [{'name': column, 'type':'string'} for column in df.columns]})
```

## Programmatic creation and setup (managed datasets)

Managed datasets are much easier to create because they are managed by DSS

### Creating a new SQL managed dataset

```python
builder = project.new_managed_dataset("mydatasetname")
builder.with_store_into("mysqlconnection")
dataset = builder.create()
```

### Creating a new Files-based managed dataset with a specific schema

```python
builder = project.new_managed_dataset("mydatasetname")
builder.with_store_into("myhdfsconnection", format_option_id="PARQUET_HIVE")
dataset = builder.create()
```

### Creating a new partitioned managed dataset

This dataset copies partitioning from an existing dataset

```python
builder = project.new_managed_dataset("mydatasetname")
builder.with_store_into("myhdfsconnection")
builder.with_copy_partitioning_from("source_dataset")
dataset = builder.create()
```

## Flow handling

For more details, please see {doc}`../flow` on programmatic flow building.

### Creating recipes from a dataset

This example creates a sync recipe to sync a dataset to another

```python
recipe_builder = dataset.new_recipe("sync")
recipe_builder.with_new_output("target_dataset", "target_connection_name")
recipe = recipe_builder.create()

# recipe is now a :class:`dataikuapi.dss.recipe.DSSRecipe`, and you can run it
recipe.run()
```

This example creates a code recipe from this dataset

```python
recipe_builder = dataset.new_recipe("python")
recipe_builder.with_script("""
import dataiku
from dataiku import recipe

input_dataset = recipe.get_inputs_as_datasets()[0]
output_dataset = recipe.get_outputs_as_datasets()[0]

df = input_dataset.get_dataframe()
df = df.groupby("mycol").count()

output_dataset.write_with_schema(df)
""")
recipe_builder.with_new_output_dataset("target_dataset", "target_connection_name")
recipe = recipe_builder.create()

# recipe is now a :class:`dataikuapi.dss.recipe.DSSRecipe`, and you can run it
recipe.run()
```

## ML & Statistics

### Creating ML models

You can create a ML Task in order to train models based on a dataset. See {doc}`../ml` for more details.

```python
dataset = project.get_dataset('mydataset')
mltask = dataset.create_prediction_ml_task("variable_to_predict")
mltask.train()
```

### Creating statistics worksheets

For more details, please see {doc}`../statistics`

```python
dataset = project.get_dataset('mydataset')
ws = dataset.create_statistics_worksheet(name="New worksheet")
```

## Misc operations

### Listing partitions

For partitioned datasets, the list of partitions is retrieved with {meth}`~dataikuapi.dss.dataset.DSSDataset.list_partitions()`:

```python
partitions = dataset.list_partitions()
# partitions is a list of string
```

### Clearing data

The rows of the dataset can be cleared, entirely or on a per-partition basis, with the {meth}`~dataikuapi.dss.dataset.DSSDataset.clear()` method.

```python
dataset = project.get_dataset('SOME_DATASET')
dataset.clear(['partition_spec_1', 'partition_spec_2'])         # clears specified partitions
dataset.clear()                                                                                         # clears all partitions
```

### Hive operations

For datasets associated with a table in the Hive metastore, the synchronization of the table definition in the metastore with the dataset's schema in DSS will be needed before it can be visible to Hive, and usable by Impala queries.

```python
dataset = project.get_dataset('SOME_HDFS_DATASET')
dataset.synchronize_hive_metastore()
```

Or in the other direction, to synchronize the dataset's information from Hive

```python
dataset = project.get_dataset('SOME_HDFS_DATASET')
dataset.update_from_hive()

# This will have the updated settings
settings = dataset.get_settings()
```

## Detailed examples

This section contains more advanced examples on Datasets.

### Clear tagged Datasets 

You can programmatically clear specific Datasets that match a given list of tags. The following code snippets will clear all Datasets that match *any* of the names in the `tag` variable:

```python
tags = ["DEPRECATED", "TO_DELETE"]
datasets_to_clear = []
for ds_item in project.list_datasets():
    tag_intersection = list(set(tags) & set(ds_item["tags"]))
    if tag_intersection:
            datasets_to_clear.append(ds_item["name"])
for d in datasets_to_clear:
    project.get_dataset(d).clear()
```

To match *all* of the names in the `tag` variable:  

```python
tags = ["DEPRECATED", "TO_DELETE"]
datasets_to_clear = []
for ds_item in project.list_datasets():
    if set(tags) == set(ds_item["tags"]):
        to_clear.append(ds_item["name"])
for d in datasets_to_clear:
    project.get_dataset(d).clear()
```

### Compare Dataset schemas

If you want to compare the schemas of two Datasets you can leverage the {meth}`~dataikuapi.dss.dataset.DSSDataset.get_schema()` method. In the following code snippet the `common_columns` contains columns names found both in Datasets `ds_a` and `ds_b`: 


```{literalinclude} ../examples/datasets/compare-schemas.py
```

## Reference documentation

### Classes

```{eval-rst}
.. autosummary::
    dataikuapi.DSSClient
    dataikuapi.dss.dataset.DSSDataset
    dataikuapi.dss.dataset.DSSDatasetSettings
    dataikuapi.dss.dataset.DSSManagedDatasetCreationHelper
    dataikuapi.dss.dataset.SQLDatasetSettings
    dataikuapi.dss.project.DSSProject
    dataikuapi.dss.recipe.CodeRecipeCreator
    dataikuapi.dss.recipe.DSSRecipeCreator
    dataikuapi.dss.recipe.SingleOutputRecipeCreator
```

### Functions
```{eval-rst}
.. autosummary::
    ~dataikuapi.dss.dataset.DSSDataset.autodetect_settings
    ~dataikuapi.dss.dataset.DSSDataset.build
    ~dataikuapi.dss.dataset.DSSDataset.clear
    ~dataikuapi.dss.dataset.DSSManagedDatasetCreationHelper.create
    ~dataikuapi.dss.recipe.DSSRecipeCreator.create
    ~dataikuapi.dss.dataset.DSSDataset.create_prediction_ml_task
    ~dataikuapi.dss.dataset.DSSDataset.create_statistics_worksheet
    ~dataikuapi.dss.project.DSSProject.create_sql_table_dataset
    ~dataikuapi.dss.project.DSSProject.create_upload_dataset
    ~dataikuapi.dss.dataset.DSSDataset.delete
    ~dataikuapi.dss.project.DSSProject.get_dataset
    ~dataikuapi.dss.dataset.DSSDatasetSettings.get_raw
    ~dataikuapi.dss.dataset.DSSDataset.get_schema
    ~dataikuapi.dss.dataset.DSSDataset.get_settings
    ~dataikuapi.DSSClient.get_default_project
    ~dataikuapi.DSSClient.get_project
    ~dataikuapi.dss.project.DSSProject.list_datasets
    ~dataiku.Dataset.list_partitions
    ~dataikuapi.dss.project.DSSProject.new_managed_dataset
    ~dataikuapi.dss.dataset.DSSDataset.new_recipe
    ~dataikuapi.dss.recipe.DSSRecipe.run
    ~dataikuapi.dss.dataset.DSSDatasetSettings.save
    ~dataikuapi.dss.dataset.SQLDatasetSettings.set_table
    ~dataikuapi.dss.recipe.SingleOutputRecipeCreator.with_new_output
    ~dataikuapi.dss.recipe.CodeRecipeCreator.with_new_output_dataset
    ~dataikuapi.dss.recipe.CodeRecipeCreator.with_script
    ~dataikuapi.dss.dataset.DSSManagedDatasetCreationHelper.with_store_into
```
