Georouting and isochrones
##########################

.. contents::
	:local:

* Isochrones are polygons centered on a geopoint that define areas reachable within a certain time, taking into account itinerary and mean of transportation.
* Georouting is the process of computing an itinerary with time and distance between two geopoints, depending on means of transportation.

.. note::

	These capabilities are provided in DSS with the Geo Router plugin. It needs to be installed : Please see :doc:`/plugins/installing`. 

	This plugin is :doc:`Not supported </troubleshooting/support-tiers>`.


It should be noted that georouting and isochrones computation are always best-effort activities. It is not always possible to perform either of these activities, data may be incomplete depending on locations. Dataiku is not able to provide any guarantee as to the completeness or correctness of any georouting-related data.

Route computation
==================
Georouting is the process of computing an itinerary with time and distance between two geopoints (driving/walking/...).

You need to have a dataset with two geopoint columns. Select your dataset, and, from the right panel, select Geo Router. This creates a recipe.

You can then select the starting and destination geopoint columns and the transport mode (car, bicycle, walking).

The recipe outputs the dataset with:

* a column containing the travel time.
* a column containing the travel distance.
* a column containing the itinerary as a geometry column (LINESTRING format), which you can then display using Geometry Map charts.

Isochrones computation
=======================
Isochrones are polygons centered on a geopoint that define areas reachable within a certain time, taking into account itinerary and mean of transportation.

You need to have a dataset with a geopoint column. Select your dataset, and, from the right panel, select Geo Router. This creates a recipe.

You can then select the geopoint column, the travel time, and the transport mode (car, bicycle, walking).

The recipe outputs the dataset with an additional geometry column (in MULTIPOLYGON format) representing the isochrone, which you can then display using Geometry Map charts.

The Geo Router plugin
=======================

The plugin uses an online routing service provided by Dataiku. Your DSS instance needs to have outgoing Internet access in order to use this capability.

When running the recipes, DSS users can chose to use a cache to store and retrieve results of the recipes for each row of the input dataset. This is to avoid making redundant calls to the server.
In case of a UIF setup for DSS, each DSS user has a personal georouting cache that is stored in the associated UNIX user's home directory, in *$UNIX_HOME/.cache/dss/plugins/georouting/*. In case of a non-UIF DSS setup, the cache is in the home directory of the UNIX user that runs DSS, in *$DSS_UNIX_HOME/.cache/dss/plugins/georouting/*.
The caches can be deleted by running the Clear georouting cache macro. In a UIF setup, using this macro, each DSS user can clean his own cache. If the DSS admin wants to delete any user's cache, he will have to manually delete the *$UNIX_HOME/.cache/dss/plugins/georouting/* directory.

The plugin has several settings :

* Batch size : number of rows of the input dataset that are processed simultaneously by the recipe. Increasing this value will reduce recipe run time, but can lead to out of memory errors.
* Routes recipe parallel workers : number of parallel workers processing a batch of rows for the compute routes recipe. It is also the number of simultaneous queries that can be sent to the online server. Increasing this value will reduce recipe run times, but can lead to timeout errors from the online server.
* Isochrones recipe parallel workers : Same as the previous setting, but for the isochrones recipe.
* Maximum cache size : maximum size that can be allocated to the plugin cache. In case of a non UIF DSS setup, there is only one cache on the machine hosting DSS. In case of a UIF setup, there can be at most one cache per DSS user. Thus the total memory allocated to georouting caches on the machine can be *cache_size X number_of_DSS_users*.

