from geopy.geocoders import Nominatim
import re
import os
from opencage.geocoder import OpenCageGeocode
from pyzipcode import ZipCodeDatabase
import math
import requests
from collections import namedtuple
from dotenv import load_dotenv

load_dotenv()
zcdb = ZipCodeDatabase()

def get_geoloc_geopy(key):
    print(f'using geopy:{key}')
    try:
        geolocator = Nominatim(user_agent="data_completion")
        location = geolocator.geocode(key)
        postal_code = location.raw.get('address', {}).get('postcode')
        if location.address:
            address = location.address
            address_content = address.split(', ') if address else []
            if postal_code:
                print(f"Code postal: {postal_code}")
            elif len(address_content)>1:
                for item in address_content:
                    item=item.strip()
                    if re.search(r'\d', item):
                        postal_code=item
            
        if not postal_code:
            postal_code=f"Zip not found! Address:{location.address}"
        print(f"""
            -----------------------
            Latitude:{location.raw['lat']}
            Longitude:{location.raw['lon']}
            Zip: {postal_code}
            """)
        return location.raw['lat'],location.raw['lon'],postal_code
    except:
        print('Error: geoloc not found')
       


def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0  
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    return distance


def geocode_query(place):
    url = os.getenv('url_search').format(key_words=place,api_key=os.getenv('API_KEY'))
    response = requests.get(url).json()
    if response['results']:
        location = response['results'][0]['geometry']
        components = response['results'][0]['components']
        state = components.get('state', None)
        city = components.get('city', None)
        postalcode = components.get('postalcode', None) 
        zip_codes=namedtuple('ZipCode', ['zip', 'city', 'state', 'longitude', 'latitude', 'timezone', 'dst'])
      
        if not postalcode:
            
            if state:
                zip_codes = zcdb.find_zip(state=state)  

            else:
                zip_codes = zcdb.find_zip(city=city) 
        
        if not zip_codes:
                    postalcode="Zip not found"
        else:
            closest_zip = min(zip_codes, key=lambda zip_code: haversine(location['lat'], location['lng'], zip_code.latitude, zip_code.longitude))
            postalcode=closest_zip.zip
        print(f"""
            -----------------------
            Latitude:{location['lat']}
            Longitude:{location['lng']}
            Zip: {postalcode}
            """)
        return location['lat'], location['lng'], postalcode
    
    else:    
        return None

def get_geoloc_opencagedata(country, province):
    print('using opencagedata')
    coords = geocode_query(f'{province}, {country}')
    if coords:
        return coords
    
    coords = geocode_query(province)
    if coords:
        return coords
    
    coords = geocode_query(country)
    if coords:
        return coords
    else:
        return None

