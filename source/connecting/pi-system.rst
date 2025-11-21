PI System / PIWebAPI server
###########################

You can create datasets based on data located in an OSIsoft PI System.

.. note::

	This capability is provided by the "pi-system" plugin, which you need to install. Please see :doc:`/plugins/installing`.

	The PI System servers you want to access must have PIWebAPI enabled.

	This plugin is :doc:`Not supported </troubleshooting/support-tiers>`

.. _setup-the-authentication-preset:

Setup the authentication preset
===============================
  
* Choose an authentication method : Basic or NTLM
* Define a default server. Note that this setting can be overwritten later on by Dataiku users.
* Select `Users can override server URL` to allow Dataiku users to use another server than the default one defined for this preset.
* Select `Users can disable SSL checks` to allow Dataiku users to disable the SSL checks for this preset.
* If your PI Server WebApi use a custom SSL certificate, set the path to a it. The certificate file and its containing directory must be readable by all system users of the Dataiku instance.

Setup authentication per user
=============================

Go to your Dataiku profile page > Credentials > Name of the preset. Click on the corresponding edit button and enter your PI System username / password.

Attribute search Dataset
========================

Select the server and database you want to search attributes on. Attributes can be searched based on their name or description. Wildcards ("*", "?") can be used in the search box.

Two types of datasets can be produced:

* A list of assets paths, which can be used later on to download the actual assets metrics (using the :ref:`Asset metrics downloader recipe <assets-metrics-downloader>`)
* A list of assets and metrics:

  * Select Retrieve metrics
  * Select the :ref:`type of data <data-types>` expected
  * Fill in the necessary Start / End time / Interval / Sync time as apply, using the available :ref:`time formats<time-formats>`

Event frames search Dataset
===========================

Select a server and a database. Event frames can be search based on:

* their name. Wildcards ("*", "?") can be used in the search box.
* start / end time, using the available :ref:`time formats<time-formats>`

Two types of datasets can be produced:

* A list of Event frames, which can be used later on to download the linked assets and metrics (using the :ref:`event-frames-downloader` recipe)
* A list of assets and metrics linked to the event frame. To do so:

  * Select Retrieve metrics
  * Select the :ref:`type of data <data-types>` expected
  * Select one or several events from in the 'Event frame to retrieve' box. If none are selected, all events matching the search will be retrieved.

PIWebAPI Toolbox Dataset
========================

This dataset allows a quick and direct access to a database, an element, an attribute or a tag, provided its full path is known. With knowledge of PIWebAPI, partial paths can be used for exploration. If the preset used has writing credentials to the attribute, the obtained dataset can also be used to write information back from Dataiku to PI System.

In the 'Object path / Tag' box, set either:

* the path to a database (\\\\server_name\\database)
* the path to an element (\\\\server_name\\database\\element_1 .. \\element_n)
* the path to an attribute (\\\\server_name\\database\\element_1 .. \\element_n|attribute)
* an attribute tag (\\\\server_name\\tag.name)

Select the :ref:`type of data <data-types>` expected. Complete the missing element (Start / end times, interval, sync time...) accordingly.

.. _assets-metrics-downloader:

Assets metrics downloader Recipe
================================

The recipe outputs a dataset containing all the values for each of the attributes present in the input. Select the input dataset's column containing the list of paths.

The start/end time of the period to recover can be specified using the available :ref:`time formats<time-formats>` and :ref:`type of data <data-types>`.

.. _event-frames-downloader:

Event frames downloader Recipe
==============================

The recipe outputs the dataset with all the assets involved in the event, as well as all the metrics for the duration of the event.

Select the column containing the webids and the :ref:`type of data <data-types>` expected.

Transpose & Synchronize Recipe
==============================

Data retrieved from PI server may contain timelines of several attributes stacked one after another (also called "long format"). To perform some analyses, it can be necessary to convert from long format to a timestamp/path array.

Another issue is that timestamps are likely out of sync with one another. So before values of different attributes can be compared, one has first to either:

* align all the columns by displaying the last value received at the time of a reference timestamp
* or interpolate their values, as long as the attribute's output are not steps

All these steps can be done in one go using the Transpose & Synchronize recipe.

Select the columns containing the timestamps, the assets paths, and the metric's values. Type in the full path of the asset to use as a time reference. 

Three synchronization modes are available:

* With `Last value received`, the selected value for each record is the last one received for that attribute, at the timestamp of the reference
* `Interpolation` uses a linear interpolation based on the previous and next value of the attribute and the timestamp of the reference. This method should only be used if it makes sense with the attribute in question. That should be the case if the Step value is set to false.
* `Mixed (based on step)` will use the last value received if the attribute is of step type, and will interpolate otherwise. For this option to work you will need to have the step column available in the input dataset, and point this column in the Step column box.

The recipe outputs the dataset with:

* a timestamp column which contains the timestamps of the time reference asset
* a column per asset, containing the last available measure at the time indicated by the reference timestamp

.. note::
  
  Each column is named with the path of the attribute. This can be incompatible with various database naming schemes. To fix this, the column names can be normalized by selecting `Show advanced parameters` > `Columns names normalization` and the most appropriate method for your use case.

Advanced parameters
===================

Activating the "Show advanced parameters" option let you:

* Disable the SSL check, if this is allowed by the :ref:`preset's configuration <setup-the-authentication-preset>`
* Point to a .pem file containing an SSL certificate. Note that this file and its containing directory must be visible to all accounts on the Dataiku server.
* Speed up values retrieval by activating the batch mode. The default value for the batches size is 500 rows. Increasing this number will speed up transfer but also increase the risk of getting a ratio error from the PI-System server.

.. _data-types:

Data types
===========================

* `Interpolated <https://docs.osisoft.com/bundle/pi-web-api-reference/page/help/controllers/stream/actions/getinterpolated.html>`_ returns the interpolated values across the specified time range with a chosen sampling interval. A start time anchor can also be set. 
* `Plot <https://docs.osisoft.com/bundle/pi-web-api-reference/page/help/controllers/stream/actions/getplot.html>`_ returns the values across a specified time range
* `Recorded <https://docs.osisoft.com/bundle/pi-web-api-reference/page/help/controllers/stream/actions/getrecorded.html>`_ returns the compressed values for the selected time range.
* **Value** returns the current value.
* **Summary** returns the time weighted data summary across the last day.

.. note::

	The maximum number of points that can be retrieved for a given attribute is limited by PiWebAPI. The default limit is usually set to 1000 elements. Once this number of rows is reached, the search time span has to be reduced or split across several search operations.

.. _time-formats:

Time formats
============

Date and time can be entered using two different formats:

* Absolute dates are using the ISO 8601 format, and should follow this pattern: `YYYY-MM-DDThh:mm:ssZ`
* Relative times and dates are also possible using the OSIsoft's `Time String format <https://docs.osisoft.com/bundle/pi-web-api-reference/page/help/topics/time-strings.html>`_
