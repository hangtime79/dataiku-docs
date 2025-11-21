Time series preparation
##################################

Before using time series data for analysis or forecasting, it is often necessary to perform one or more preparation steps on the data. 

For example, given time series data with missing or irregular timestamps, you may consider performing preparation steps such as resampling and interpolation. You may also want to perform smoothing, extrema extraction, or segmentation on the data. 

.. _preparation_plugin_label:

Time series preparation plugin
===============================

Dataiku DSS provides a preparation plugin that includes visual recipes for performing the following operations on time series data:

.. toctree::
	:maxdepth: 1
	
	resampling
	windowing
	extrema-extraction
	interval-extraction
	decomposition
	

.. note::

    The time series preparation plugin is fully supported by Dataiku.

Plugin installation
-------------------

You can install the time series preparation plugin (and other plugins) if you are a user with administrative privileges. See :doc:`/plugins/installing` for more details.

Once the plugin is installed, users with normal privileges can view the plugin store and the list of installed plugins, and use any plugins installed on the Dataiku DSS instance. See :doc:`/plugins/installed` for more details.

Upgrade note
------------

Starting with version 2.0.3, this plugin supports Python versions 3.6 to 3.11. If you have already installed the plugin and want to use its latest features, make sure to use one of these Python versions.
