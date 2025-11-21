# Using Dataiku's Python packages 

## Using the client from inside Dataiku

You have nothing to do when you use the client from inside Dataiku. 
The packages are preinstalled, and you don't need to provide an API key.
The client will inherit credentials from the current context.
Both packages (`dataiku` and `dataikuapi`) can be used.
The easiest way to create a client is:

```python
import dataiku

client = dataiku.api_client()

# client is now a DSSClient and can perform all authorized actions.
# For example, list the project keys for which you have access
client.list_project_keys()
```

## Using the client from outside Dataiku

There are a few additional setup steps to complete.
This tutorial will help you set up your local environment by following these steps.

## Prerequisites

* Access to a Dataiku instance via an API key (see {doc}`the documentation <refdoc:publicapi/keys>` for explanations on how to generate one)
* Python >= 3.9 with the following packages:
  * `numpy`
  * `pandas`

::: {note}
  This tutorial has been tested with `Python 3.10` and
  ```python
  numpy==2.1.1
  pandas==2.2.2
  ```
:::

## Building your local virtual environment

The first step is to create a Python virtual environment on your computer in which you will install all the required dependencies. 

* Generate a new virtual environment using the tool of your choice (venv, Pipfile, poetry). 
  In this tutorial, we'll use `venv` and call our environment `dataiku_local_env`:
  ```bash
  # Create the virtual environment
  python3 -m venv dataiku_local_env

  # Activate the virtual environment
  source dataiku_local_env/bin/activate
  ```

### Installing the `dataiku` package


`````{tabs}
````{group-tab} Via pip

Install the `dataiku` package by running the following command

```bash
pip install http(s)://DATAIKU_HOST:DATAIKU_PORT/public/packages/dataiku-internal-client.tar.gz
```

:::{warning}
If your instance has a self-signed or expired certificate, to connect with HTTP, you will need to add the `--trusted-host` flag:

```bash
pip install http(s)://DATAIKU_HOST:DATAIKU_PORT/public/packages/dataiku-internal-client.tar.gz --trusted-host=DATAIKU_HOST:DATAIKU_PORT
```
:::
  
````

````{group-tab} In a requirements.txt

In your requirements.txt file, add a line:

``` shell
http(s)://DATAIKU_HOST:DATAIKU_PORT/public/packages/dataiku-internal-client.tar.gz
```

Then update your requirements with `pip install -r requirements.txt`

If you use HTTPS without a proper certificate, you may need to add
`--trusted-host=DATAIKU_HOST:DATAIKU_PORT` to your pip command line.

````

````{group-tab} Manually

-   Download the package\'s tar.gz file from your Dataiku instance:

    `http(s)://DATAIKU_HOST:DATAIKU_PORT/public/packages/dataiku-internal-client.tar.gz`
-   Install it with `pip install dataiku-internal-client.tar.gz`
````
`````

### Installing the `dataikuapi` package

Install the `dataikuapi` package directly from the PyPI repository:

```bash
pip install dataiku-api-client
```
This installs the client in the system-wide Python installation,
so if you are not using virtualenv, you may need to replace `pip` with `sudo pip`.

Note that this will always install the latest version of the API client.
You might need to request a version that is compatible with your Dataiku version.

When connecting from the outside world, you need an API key.
See {doc}`Public API Keys<refdoc:publicapi/keys>`) for more information on creating an API key and the associated privileges.

You also need to connect using the base URL of your Dataiku instance.

Once all relevant packages are installed, you can connect with your Dataiku instance.

(connecting-dataiku-instance)=
## Connecting to your Dataiku instance

`````{tabs}
````{group-tab} Using dataiku package

The connection with your Dataiku instance will be established by the `dataiku` package, which will look for :
* the instance URL,
* the API key to use for authentication.

You can provide this information in different ways:

