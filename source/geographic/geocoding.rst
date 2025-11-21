Geocoding and reverse geocoding
################################

.. contents::
	:local:

* Geocoding (sometimes called Forward Geocoding) is the process of transforming an address into geographic coordinates
* Reverse geocoding is the process geographic coordinates into administrative information (country, region, city, ...)

It should be noted that geocoding and reverse geocoding are always best-effort activities. It is not always possible to perform either of these activities, data may be incomplete depending on locations. Dataiku is not able to provide any guarantee as to the completeness of correctness of any geocoding-related data.

Geocoding
==========

.. note::

	This capability is provided by the Geocoder plugin, which you need to install. Please see :doc:`/plugins/installing`.

	This plugin is :doc:`Not supported </troubleshooting/support-tiers>`

The Geocoder uses online geocoding service providers. Your DSS instance needs to have outgoing Internet access.

You will need an API key for most of these providers. Some providers have some free plans, sometimes with limits, sometimes with various usage policies. Please make sure to review the usage policy of each provider before using it.

Not all providers have the same level of coverage of the world, so you should use providers depending on their coverage.

Providers with "Batch available" usually have significantly better performance

.. csv-table::
   :header: "Provider", "Optimal for", "Usage Policy", "Batch available"

    ArcGIS,World,,
    Baidu,China,API key,
    Bing,World,API key,yes
    CanadaPost,Canada,API key,
    FreeGeoIP,World,,
    Gaode,China,API key,
    Geocoder.ca (Geolytica),CA & US,Rate Limit,
    GeocodeFarm,World,Policy,
    GeoNames,World,Username,
    GeoOttawa,Ottawa,,
    Gisgraphy,World,API key,
    Google,World,"Rate Limit, Policy",
    HERE,World,API key,
    IPInfo,World,"Rate Limit, Plans",
    Komoot (OSM powered),World,,
    LocationIQ,World,API Key,
    Mapbox,World,API key,
    MapQuest,World,API key,yes
    MaxMind,World,,
    OpenCage,World,API key,
    OpenStreetMap,World,Policy,
    Tamu,US,API key,
    TGOS,Taiwan,,
    TomTom,World,API key,
    USCensus,US,,yes
    What3Words,World,API key,
    Yahoo,World,,
    Yandex,Russia,,

The plugin provides a recipe. You can use this recipe multiple times in a row using different providers, for example in case the previous providers failed on some inputs. The recipe will only try to recompute rows for which outputs are not already filled.

Reverse geocoding
==================

DSS provides two different reverse geocoding capabilities:

* A native one, which reverse geocodes at the city level, and uses bundled data. This reverse geocoder is available as a preparation processor. It does not use any external provider, does not need any API key or payment, and is fast

* The ability to call external providers, which require API keys or payments, requires Internet access, and is usually significantly slower, but that provide better resolution (up to the address level)

Bundled-data city-level reverse geocoder
-----------------------------------------

.. note::

	This capability is provided by the "Reverse geocoding" plugin, which you need to install. Please see :doc:`/plugins/installing`.

	This plugin is covered by :doc:`Tier 2 support </troubleshooting/support-tiers>`

The reverse geocoding prepare processor takes geographic coordinates as input and extracts the different levels of administrative boundary to which it belongs (country, region, city ...). The administrative boundaries we use are the ones defined in Open Street Map. The type of administrative boundary for each level depends on the country. For more information please refer to the `Open Street Map documentation <https://wiki.openstreetmap.org/wiki/Tag:boundary=administrative>`_.

* You need a column containing a Geo Point or a Geometry as input.
* The processor outputs two columns per administrative level for which you provide a column name: one with the local name of the administrative entity and one with the English name.
* Selecting "Output the smallest selected administrative area" will output the shape of the administrative entity. This polygon is encoded using `WKT format <https://en.wikipedia.org/wiki/Well-known_text_representation_of_geometry>`_. It is displayed as a third column to the administrative level for which you provided a column name. In case several levels are selected, only the smallest in size is displayed (for instance if both city and country are selected, it will return the shape of the city).

Online reverse geocoder
------------------------

.. note::
	
	This capability is provided by the "Geocoder plugin, which you need to install. Please see :doc:`/plugins/installing`.

	This plugin is :doc:`Not supported </troubleshooting/support-tiers>`

The Reverse Geocoder uses online reverse geocoding service providers. Your DSS instance needs to have outgoing Internet access.

You will need an API key for most of these providers. Some providers have some free plans, sometimes with limits, sometimes with various usage policies. Please make sure to review the usage policy of each provider before using it.

Not all providers have the same level of coverage of the world, so you should use providers depending on their coverage.

Providers with "Batch available" usually have significantly better performance

.. csv-table::
   :header: "Provider", "Optimal for", "Usage Policy", "Batch available"

    ArcGIS,World,,
    Baidu,China,API key,
    Bing,World,API key,yes
    Gaode,China,API key,
    GeocodeFarm,World,Policy,
    Gisgraphy,World,API key,
    Google,World,"Rate Limit, Policy",
    HERE,World,API key,
    Komoot (OSM powered),World,,
    LocationIQ,World,API Key,
    Mapbox,World,API key,
    MapQuest,World,API key,
    OpenCage,World,API key,
    OpenStreetMap,World,Policy,
    USCensus,US,,
    What3Words,World,API key,
    Yandex,Russia,,

The plugin provides a recipe. You can use this recipe multiple times in a row using different providers, for example in case the previous providers failed on some inputs. The recipe will only try to recompute rows for which outputs are not already filled.

Zipcode geocoding
====================

Zipcode geocoding provides "Country + zipcode" --> "Geographic coordinates" resolution, at the city-level resolution.

.. note::

	This capability is provided by the "Zipcode geocoding" plugin, which you need to install. Please see :doc:`/plugins/installing`.

	This plugin is covered by :doc:`Tier 2 support </troubleshooting/support-tiers>`

It is available as a preparation recipe processor

* You need a column containing the country (name or ISO code) and a column containing the zipcode
* The processor outputs a Geo Point column