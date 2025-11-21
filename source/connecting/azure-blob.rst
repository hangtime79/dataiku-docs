Azure Blob Storage
####################

DSS can interact with Azure Blob Storage to:

* read and write datasets
* read and write managed folders

Azure Blob Storage is an object storage service: you create "buckets"
that can store arbitrary binary content and textual metadata under a specific key, unique in the bucket.

While not technically a hierarchical file system with folders, sub-folders and
files, that behavior can be emulated by using keys containing ``/``. For
instance, you can store your daily logs using keys like ``2015/01/24/app.log``.

DSS uses the same filesystem-like mechanism when accessing Azure: when you specify
a container, you can browse it to quickly find your data, or you can set the
prefix in which DSS may output datasets. Datasets on Azure thus must be in one of
the supported :ref:`filesystem formats <file-formats>`.

.. note::

    Azure Blob as a filesystem-like storage comes with a few limitations:
      - keys must not start with a ``/``
      - "files" with names containing ``/`` are not supported
      - "folders" (prefixes) ``.`` and ``..`` are not supported
      - like on a filesystem, a file and a folder with the same name are not
        supported: if a file ``some/key`` exists, it takes precedence over a
        ``some/key/`` prefix / folder
      - multiple successive / are not supported

Creating a Azure connection
===========================

Before connecting to Azure Blob Storage with DSS you need to  :

- create at least one container on azure
- retrieve the storage account and a accesskey


(*See the* `official documentation <https://docs.microsoft.com/en-us/azure/storage/storage-create-storage-account>`_  *for more details*)

To configure your connection you must specify :

- your storage account on the ``storageAccount`` field
- your secret key on the ``accessKey`` field
- ideally a default managed container for managed dataset
- you can also specify a path within container for managed datasets

Connecting to Azure using OAuth2
======================================

DSS can also access using OAuth2 on Azure Blob Storage.

OAuth2 can be performed either:

* using a single service account
* using per-user credentials. ie: DSS will use the OAuth2 protocol to access the resources in Azure on behalf of a user

Use a service account if:

* your DSS users don't have direct access to the resources in Azure
* you don't need resource access filtering per user


Use per-user credentials if:

* your DSS users got access to your Azure project and especially to Azure Blob storage
* you don't want your users to access resources via DSS in Azure Blob storage which they don't have permission for
* you want an audit in Azure of your users accesses

Access using a single service account
-------------------------------------

* create a new App (Azure Portal  > Azure Active Directory > App registrations). DSS will connect with the identity of this app
* in the Overview tab, note the `Application (client) ID` and the `Directory (tenant) ID`
* create a client secret for this application (App registration > Certificates & Secrets), note the client (app) secret
* create a new Azure Blob Storage connection in DSS
* fill in the storage account name in the "Azure Storage account" field
* select "OAuth from App" as the "Auth Type"
* fill the "Tenant id", "App id", and "App secret" fields with the fields you noted earlier in the Azure App
* leave the "Auth endpoint" blank in order to use the default endpoint, or fill it in if you need to use a custom endpoint
* select "Global" in the "Credentials mode" dropdown

Access using per-user OAuth tokens
-----------------------------------

* create a new App (Azure Portal  > Azure Active Directory > App registrations). DSS will connect with the identity of this app
* in the Overview tab, note the `Application (client) ID` and the `Directory (tenant) ID`
* in the Authentication tab, add a new Platform

    * in order to use Hadoop specific formats or Spark with this connection, you must use a public Azure App. This means selecting a "Mobile and desktop applications" platform and not creating a client secret later
    * otherwise, choose the "Web" platform
    * in either case, add a redirect URI of `DSS_BASE_URL/dip/api/oauth2-callback` 

.. note::
  For example if DSS is accessed at https://dss.mycompany.corp/, the OAuth2 redirect URL is https://dss.mycompany.corp/dip/api/oauth2-callback

* if you selected the "Web" platform earlier, create a client secret for this application (App registration > Certificates & Secrets), note the client (app) secret
* create a new Azure Blob Storage connection in DSS
* fill in the storage account name in the "Azure Storage account" field
* select "OAuth from App" as the "Auth Type"
* fill the "Tenant id", "App id", and "App secret" (if there is one) fields with the fields you noted earlier in the Azure App
* leave the "authorization endpoint" and "token endpoint" blank in order to use the default endpoints, or fill them in if you need to use custom endpoints
* select "Per user" in the "Credentials mode" dropdown
* create the connection (you can't test it yet)

Then for each user:

* go to user profile > credentials
* click the "Edit" button next to the new connection name
* follow the instructions that appear

Common errors
---------------

* Problem: In per-user mode, the connection fails with the following error when trying to use it with Hadoop specific formats or Spark (but works in other use cases): `AADSTS700016: Application with identifier '[app id]' was not found in the directory '[other id]'. This can happen if the application has not been installed by the administrator of the tenant or consented to by any user in the tenant. You may have sent your authentication request to the wrong tenant.`
* Solution: You must use Hadoop 3.2.2+

|

* Problem: In per-user mode, the connection fails with the following error when trying to use it with Hadoop specific formats or Spark (but works in other use cases): `AADSTS7000218: The request body must contain the following parameter: 'client_assertion' or 'client_secret'.`
* Solution: You must use a public Azure app. Remove the client (app) secret and select the "Mobile and desktop applications" platform (not "Web") in the Authentication tab of the Azure app.

Creating Azure Blob Storage datasets
=======================================

After creating your Azure connection in Administration, you can create Azure Blob Storage datasets.

From either the Flow or the datasets list, click on New dataset > Azure Blob Storage.

* select the connection in which your files are located
* if available, select the bucket (either by listing or entering it)
* click on "Browse" to locate your files

Connections path handling
==========================

The Azure connection can be either in "free selection" mode, or in "path restriction mode".

In "free selection" mode, users can select the bucket in which they want to read, and the path within the bucket. If the credentials have the permission to list buckets, a bucket selector will be available for users.

In "path restriction mode", you choose a bucket, and optionally a path within the bucket. Users will only be able to read and write data within that "base bucket + path".

To enable "path restriction mode", simply write a bucket name (and optionally a path in bucket) in the "Path restrictions" section of the connection settings

Location of managed datasets and folders
===========================================

For a "free selection" connection
----------------------------------

When you create a managed dataset or folder in a Azure connection, DSS will automatically create it within the "Default bucket" and the "Default path".

Below that root path, the "naming rule" applies. See :doc:`relocation` for more information.

For a "path restriction" connection
-------------------------------------

When you create a managed dataset or folder in a Azure connection, DSS will automatically create it within the Bucket and Path selected in the "Path restrictions" section, and will append the "Default path" from the "managed datasets & folders" section.

Below that root path, the "naming rule" applies. See :doc:`relocation` for more information.
