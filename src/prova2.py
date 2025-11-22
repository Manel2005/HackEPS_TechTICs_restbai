import requests
import json
from shapely.geometry import Point, shape

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

    for feature in barris['geometry']:
        geom=feature['geometry']
        forma=shape(geom)

        if forma.contains(punt):
            nom=feature['properties'].get('name','Barri')
            return nom
        
    return "Desconegut"

def agrupar_barris(llocs):
    """
    Agrupa els elements d'Overpass en un diccionari de resultats per nom de barri.
    """
    dic_barris={}
    
    barris=dades_barris()

    for element in llocs:
        lat=element.get('lat')
        lon=element.get('lon')
        
        b=get_barri(lat,lon,barris)
        
        if b not in dic_barris:
            dic_barris[b]=[element]
        else:
            dic_barris[b].append(element)
            

    return dic_barris

    

if __name__ == '__main__':
    
    e_agrupats=agrupar_barris(llocs)
    print(e_agrupats)

