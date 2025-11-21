# The Dataiku Python packages

Code-savvy users of the Dataiku platform can interact with it using a complete set of Python APIs that are split 
between two packages, respectively called `dataiku` and `dataikuapi`.
While they are often used together, their underlying primitives serve distinct purposes:

* [`dataikuapi`](https://pypi.org/project/dataiku-api-client/) is a client for Dataiku's public REST API,
  which is helpful in programmatically maintaining the platform
  or making it interact with other applications or systems.
* `dataiku` is for **internal operations**, data processing, and machine learning tasks within the platform. 
  It allows low-level interactions with core items such as datasets and saved models.

Both packages can be used from Dataiku out of the box;
you can connect to your instance and perform some operations, like:

```python
import dataiku

client = dataiku.api_client()

# client is now a DSSClient and can perform all authorized actions.
# For example, list the project keys for which you have access
client.list_project_keys()
```

Please refer to the {doc}`/tutorials/devtools/api` section for a deeper insight into the Dataiku API usage. 

```{attention}
If you edit code outside the platform (e.g., using the VSCode or PyCharm editor plugins),
don't forget to {doc}`install the Dataiku Python APIs locally </tutorials/devtools/python-client/index>`. 
```

* If you are a beginner user looking to get more familiar with the basics of Dataiku's public API, start with 
    the {doc}`/tutorials/devtools/public-api-intro/index` tutorial.

* Check out the {doc}`API reference </api-reference/python/index>` section for complete documentation of the `dataiku`
  and `dataikuapi` packages.

In the rest of this Developer Guide, for the sake of simplicity,
we won't distinguish between `dataiku` and `dataikuapi` unless absolutely needed:
we will refer to the "Dataiku Python APIs" instead. 
