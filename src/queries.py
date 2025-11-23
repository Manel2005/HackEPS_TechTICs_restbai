import requests
import json

overpass_url = 'https://overpass-api.de/api/interpreter'
overpass_query_noAccess = '''
[out:json];
area["boundary"="administrative"]["admin_level"="8"][name="Los Angeles"]->.la;
nwr
'''

overpass_query_Access = '''
[out:json];
area["boundary"="administrative"]["admin_level"="8"][name="Los Angeles"]->.la;
nwr["wheelchair"="yes"]
'''

def do_query(params, access=0):
    global overpass_query_noAccess
    global overpass_query_Access

    if access == 1:
        overpass_query = overpass_query_Access
    else:
        overpass_query = overpass_query_noAccess

    l = []

    for param in params:
        data = overpass_query + param + '(area.la);out center;'
        response = requests.post(overpass_url, data={'data':data})
        l.extend(response.json().get('elements'))
    return l



if __name__=='__main__':
    print(do_query(['["amenity"="restaurant"]', '["amenity"="bar"]']))