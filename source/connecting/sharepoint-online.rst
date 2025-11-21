SharePoint Online 
#################

Dataiku can interact with SharePoint Online to:

* read and write datasets based on SharePoint Online lists
* read and write datasets based on SharePoint Online stored documents
* read and write managed folders

There are two types of SharePoint objects that can be leveraged: document libraries and lists.

To interact with a document, you will need to know its SharePoint site, the drive in which it is stored, and its path within this drive.

Dataiku uses the same filesystem-like mechanism when accessing SharePoint Online: when you specify
a site and drive, you can browse it to quickly find your data, or you can set the
prefix in which Dataiku may output datasets. Datasets on SharePoint thus must be in one of
the supported :ref:`filesystem formats <file-formats>`.

To interact with SharePoint lists, you will need to know the site, and the name of the list.

.. warning::

	Sharepoint list views are not supported by the native connector. If you need to read data from a view, please use the plugin `Sharepoint Online <https://www.dataiku.com/product/plugins/sharepoint-online/>`_ instead.

Creating a SharePoint Online connection
=======================================

Before connecting to SharePoint Online with Dataiku you need to  :

- create at least one site on your SharePoint instance
- define an app on Azure portal and retrieve its client id and client secret

Connecting to SharePoint Online using OAuth2
============================================

Dataiku can access SharePoint Online using OAuth2 as a per-user credential.

* create a new App registration (**Azure Portal  > Microsoft Entra ID > App registrations**). Dataiku will connect with the identity of this app
* in the Overview tab, note the `Application (client) ID` and the `Directory (tenant) ID`
* in the Authentication tab, add a new Platform

    * choose the "Web" platform
    * add a redirect URI of `DSS_BASE_URL/dip/api/oauth2-callback` 

.. note::
  For example if Dataiku is accessed at https://dss.mycompany.corp/, the OAuth2 redirect URL is https://dss.mycompany.corp/dip/api/oauth2-callback

* if you selected the "Web" platform earlier, create a client secret for this application (**App registration > Certificates & Secrets**), note the client (app) secret
* navigate to the API permissions tab and add the appropriate permissions. Click **+ Add a permission > Microsoft Graph > Delegated permissions**. It is advised to add openid, Files.ReadWrite.All, Sites.ReadWrite.All and User.Read.
* create a new SharePoint Online connection in Dataiku
* fill the "Tenant id", "App id", and "App secret" fields with the fields you noted earlier in the Azure App
* "Authorization endpoint" should be "`https://login.microsoftonline.com/<<your tenant id>>/oauth2/v2.0/authorize`" for single tenant apps, where <<your tenant id>> must be replaced with your tenant's guid. In the special case of multi-tenant apps, the endpoint is "`https://login.microsoftonline.com/common/oauth2/v2.0/authorize`".
* "Token endpoint" should be "`https://login.microsoftonline.com/<<your tenant id>>/oauth2/v2.0/token`" for single tenant apps. In the special case of multi-tenant apps, it can be "`https://login.microsoftonline.com/common/oauth2/v2.0/token`".
* "Scope" should be "`offline_access User.Read Files.ReadWrite.All Sites.ReadWrite.All Sites.Manage.All`"
* "Default site" should contain the name for an existing SharePoint site where new managed datasets will be created by default. To find the site name, browse to that site and copy the section of the URL following /sites/. For instance, if the URL looks like "`https://my-corp.sharepoint.com/sites/myproject/_layouts/15/viewlsts.aspx?view=14`" the site name is `myproject`.
* "Default drive" should contain the name of an existing drive where new managed datasets will be created by default. This drive must belong to the default site. To find the drive name, go to the "Site contents" section and copy the name of the document library containing your drive.
* "Default path" is the path to the directory within the default drive where managed folders will be created
* create the connection. Note that this connection can only be tested once you have entered your credential in your Dataiku user profile.

Then for each user:

* go to **user profile > Credentials**
* click the "Edit" button next to the new connection name
* follow the instructions that appear

Connecting to SharePoint Online using user name and password
============================================================

Dataiku can access SharePoint Online using OAuth2 as a per-user or global credentials.

.. note::
  This type of connection is only possible with managed accounts. To know if an account is managed, go to this URl using a web browser, after editing the email address with the one you intend to use: https://login.microsoftonline.com/GetUserRealm.srf?login=your.SharePoint@email.address. The key `NameSpaceType` should read `Managed`.

* create a new App registration (**Azure Portal  > Microsoft Entra ID > App registrations**). Note that the APIs used by the native SharePoint connector are different from those used by the SharePoint Online plugin. So if you already have an app to connect your Dataiku instance to SharePoint Online, you will either need a new one or adds APIs to the old one.
* in **Authentication > Advanced settings**, allow public client flows
* navigate to the API permissions tab and add the appropriate permissions. Click **+ Add a permission > Microsoft Graph > Delegated permissions**. It is advised to add openid, Files.ReadWrite.All, Sites.ReadWrite.All and User.Read.
* create a new SharePoint Online connection in Dataiku
* choose User / Password as Auth type
* fill the "Tenant id" and "App id" fields with the fields you noted earlier in the Azure App
* "Authorization endpoint" should be "`https://login.microsoftonline.com/<<your tenant id>>/oauth2/v2.0/authorize`" for single tenant apps, where <<your tenant id>> must be replaced with your tenant's guid. In the special case of multi-tenant apps, the endpoint is "`https://login.microsoftonline.com/common/oauth2/v2.0/authorize`".
* "Token endpoint" should be "`https://login.microsoftonline.com/<<your tenant id>>/oauth2/v2.0/token`" for single tenant apps. In the special case of multi-tenant apps, it can be "`https://login.microsoftonline.com/common/oauth2/v2.0/token`".
* "Scope" should be "`offline_access User.Read Files.ReadWrite.All Sites.ReadWrite.All Sites.Manage.All`"
* "Default site" should contain the name for an existing SharePoint site where new managed datasets will be created by default. To find the site name, browse to that site and copy the section of the URL following /sites/. For instance, if the URL looks like "`https://my-corp.sharepoint.com/sites/myproject/_layouts/15/viewlsts.aspx?view=14`", the site name is `myproject`.
* "Default drive" should contain the name of an existing drive where new managed datasets will be created by default. This drive must belong to the default site. To find the drive name, go to the "Site contents" section and copy the name of the document library containing your drive.
* "Default path" is the path to the directory within the default drive where managed folders will be created
* pick a credential mode. "Per user" means that each Dataiku user will have to put their SharePoint user name and password in their credential page before using the connection. "Global" means that this username access will be shared with all the Dataiku users with access rights to this connection.
* create the connection
* if the credential mode mode is "Global", you can test the connection. Otherwise you have to enter your credential in your Dataiku user profile first.

