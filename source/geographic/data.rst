Geographic data 
#################

Dataiku DSS can connect to the following type of geographic data:

GeoJSON files
==============

DSS can read GeoJSON files stored on any filesystem.

DSS can also export any dataset containing a geographic column to GeoJSON

ESRI Shapefiles
===============

DSS can read ESRI Shapefiles. Please see :doc:`/connecting/formats/shapefile` for more details

WKT
===

Any column containing `WKT <https://en.wikipedia.org/wiki/Well-known_text_representation_of_geometry>`_ can be treated as geographic data 

KML
===

DSS can read KML/KMZ files.

.. note::

	This capability is provided by the "KML Format extractor", which you need to install. Please see :doc:`/plugins/installing`.

	This plugin is :doc:`Not supported </troubleshooting/support-tiers>`

Snowflake
=========

DSS can natively read and write the Snowflake GEOGRAPHY data type, which is read as `geometry` DSS columns.

Please see :doc:`/connecting/sql/snowflake` for more details.

DSS can also push-down some geographic computation to Snowflake

PostGIS
========

`PostGIS <https://postgis.net/>`_ is a widely used PostgreSQL database extension that allows to store and process geospatial data.

DSS can natively read and write PostGIS geo data types.

Please see :doc:`/connecting/sql/postgresql` for more details.

DSS can also push-down some geographic computation to PostgreSQL / PostGIS