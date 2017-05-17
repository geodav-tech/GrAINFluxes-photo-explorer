var map;
var infowindow;

function infowindowEventClosure(marker, contentObj) {
    google.maps.event.addListener(marker, 'spider_click', function(e) {
        infowindow.setContent(contentObj.properties.name);
        infowindow.open(map, marker);
        $('#photo-title-link').attr('href', 'media/photos/' + contentObj.properties.name);
        $('#photo-title').html(contentObj.properties.name);
        $('#selected-photo').attr('src', 'media/photos/' + contentObj.properties.name);
        $('#date-time').html(contentObj.properties.date + ', ' + contentObj.properties.time + ' local time');
    });
}

function initMap() {
    map = new google.maps.Map(document.getElementById('map'), {
        center: { lat: 67.04583277326387, lng: -50.850143432617195 },
        zoom: 9,
        mapTypeId: 'satellite'
    });
    infowindow = new google.maps.InfoWindow();

    var oms = new OverlappingMarkerSpiderfier(map, {
        markersWontMove: true,
        markersWontHide: true,
        basicFormatEvents: true
    });

    $.getJSON('data/output.geojson', function(data) {
        for (var i = 0, len = data.features.length; i < len; i++) {
            var marker = new google.maps.Marker({
                position: {
                    lat: data.features[i].geometry.coordinates[1],
                    lng: data.features[i].geometry.coordinates[0]
                }
            });
            infowindowEventClosure(marker, data.features[i]);
            oms.addMarker(marker);
        }
    });
}
