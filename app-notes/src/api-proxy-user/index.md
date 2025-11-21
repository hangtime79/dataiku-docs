# Proxy user for API calls

In some cases, you could want to make API calls to DSS using the identity of a different user.

For instance, say you have an external app that makes call to DSS on behalf of some user (from the same identity provider). You may want the call to be logged as being done by the user in question, and with their privileges/permissions. The user is authenticated within your app, but you don't have a DSS API key for each user logging into your app.

This is achievable, provided that you use an admin API key to make API calls to DSS. Making impersonated calls requires administrative privileges.


## Using the Python API client

You can use [`DSSUser.get_client_as()`](https://developer.dataiku.com/latest/api-reference/python/users-groups.html#dataikuapi.dss.admin.DSSUser.get_client_as):

```python
from dataikuapi.dssclient import DSSClient
admin_client = DSSClient(host, adminApiKey)
user = client.get_user("target_user_login")
user_client = user.get_client_as()
```

Any call you then make with `user_client` will be impersonated.


## Using the HTTP REST API

When making HTTP calls to DSS with your admin API key, specify a `X-Dku-ProxyUser` header with the target user's login as value in your call.