* **directly inside your code**, by using the `set_remote_dss()` method and replacing `YOURAPIKEY` with your own API key:
  ```python
  import dataiku
  dataiku.set_remote_dss("https://dss.example", "YOURAPIKEY")
  ```
  :::{warning}
  If your instance has a self-signed or expired certificate, in order to connect with HTTPS you will need to pass the `no_check_certificate` flag:
  ```python
  import dataiku
  
  dataiku.set_remote_dss("https://dss.example", "YOURAPIKEY", no_check_certificate=True)
  client = dataiku.api_client()
  print(client.list_project_keys())
  ```
  :::

* **with environment variables** to be initialized before starting your Python environment:
  ```bash
  export DKU_DSS_URL="https://dss.example"
  export DKU_API_KEY="YOURAPIKEY"
  ```
  ```python
  import dataiku
  
  client = dataiku.api_client()
  print(client.list_project_keys())
  ```  
  
  :::{warning}
  You can not turn off certificate checking via environment variables.
  :::
  
* **with a configuration file** that should be located at `$HOME/.dataiku/.config.json` (or `%USERPROFILE%/.dataiku/config.json` on Windows) with the following structure:
  ```json
  {
    "dss_instances": {
      "default": {
        "url": "https://dss.example",
        "api_key": "YOURAPIKEY"
      }
    },
    "default_instance": "default"
  }
  ```
  ```python
  import dataiku
  
  client = dataiku.api_client()
  print(client.list_project_keys())
  ```

  :::{warning}
  If your instance has a self-signed or expired certificate, in order to connect with HTTPS you will need to add the `no_check_certificate` property:
  ```json
  {
    "dss_instances": {
      "default": {
        "url": "https://dss.example",
        "api_key": "YOURAPIKEY",
        "no_check_certificate": true
      }
    },
    "default_instance": "default"
  }
  ```
  :::

  If at some point you need to clear the connection settings, you can do so with the following code:

  ``` python
  dataiku.clear_remote_dss()
  ```

  The configuration will be cleared.
  If you are using the client within your Dataiku instance, it will target the API of your instance.

````
````{group-tab} Using the dataikuapi package
To work with the API, a connection needs to be established with Dataiku, by creating a {py:class}`~dataikuapi.dssclient.DSSClient` object.
Once the connection is established, the {py:class}`~dataikuapi.dssclient.DSSClient` object serves as the entry point to the other calls.

```python
import dataikuapi

host = "http://localhost:11200"
apiKey = "some_key"
client = dataikuapi.DSSClient(host, apiKey)

# client is now a DSSClient and can perform all authorized actions.
# For example, list the project keys for which the API key has access
client.list_project_keys()
```

:::{warning}
If your Dataiku has SSL enabled, the package will verify the certificate.
In order for this to work, you may need to add the root authority that signed the Dataiku SSL certificate to your local trust store.
Please refer to your OS or Python manual for instructions.

If this is not possible, you can also disable checking the SSL certificate by using `DSSClient(host, apiKey, insecure_tls=True)`
:::
````
`````
## Testing your setup 

The last step is to check if you can properly connect to your Dataiku instance.
For that, you can use the code snippet below: 

```python
import dataiku

# Uncomment this if you are not using environment variables or a configuration file
# dataiku.set_remote_dss("https://dss.example", "YOURAPIKEY")

client = dataiku.api_client()

# Uncomment this if your instance has a self-signed certificate
# client._session.verify = False

info = client.get_auth_info()
print(info)

```

If all goes well, you should see an output similar to this:

```text
{
    "authSource": "PERSONAL_API_KEY",
    "via": [],
    "authIdentifier": "your-user-name",
    "groups": ["one_group", "another_group"],
    "userProfile": "DESIGNER",
    "associatedDSSUSer": "your-user-name",
    "userForImpersonation": "your-user-name"
}
```

If so, congratulations: your setup is now fully operational!
You can move on and set up Dataiku plugins/extensions in your favorite IDE
or learn more about how to automate things using the public API.

