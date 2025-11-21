# Howto: Alation Integration in DSS

  * [1. Overview](#1-overview)
  * [2. Setup](#2-setup)
  * [3. Troubleshooting](#3-troubleshooting)


<a name="1-overview"></a>

## 1. Overview

DSS features an integration with the Alation data catalog that allows you to easily:

* Import tables that are in Alation as DSS datasets
* From a table in Alation, quickly navigate to the corresponding DSS dataset(s), if they already exist.

The integration can be invoked:

* From DSS: when you click on the "New dataset" button, you have an option "Import from Alation" that opens an Alation browser embedded in the DSS window. In the Alation browser, you can select a table and then import it as a dataset in DSS. This [quick video](http://dku-files.s3.amazonaws.com/alation/Dataiku%20-%20Embedded%20Alation%20Catalog%20Chooser.mp4) shows this mode of operation

* From Alation: when you are in Alation on the page of a table, you can click "Open With > Dataiku" to either navigate to the page of the corresponding dataset in DSS (if any), or to import the table as a new dataset in DSS. This [quick video](http://dku-files.s3.amazonaws.com/alation/Alation%20-%20Open%20In%20Dataiku.mp4) shows this mode of operation.

In both cases, the integration will respect both Alation and DSS security rules. The user of the integration needs accounts both on the Alation and DSS sides.

Integration supports both SQL tables (all types supported by DSS) and Hive tables from Alation.

<a name="2-setup"></a>

## 2. Setup

To enable Alation integration, you need to have an admin Alation API token. Alation integration needs to be performed by a DSS administrator.

* In DSS, go to Administration > Settings > Misc.
* Scroll to the bottom to Alation Integration
* Check Enable
* Enter the base URL of your Alation server
* Save settings
* Enter your Admin API token and click on the Register button (needed only for "Open With" mode)
* Reload the page in your browser

You should now:

* Have a new "Import from Alation" button from your DSS "New dataset" button
* Have a new "Open With > Dataiku" button in the table page of DSS.

<a name="3-troubleshooting"></a>

# 3. Troubleshooting

## 3.1. Registration fails with "PKIX" errors

This happens if your Alation server is using HTTPS but your DSS is not configured to recognize the root certificate of Alation.

Follow [these instructions](https://doc.dataiku.com/dss/latest/installation/java_env.html#adding-ssl-certificates-to-the-java-truststore) to properly configure certificates in DSS.

## 3.2. Registration fails with "already existing" error

This generally means that registration has already been performed on the Alation side. When this is the case, DSS tries to remove the previous registration and to setup a new one on the Alation side, but it does not always succeed.

If "Open With > Dataiku" still does not work, see with your Alation administrator to check why unregistration fails, and to manually remove the registration.