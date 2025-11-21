(feature-store)=

```{eval-rst}
..
  this code samples has been verified on DSS: 14.2.0-alpha3
  Date of check: 16/09/2025

  this code samples has been verified on DSS: 13.2.0
  Date of check: 03/10/2024
```

# Feature Store

The public API allows you to:

- list feature groups {meth}`dataikuapi.dss.feature_store.DSSFeatureStore.list_feature_groups`
- check if a dataset is a feature group {meth}`dataikuapi.dss.dataset.DSSDatasetSettings.is_feature_group`
- set/unset a dataset as a feature group: {meth}`dataikuapi.dss.dataset.DSSDatasetSettings.set_feature_group`

See [Feature Store](https://doc.dataiku.com/dss/latest/mlops/feature-store/index.html) for more information.

## Listing feature groups

```python
import dataiku

# if using API from inside DSS
client = dataiku.api_client()

feature_store = client.get_feature_store()

feature_groups = feature_store.list_feature_groups()

for feature_group in feature_groups:
    print("{}".format(feature_group.id))
```

:::{note}
This will only display feature groups of projects on which the user has at least read permission
:::

:::{note}
Because of indexing latency, you have have to wait a few seconds before newly defined feature groups are visible
:::

## (Un)setting a dataset as a Feature Group

```python
import dataiku

# if using API from inside DSS
client = dataiku.api_client()

project = client.get_project('PROJECT_ID')

ds = project.get_dataset('DATASET_ID')

ds_settings = ds.get_settings()

# pass False to undefine as Feature Group
ds_settings.set_feature_group(True)

ds_settings.save()
```

## Collecting feature groups with a specific meaning

```python
import dataiku

# if using API from inside DSS
client = dataiku.api_client()

# Define the meaning ID to look for
meaning="doublemeaning"

result = set()

# List feature group
feature_store = client.get_feature_store()
feature_groups = feature_store.list_feature_groups()
feature_groups = [ feature_group.id for feature_group in feature_groups ]

# Search for meaning
for f in feature_groups:
    data = f.split('.')
    project = client.get_project(data[0])
    dataset = project.get_dataset(data[1])
    schema = dataset.get_schema()
    for col in schema['columns']:
        if ('meaning' in col) and (col['meaning'] == meaning):
            result.add(f)
print(result)
```

## Documenting a feature store

There are several ways to document a feature group, acting on the underlying dataset:

- [Adding a description](ce/datasets/datasets-other/modifying-the-description-for-a-dataset)
- [Adding some tags](ce/datasets/datasets-other/modifying-tags-for-a-dataset)
- [Describing the schema (meaning and comment)](ce/datasets/datasets-other/modifying-meaning-of-a-column) 


## Reference documentation


### Classes

```{eval-rst}
.. autosummary::
  dataikuapi.dss.feature_store.DSSFeatureStore
  dataikuapi.dss.feature_store.DSSFeatureGroupListItem
```

### Functions

```{eval-rst}
.. autosummary::
    ~dataikuapi.dss.project.DSSProject.get_dataset
    ~dataikuapi.DSSClient.get_feature_store
    ~dataikuapi.DSSClient.get_project
    ~dataikuapi.dss.dataset.DSSDataset.get_schema
    ~dataikuapi.dss.dataset.DSSDataset.get_settings
    ~dataikuapi.dss.feature_store.DSSFeatureStore.list_feature_groups
    ~dataikuapi.dss.dataset.DSSDatasetSettings.save
    ~dataikuapi.dss.dataset.DSSDatasetSettings.set_feature_group
```
