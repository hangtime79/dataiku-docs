ESRI Shapefiles
################

DSS can parse ESRI shapefiles. You can either use a folder containing all the required files, or a .shp.zip

Vecmath library
=================

Shapefiles can contain data in a very large number of projections. Some projections require advanced math to parse. This capability is provided by a library called **Vecmath**. Vecmath is also required for some projections handling in data preparation

Vecmath is a GPL library. For licensing reasons, DSS is not provided with Vecmath. To open some Shapefiles, you need to download and install Vecmath manually. Please install vecmath-1.3.1.jar or later.

* Download it from MVN repository and review the licensing terms: https://mvnrepository.com/artifact/javax.vecmath/vecmath/1.5.2

* Put the downloaded jar in DSS_DATA_DIR/lib/jdbc

* Restart DSS:

.. code-block:: bash

	./bin/dss restart

You should now be able to read all Shapefiles.
