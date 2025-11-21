
(projects)=

```{eval-rst}
..
  this code samples has been verified on DSS: 14.1.0
  Date of check: 14/08/2025
  
  this code samples has been verified on DSS: 13.2.0
  Date of check: 23/09/2024
```

# Projects

[Projects](https://doc.dataiku.com/dss/latest/concepts/projects/index.html) are the main unit for organising workflows within the Dataiku platform.

## Basic operations

This section provides common examples of how to programmatically manipulate Projects.

### Listing Projects

The main identifier for Projects is the **Project Key**. The following can be run to access the list of Project Keys on a Dataiku instance:

```python
import dataiku
client = dataiku.api_client()

# Get a list of Project Keys
project_keys = client.list_project_keys()
```

### Handling an existing Project

To manipulate a Project and its associated items you first need to get its handle, in the form of a {py:class}`dataikuapi.dss.project.DSSProject` object. If the Project already exists on the instance, run:

```python
project = client.get_project("CHURN")
```

You can also directly get a handle on the current Project you are working on:

```python
project = client.get_default_project()
```

### Creating a new Project

The following code will create a new empty Project and return its handle:

```python
project = client.create_project(project_key="MYPROJECT",
                                    name="My very own project",
                                    owner="alice")
```

You can also duplicate an existing Project and get a handle on its copy:

```python
original_project = client.get_project("CHURN")
copy_result = original_project.duplicate(target_project_key="CHURNCOPY",
                                          target_project_name="Churn (copy)")
project = client.get_project(copy_result.get('targetProjectKey', None))
```

Finally, you can import a Project archive (zip file) and get a handle on the resulting Project.
The newly imported Project should not already exist, and the `projectKey` must be unique.

```python
archive_path = "/path/to/archive.zip"
with open(archive_path, "rb") as f:
    import_result = client.prepare_project_import(f).execute()
    # TODO Get handle
```

### Accessing Project items

Once your Project handle is created, you can use it to create, list and interact with Project items:

```python
# Print the names of all Datasets in the Project:
for d in project.list_datasets():
    print(d.name)

# Create a new empty Managed Folder:
folder = project.create_managed_folder(name="myfolder")

# Get a handle on a Dataset:
customer_data = project.get_dataset("customers")
```

(ce_projects_exporting_a_project)=
### Exporting a Project

To create a Project export archive and save it locally (i.e. on the Dataiku instance server), run the following:

```python
import os
dir_path = "path/to/your/project/export/directory"
archive_name = f"{project.project_key}.zip"
with project.get_export_stream() as s:
    target = os.path.join(dir_path, archive_name)
    with open(target, "wb") as f:
        for chunk in s.stream(512):
            f.write(chunk)
```

### Deleting a Project

To delete a Project and all its associated objects, run the following:

```python
project.delete()
```

```{warning}
While the Project's Dataset objects will be deleted, by default the underlying data will remain. To clear the data as well, set the `clear_managed_datasets` argument to `True`. **The deletion operation is permanent so use this method with caution.**
```
## Detailed examples

This section contains more advanced examples on Projects.
### Editing Project permissions

You can programmatically add or change Group permissions for a given Project using the {meth}`~dataikuapi.dss.project.DSSProject.set_permissions()` method. In the following example, the 'readers' Group is added to the `DKU_TSHIRTS` Project with read-only permissions:

```{literalinclude} examples/projects/edit-permissions.py
```
### Creating a Project with custom settings

You can add pre-built properties to your Projects when creating them using the API. This example illustrates how to generate a Project and define the following properties:
* name
* description
* tags
* status
* checklist

First, create a helper function to generate the checklist :

```{literalinclude} examples/projects/create-new-custom-project.py
:lines: 4-18
```

You can now write the creation function, which wraps the {meth}`~dataikuapi.DSSClient.create_project()` method and returns a handle to the newly-created Project:

```{literalinclude} examples/projects/create-new-custom-project.py
:lines: 20-47
```

This is how you would call this function:

```{literalinclude} examples/projects/create-new-custom-project.py
:lines: 50-65
```

### Export multiple Projects at once

If instead of just {ref}`exporting a single Project <ce_projects_exporting_a_project>` you want to generate exports several Projects in one go and store the resulting archives in a local Managed Folder, you can extend the usage of {meth}`~dataikuapi.dss.project.DSSProject.get_export_stream()` with the following example:

```{literalinclude} examples/projects/export-multiple-projects.py
```

## Reference documentation

### Classes

```{eval-rst}
.. autosummary::
    dataiku.Folder
    dataikuapi.dss.project.DSSProject
  	dataikuapi.dss.project.DSSProjectGit
    dataiku.Project

```

### Functions
```{eval-rst}
.. autosummary::
    ~dataikuapi.dss.project.DSSProject.create_managed_folder
    ~dataikuapi.DSSClient.create_project
    ~dataikuapi.dss.project.DSSProject.delete
    ~dataikuapi.dss.project.DSSProject.duplicate
    ~dataikuapi.DSSClient.get_auth_info
    ~dataikuapi.dss.project.DSSProject.get_dataset
    ~dataikuapi.dss.project.DSSProject.get_export_stream
    ~dataikuapi.DSSClient.get_default_project
    ~dataikuapi.dss.project.DSSProject.get_metadata
    ~dataiku.Folder.get_path
    ~dataikuapi.dss.project.DSSProject.get_permissions 
    ~dataikuapi.DSSClient.get_project
    ~dataikuapi.dss.project.DSSProject.get_settings
    ~dataikuapi.dss.project.DSSProject.get_tags
    ~dataikuapi.dss.project.DSSProject.list_datasets
    ~dataikuapi.DSSClient.list_project_keys
    ~dataikuapi.dss.project.DSSProject.set_metadata
    ~dataikuapi.dss.project.DSSProject.set_permissions
    ~dataikuapi.dss.project.DSSProject.set_tags
```