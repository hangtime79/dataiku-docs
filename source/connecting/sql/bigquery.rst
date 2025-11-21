Google BigQuery
################

.. contents::
    :local:

Dataiku DSS has native support for Google BigQuery

BigQuery uses wording that sometime clashes with DSS concepts. Here are a few hints:

* The concept of "DSS Dataset" corresponds to a BigQuery table (single table)
* The concept of "BigQuery Dataset" is usually called schema in DSS (group of tables)
* A DSS partition might not translate into a BigQuery table partition and vice-versa (see below for more explanations)

Supported and unsupported features
===================================

DSS has complete support for BigQuery, except for the following:

* SQL script recipes
* Creation of BigQuery tables partitioned by ingestion time
* BigQuery wildcard tables
* Random :doc:`sampling </sampling/index>` will not be pushed-down to BigQuery if a random seed is used

The two drivers
=================

Connecting to BigQuery is usually done using a built-in driver developed by Dataiku.

Alternatively to the built-in driver, connection to BigQuery can also be done using a third-party driver provided by Google (sometimes also called the "Simba Driver").

The benefits of using the built-in driver are the following:

* dataset preview and explore (when there is no filter or selected partition) are done using `tabledata.list` which does not incur any billing from Google
* in SQL notebooks, you can preview the cost of a query before executing it (using the Explain Plan button)
* in SQL notebooks, you can view the cost of a query after its execution
* in Job logs, you can view all statistics about the executed queries (including their costs and execution plans)
* some complex NESTED fields are not read correctly using the Simba driver. The built-in driver is able to read these correctly
* you can configure labels to be applied to BigQuery jobs which helps monitor costs

The limitations of the built-in driver are the following:

* the built-in driver waits for queries completion without any configurable time out

Installing the JDBC driver
===========================

Built-in driver
----------------

No additional setup is required

Google-provided driver
------------------------

.. warning::

    We recommend that you use the latest version of the driver (1.2.16.1020 or above).

* go to https://cloud.google.com/bigquery/docs/reference/odbc-jdbc-drivers
* choose the "JDBC 4.2-compatible" download (beware: do not choose ODBC but JDBC)
* unzip the downloaded file

The JDBC driver is made of many JAR files, all of which are contained in the Zip file.

* in your DSS data directory, create a subdirectory of ``lib/jdbc`` folder named ``bigquery``. If you are updating the driver from an old version and the directory already exist, remove all files inside the ``bigquery`` folder
* copy all the JAR files to the ``lib/jdbc/bigquery`` folder 
* if the file ``slf4j-api-1.7.30.jar`` (or a later version) is present in ``lib/jdbc/bigquery``, remove the file

.. note::
    If you are updating your BigQuery driver to a newer version and the old version had been copied into ``lib/jdbc``,
    carefully remove all the files of the old BigQuery driver in ``lib/jdbc``, and then copy the files of the new
    driver into ``lib/jdbc/bigquery`` (except ``slf4j-api-1.7.30.jar``).

Connecting to BigQuery
========================

DSS supports connecting to BigQuery using a Service Account or OAuth2.

With service account credentials, DSS will be able to access all resources associated with this service account, independently of the user initiating the connection.
This also means that in the GCP audit logs, you won't have a tracing of the user behind this connection.

OAuth2 connection access means DSS will use the OAuth2 protocol to access the resources in GCP. DSS will be registered as an OAuth2 client, authorized to request and gain access
on behalf of your DSS users. 

Use a service account if:

* your DSS users don't have direct access to the resources in GCP
* you don't need resources access filtering per user

Use OAuth2 if:

* your DSS users got access to your GCP project and particularly to BigQuery
* you don't want your users to access resources via DSS in BigQuery which they don't have permission for
* you want an audit in GCP of your users accesses

Using Service Account
------------------------------------------

* you first need to create a Google Service Account
* create a private key for this account, and download the corresponding JSON file
* upload the JSON file somewhere on the DSS server

In the connection settings in DSS:

* select the credential type `Private key`
* in the Secret key field, enter the absolute path (on the DSS server) to the credentials JSON file

Alternatively, you can directly enter the content of the JSON file in the Secret key field to avoid storing the file on the server. Keep in mind that in this latter case, any DSS administrator will be able to see the content of this private file.

You can also let DSS retrieve the private key via `Application Default Credentials <https://cloud.google.com/docs/authentication/application-default-credentials>`_. In this case, simply select the credential type `Environment`.


Using OAuth2
------------------------------------------

The OAuth2 connection is performed using per-user credentials. Each user must grant DSS permission to access BigQuery on their behalf.
You will need to create an OAuth2 client in your GCP project and configure the credentials in your DSS BigQuery connection.

To create an OAuth 2.0 client ID in the console, please refer to the `following documentation <https://support.google.com/cloud/answer/6158849?hl=en>`_ .
When creating your OAuth2 client in google, you will need to:

* Select the application type `Web application`
* Add the following redirect URI `DSS_BASE_URL/dip/api/oauth2-callback` 

