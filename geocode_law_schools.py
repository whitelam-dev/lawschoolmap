import requests
import time
import json

# Load all law school data files
files = [
    'law_schools_top14.json',
    'law_schools_15_30.json',
    'law_schools_31_75.json',
    'law_schools_76_100.json'
]

all_schools = []
for fname in files:
    with open(fname, 'r', encoding='utf-8') as f:
        all_schools.extend(json.load(f))

# Geocode using Nominatim
GEOCODE_URL = 'https://nominatim.openstreetmap.org/search'
headers = {'User-Agent': 'LawSchoolMapBot/1.0'}
results = []

for school in all_schools:
    address = school.get('address')
    if not address:
        continue
    params = {
        'q': address,
        'format': 'json',
        'limit': 1
    }
    resp = requests.get(GEOCODE_URL, params=params, headers=headers)
    data = resp.json()
    lat, lon = None, None
    if data:
        lat = data[0]['lat']
        lon = data[0]['lon']
    school['lat'] = lat
    school['lon'] = lon
    results.append(school)
    time.sleep(1)  # Be polite to Nominatim

with open('law_schools_geocoded.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, indent=2)

print(f"Geocoded {len(results)} schools. Output: law_schools_geocoded.json")
