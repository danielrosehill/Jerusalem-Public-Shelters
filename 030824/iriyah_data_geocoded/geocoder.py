import pandas as pd
import requests

input_file_path = '/home/daniel/Git/jlmpublicshelters/030824/iriyah_data_geocoded/inputs/jlmshelters.csv'
output_file_path = '/home/daniel/Git/jlmpublicshelters/030824/iriyah_data_geocoded/output/geocoded.csv'

df = pd.read_csv(input_file_path)

address_column = 'Address'

def geocode_address(address):
    try:

        encoded_address = requests.utils.quote(address)
        url = f"https://geocode.xyz/{encoded_address}?json=1"
        response = requests.get(url)
        data = response.json()
        

        latitude = data.get('latt')
        longitude = data.get('longt')
        return latitude, longitude
    except Exception as e:
        print(f"Error: {e}")
        return None, None

df['Latitude'], df['Longitude'] = zip(*df[address_column].apply(geocode_address))


df.to_csv(output_file_path, index=False)

print(f"Geocoding complete. The results are saved in '{output_file_path}'.")