.. note::
  For example if DSS is accessed at https://dss.mycompany.corp/, the OAuth2 redirect URL is https://dss.mycompany.corp/dip/api/oauth2-callback

Once created, configure DSS to use this OAuth2 client. Do in DSS the following:

* create a new BigQuery connection
* fill in the basic params as usual
* select "OAuth" as the "credentials". Note that this will force you to use per-user credential
* fill the "Client id", "Client secret" (if there is one) with the information from your OAuth app
* create the connection

.. note:: 
	At this point, although the connection is operational, you can't test it yet as your user hasn't authorized DSS to access BigQuery on their behalf.

Each user, including you, will need to follow these steps to allow DSS to access GCP on their behalf:

* go to user profile > credentials
* the user will see that no authorization was given yet to DSS for this connection
* click the "Edit" button next to the new connection name
* follow the instructions that appear: Google will authenticate and get the user consent to authorize DSS to access BigQuery
* the user will be redirected automatically to DSS and will notice that credentials have successfully been obtained for the connection

If you did these steps with a user allowed to modify the connection, like an admin user, you should now be able to test the connection:

* go back to your connection settings
* click on the `Test` button which should be successful


Advanced setup (if using the built-in driver)
---------------------------------------------

Using the "Job labels" setting you can specify labels which will be applied to any BigQuery job run by DSS (this typically happens when DSS executes a query in BigQuery). The feature is designed to help you monitor BigQuery costs.

DSS variable expansion takes place when the labels are applied and the resulting labels must meet the following requirements:

* Multiple labels can be applied, up to a maximum of 64.
* Each label must be a key-value pair.
* Keys have a minimum length of 1 character and a maximum length of 63 characters, and cannot be empty. Values can be empty, and have a maximum length of 63 characters.
* Keys and values can contain only lowercase letters, numeric characters, underscores, and dashes. All characters must use UTF-8 encoding, and international characters are allowed.
* The key portion of a label must be unique within a single job. However, you can use the same key with multiple jobs.
* Keys must start with a lowercase letter or international character.

For more information on labels please refer to the `BigQuery documentation <https://cloud.google.com/bigquery/docs/labels-intro>`__.

Finally we recommend that you add an advanced property:

* Key: ``Timeout`` (DSS 13.0.2 or above)
* Value: 180

If you need an encryption key to read/write BigQuery data, you must add the following advanced property:

* Key: ``KMSKeyName`` (DSS 12.6.2 or above)
* Value: The key name of the customer-managed encryption key (CMEK) that you want DSS to use when executing queries.


Advanced setup (if using the Google-provided driver)
--------------------------------------------------------

In the connection settings, you must also specify the location of the JDBC driver jar: Enter ``lib/jdbc/bigquery`` in the Driver jars directory field.

Finally we recommend that you add an Advanced JDBC property:

* Key: ``Timeout``
* Value: 180

If you need to connect to BigQuery via a Proxy, you must add the following advanced JDBC properties (and also configure the global proxy for DSS in the "Settings" tab of the Administration page):

* Key: ``ProxyHost`` 
* Value: The IP address or host name of your proxy server.


* Key: ``ProxyPort``
* Value: The listening port of your proxy server.


* Key: ``ProxyUser``
* Value: The user name, if needed, for proxy server settings.


* Key: ``ProxyPassword``
* Value: The password, if needed, for proxy server settings.

If you need an encryption key to read/write BigQuery data, you must add the following advanced JDBC property:

* Key: ``KMSKeyName`` (DSS 12.6.2 or above)
* Value: The key name of the customer-managed encryption key (CMEK) that you want DSS to use when executing queries.


Writing data into BigQuery
===========================

The recommended way to load data into BigQuery is either using the BigQuery
Storage Write API or to do it from files stored in Google Cloud Storage.

By default DSS uses the BigQuery Storage Write API. It can however also use the
fast load method utilizing Google Cloud Storage. For that, you need a GCS
connection. Then, in the settings of the BigQuery connection:

* Enable "Automatic fast-write"
* In "Auto fast write connection", enter the name of the GCS connection to use
* In "Path in connection", enter a relative path to the root of the GCS connection, such as "bigquery-tmp". This is a temporary path that will be used in order to put temporary upload files. This should not be a path containing datasets.

DSS will now automatically use the optimal GCS-to-BigQuery copy mechanism when executing a recipe that needs to load data "from the outside" into BigQuery, such as a code recipe.

Note that when running visual recipes directly in-database, this does not apply, as the data does not move outside of the database.

The GCS bucket and BigQuery database should be in the same GCP region and
project.

.. warning::

    When using the BigQuery Storage Write API, you can only stream data into a table partitioned by a time-unit column if the partitions are between 10 years in the past and 1 year in the future. See `BigQuery documentation <https://cloud.google.com/bigquery/docs/write-api#time-unit_column_partitioning>`__.

    For tables with more than 10 years of history, you can ask your Administrator to enable "Automatic fast-write" on the connection instead.

Explicit sync from GCS
-----------------------

