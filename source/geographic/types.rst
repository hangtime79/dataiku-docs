Geographic data types
#####################

DSS only supports 2D geography.

Columns in any DSS dataset can have one of two geographic data types:

* `geopoint`: This column can contain the coordinates of a single point, expressed using WKT
* `geometry`: This column can contain any geometry type (point, linestring, polygon, multipolygon), expressed using WKT

Reference systems
===================

Geographic data is associated with reference systems, sometimes also referred to as CRS (Coordinate Reference System) or SRID (spatial reference identifier), which indicates how the data is projected

Geographic data types in DSS do not reference a specific CRS.

Most processing capabilities in DSS assume that the data in geographic columns uses GPS coordinates, also known as WGS-84, SRID 4326 or EPSG:4326

You can change the CRS of a geographic column using the "Change CRS processor" in the prepare recipe