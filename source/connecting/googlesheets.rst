Google Sheets
####################


Dataiku can interact with Google Sheets to:

* read and write datasets
* populate a project with a dataset per sheet

.. note::

	This capability is provided by the "googlesheets" plugin, which you need to install. Please see :doc:`/plugins/installing`.

	This plugin is :doc:`Not supported </troubleshooting/support-tiers>`


Create a Google Sheets preset
=============================
Dataiku supports connecting to Google Sheets using a Service Account or OAuth2.

With service account credentials, Dataiku will be able to access all resources associated with this service account, independently of the user initiating the preset.

OAuth2 preset access means Dataiku will use the OAuth2 protocol to access the resources in Google Sheets. Dataiku will be registered as an OAuth2 client, authorized to request and gain access on behalf of your Dataiku users. 

Use a service account if:

* your Dataiku users don't have direct access to the resources in Google Sheets
* you don't need resources access filtering per user

Use OAuth2 if:

* your Dataiku users have access to your Google Sheets resources
* you do not want your users to access resources via Dataiku in Google Sheets which they do not have permission for

Using Service Account
------------------------------------------

Before connecting to Google Cloud via Dataiku you will have to: 

* make sure "Google Sheets API" is enabled in `Google Cloud console's API Manager <https://console.cloud.google.com/apis/library/sheets.googleapis.com>`_
* `create a service account <https://console.developers.google.com/iam-admin/serviceaccounts>`_ and export your private key in **JSON** format
* note the service account email address. You will need to share any document you want to access on Dataiku with this address.

Configure your Service Account preset : 

* navigate to the **Google Sheets plugin page > Settings > Service Account > + Add preset**
* parse the entire content of your service account private key in JSON format in the **Service Account credentials** box

Using OAuth2
------------------------------------------

The OAuth2 connection is performed using per-user credentials. Each user must grant Dataiku permission to access Google Sheets on their behalf.
You will need first to create an OAuth2 client in your Google Sheets project and configure the credentials in your Dataiku Google Sheets preset.

To create an OAuth 2.0 client ID in the console, please refer to the `following documentation <https://support.google.com/cloud/answer/6158849?hl=en>`_ .
When creating your OAuth2 client in google, you will need to:

* make sure "Google Sheets API" is enabled in `Google Cloud console's API Manager <https://console.cloud.google.com/apis/library/sheets.googleapis.com>`_
    * "Google Drive API" also need to be enabled if you intend to use the Google Sheets "Last modified based on file ID" scenario trigger.
* select the application type `Web application`
* add the following redirect URI `DSS_BASE_URL/dip/api/oauth2-callback`

.. note::
  For example if Dataiku is accessed at https://dataiku.mycompany.corp/, the OAuth2 redirect URL is https://dataiku.mycompany.corp/dip/api/oauth2-callback


Once created, configure Dataiku to use this OAuth2 client. In the **Google Sheet plugin page > Settings > Google Single Sign On**, do the following:

* create a new Google Single Sign On preset
* fill the "Client id", "Client secret" with the information from your OAuth app

.. note::
  At this point, although the preset is operational, you can't test it yet as your user hasn't authorized Dataiku to access Google Sheets on their behalf.

Each user, including you, will need to follow these steps to allow Dataiku to access Google Sheets on their behalf:

* go to user `Profile and settings > Credentials`
* the user will see that no authorization was given yet to Dataiku for this preset
* click the "Edit" button next to the new preset name
* follow the instructions that appear: Google will authenticate and get the user consent to authorize Dataiku to access Google Sheets
* the user will be redirected automatically to Dataiku and will notice that credentials have successfully been obtained for the preset

Usage
======================

Share a spreadsheet
------------------------------------------

* if you are using a service account, make sure the document you want to access via the plugin is shared with the service account's email address.
* find the **document ID** for the Google Sheets you want to interact with. It can be found in the document's URL, in the section between *https://docs.google.com/spreadsheets/d/* and */*. For instance, if the URL is `https://docs.google.com/spreadsheets/d/4RMEq[...]mHUz4/edit#gid=0` the **document ID** is `4RMEq[...]mHUz4`.

Creating Google Sheets datasets
------------------------------------------

From either the Flow or the datasets list, click on +Dataset > Google Sheets > Google Sheets document. 

* select the type of authentication (Single Sign On or Service account)
* select the authentication preset
* input the **document ID**
* if all is correct, the list of sheets available with the document should update itself.
* finally, preset Test & Get schema 

* Format (advanced parameters):
    * First row contains column headers
    * First row contains data
    * JSON

Write or append lines to a Google Sheets documents
--------------------------------------------------

From a project's flow, select a source dataset, then click on **Google Sheets > Google Sheet - append recipe** from the right panel. Select the write mode:

* Append to the sheet: Running this recipe will add all the line from the source dataset at the end of the target Google Sheets document. 
* Overwrite the sheet: the target Google Sheets document's content will be replaced with the dataset.

* Values interpretation (`from Google's documentation <https://developers.google.com/sheets/api/reference/rest/v4/ValueInputOption>`_):
    * RAW: The values the user has entered will not be parsed and will be stored as-is.
    * Format numbers, dates, or currencies in the spreadsheet: The values will be parsed as if the user typed them into the UI. Numbers will stay as numbers, but strings may be converted to numbers, dates, etc. following the same rules that are applied when entering text into a cell via the Google Sheets UI.

Add one dataset per sheet in your project's flow
------------------------------------------------

This macro imports all the selected sheets of a Google Sheets document and add them to your project as datasets. Initially , they will all be added to a zone created after the name of the Google Sheets document.

.. note::

  These datasets are copies of the initial Google Sheets. The macro needs to be run again every time the data content requires to be refreshed. This can be done by mean of a scenario step for instance.

In your Dataiku project, select **... > Macros > googlesheets > Import GoogleSheets**. Select the type of authentication, the preset, **document ID**, the sheets to import. If no sheet is selected, all sheets will be imported.

* Dataset creation mode:
    * **Overwrite the existing datasets**: Datasets will be created with this name structure <<Spreadsheet name>>_<<Sheet name>>. If it already exists, the dataset content will be replaced with the sheet's content.
    * **Create new datasets if already exist**: If a Dataset with the name already exists, a new one will be created with another name.
    * **Skip the existing datasets**: nothing is done with the sheet if a dataset with that name already exists.

* **Dry run**: When activated, this option allows the user to safely list what operations will be performed if the macro is run
