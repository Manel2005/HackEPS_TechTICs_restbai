import shapely
from barris import *

def calcular_duresa_barri(barri_feature, duresa_geojson):
    """
    Calcula l'índex HD_IND_W mitjà ponderat per àrea per a un únic barri.
    """
    index_duresa_list = []

    # 1. Preparar la geometria del barri (el contenidor)
    geom = barri_feature['geometry']
    # Adaptació a format Shapely si utilitza 'rings' (la teva lògica)
    if 'rings' in geom:
        geo_adaptat = {
            'type': 'Polygon',  
            'coordinates': geom['rings'] 
        }
    else:
        geo_adaptat = geom
        
    forma_barri = shape(geo_adaptat)

    # 2. Iterar sobre les àrees de duresa (el contingut)
    for att in duresa_geojson['features']:
        geom_var = att['geometry']
        forma_var = shape(geom_var)

        # Comprovar si hi ha solapament
        if forma_barri.intersects(forma_var):
            
            # Calcular la intersecció (l'àrea de solapament)
            interseccio = forma_barri.intersection(forma_var)
            
            if not interseccio.is_empty:
                # Obtenir l'índex de duresa
                HD_IND_W = att['properties']['HD_IND_W']
                
                # Afegir a la llista amb el pes de l'àrea d'intersecció
                index_duresa_list.append({
                    'index': HD_IND_W,
                    'area': interseccio.area
                })

    # 3. Suma Ponderada Final
    if index_duresa_list:
        suma_area_ponderada = sum(item['index'] * item['area'] for item in index_duresa_list)
        area_total_coberta = sum(item['area'] for item in index_duresa_list)
        
        # El resultat és la mitjana ponderada (Suma(Index * Àrea) / Suma(Àrea))
        mitjana_ponderada = suma_area_ponderada / area_total_coberta
        return mitjana_ponderada
    else:
        # Cap zona de duresa intersecta aquest barri
        return None
    
    
def agrupar_duresa_per_barris(barris_geojson, duresa_geojson):
    """
    Calcula la mitjana ponderada de l'índex HD_IND_W per a cada barri
    i retorna un diccionari simplificat: {nom_barri: HD_IND_W_MITJANA}.
    """

    # Inicialitzem el diccionari 
    dic_barris_amb_duresa = {}
    
    # 1. Iterar sobre cada feature de barri
    for feature in barris_geojson['features']:
        
        # Extreure el nom del barri per utilitzar-lo com a clau
        try:
            # Assumim que el nom és a 'attributes' (com és comú en JSON d'ArcGIS)
            nom_barri = feature['attributes']['name'] 
        except KeyError:
            # Si no hi és a 'attributes', buscar a 'properties'
            nom_barri = feature['properties'].get('name', f"Barri sense nom ID {feature.get('id', 'Desconegut')}")
        
        # 2. Calcular la duresa ponderada utilitzant la funció auxiliar
        hd_ind_w_mitja = calcular_duresa_barri(feature, duresa_geojson)
        
        # 3. Ficar el resultat al diccionari de la manera simplificada: {nom_barri: valor}
        
        # Evitem duplicats/sobrescriure si ja existeix, tot i que amb GeoJSON de barris és rar
        if nom_barri not in dic_barris_amb_duresa:
            # Afegim la mitjana calculada com a valor per a la clau del nom del barri
            dic_barris_amb_duresa[nom_barri] = hd_ind_w_mitja
        
        # Si hi hagués duplicats, l'últim valor prevaldria
        # else:
        # dic_barris_amb_duresa[nom_barri] = hd_ind_w_mitja


    return dic_barris_amb_duresa

if __name__ == '__main__':
    url_barris="https://services5.arcgis.com/7nsPwEMP38bSkCjy/arcgis/rest/services/LA_Times_Neighborhoods/FeatureServer/0/query?where=1%3D1&outFields=*&outSR=4326&f=json"
    url_crims='https://services1.arcgis.com/tp9wqSVX1AitKgjd/arcgis/rest/services/chei/FeatureServer/0/query?outFields=*&where=1%3D1&f=geojson'
    barris=dades_barris(url_barris)
    duresa=dades_barris(url_crims)
    print(agrupar_duresa_per_barris(barris,duresa))


