(plugins)=

```{eval-rst}
..
  this code samples has been verified on DSS: 14.2.0-beta1
  Date of check: 17/09/2025

  this code samples has been verified on DSS: 13.2.0
  Date of check: 26/09/2024
```

# Plugins

The API offers methods to:

- Install plugins
- Uninstall plugins and list their usages
- Update plugins
- Read and write plugin settings
- Create and update plugin code envs
- List macros that can be run
- Run macros

## Installing plugins

### From a Zip file

```python
with open("myplugin.zip", "rb") as f:
    client.install_plugin_from_archive(f)
```

### From the Dataiku plugin store

```python
future = client.install_plugin_from_store("googlesheets")
future.wait_for_result()
```

### From a Git repository

```python
future = client.install_plugin_from_git("git@github.com:myorg/myrepo")
future.wait_for_result()
```

## Uninstalling plugins

### Listing usages of a plugin

```python
plugin = client.get_plugin('my-plugin-id')
usages = plugin.list_usages()
```

### Uninstalling a plugin

```python
plugin = client.get_plugin('my-plugin-id')
future = plugin.delete()
```

Plugin deletion fails if a usage is detected. It can be forced with `force=True`:

```python
plugin = client.get_plugin('my-plugin-id')
future = plugin.delete(force=True)
```

## Managing code envs

```python
plugin = client.get_plugin("myplugin")

# Start creating the code env, and wait for it to be done
future = plugin.create_code_env()
result = future.wait_for_result()

# NB: If the plugin requires Python 3.9 for example, you will use something like:
# future = plugin.create_code_env(python_interpreter="PYTHON39")
# result = future.wait_for_result()

# Now the code env is created, but we still need to configure the plugin to use it
settings = plugin.get_settings()
settings.set_code_env(result["envName"])
settings.save()
```

## Handling settings

```python
plugin = client.get_plugin("myplugin")

# Obtain the current settings
settings = plugin.get_settings()
raw_settings = settings.get_raw()

# Modify the settings
# ...

# And save them back
settings.save()
```

## Reference documentation

### Classes

```{eval-rst}
.. autosummary::
  dataikuapi.dss.future.DSSFuture
  dataikuapi.dss.macro.DSSMacro
  dataikuapi.dss.plugin.DSSMissingType
  dataikuapi.dss.plugin.DSSPlugin
  dataikuapi.dss.plugin.DSSPluginSettings
  dataikuapi.dss.plugin.DSSPluginParameterSet
  dataikuapi.dss.plugin.DSSPluginUsage
  dataikuapi.dss.plugin.DSSMissingType
  dataikuapi.dss.plugin.DSSPluginUsages
```

### Functions

```{eval-rst}
.. autosummary::
  ~dataikuapi.dss.plugin.DSSPlugin.create_code_env
  ~dataikuapi.dss.plugin.DSSPlugin.delete
  ~dataikuapi.DSSClient.get_plugin
  ~dataikuapi.dss.plugin.DSSPlugin.get_settings
  ~dataikuapi.DSSClient.install_plugin_from_archive
  ~dataikuapi.DSSClient.install_plugin_from_git
  ~dataikuapi.DSSClient.install_plugin_from_store
  ~dataikuapi.dss.plugin.DSSPlugin.list_usages
  ~dataikuapi.dss.plugin.DSSPluginSettings.save
  ~dataikuapi.dss.plugin.DSSPluginSettings.set_code_env
  ~dataikuapi.dss.future.DSSFuture.wait_for_result
```