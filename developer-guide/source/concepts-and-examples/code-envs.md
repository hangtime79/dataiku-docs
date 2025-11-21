(code-envs)=

```{eval-rst}
..
  this code samples has been verified on DSS: 14.2.0-beta1
  Date of check: 17/09/2025

  this code samples has been verified on DSS: 13.2.0
  Date of check: 29/09/2024
```
# Code envs

The API offers methods to:

- Create code envs
- Read and write settings and packages of code envs
- Update code envs
- Reinstall
- Set code environment resources environment variables

## Creating a code env

### Code env with default Python without Jupyter support

```python
client = dataiku.api_client()

# Create the code env
code_env = client.create_code_env("PYTHON", "my_code_env_name", "DESIGN_MANAGED")

# Setup packages to install
definition = code_env.get_settings()
definition.settings["desc"]["installCorePackages"] = True

# We want to install 2 packages (tabulate and nameparser)
definition.settings["specPackageList"] = "tabulate\nnameparser"

# Save the new settings
definition.save()

# Actually perform the installation
code_env.update_packages()
```

### Code env with specific Python version with Jupyter support

```python
client = dataiku.api_client()

# Create the code env
code_env = client.create_code_env("PYTHON", "my_code_env_name", 
                                  "DESIGN_MANAGED", {"pythonInterpreter": "PYTHON310"})

# Setup packages to install
definition = code_env.get_settings()
definition.settings["desc"]["installCorePackages"] = True
definition.settings["desc"]["installJupyterSupport"] = True

# We want to install 2 packages (tabulate and nameparser)
definition.settings["specPackageList"] = "tabulate\nnameparser"

# Save the new settings
definition.save()

# Actually perform the installation
code_env.update_packages()
code_env.set_jupyter_support(True)
```

## Managing the code environment resources directory environment variables

These methods may only be called from a resource initialization script. See [Managed code environment resources directory](https://doc.dataiku.com/dss/latest/code-envs/operations-python.html#code-env-resources-directory).

```python
from dataiku.code_env_resources import clear_all_env_vars
from dataiku.code_env_resources import delete_env_var
from dataiku.code_env_resources import get_env_var
from dataiku.code_env_resources import set_env_var
from dataiku.code_env_resources import set_env_path

# Delete all environment variables from the code environment runtime
clear_all_env_vars()

# Set a raw environment variable for the code environment runtime
set_env_var("ENV_VAR", "42")

# Set a relative path environment variable to be loaded at runtime
# (relative path with respect to the code env resources directory)
set_env_path("TFHUB_CACHE_DIR", "tensorflow")

# Get an environment variable from the code environment runtime
print("TFHUB_CACHE_DIR:", get_env_var("TFHUB_CACHE_DIR"))

# Delete an environment variable from the code environment runtime
delete_env_var("ENV_VAR")

# Then download pre-trained models in the resources directory, e.g.
# for TensorFlow
# import tensorflow_hub
# tensorflow_hub.KerasLayer("https://tfhub.dev/google/imagenet/mobilenet_v2_140_224/classification/4")
```

**(Advanced)** The method `dataiku.code_env_resources.fetch_from_backend` allows to fetch specific resources files or folders from the
backend, when running in containerized execution. It is meant to be called in a python recipe/notebook, when the
resources were not already copied or initialized for containerized execution at build time (see [Code environment resources directory](https://doc.dataiku.com/dss/latest/containers/code-envs.html#code-env-resources-containerized)).

```python
from dataiku.code_env_resources import fetch_from_backend

# Fetch resources files and folders from the backend
fetch_from_backend([
    "pytorch/hub/checkpoints/fasterrcnn_resnet50_fpn_coco-258fb6c6.pth",
    "huggingface/",
])

# Load pre-trained models as usual
```

## Detailed examples

### Get Recipes using specific Code Environments 

When editing a Code Environment you may want to assess which Code Recipe is using that environment and thus could be affected by the changes. The following code snippet allows you to get such a mapping:

```{literalinclude} examples/code-envs/map-code-envs.py
```

## Reference documentation

### Classes

```{eval-rst}
.. autosummary::
    dataikuapi.dss.admin.DSSAutomationCodeEnvSettings
    dataikuapi.dss.admin.DSSAutomationCodeEnvVersionSettings
    dataikuapi.DSSClient
    dataikuapi.dss.admin.DSSCodeEnv
    dataikuapi.dss.admin.DSSDesignCodeEnvSettings
    dataikuapi.dss.admin.DSSGeneralSettings
    dataikuapi.dss.project.DSSProject
    dataikuapi.dss.project.DSSProjectSettings
```

### Functions

```{eval-rst}
.. autosummary::
  ~dataikuapi.DSSClient.create_code_env
  ~dataikuapi.DSSClient.get_default_project
  ~dataikuapi.DSSClient.get_general_settings
  ~dataikuapi.dss.admin.DSSCodeEnv.get_settings
  ~dataikuapi.dss.project.DSSProject.get_settings
  ~dataikuapi.dss.project.DSSProject.list_recipes
  ~dataikuapi.dss.admin.DSSAutomationCodeEnvSettings.save
  ~dataikuapi.dss.admin.DSSDesignCodeEnvSettings.save
  ~dataikuapi.dss.admin.DSSCodeEnv.set_jupyter_support
  ~dataikuapi.dss.admin.DSSCodeEnv.update_packages

```