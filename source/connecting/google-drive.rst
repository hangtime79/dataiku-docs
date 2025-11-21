Google Drive
####################

Dataiku can interact with Google Drive to read and write files stored on shared folders.

.. note::

	This capability is provided by the "google-drive" plugin, which you need to install. Please see :doc:`/plugins/installing`.

	This plugin is :doc:`Not supported </troubleshooting/support-tiers>`

Create a Google Drive preset
=============================

Dataiku supports connecting to Google Drive using a Service Account or OAuth2.

With service account credentials, Dataiku will be able to access all resources associated with this service account, independently of the user initiating the preset.

OAuth2 preset access means Dataiku will use the OAuth2 protocol to access the resources in Google Drive. Dataiku will be registered as an OAuth2 client, authorized to request and gain access on behalf of your Dataiku users. 

Use a service account if:

* your Dataiku users don't have direct access to the resources in Google Drive
* you don't need resources access filtering per user

Use OAuth2 if:

* your Dataiku users have access to your Google Drive resources
* you do not want your users to access resources via Dataiku in Google Drive which they do not have permission for

Using Service Account
------------------------------------------

Before connecting to Google Cloud via Dataiku you will have to: 

* make sure "Google Drive API" is enabled in `Google Cloud console's API Manager <https://console.cloud.google.com/apis/library/drive.googleapis.com>`_
* `create a service account <https://console.developers.google.com/iam-admin/serviceaccounts>`_ and export your private key in **JSON** format
* note the service account email address. You will need to share any document you want to access on Dataiku with this address.

Configure your Service Account preset : 

* navigate to the **Google Drive plugin page > Settings > Google Drive Token > + Add preset**
* parse the entire content of your service account private key in JSON format in the **Access credentials** box

Using OAuth2
------------------------------------------

The OAuth2 connection is performed using per-user credentials. Each user must grant Dataiku permission to access Google Drive on their behalf.
You will first need to create an OAuth2 client in your Google Drive project and configure the credentials in your Dataiku Google Drive preset.

To create an OAuth 2.0 client ID in the console, please refer to the `following documentation <https://support.google.com/cloud/answer/6158849?hl=en>`_ .
When creating your OAuth2 client in google, you will need to:

* make sure "Google Drive API" is enabled in `Google Cloud console's API Manager <https://console.cloud.google.com/apis/library/drive.googleapis.com>`_
* select the application type `Web application`
* add the following redirect URI `DSS_BASE_URL/dip/api/oauth2-callback`

.. note::
  For example if Dataiku is accessed at https://dataiku.mycompany.corp/, the OAuth2 redirect URL is https://dataiku.mycompany.corp/dip/api/oauth2-callback


Once created, configure Dataiku to use this OAuth2 client. In the **Google Drive plugin page > Settings > Google Single Sign On**, do the following:

* create a new Google Single Sign On preset
* fill the "Client id", "Client secret" with the information from your OAuth app

.. note::
  At this point, although the preset is operational, you can't test it yet as your user hasn't authorized Dataiku to access Google Drive on their behalf.

Each user, including you, will need to follow these steps to allow Dataiku to access Google Drive on their behalf:

* go to user `Profile and settings > Credentials`
* the user will see that no authorization was given yet to Dataiku for this preset
* click the "Edit" button next to the new preset name
* follow the instructions that appear: Google will authenticate and get the user consent to authorize Dataiku to access Google Drive
* the user will be redirected automatically to Dataiku and will notice that credentials have successfully been obtained for the preset

Usage
======================

Read a dataset
------------------------------------------

- If you are using a service account, you must first share the Google Drive document or directory with the service account email address you took note of
- Take note of the directory ID, which is the section of the directory's URL after the last slash character
- Create a new dataset in Dataiku DSS by selecting Dataset > Googledrive > Googledrive
- Pick your preset for the connection, and in ID of root directory, paste the previously copied directory ID

Write data into Google Drive
------------------------------------------

- In your DSS project flow, select **Dataset** > **Folder**
- Choose **Google drive** in the **Store into** parameter and click **Create**. An **External code failed** error may appear because you have not selected your preset yet.
- In the Settings tab of the folder, select the authentication type, your preset, add your Drive directory ID, and save. You can now export your dataset into your newly created Google Drive managed folder.

Opening multisheets GoogleSheet documents
------------------------------------------

By default the plugin transmits GoogleSheet documents to Dataiku as CSV files. In cases where a Google Sheet document contains several sheets, the plugin can be set to return datasets in the Excel format instead.
To do so, in your newly created dataset or folder Settings tab, activate the read parameter **Convert Google Sheets to .xlsx**. In some instances, DSS might have difficulty recognizing the file format. Go in the *Format/Preview* tab. The **Type** should be set to *Excel* and **XLSX format** should be on.
