import geojson
from pyproj import Transformer

source_crs = "EPSG:4326"  
destination_crs = "EPSG:3857"  

transformer = Transformer.from_crs(source_crs, destination_crs)

def transform_coords(coords):
    if isinstance(coords[0], list):
        return [transform_coords(coord) for coord in coords]
    else:
        return list(transformer.transform(*coords))

with open('/home/daniel/Git/jlmpublicshelters/250823/conversion/data.geojson') as f:
    data = geojson.load(f)

if 'features' in data:
    for feature in data['features']:
        geometry = feature['geometry']
        if geometry['type'] == 'Point':
            geometry['coordinates'] = transform_coords(geometry['coordinates'])
        elif geometry['type'] in ['LineString', 'MultiPoint']:
            geometry['coordinates'] = transform_coords(geometry['coordinates'])
        elif geometry['type'] in ['Polygon', 'MultiLineString']:
            geometry['coordinates'] = [transform_coords(coords) for coords in geometry['coordinates']]
        elif geometry['type'] == 'MultiPolygon':
            geometry['coordinates'] = [[transform_coords(coords) for coords in polygon] for polygon in geometry['coordinates']]

with open('output.geojson', 'w') as f:
    geojson.dump(data, f)
