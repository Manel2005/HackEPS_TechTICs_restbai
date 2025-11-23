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
        try:
            response = requests.post(
                overpass_url,
                data={'data': data},
                timeout=30
            )
            response.raise_for_status()  # error si codi HTTP no és 200
            json_data = response.json()
        except (requests.RequestException, ValueError) as e:
            # Aquí NO petem l'app, només registrem/ignorem
            print(f"[Overpass] Error amb el filtre {param}: {e}")
            continue
        else:
            elements = json_data.get('elements', [])
            l.extend(elements)

    return l