// Create a Map
var map = L.map('map').setView([37.76, -122.4487], 11);

// Add an OpenStreetMap(c) based background
var cartodb = new L.tileLayer(
    'http://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, &copy; <a href="http://cartodb.com/attributions">CartoDB</a>'
    })
map.addLayer(cartodb);

// This function calls the `Count_crime` endpoint of the backend to retrieve the lattice into the `data` variable. It then goes through each lattice square to draw it on the map with a proper color (the more red, the more crimes).
var draw_map = function (year) { // (1)
    // Request aggregated data from the backend
    $.getJSON(getWebAppBackendUrl('Count_crime'), {year: year}).done(function (data) {
        // Draw data on the map using d3.js
        var cmap = d3.scale.sqrt()
            .domain([data.min_nb, data.max_nb])
            .range(["steelblue", "red"])
            .interpolate(d3.interpolateHcl);

        for (var i = 0; i < data.nb_crimes.length; i++) {
            // Retrieve square corner
            c_1 = [data.bin_y[data.nb_crimes[i].latitude], data.bin_x[data.nb_crimes[i].longitude]];
            c_2 = [data.bin_y[data.nb_crimes[i].latitude], data.bin_x[data.nb_crimes[i].longitude + 1]];
            c_3 = [data.bin_y[data.nb_crimes[i].latitude + 1], data.bin_x[data.nb_crimes[i].longitude + 1]];
            c_4 = [data.bin_y[data.nb_crimes[i].latitude + 1], data.bin_x[data.nb_crimes[i].longitude]];

            // Draw square coloured by the number of crimes
            var polygon = L.polygon([c_1, c_2, c_3, c_4], {
                fillOpacity: 0.4,
                clickable: false,
                color: cmap(data.nb_crimes[i].C)
            })
                .addTo(map);
        }
    });
};

function clearMap() {
    for (i in map._layers) {
        if (map._layers[i]._path != undefined) {
            try {
                map.removeLayer(map._layers[i]);
            } catch (e) {
                console.log("Problem with " + e + map._layers[i]);
            }
        }
    }
}

$('#slider').slider({
    value: 2014,
    min: 2004,
    max: 2014,
    step: 1,
    create: function (event, ui) {
        $('#amount').val($(this).slider('value'));
        draw_map($(this).slider('value'));
    },
    change: function (event, ui) {
        $('#amount').val(ui.value);
        clearMap();
        draw_map(ui.value);
    }
});

$('#amount').val($('#slider').slider('value'));