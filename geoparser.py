import exifread  # this is the only non-standard dependency
import os
import datetime
import json

# Photos directory path, must contain only photos
photos_dir = 'media/photos'

# The output schema, standard geojson
output_geojson = {
    "type": "FeatureCollection",
    "crs": {
        "type": "name",
        "properties": {
            "name": "urn:ogc:def:crs:OGC:1.3:CRS84"
        }
    },
    "features": []
}


def _convert_to_degress(value):
    """
    Borrowed from https://gist.github.com/snakeye/fdc372dbf11370fe29eb

    Helper function to convert the GPS coordinates stored in the EXIF to degress in float format
    :param value:
    :type value: exifread.utils.Ratio
    :rtype: float
    """
    d = float(value.values[0].num) / float(value.values[0].den)
    m = float(value.values[1].num) / float(value.values[1].den)
    s = float(value.values[2].num) / float(value.values[2].den)

    return d + (m / 60.0) + (s / 3600.0)


def get_exif_location(exif_data):
    """
    Borrowed from https://gist.github.com/snakeye/fdc372dbf11370fe29eb

    Returns the latitude and longitude, if available, from the provided exif_data (obtained through get_exif_data above)
    """
    lat = None
    lon = None

    gps_latitude = exif_data['GPS GPSLatitude']
    gps_latitude_ref = exif_data['GPS GPSLatitudeRef']
    gps_longitude = exif_data['GPS GPSLongitude']
    gps_longitude_ref = exif_data['GPS GPSLongitudeRef']

    if gps_latitude and gps_latitude_ref and gps_longitude and gps_longitude_ref:
        lat = _convert_to_degress(gps_latitude)
        if gps_latitude_ref.values[0] != 'N':
            lat = 0 - lat

        lon = _convert_to_degress(gps_longitude)
        if gps_longitude_ref.values[0] != 'E':
            lon = 0 - lon

    return lat, lon


# Iterates through photos in photos_dir, reads metadata, writes coordinates (if any) and metadata to our geojson object
for photo_name in os.listdir(os.path.abspath(photos_dir)):
    with open(os.path.join(os.path.abspath(photos_dir), photo_name)) as photo:
        tags = exifread.process_file(photo)
        if 'GPS GPSLongitude' in tags:
            datetime_obj = datetime.datetime.strptime(str(tags['Image DateTime']), '%Y:%m:%d %H:%M:%S')

            lat, lon = get_exif_location(tags)
            alt_meters = str(tags['GPS GPSAltitude'])
            date = datetime_obj.strftime('%Y-%m-%d')
            time = datetime_obj.strftime('%-I:%M:%S %p')
            name = photo_name

            output_geojson['features'].append({
                "type": "Feature",
                "properties": {
                    "date": date,
                    "time": time,
                    "name": name,
                    "altitude": alt_meters
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        lon,
                        lat
                    ]
                }
            })
        else:
            print '{} lacks GPS data.'.format(photo_name)

# Writes the geojson object out to file at the photos_dir path
with open(os.path.join(os.path.abspath(photos_dir), 'output.geojson'), 'w') as outfile:
    json.dump(output_geojson, outfile)

print 'Done!'
