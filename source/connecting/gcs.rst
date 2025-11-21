Google Cloud Storage
####################


DSS can interact with Google Cloud Storage to:

* read and write datasets
* read and write managed folders

GCS is an object storage service: you create "containers"
that can store arbitrary binary content and textual metadata under a specific key, unique in the container.

While not technically a hierarchical file system with folders, sub-folders and
files, that behavior can be emulated by using keys containing ``/``. For
instance, you can store your daily logs using keys like ``2015/01/24/app.log``.

DSS uses the same filesystem-like mechanism when accessing GCS: when you specify
a container, you can browse it to quickly find your data, or you can set the
prefix in which DSS may output datasets. Datasets on GCS thus must be in one of
the supported :ref:`filesystem formats <file-formats>`.


.. note::

    Besides `GCS naming guide lines <https://cloud.google.com/storage/docs/naming>`_  GCS as a filesystem-like storage comes with a few limitations:
      - keys must not start with a ``/``
      - "files" with names containing ``/`` are not supported
      - "folders" (prefixes) ``.`` and ``..`` are not supported
      - like on a filesystem, a file and a folder with the same name are not
        supported: if a file ``some/key`` exists, it takes precedence over a
        ``some/key/`` prefix / folder
      - multiple successive / are not supported

Create a GCS connection
========================
DSS supports connecting to GCS using a Service Account or OAuth2.

With service account credentials, DSS will be able to access all resources associated with this service account, independently of the user initiating the connection.
This also means that in the GCP audit logs, you won't have a tracing of the user behind this connection.

OAuth2 connection access means DSS will use the OAuth2 protocol to access the resources in GCP. DSS will be registered as an OAuth2 client, authorized to request and gain access
on behalf of your DSS users. 

Use a service account if:

* your DSS users don't have direct access to the resources in GCP
* you don't need resources access filtering per user

Use OAuth2 if:

* your DSS users have access to your GCP project and particularly to GCS
* you don't want your users to access resources via DSS in GCS which they don't have permission for
* you want an audit in GCP of your users accesses

Using Service Account
------------------------------------------

Before connecting to Google Cloud via DSS you will have to: 

- make sure "Google Cloud Storage"  and "Google Cloud Storage JSON API" are enabled in Google Cloud console's API Manager
- create at least one Storage bucket in your Google cloud account
- `create a service account <https://developers.google.com/identity/protocols/OAuth2ServiceAccount>`_ and export your private key in **JSON** format

.. note::
  In order to let DSS create new datasets, your storage account will have to be granted "project editor" role . A "project viewer" should be sufficient for read-only connection 


(*See the* `official documentation <https://cloud.google.com/storage/docs/quickstart-console>`_  *for more details*) 

To configure your connection you must specify : 

- your project ID (you can find it in your  GCLOUD project list next to your project name ) 
- the entire content of your service account private key in JSON format

Using OAuth2
------------------------------------------

The OAuth2 connection is performed using per-user credentials. Each user must grant DSS permission to access GCS on their behalf.
You will need to create an OAuth2 client in your GCP project and configure the credentials in your DSS GCS connection.

To create an OAuth 2.0 client ID in the console, please refer to the `following documentation <https://support.google.com/cloud/answer/6158849?hl=en>`_ .
When creating your OAuth2 client in google, you will need to:

* select the application type `Web application`
* add the following redirect URI `DSS_BASE_URL/dip/api/oauth2-callback`

.. note::
  For example if DSS is accessed at https://dss.mycompany.corp/, the OAuth2 redirect URL is https://dss.mycompany.corp/dip/api/oauth2-callback


Once created, configure DSS to use this OAuth2 client. Do in DSS the following:

* create a new GCS connection
* fill in the basic params as usual
* select "OAuth" as the "credentials". Note that this will force you to use per-user credential
* fill the "Client id", "Client secret" (if there is one) with the information from your OAuth app
* create the connection

.. note::
  At this point, although the connection is operational, you can't test it yet as your user hasn't authorized DSS to access GCS on their behalf.

Each user, including you, will need to follow these steps to allow DSS to access GCP on their behalf:

* go to user `profile > credentials`
* the user will see that no authorization was given yet to DSS for this connection
* click the "Edit" button next to the new connection name
* follow the instructions that appear: Google will authenticate and get the user consent to authorize DSS to access GCS
* the user will be redirected automatically to DSS and will notice that credentials have successfully been obtained for the connection

If you did these steps with a user allowed to modify the connection, like an admin user, you should now be able to test the connection:

* go back to your connection settings
* click on the `Test` button which should be successful

Creating GCS datasets
======================

After creating your GCS connection in Administration, you can create GCS datasets.

From either the Flow or the datasets list, click on New dataset > GCS. 

* select the connection in which your files are located
* if available, select the container (either by listing or entering it)
* click on "Browse" to locate your files

Connections path handling
==========================

The GCS connection can be either in "free selection" mode, or in "path restriction mode".

In "free selection" mode, users can select the container in which they want to read, and the path within the container. If the credentials have the permission to list containers, a container selector will be available for users.

In "path restriction mode", you choose a container, and optionally a path within the container. Users will only be able to read and write data within that "base container + path".

To enable "path restriction mode", simply write a container name (and optionally a path in container) in the "Path restrictions" section of the connection settings

Location of managed datasets and folders
===========================================

For a "free selection" connection
----------------------------------

When you create a managed dataset or folder in a GCS connection, DSS will automatically create it within the "Default container" and the "Default path". 

Below that root path, the "naming rule" applies. See :doc:`relocation` for more information.

For a "path restriction" connection
-------------------------------------

When you create a managed dataset or folder in a GCS connection, DSS will automatically create it within the container and Path selected in the "Path restrictions" section, and will append the "Default path" from the "managed datasets & folders" section.

Below that root path, the "naming rule" applies. See :doc:`relocation` for more information.
