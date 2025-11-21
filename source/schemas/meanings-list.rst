List of recognized meanings
#############################

.. contents::
	:local:

Here is the list of meanings that DSS recognizes.

Basic meanings
================

Text
-----

Anything is valid for the "Text" meaning.

Decimal
--------

Recognizes "raw" decimals (like: 1234.32). Accepts negative and scientific notation

Integer
--------

Recognizes "raw" integers (like: 1234). If the number is higher than 2147483647 or lower than -2147483648, use bigint type.

Boolean
--------

This meaning recognizes a large number of possible values (true, false, yes, no, 1, 0, ...)

Datetime with zone / Dates (needs parsing)
------------------------------------------

The Datetime with zone meaning only recognizes datetimes in the ISO-8601 format, ie dates like ``2014-12-31T23:05:43.123Z``

Note that the timezone information is mandatory for a valid *Datetime with eone*

For all other kinds of dates the "Date (needs parsing)" meaning will be recognized. For more information, see:

* :doc:`dates`
* :doc:`/preparation/dates`

Datetime no zone
------------------------------

The Datetime no zone meaning only recognizes datetimes in the ``yyyy-MM-dd HH:mm:ss`` format, ie dates like ``2014-12-31 23:05:43``. Fractional seconds are optional.

Date only
------------------------------

The Date only meaning only recognizes "pure" dates, that is values denoting a calendar day in the ``yyyy-MM-dd`` format, like ``2014-12-31``.


Object / Array
---------------

Recognizes objects and arrays in JSON notation

Natural language
-----------------

Recognizes "long text made of words"

Geospatial meanings
====================

Latitude / Longitude
----------------------

This meaning recognizes a large number of formats for expressing geometric coordinates.

Geopoint
---------

This meaning recognizes a large number of formats for expressing a point in geometric coordinates (notably WKT)

Geometry
---------

This meaning recognizes WKT format for geographic lines, polygons and multipolygons.

Country
--------

The Country meaning recognizes country names (in English) and ISO Country codes

US State
---------

This meaning recognizes both short codes and full names for USA states.


Web-specific meanings
========================

* IP Address (IPv4 and IPv6)
* URL
* HTTP Query String
* User Agent
* E-Mail address

Other meanings
================

DSS recognizes a few other specific meanings
