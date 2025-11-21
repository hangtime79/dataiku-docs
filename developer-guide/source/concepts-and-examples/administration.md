(administration)=

```{eval-rst}
..
  this code samples has been verified on DSS: 14.2.0-alpha3
  Date of check: 11/09/2025

  this code samples has been verified on DSS: 13.2.0
  Date of check: 04/10/2024
```

# Administration

Here are some more global administration tasks that can be performed using the DSS Public API:

- Reading and writing general instance settings
- Managing user and group impersonation rules for [User Isolation Framework](https://doc.dataiku.com/dss/latest/user-isolation/index.html)
- Managing (creating/modifying) code environments
- Managing instance variables
- Listing long-running tasks, getting their status, aborting them
- Listing running notebooks, getting their status, unloading them
- Managing global API keys
- Listing global DSS usages (projects, datasets, recipes, scenarios...)
- Managing personal API keys

## Detailed examples

This section contains more advanced examples on administration tasks.

### List running Jupyter notebooks

You can use {py:meth}`dataikuapi.dss.project.DSSProject.list_jupyter_notebooks` to retrieve a list of notebooks for a given Project, along with useful metadata. 

```{literalinclude} examples/administration/list-running-notebooks.py
```

## Reference documentation

### Classes

```{eval-rst}
.. autosummary::
  dataikuapi.dss.admin.DSSGeneralSettings
  dataikuapi.dss.admin.DSSUserImpersonationRule
  dataikuapi.dss.admin.DSSGroupImpersonationRule
  dataikuapi.dss.admin.DSSInstanceVariables
  dataikuapi.dss.future.DSSFuture
  dataikuapi.dss.jupyternotebook.DSSJupyterNotebook
  dataikuapi.dss.jupyternotebook.DSSJupyterNotebookListItem
  dataikuapi.dss.jupyternotebook.DSSNotebookSession
  dataikuapi.dss.jupyternotebook.DSSNotebookContent
  dataikuapi.dss.sqlnotebook.DSSSQLNotebook
  dataikuapi.dss.sqlnotebook.DSSSQLNotebookListItem
  dataikuapi.dss.sqlnotebook.DSSNotebookContent
  dataikuapi.dss.sqlnotebook.DSSNotebookHistory
  dataikuapi.dss.sqlnotebook.DSSNotebookQueryRunListItem
  dataikuapi.dss.notebook.DSSNotebook
  dataikuapi.dss.admin.DSSGlobalApiKey
  dataikuapi.dss.admin.DSSGlobalApiKeyListItem
  dataikuapi.dss.admin.DSSPersonalApiKey
  dataikuapi.dss.admin.DSSPersonalApiKeyListItem
```

### Functions

```{eval-rst}
.. autosummary::
    ~dataikuapi.DSSClient.get_project
    ~dataikuapi.dss.jupyternotebook.DSSJupyterNotebook.get_sessions
    ~dataikuapi.dss.project.DSSProject.list_jupyter_notebooks
    ~dataikuapi.DSSClient.list_projects
```