(project-folders)=

```{eval-rst}
..
  this code samples has been verified on DSS: 14.2.0-beta1
  Date of check: 17/09/2025

  this code samples has been verified on DSS: 13.2.0
  Date of check: 26/09/2024
```

# Project folders

You can interact with project folders through the API.

## Basic operations

The ROOT project folder can be retrieved with the {meth}`~dataikuapi.DSSClient.get_root_project_folder` method.

```python
root_folder = client.get_root_project_folder()
```

Alternatively any project folder can be retrieved with its ID with the {meth}`~dataikuapi.DSSClient.get_project_folder` method.

```python
project_folder = client.get_project_folder(project_folder_id)
```

You can obtain the `project_folder_id` by using or adapting this function:
```python
def list_child_project(folder_id, prefix="", print_project=False):
    folder = client.get_project_folder(folder_id)
    print(prefix + "+", folder.name, " --> ", folder.id)
    if print_project:
        [print(prefix + "|--", p.project_key, "(", p.get_metadata().get('label'), ")")
         for p in client.get_project_folder(folder.id).list_projects()]
    children = folder.list_child_folders()
    if children:
        [list_child_project(child.id, prefix+"+--",print_project) for child in children]

list_child_project(root_folder.id)
```
Getting basic attributes:

```python
# Getting the id of a project folder (for "get_project_folder")
id = project_folder.id

# Getting the name of a project folder:
name = project_folder.name

# Getting the "virtual path" of a project folder (NB: for information purpose only, does not hold special significance)
path = project_folder.get_path()
```

## Navigating within project folders

In order to navigate from a project folder, its parent and children can be retrieved.

```python
parent = project_folder.get_parent()
children = project_folder.list_child_folders()
```

This will list all its projects.

```python
project_key_list = project_folder.list_project_keys()
project_list = project_folder.list_projects()
```

## Finding the folder of a project

From a project, you can find its project folder

```python
project = client.get_project("MYPROJECT")
folder = project.get_project_folder()
print("Project is in folder %s (path %s)" % (folder.name, folder.get_path()))
```

## Creating entities

To create a child project folder, use the {py:meth}`~dataikuapi.dss.projectfolder.DSSProjectFolder.create_sub_folder` method.

```python
# Creating a new project folder
newborn_child = project_folder.create_sub_folder(project_folder_name)

# Creating a project directly into a project folder
new_project = project_folder.create_project(project_key, project_name, owner)
```

## Moving entities

To move a project folder to another location (into another project folder), use the {py:meth}`~dataikuapi.dss.projectfolder.DSSProjectFolder.move_to` method.

```python
project_folder.move_to(new_parent)

project_folder.move_project_to(project_key, new_parent)
```

You can also move a project directly

```python
project.move_to_folder(target_folder)
```

## Managing project folders

### Deleting a project folder

```python
project_folder.delete()
```

### Modifying settings

```python
project_folder_settings = project_folder.get_settings()
project_folder_settings.set_name(new_name)
project_folder_settings.set_owner(new_owner)
project_folder_permissions = project_folder_settings.get_permissions()
new_perm = {'read': False, 'writeContents': False, 'admin': False}
project_folder_permissions.append(new_perm)
project_folder_settings.save()
```

## Reference documentation

### Classes
```{eval-rst}
.. autosummary::
        dataikuapi.dss.projectfolder.DSSProjectFolder
        dataikuapi.dss.projectfolder.DSSProjectFolderSettings
```

### Functions

```{eval-rst}
.. autosummary::
    ~dataikuapi.dss.projectfolder.DSSProjectFolder.create_project
    ~dataikuapi.dss.projectfolder.DSSProjectFolder.create_sub_folder
    ~dataikuapi.dss.projectfolder.DSSProjectFolder.delete
    ~dataikuapi.dss.projectfolder.DSSProjectFolder.get_path
    ~dataikuapi.dss.projectfolder.DSSProjectFolder.get_parent
    ~dataikuapi.dss.projectfolder.DSSProjectFolderSettings.get_permissions
    ~dataikuapi.DSSClient.get_project_folder
    ~dataikuapi.DSSClient.get_root_project_folder
    ~dataikuapi.dss.projectfolder.DSSProjectFolder.get_settings
    ~dataikuapi.dss.projectfolder.DSSProjectFolder.list_child_folders
    ~dataikuapi.dss.projectfolder.DSSProjectFolder.list_projects
    ~dataikuapi.dss.projectfolder.DSSProjectFolder.list_project_keys
    ~dataikuapi.dss.projectfolder.DSSProjectFolder.move_project_to
    ~dataikuapi.dss.projectfolder.DSSProjectFolder.move_to
    ~dataikuapi.dss.project.DSSProject.move_to_folder
    ~dataikuapi.dss.projectfolder.DSSProjectFolderSettings.save
    ~dataikuapi.dss.projectfolder.DSSProjectFolderSettings.set_name
    ~dataikuapi.dss.projectfolder.DSSProjectFolderSettings.set_owner
    
```
