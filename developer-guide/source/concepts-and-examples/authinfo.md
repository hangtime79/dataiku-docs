(authinfo)=

```{eval-rst}
..
  this code samples has been verified on DSS: 13.2.0
  Date of check: 24/09/2024
  
  this code samples has been verified on DSS: 14.2.0
  Date of check: 15/09/2025
```

# Authentication information and impersonation

## Introduction

From any Python code, it is possible to retrieve information about the user or API key currently running this code.

This can be used:

- From code running within a recipe or notebook, for the code to know who is running said code
- From code running with a plugin recipe, for the code to know who is running said code
- From code running outside of DSS, simply to retrieve details of the current API key

Furthermore, the API provides the ability, from a set of HTTP headers, to identify the user represented by these headers. This can be used in the backend of a webapp (either Flask, FastAPI, Bokeh, Dash, or Streamlit), in order to securely identify which user is currently browsing the webapp.

## Code samples

### Getting your own login information

```python
import dataiku

client = dataiku.api_client()
auth_info = client.get_auth_info()

# auth_info is a dict which contains at least a "authIdentifier" field, which is the login for a user
print("User running this code is %s" % auth_info["authIdentifier"])
```

### Authenticating calls made from a webapp

Please see [Webapps and security](https://doc.dataiku.com/dss/latest/webapps/security.html) and [](/tutorials/webapps/common/impersonation/index)

### Impersonating another user

As a DSS administrator, it can be useful to be able to perform API calls on behalf of another user.

```python
import dataiku

client = dataiku.api_client()

user = client.get_user("the_user_to_impersonate")
client_as_user = user.get_client_as()

# All calls done using `client_as_user` will appear as being performed by `the_user_to_impersonate` and will inherit
# its permissions
```

### Modifying your own user properties

As a user (not an administrator), you can modify some of your own settings:

- User properties
- User secrets (see below)
- Per-user-credentials (see below)

```python
import dataiku

client = dataiku.api_client()
my_user = client.get_own_user()
settings = my_user.get_settings()
settings.user_properties["myprop"] = "myvalue"
settings.save()
```

### Modifying your own user secrets

```python
import dataiku

client = dataiku.api_client()
my_user = client.get_own_user()
settings = my_user.get_settings()
settings.add_secret("secretname", "secretvalue")
settings.save()
```

### Entering a per-user-credential for a connection, for yourself

To do it for other users, [Users and groups](https://doc.dataiku.com/dss/latest/python-api/users-groups.html).

```python
import dataiku

client = dataiku.api_client()
my_user = client.get_own_user()
settings = my_user.get_settings()
settings.set_basic_connection_credential("myconnection", "username", "password")
settings.save()
```

### Entering a per-user-credential for a plugin preset, for yourself

To do it for other users, see [Users and groups](https://doc.dataiku.com/dss/latest/python-api/users-groups.html).

```python
import dataiku

client = dataiku.api_client()
my_user = client.get_own_user()
settings = my_user.get_settings()
settings.set_basic_plugin_credential("myplugin", "my_paramset_id", "mypreset_id", "param_name", "username", "password")
settings.save()
```

## Reference documentation

### Classes

```{eval-rst}
.. autosummary::
    dataikuapi.DSSClient
    dataikuapi.dss.admin.DSSOwnUser
    dataikuapi.dss.admin.DSSOwnUserSettings
    dataikuapi.dss.admin.DSSUser
```

### Functions

```{eval-rst}
.. autosummary::
    ~dataikuapi.dss.admin.DSSOwnUserSettings.add_secret
    ~dataikuapi.DSSClient.get_auth_info
    ~dataikuapi.DSSClient.get_auth_info_from_browser_headers
    ~dataikuapi.dss.admin.DSSUser.get_client_as
    ~dataikuapi.DSSClient.get_own_user
    ~dataikuapi.dss.admin.DSSOwnUser.get_settings
    ~dataikuapi.DSSClient.get_user
    ~dataikuapi.dss.admin.DSSOwnUserSettings.set_basic_connection_credential
    ~dataikuapi.dss.admin.DSSOwnUserSettings.set_basic_plugin_credential
    ~dataikuapi.dss.admin.DSSOwnUserSettings.user_properties
```