In addition to the automatic fast-write that happens transparently whenever a
recipe has to write into BigQuery, assuming the automatic fast-write is
configured, the Sync recipe also has an explicit "GCS to BigQuery" engine. This
is faster than the automatic fast-write because it does not copy to the
temporary location in GCS first.

It will be used automatically if the following constraints are met:

* The source dataset is stored on GCS 
* The destination dataset is stored on BigQuery

In addition:

* The GCS bucket and BigQuery database should be in the same GCP region and project
* The schema of the input dataset must match the schema of the output dataset, and values stored in fields must be valid with respect to the declared BigQuery column type.

BigQuery native partitioning and clustering
============================================

By default, Dataiku does not create BigQuery tables that are partitioned, unless the associated managed DSS dataset is partitioned by a time range dimension. In this case, the native partitioning will be automatically proposed.

For partitioning based on discrete values, a warning will be displayed if the native partitioning is not properly configured, as it could lead to increased query costs.

To create a BigQuery table that is natively partitioned:

* Go to the settings for your Dataset and open the **Advanced** settings tab
* Check the "Create BigQuery partitioned table" checkbox and indicate the column to use to partition the table. This column must be of type DATE, DATEONLY, DATETIMENOTZ, INT, TINYINT, SMALLINT or BIGINT (in the DSS semantic)

BigQuery partitioned tables can also be clustered by up to 4 clustering columns of STRING, DATE, DATEONLY, DATETIMENOTZ, BOOLEAN, INT, TINYINT, SMALLINT or BIGINT (in DSS semantic).

.. warning::

    You might have to configure the BigQuery native partitioning and clustering for any new DSS dataset. DSS does not always automatically propagate these settings when creating new datasets.

.. note::

    You can create a BigQuery partitioned table even for a DSS dataset that is not partitioned (in DSS semantic).

Partition filter requirements
-----------------------------

When you create a partitioned table, you can require that all queries on that table must include a predicate filter (a WHERE clause) on the partitioning column.

This option can improve performance and reduce costs. See `BigQuery documentation <https://cloud.google.com/bigquery/docs/managing-partitioned-tables#require-filter>`__.

To enable this option when creating a BigQuery partitioned table with DSS, go to the **Advanced** settings tab, set the Partitioning if it is not already configured, and check the "Require partition filter" option.

Partitioning consistency
------------------------

To prevent generating uncontrolled amount of data on non-partitioned BigQuery tables, you can forbid users to write partitioned data to tables on a specific connection if there is a mismatch between the dataset and the BigQuery native partitioning (dataset is partitioned while the table is not or there is a difference between the partitioning of each).

To enable this feature, go to the settings for your connection and enable the "Partitioning consistency" parameter.

This setting can be overridden for individual datasets within the **Advanced** settings tab, by setting the "Partitioning consistency" parameter. By default, it will inherit the value of the connection.

If enabled for a dataset, recipes will now be prevented from writing data to a BigQuery table if the associated DSS dataset partitioning does not match the table partitioning.

External datasets
----------------------

DSS can also read partitioned BigQuery tables as external datasets. However, if the partitioned BigQuery table has the "Require partition filter" option activated,
then DSS will automatically partition the DSS dataset with the corresponding dimension matching the partitioning settings on the BigQuery table.
This ensures that DSS automatically adds the required partition filter when generating SQL code for visual recipes.

.. note::

    If the "Require partition filter" is activated on the BigQuery table, and the partitioning column is a timestamp without time zone (that is, a DATETIME column), then the partition IDs may differ between BigQuery and DSS. DSS will interpret its own partition IDs as being at UTC time, while the BigQuery partitioning column, and therefore the BigQuery partition IDs, will be interpreted to be at the "assumed time zone" selected on the dataset settings page.


Bigframes integration
=====================

Dataiku can leverage the `Bigframes framework <https://cloud.google.com/python/docs/reference/bigframes/latest>`_ in order to read Dataiku datasets stored in BigQuery, build queries using Dataframes and then write the result back to a BigQuery dataset.

Bigframes integration can be used in Python code recipes and in Jupyter notebooks.

In order to use it, you will need:

* A BigQuery connection, with :

    - Security option "Details readable by" set to Every analyst or Selected groups.
    - Either `Location` or `DefaultDataset` defined in the ``Advanced properties`` (if not using the default location, which is `US`)

* A Dataiku Code Env based on Python 3.9, with the package "bigframes" installed. 

To get started with Bigframes, follow these steps:

* Ensure the above prerequisites are fulfilled
* Create a BigQuery dataset
* From this dataset, create a Python recipe with an output dataset stored on the BigQuery connection
* Switch to Advanced tab. In the Python environment section, select a Code Env with Bigframes installed
* Switch to Code tab. Delete all lines except the first two (keep the import dataiku)
* Click the "{} CODE SAMPLES" button and enter Bigframes in the search field.
* Select "Read and Write datasets with Bigframes"
* Click the "+ INSERT" button corresponding to "Load a dataset as a Bigframes dataframe and write into another dataset"
* Run the recipe. You're all set.

You can also check the :doc:`reference documentation <devguide:concepts-and-examples/bigframes>`

