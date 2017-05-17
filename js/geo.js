var map;

function initMap() {
    map = new google.maps.Map(document.getElementById('map'), {
        center: { lat: 67.04583277326387, lng: -50.850143432617195 },
        zoom: 9,
        mapTypeId: 'satellite'
    });
}

$(document).ready(function() {
    $.getJSON('data/output.geojson', function(data) {
        map.data.addGeoJson(data);
    });

    map.data.addListener('click', function(event) {
        $('#photo-title-link').attr('href', 'media/photos/' + event.feature.getProperty("name"));
        $('#photo-title').html(event.feature.getProperty("name"));
        $('#selected-photo').attr('src', 'media/photos/' + event.feature.getProperty("name"));
        $('#date-time').html(event.feature.getProperty("date") + ', ' + event.feature.getProperty("time") + ' local time');
    });
});
