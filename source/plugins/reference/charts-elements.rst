Components: Custom chart palettes and map backgrounds
#######################################################

Plugins can embed custom elements that personalize charts: color palettes and map backgrounds. In order to add a custom element, you must add the element description in a Javascript file in the plugin content.

Color palettes
==============

See :doc:`/visualization/palettes` for general information about color palettes in charts.

Color palettes can provide same graph color patterns across different charts. From the global Javascript object ``dkuColorPalettes``, there are three different functions depending on the palette type:

- Discrete: ``dkuColorPalettes.addDiscrete(palette)``
- Continuous: ``dkuColorPalettes.addContinuous(palette)``
- Diverging (continuous but colors expand to both side from the middle value): ``dkuColorPalettes.addDiverging(palette)``

The ``palette`` object has several properties:

- ``id``: unique ID across all color palettes in DSS
- ``name``: displayed name
- ``category``: category in the list
- ``colors``: array of the ordered colors (can be ``#012345`` or ``rgb(r, g, b)`` styles)
- ``values``: array of the ordered values (a value can be ``null`` for auto matching)

.. code-block:: javascript

	dkuColorPalettes.addDiscrete({
		id: 'palette-id',
		name: 'palette-name',
		category: 'palette-category',
		colors: ['#012345', 'rbg(r, g, b)'],
		values: [1, 2]
	});

Map backgrounds
==================

Map backgrounds can be customized in order to improve map style or to enable maps on offline DSS instances. From the global Javascript object ``dkuMapBackgrounds``, there are three different function to add a map background:

- ``dkuMapBackgrounds.addMapbox(mapId, displayLabel, accessToken)``: add a `Mapbox <https://www.mapbox.com/>`_ background, `see Mapbox documentation <https://www.mapbox.com/api-documentation/?language=cURL#maps>`_ Note that a "Mapbox" plugin for DSS already allows you to add Mapbox backgrounds.

	- ``mapId`` Mapbox identifier of the background
	- ``displayLabel`` How it will appear in DSS
	- ``accessToken`` Mapbox API token

.. code-block:: javascript

	dkuMapBackgrounds.addMapbox('mapbox.satellite', 'Satellites', 'ABCDE1234');


- ``dkuMapBackgrounds.addWMS(id, name, category, wmsURL, layerId)``: add a generic `WMS <https://en.wikipedia.org/wiki/Web_Map_Service>`_ layer, `see Leaflet documentation <https://leafletjs.com/reference.html#tilelayer-wms>`__

	- ``id`` unique ID across all map backgrounds in DSS
	- ``name`` displayed name
	- ``category`` category in the list
	- ``wmsURL`` WMS service URL
	- ``layerId`` layer ID of the WMS service

.. code-block:: javascript

	dkuMapBackgrounds.addWMS('mws-map-bg', 'Map background', 'My backgrounds', 'http://mesonet.agron.iastate.edu/cgi-bin/wms/nexrad/n0r.cgi', 'nexrad-n0r-900913');

- ``dkuMapBackgrounds.addCustom(background)``: a custom map background

	- ``id`` unique ID across all map backgrounds in DSS
	- ``name`` displayed name
	- ``category`` category in the list
	- ``fadeColor`` color of faded map object
	- ``getTileLayer`` function that returns a Leaflet TileLayer object, `see Leaflet documentation <https://leafletjs.com/reference.html#tilelayer>`__

.. code-block:: javascript

	dkuMapBackgrounds.addCustom({
		id: 'map-bg',
		name: 'Map background 2',
		category: 'Custom map backgrounds',
		fadeColor: '#333',
		getTileLayer: function() {
			return new L.tileLayer('http://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png', {
				attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, &copy; <a href="http://cartodb.com/attributions">CartoDB</a>'
			});
		}
	});
