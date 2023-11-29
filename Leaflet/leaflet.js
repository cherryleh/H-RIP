var latitude = 20.389
var longitude = -157.52275766141424
var map = L.map(document.getElementById('mapDIV'), {
    center: [latitude, longitude],
    zoom: 7
});
var basemap = L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {});
basemap.addTo(map);


var ranches = L.geoJSON(ranchSquares, {
    color: 'red',
    weight: 1,

    onEachFeature: function (feature, layer) {
        var ranchName = feature.properties.Polygon;
        var currentPath = window.location.pathname;
        var url = currentPath + 'RID.php?ranch=' + ranchName;
        layer.bindPopup('<a href="' + url+'" target="_blank">'+ranchName+'</a>');
        layer.on('click', function () { layer.openPopup(); });
                

    }
}
);

ranches.addTo(map);

var islands = L.geoJSON(coastline, {
    color:'none',
}
);

islands.addTo(map);


selectbox = document.getElementById('zoombox');

var featuremap = {};



for (var i = 0; i < coastline['features'].length; i++) {
    feature = coastline['features'][i];
    featuremap[feature['properties']['isle']] = feature['properties'];

}

function zoomToIsl() {
    key = selectbox.value;
    obj = featuremap[key];
    isl = obj[Object.keys(obj)[0]];
    if (isl == 'Hawaii') {
        map.setView([obj['lat'], obj['lon']], 9);
    } else if (isl == 'Lanai') {
        map.setView([obj['lat'], obj['lon']], 11);
    } else {
        map.setView([obj['lat'], obj['lon']], 10);
    }
            
}