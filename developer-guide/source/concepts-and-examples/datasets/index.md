(datasets)=

```{eval-rst}
..
  this code samples has been verified on DSS: 13.2.0
  Date of check: 19/09/2024
  
  this code samples has been "verified" on DSS: 14.1.0
  Date of check: 06/08/2025

```

# Datasets

:::{note}
There are two main classes related to datasets handling in Dataiku's Python APIs:

- {py:class}`dataiku.core.dataset.Dataset` in the `dataiku` package, which deals primarily with reading and writing data. It has the most flexibility when it comes to reading and writing
- {py:class}`dataikuapi.dss.dataset.DSSDataset` in the `dataikuapi` package which is mostly used for creating datasets, managing their settings, building flows, creating ML models, and performing a wider range of operations on datasets.

For more details on the two packages, please see {doc}`../../getting-started/index`
:::

For starting code samples, please see [Python Recipes](https://doc.dataiku.com/dss/latest/code_recipes/python.html).

Detailed samples about interacting with datasets can be found in:

```{eval-rst}
.. toctree::
        :maxdepth: 1

        datasets-data
        datasets-other

```

Reference documentation for the classes supporting interaction with datasets can be found in {doc}`../../api-reference/python/datasets`