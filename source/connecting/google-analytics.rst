Google Analytics
####################

Dataiku can interact with Google Analytics to read datasets.

.. note::

	This capability is provided by the "google-analytics-4" plugin, which you need to install. Please see :doc:`/plugins/installing`.

	This plugin is :doc:`Not supported </troubleshooting/support-tiers>`

Create a Google Analytics preset
================================
Dataiku supports connecting to Google Analytics using OAuth2.

The OAuth2 connection is performed using per-user credentials. Each user must grant Dataiku permission to access Google Analytics on their behalf.
You will need first to create an OAuth2 client in your `Google Analytics project <https://console.cloud.google.com>`_ and configure the credentials in your Dataiku Google Analytics preset.

To create an OAuth 2.0 client ID in the console, please refer to the `following documentation <https://support.google.com/cloud/answer/6158849?hl=en>`_ .
When creating your OAuth2 client in google, you will need to:

* make sure `Google Analytics API <https://console.cloud.google.com/apis/api/analytics.googleapis.com>`_, `Google Analytics Data API <https://console.cloud.google.com/apis/api/analyticsdata.googleapis.com>`_ and `Google Analytics Admin API <https://console.cloud.google.com/apis/api/analyticsadmin.googleapis.com>`_ are enabled
* select the application type `Web application`
* add the following redirect URI `DSS_BASE_URL/dip/api/oauth2-callback`

.. note::
  For example if Dataiku is accessed at https://dataiku.mycompany.corp/, the OAuth2 redirect URL is https://dataiku.mycompany.corp/dip/api/oauth2-callback


Once created, configure Dataiku to use this OAuth2 client. In the **Google Analytics 4 plugin page > Settings > Google Single Sign On**, do the following:

* create a new Google Single Sign On preset
* fill the "Client id", "Client secret" with the information from your OAuth app

.. note::
  At this point, although the preset is operational, you can't test it yet as your user hasn't authorized Dataiku to access Google Analytics on their behalf.

Each user, including you, will need to follow these steps to allow Dataiku to access Google Analytics on their behalf:

* go to user `Profile and settings > Credentials`
* the user will see that no authorization was given yet to Dataiku for this preset
* click the "Edit" button next to the new preset name
* follow the instructions that appear: Google will authenticate and get the user consent to authorize Dataiku to access Google Analytics
* the user will be redirected automatically to Dataiku and will notice that credentials have successfully been obtained for the preset

Usage
======================

Creating Google Analytics datasets
------------------------------------------

From either the Flow or the datasets list, click on +Dataset > Google Analytics 4 > Get Report (GA4).

* select the authentication preset
* select the analytics account
* select the property / app, or the property / app ID by selecting the **Enter manually** option
* select between one and 10 metrics or goals
* optionally, select up to 9 dimensions
* enter the time range, either using the calendars or the **YYYY-MM-DD** format

Finally, hit *Test & get schema* and *Create*