If the credential mode is "Per user", this extra steps are necessary for each Dataiku user:

* go to **User profile > Credentials**
* click the "Edit" button next to the new connection name
* follow the instructions that appear

Connecting to SharePoint Online using certificates
============================================================

Dataiku can access SharePoint Online using certificate and private key as global credentials.

* get your certificate and private key ready. If you do not already have one, it can be created for instance by using openssl: `openssl req -newkey rsa:2048 -new -nodes -x509 -days 3650 -keyout private_key.pem -out certificate.pem`
* create a new App registration (**Azure Portal  > Microsoft Entra ID > App registrations**)
* in **Authentication > Advanced settings**, allow public client flows
* in Certificates & secrets, upload your certificate (or certificate.pem created from the first step). Copy the certificate's thumbprint.
* navigate to the API permissions tab and add the appropriate permissions. Click **+ Add a permission > Microsoft Graph > Application permissions**. It is advised to add Sites.FullControl.All and Sites.Managed.All. These permissions require the Azure admin consent.
* create a new SharePoint Online connection in Dataiku
* choose "Private key" as Auth type
* fill the "Tenant id", "App id" and "Thumbprint" fields with the fields you noted earlier in the Azure App
* open the private key file (or private_key.pem created earlier) in a text application and copy/paste its content into the Client certificate (private key) input box. The section to copy starts and ends with "`\-\-\-\-\-BEGIN PRIVATE KEY\-\-\-\-\-`" / "`\-\-\-\-\-END PRIVATE KEY\-\-\-\-\-`".
* "Authorization endpoint" should be "`https://login.microsoftonline.com/<<your tenant id>>/oauth2/v2.0/authorize`" for single tenant apps, where <<your tenant id>> must be replaced with your tenant's guid. In the special case of multi-tenant apps, the endpoint is "`https://login.microsoftonline.com/common/oauth2/v2.0/authorize`".
* "Token endpoint" should be "`https://login.microsoftonline.com/<<your tenant id>>/oauth2/v2.0/token`" for single tenant apps. In the special case of multi-tenant apps, it can be "`https://login.microsoftonline.com/common/oauth2/v2.0/token`".
* "Scope" should be "`https://graph.microsoft.com/.default`"
* "Default site" should contain the name for an existing SharePoint site where new managed datasets will be created by default. To find the site name, browse to that site and copy the section of the URL following /sites/. For instance, if the URL looks like "`https://my-corp.sharepoint.com/sites/myproject/_layouts/15/viewlsts.aspx?view=14`", the site name is `myproject`.
* "Default drive" should contain the name of an existing drive where new managed datasets will be created by default. This drive must belong to the default site. To find the drive name, go to the "Site contents" section and copy the name of the document library containing your drive.
* "Default path" is the path to the directory within the default drive where managed folders will be created
* create and test the connection

Advanced connection properties
============================================================

If you ever encounters timeouts while connecting to SharePoint, it's possible to configure different timeouts properties in the `Advanced connection properties` section:

+------------------------------------+---------------------------------------------------------------+
|       Name                         |                             Description                       |
+====================================+===============================================================+
| ConnectTimeout                     | Max time to establish a connection (milliseconds). default 10s|
+------------------------------------+---------------------------------------------------------------+
| ReadTimeout                        | Max time waiting for data (milliseconds). default 10s         |
+------------------------------------+---------------------------------------------------------------+
| WriteTimeout                       | Max time to send data (milliseconds). default 10s             |
+------------------------------------+---------------------------------------------------------------+

Creating SharePoint Online datasets
=======================================

From a SharePoint document
--------------------------

After creating your SharePoint Online connection in Administration, you can create datasets from documents stored on SharePoint.

From either the Flow or the datasets list, click on **+Dataset > Cloud Storage & Social > SharePoint Document**.

* select the connection
* select the SharePoint site and the drive in which your files are located
* click on "Browse" to locate your files

From a SharePoint list
----------------------

After creating your SharePoint Online connection in Administration, you can create datasets from a SharePoint list.

From either the Flow or the datasets list, click on **+Dataset > Cloud Storage & Social > SharePoint List**.

* select the connection in which your lists are located
* select the SharePoint site and the list

Location of managed datasets and folders
===========================================

When you create a managed dataset or folder in a SharePoint Online connection, Dataiku will automatically create it within the "Default site", "Default drive" and the "Default path".

Below that root path, the "naming rule" applies. See :doc:`relocation` for more information.
