(users-groups)=

```{eval-rst}
..
  this code samples has been verified on DSS: 13.2.0
  Date of check: 25/09/2024
  
  this code samples has been verified on DSS: 14.2.0
  Date of check: 18/09/2025
```

# Users and groups

The API exposes key parts of the DSS access control management: users and groups. All these can be created, modified and deleted through the API.

## Example use cases

In all examples, `client` is a {class}`dataikuapi.dssclient.DSSClient`, obtained either using {meth}`dataikuapi.DSSClient` or {meth}`~dataiku.api_client`

### Listing users

```python
client = DSSClient(host, apiKey)
dss_users = client.list_users()
# dss_users is a list of dict. Each item represents one user
prettyprinter.pprint(dss_users)
```

outputs:

```
[   {   'activeWebSocketSesssions': 0,
        'codeAllowed': True,
        'displayName': 'Administrator',
        'groups': ['administrators', 'data_scientists'],
        'login': 'admin',
        'objectImgHash': 0,
        'sourceType': 'LOCAL'},
    ...
]
```

### Listing connected users

You can programmatically retrieve the list of connected users on a Dataiku instance, for example to check if you can safely turn off/restart the instance. This is possible by using the [`list_users()`](https://doc.dataiku.com/dss/latest/python-api/users-groups.html) method of the Dataiku public API. That method returns a value for `activeWebSocketSessions`which indicates the number of sessions that a user is logged into at the moment. Anything other than 0 indicates that a user is connected to the instance.


```{literalinclude} examples/users-groups/list-connected-users.py
```

### Creating a user

#### A local user with a password

```python
new_user = client.create_user('test_login', 'test_password', display_name='a test user', groups=['all_powerful_group'])
```

`new_user` is a {class}`dataikuapi.dss.admin.DSSUser`

#### A user who will login through LDAP

Note that it is not usually required to manually create users who will login through LDAP as they can be automatically provisionned

```python
new_user = client.create_user('test_login', password=None, display_name='a test user', source_type="LDAP", groups=['all_powerful_group'], profile="DESIGNER")
```

#### A user who will login through SSO

This is only for non-LDAP users that thus will not be automatically provisioned, buut should still be able to log in through SSO.

```python
new_user = client.create_user('test_login', password=None, display_name='a test user', source_type="LOCAL_NO_AUTH", groups=['all_powerful_group'], profile="DESIGNER")
```

### Modifying a user's display name, groups, profile, email, ...

To modify the settings of a user, get a handle through {meth}`~dataikuapi.DSSClient.get_user`, then use {meth}`~dataikuapi.dss.admin.DSSUser.get_settings`

```python
user = client.get_user("theuserslogin")

settings = user.get_settings()

# Modify the settings in the `get_raw()` dict
settings.get_raw()["displayName"] = "DSS Lover"
settings.get_raw()["email"] = "my.new.email@stuff.com"
settings.get_raw()["userProfile"] = "DESIGNER"
settings.get_raw()["groups"] = ["group1", "group2", "group3"] # This completely overrides previous groups

# Save the modifications
settings.save()
```

### Modifying user preferences

You can modify user preferences through the given handle (here `ui_language` for the language - see {class}`dataikuapi.dss.admin.DSSUserPreferences` for a comprehensive list of handles).

```python
user = client.get_user("theuserslogin")
settings = user.get_settings()
settings.preferences.ui_language = 'ja'
settings.preferences.daily_digest_emails = true
settings.save()
```

You can also do it through the {meth}`~dataikuapi.dss.admin.DSSUserSettings.get_raw` method described above :
```python
user = client.get_user("theuserslogin")

settings = user.get_settings()

# Modify the preferences in the `get_raw()` dict
settings.get_raw()["preferences"]["uiLanguage"] = "en"
settings.get_raw()["preferences"]["discussionEmails"] = false
settings.get_raw()["preferences"]["rememberPositionFlow"] = true

# Save the modifications
settings.save()
```

### Deleting a user

```python
user = client.get_user('test_login')
user.delete()
```

### Modifying user and admin properties

```python
user = client.get_user("test_login")
settings = user.get_settings()
settings.user_properties["myprop"] = "myvalue"
settings.admin_properties["myadminprop"] = "myadminvalue"
settings.save()
```

(users_groups_modify_user_secrets)=
### Modifying user secrets

```python
user = client.get_user("test_login")
settings = user.get_settings()
settings.add_secret("secretname", "secretvalue")
settings.save()
```

### Entering a per-user-credential for a connection

```python
user = client.get_user('test_login')
settings = user.get_settings()
settings.set_basic_connection_credential("myconnection", "username", "password")
settings.save()
```

### Entering a per-user-credential for a plugin preset

```python
user = client.get_user('test_login')
settings = user.get_settings()
settings.set_basic_plugin_credential("myplugin", "my_paramset_id", "mypreset_id", "param_name", "username", "password")
settings.save()
```

### Retrieve per-user-credential for all the users

Understanding what connections users are using and with what credentials can be useful for a DSS administrator.

```python
for dss_user in client.list_users(as_objects=True):
    creds = dss_user.get_settings().get_raw()["credentials"]
    for key, cred in creds.items():
        if cred["type"] == "BASIC":
            user = cred["user"]
        else:
            user = "N/A"  # OAuth credentials don't have a "user"

        if "lastUpdate" in cred:
            last_update = str(
                datetime.datetime.fromtimestamp(cred["lastUpdate"] / 1000)
            )
        else:
            last_update = "NaN"
        print(
            "DSS user=%s cred_for=%s cred_type=%s user=%s lastUpdate=%s"
            % (dss_user.login, key, cred["type"], user, last_update)
        )
```

### Impersonating another user

As a DSS administrator, it can be useful to be able to perform API calls on behalf of another user.

```python
user = client.get_user("the_user_to_impersonate")
client_as_user = user.get_client_as()

# All calls done using `client_as_user` will appear as being performed by `the_user_to_impersonate` and will inherit
# its permissions
```
### Managing trial status

The **trialStatus** field, part of the user settings, allows you to manage and monitor user trials on a Dataiku instance. The trial status provides details about whether a user is currently on trial, its validity, and expiration. This can be retrieved programmatically via the Dataiku API when querying user details.

#### Example: Checking Trial Status

To retrieve trial status for all users and display their trial details:

```
import dataiku

client = dataiku.api_client()
dss_users = client.list_users()

for user in dss_users:
    trial_status = user.get("trialStatus", {})
    if trial_status.get("exists", False):
        print(f"User: {user['displayName']}")
        print(f"  Trial granted on: {trial_status['grantedOn']}")
        print(f"  Trial expires on: {trial_status['expiresOn']}")
        print(f"  Trial valid: {trial_status['valid']}")
        print(f"  Trial expired: {trial_status['expired']}")

```

#### Trial Status Fields

- **`exists`**: Indicates if the user is or was on a trial license (`true` if on trial).

- **`expired`**: Indicates if the trial period has ended (`true` if expired).

- **`valid`**: Indicates if the trial is active and authorized (`true` if valid).

- **`expiresOn`**: Timestamp (ms since epoch) for when the trial expires.

- **`grantedOn`**: Timestamp (ms since epoch) for when the trial was granted.

### Listing groups

A list of the groups can by obtained with the {meth}`~dataikuapi.DSSClient.list_groups` method:

```python
client = DSSClient(host, apiKey)
# dss_groups is a list of dict. Each group contains at least a "name" attribute
dss_groups = client.list_groups()
prettyprinter.pprint(dss_groups)
```

outputs

```
[   {   'admin': True,
        'description': 'DSS administrators',
        'name': 'administrators',
        'sourceType': 'LOCAL'},
    {   'admin': False,
        'description': 'Read-write access to projects',
        'name': 'data_scientists',
        'sourceType': 'LOCAL'},
    {   'admin': False,
        'description': 'Read-only access to projects',
        'name': 'readers',
        'sourceType': 'LOCAL'}]
```

### Creating a group

```python
new_group = client.create_group('test_group', description='test group', source_type='LOCAL')
```

### Modifying settings of a group

First, retrieve the group definition with a {py:meth}`~dataikuapi.dss.admin.DSSGroup.get_definition` call, alter the definition, and set it back into DSS:

```python
group_definition = new_group.get_definition()
group_definition['admin'] = True
group_definition['ldapGroupNames'] = ['group1', 'group2']
new_group.set_definition(group_definition)
```

### Deleting a group

```python
group = client.get_group('test_group')
group.delete()
```

## Reference documentation

### Classes

```{eval-rst}
.. autosummary::
        dataikuapi.dss.admin.DSSAuthorizationMatrix
        dataikuapi.dss.admin.DSSGroup
        dataikuapi.dss.admin.DSSOwnUser
        dataikuapi.dss.admin.DSSOwnUserSettings
        dataikuapi.dss.admin.DSSUser
        dataikuapi.dss.admin.DSSUserActivity
        dataikuapi.dss.admin.DSSUserSettings
        dataikuapi.dss.admin.DSSUserPreferences
```

### Functions

```{eval-rst}
.. autosummary::
    ~dataikuapi.dss.admin.DSSUserSettings.add_secret
    ~dataikuapi.DSSClient.create_group
    ~dataikuapi.DSSClient.create_user
    ~dataikuapi.dss.admin.DSSGroup.delete
    ~dataikuapi.dss.admin.DSSUser.delete
    ~dataikuapi.dss.admin.DSSUser.get_client_as
    ~dataikuapi.dss.admin.DSSGroup.get_definition
    ~dataikuapi.dss.admin.DSSUserSettings.get_raw
    ~dataikuapi.dss.admin.DSSUser.get_settings
    ~dataikuapi.DSSClient.get_user
    ~dataikuapi.DSSClient.list_groups
    ~dataikuapi.DSSClient.list_users
    ~dataikuapi.dss.admin.DSSUserSettings.save
    ~dataikuapi.dss.admin.DSSUserSettings.set_basic_connection_credential
    ~dataikuapi.dss.admin.DSSUserSettings.set_basic_plugin_credential
    ~dataikuapi.dss.admin.DSSGroup.set_definition
    
```

