import requests
import json
from shapely.geometry import Point, shape
import queries

url="https://services5.arcgis.com/7nsPwEMP38bSkCjy/arcgis/rest/services/LA_Times_Neighborhoods/FeatureServer/0/query?where=1%3D1&outFields=*&outSR=4326&f=json"

def dades_barris():
    try:
        resposta = requests.get(url)
        resposta.raise_for_status() # Llença una excepció per a codis d'estat HTTP dolents
        return resposta.json()
    except requests.exceptions.RequestException as e:
        print(f"Error en descarregar el GeoJSON: {e}")
        return None

def get_barri(lat,lon,barris):
    punt=Point(lon,lat)

    for feature in barris['features']:
        geom=feature['geometry']
        if 'rings' in geom:
            geo_adaptat = {
                'type': 'Polygon',  
                'coordinates': geom['rings'] 
            }
        forma=shape(geo_adaptat)

        if forma.contains(punt):
            nom=feature['attributes']['name']
            return nom
        
    return "Desconegut"

def agrupar_barris(llocs,barris):
    """
    Agrupa els elements d'Overpass en un diccionari de resultats per nom de barri.
    """
    
    for element in llocs:
        if 'node' in element:
            lat=element.get('lat')
            lon=element.get('lon')
        elif 'center' in element:
            lat=element['center'].get('lat')
            lon=element['center'].get('lon')
        else:
            continue
        
        b=get_barri(lat,lon,barris)
        
        if b not in dic_barris:
            dic_barris[b]=[element]
        else:
            if element['id'] not in dic_barris[b]:
                dic_barris[b].append(element)
            

    return dic_barris

    

if __name__ == '__main__':
    dic_barris={}
    barris=dades_barris()
    llocs=queries.do_query("Groceries")
    #print(llocs)
    e_agrupats=agrupar_barris(llocs,barris)
    #print(e_agrupats)

