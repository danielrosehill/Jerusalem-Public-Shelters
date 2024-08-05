import geojson
import logging
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import geopandas as gpd
from shapely.geometry import Point

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

geolocator = Nominatim(user_agent="geojson_reverse_geocoder")
reverse = RateLimiter(geolocator.reverse, min_delay_seconds=1)

def reverse_geocode(coords, language):
    try:
        logging.info(f"Starting geocoding process for coordinates: {coords} with language setting: {language}")
        location = geolocator.reverse(coords, exactly_one=True, language=language)
        if location:
            address = location.address
            logging.info(f"Successfully retrieved address: {address}")
        else:
            address = "Address not found"
            logging.warning(f"No address found for coordinates: {coords}")
        return address
    except Exception as e:
        logging.error(f"Encountered an error while geocoding coordinates: {coords} in language: {language}. Error details: {e}")
        return "Error fetching address"

input_path = '/home/daniel/Git/jlmpublicshelters/250823/original_data2/data.geojson'
logging.info(f"Attempting to load GeoJSON data from file path: {input_path}")
with open(input_path, 'r') as f:
    data = geojson.load(f)
logging.info("Successfully loaded GeoJSON data")

points = []
for feature in data['features']:
    if feature['geometry']['type'] == 'Point':
        coords = feature['geometry']['coordinates']
        logging.info(f"Extracting point coordinates: {coords}")
        points.append(Point(coords[0], coords[1]))
    else:
        logging.debug(f"Skipping non-point feature with geometry type: {feature['geometry']['type']}")

gdf = gpd.GeoDataFrame(geometry=points, crs='EPSG:4326')
logging.info(f"Initial GeoDataFrame created with CRS: {gdf.crs}")

projected_gdf = gdf.to_crs(epsg=3857)
logging.info(f"GeoDataFrame re-projected to CRS: {projected_gdf.crs}")

for i, feature in enumerate(data['features']):
    if feature['geometry']['type'] == 'Point':
        original_coords = (feature['geometry']['coordinates'][1], feature['geometry']['coordinates'][0])
        projected_coords = projected_gdf.geometry[i].coords[0]
        logging.info(f"Processing feature {i+1}/{len(data['features'])}: Original coordinates: {original_coords}, Projected coordinates: {projected_coords}")

        address_he = reverse_geocode(projected_coords, language='he')
        logging.info(f"Retrieved Hebrew address: {address_he}")
        feature['properties']['address_he'] = address_he

        address_en = reverse_geocode(projected_coords, language='en')
        logging.info(f"Retrieved English address: {address_en}")
        feature['properties']['address_en'] = address_en

output_path = '/home/daniel/Git/jlmpublicshelters/250823/geocoded/updateddata.geojson'
logging.info(f"Saving modified GeoJSON data to file path: {output_path}")
with open(output_path, 'w') as f:
    geojson.dump(data, f, indent=2)

logging.info("GeoJSON data successfully saved. Reverse geolocation process completed.")
