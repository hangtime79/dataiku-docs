Using the R API outside of DSS
##############################

You can use most of the R APIs outside of DSS in your favorite IDE, such as RStudio.  This allows you to develop code in that IDE and then push it to DSS.

.. contents::
    :local:


Installing the dataiku package
===============================

The ``dataiku`` package is not available through CRAN. Instead, it must be obtained from the DSS instance itself.

.. code-block:: r

    install.packages("http(s)://DSS_HOST:DSS_PORT/public/packages/dataiku_current.tar.gz", repos=NULL)


Setting up the connection with DSS
====================================

In order to connect to DSS, you'll need to supply:

* The URL of DSS
* A REST API key in order to perform actions

We strongly recommend that you use a personal API key. Please see :doc:`/publicapi/keys` for more information

There are three ways to supply this information:

* Using the RStudio integration, as described in :doc:`/R/rstudio/`

* Through code:

.. code-block:: R

    library(dataiku)

    dkuSetRemoteDSS("http(s)://DSS_HOST:DSS_PORT/", "Your API Key secret")

* Through environment variables. Before starting your R process, export the following environment variables:

.. code-block:: bash

    export DKU_DSS_URL=http(s)://DSS_HOST:DSS_PORT/
    export DKU_API_KEY="Your API key secret"

* Through a configuration file. Create or edit the file ``~/.dataiku/config.json`` (or ``%USERPROFILE%/.dataiku/config.json`` on Windows), and add the following content:

.. code-block:: json

    {
      "dss_instances": {
        "default": {
          "url": "http(s)://DSS_HOST:DSS_PORT/",
          "api_key": "Your API key secret"
        },
      },
      "default_instance": "default"
    }

You can now use most of the functions of the ``dataiku`` package from your own machine, independently from the DSS installation.

Setting the current project
----------------------------

Most functions of the ``dataiku`` package require a "current project" to be set. This allows functions like ``dkuReadDataset("my_dataset_name")`` to know which project to load the dataset from.

To set the current project, use:

.. code-block:: R

    dkuSetCurrentProjectKey("PROJECT_KEY")


Advanced options
-----------------

Disabling SSL certificate check
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

If your DSS has SSL enabled, the packages will verify the certificate. In order for this to work, you may need to add the root authority that signed the DSS SSL certificate to your local trust store. Please refer to your OS or Python manual for instructions.

If this is not possible, you can also disable checking the SSL certificate:

* Through code:

.. code-block:: R

  dkuSetRemoteDSS("http(s)://DSS_HOST:DSS_PORT/", "Your API Key secret", TRUE)


* Through environment variables: Not supported at the moment

* Through configuration file: Modify the configuration file as such:

.. code-block:: json

    {
      "dss_instances": {
        "default": {
          "url": "http(s)://DSS_HOST:DSS_PORT/",
          "api_key": "Your API key secret",
          "no_check_certificate": true
        }
      },
      "default_instance": "default"
    }
