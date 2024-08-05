import geojson
import logging
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

logging.basicConfig(level=logging.INFO, format='%(levelname)s:%(message)s')

geolocator = Nominatim(user_agent="geojson_reverse_geocoder")
reverse = RateLimiter(geolocator.reverse, min_delay_seconds=1)

def reverse_geocode(coords, language):
    try:
        logging.info(f"Geocoding coordinates {coords} in {language}")
        location = geolocator.reverse(coords, exactly_one=True, language=language)
        address = location.address if location else "Address not found"
        logging.info(f"Retrieved address: {address}")
        return address
    except Exception as e:
        logging.error(f"Error geocoding {coords} in {language}: {e}")
        return "Error fetching address"

input_path = '/home/daniel/Git/jlmpublicshelters/250823/conversion/data.geojson'
logging.info(f"Loading GeoJSON data from {input_path}")
with open(input_path, 'r') as f:
    data = geojson.load(f)

for feature in data['features']:
    if feature['geometry']['type'] == 'Point':
        coords = (feature['geometry']['coordinates'][1], feature['geometry']['coordinates'][0])
        feature['properties']['address_he'] = reverse_geocode(coords, language='he')
        feature['properties']['address_en'] = reverse_geocode(coords, language='en')

output_path = '/home/daniel/Git/jlmpublicshelters/250823/conversion/updateddata.geojson'
logging.info(f"Saving modified GeoJSON data to {output_path}")
with open(output_path, 'w') as f:
    geojson.dump(data, f, indent=2)

logging.info("Reverse geolocation completed.")