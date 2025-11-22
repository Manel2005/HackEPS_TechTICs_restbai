import requests
import json

overpass_url = 'https://overpass-api.de/api/interpreter'
overpass_query = '''
[out:json];
area["boundary"="administrative"]["admin_level"="8"][name="Los Angeles"]->.la;
nwr
'''

def do_query(param):
    global overpass_query

    # Amb
    if param == "Groceries":
        data = overpass_query+'["shop"="supermarket"](area.la);out;'
        response = requests.get(overpass_url, params={'data': data})
        print(response.json().get('elements'))
    elif param == "":
        overpass_query += '["leisure"="dog_park"]'
    elif param == "":
        overpass_query += '["leisure"="park"]'
    elif param == "":
        overpass_query += '["leisure"="nature-reserve"]'
    elif param == "":
        overpass_query += '["leisure"="garden"]'
    elif param == "":
        overpass_query += '["amenity"="nightclub"]'
    elif param == "":
        overpass_query += '["amenity"="pub"]'
    elif param == "":
        overpass_query += '["amenity"="bar"]'
    elif param == "":
        overpass_query += '["amenity"="kindergarten"]'
    elif param == "":
        overpass_query += '["amenity"="school"]'
    elif param == "":
        overpass_query += '["amenity"="college"]'
    elif param == "":
        overpass_query += '["amenity"="university"]'
    elif param == "":
        overpass_query += '["shop"="jewelry"]'

    # Yes/No Parameters'
    if param == "Access":
        overpass_query += '["wheelchair"="yes"]'

if __name__=='__main__':
    do_query("Sustainable")
    do_query("Groceries")