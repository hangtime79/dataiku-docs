(managed-folders)=

```{eval-rst}
..  
  this code samples has been verified on DSS: 14.2.0
  Date of check: 19/09/2025
```

# Managed folders

:::{note}
There are two main classes related to managed folder handling in Dataiku's Python APIs:

- {class}`dataiku.Folder` in the `dataiku` package. It was initially designed for usage within DSS in recipes and Jupyter notebooks.
- {class}`dataikuapi.dss.managedfolder.DSSManagedFolder` in the `dataikuapi` package. It was initially designed for usage outside of DSS.

Both classes have fairly similar capabilities, but we recommend using {class}`dataiku.Folder` within DSS.

For more details on the two packages, please see {doc}`../getting-started/index`
:::

## Detailed examples

This section contains more advanced examples on Managed Folders.

### Load a model from a remote Managed Folder

If you have a trained model artifact stored remotely (e.g. using a cloud object storage Connection like AWS S3), then you can leverage it in a code Recipe. To do so, you first need to download the artifact and temporarily store it on the Dataiku instance's local filesystem. The following code sample illustrates an example using a Tensorflow serialized model and assumes that it is stored in a Managed Folder called `spam_detection` alog with the following files:

- `saved_model.pb`
- `variables/variables.data-00000-of-00001`
- `variables/variables.index`


```{literalinclude} examples/managed-folders/load-model-from-remote.py
```

## Reference documentation

Use the following class to interact with managed folders in Python recipes and notebooks. For more information see [Managed folders](https://doc.dataiku.com/dss/latest/connecting/managed_folders.html) and [Usage in Python](https://doc.dataiku.com/dss/latest/connecting/managed_folders.html#usage-in-python) for usage examples of the Folder API.

### Classes

```{eval-rst}
.. autosummary::
    dataiku.Folder
    dataikuapi.dss.managedfolder.DSSManagedFolder
    dataikuapi.dss.managedfolder.DSSManagedFolderSettings
```

### Functions

```{eval-rst}
.. autosummary::
    ~dataiku.Folder.get_download_stream
    ~dataiku.Folder.list_paths_in_partition
```
