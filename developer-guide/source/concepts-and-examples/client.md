(client)=

```{eval-rst}
..
  this code samples has been verified on DSS: 14.1.0
  Date of check: 13/08/2025

  this code samples has been verified on DSS: 13.2.0
  Date of check: 19/09/2024
```

# The main API client

The {class}`~dataikuapi.DSSClient` class is the entry point for many of the capabilities of the Dataiku API.

Dataiku provides two different packages serving different roles.
For more on the differences between the packages, please refer to {doc}`/getting-started/dataiku-python-apis/index`.
For additional information, please refer to the {doc}`/tutorials/devtools/api` section.

## Creating a client from inside DSS

To work with the API,
a connection must be established with DSS by creating a {py:class}`~dataikuapi.dssclient.DSSClient` object.
Once the connection is established, 
the {py:class}`~dataikuapi.dssclient.DSSClient` object serves as the entry point to the other calls.

```python
import dataiku

client = dataiku.api_client()

# client is now a DSSClient and can perform all authorized actions.
# For example, list the project keys for which you have access
client.list_project_keys()
```

## Creating a client from outside DSS

To work with the API, 
a connection must be established with DSS by creating a {py:class}`~dataikuapi.dssclient.DSSClient` object. 
Once the connection is established, 
the {py:class}`~dataikuapi.dssclient.DSSClient` object serves as the entry point to the other calls.

```python
import dataikuapi

host = "http://localhost:11200"
apiKey = "some_key"
client = dataikuapi.DSSClient(host, apiKey)

# client is now a DSSClient and can perform all authorized actions.
# For example, list the project keys for which the API key has access
client.list_project_keys()
```

### Turning off the SSL certificate check

If your DSS has SSL enabled, the package will verify the certificate.
You may need to add the root authority that signed the DSS SSL certificate to your local trust store for this to work.
Please refer to your OS or Python manual for instructions.

If this is not possible, you can also turn off checking the SSL certificate by using `DSSClient(host, apiKey, insecure_tls=True)`

## Reference documentation

## Reference documentation

### Classes

```{eval-rst}
.. autosummary::
    dataikuapi.dssclient.DSSClient

```

### Functions
```{eval-rst}
.. autosummary::
    ~dataikuapi.DSSClient.list_project_keys
```
