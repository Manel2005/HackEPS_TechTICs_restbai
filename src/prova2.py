import overpy
from overpy.exception import OverpassGatewayTimeout

api = overpy.Overpass()

# Bounding Box de la Gran Los Angeles: (Sud, Oest, Nord, Est)
BB_LA = (33.70, -118.60, 34.30, -117.90) 

def consulta_amenity_amb_barri(tag_key, tag_value, bounding_box, timeout=120):
    """
    Busca totes les amenities dins del BB i intenta adjuntar el nom del barri (place=neighbourhood)
    utilitzant la sintaxi Overpass 'is_in'.
    """
    min_lat, min_lon, max_lat, max_lon = bounding_box
    
    query = f"""
    [out:json][timeout:{timeout}];
    
    // 1. Cerca TOTS els elements amb l'amenity dins del BB
    (
      node[{tag_key}="{tag_value}"]({min_lat},{min_lon},{max_lat},{max_lon});
      way[{tag_key}="{tag_value}"]({min_lat},{min_lon},{max_lat},{max_lon});
      relation[{tag_key}="{tag_value}"]({min_lat},{min_lon},{max_lat},{max_lon});
    )->.amenities;
    
    // 2. Adjunta el nom del barri més proper/contenidor:
    // Aquesta funció cerca l'àrea circumdant i adjunta les etiquetes de contenció.
    .amenities is_in;
    
    // 3. Imprimeix els resultats amb les noves etiquetes adjuntes
    out center;
    """
    
    try:
        print(f"Iniciant cerca global de {tag_key}={tag_value} a LA i adjuntant dades de barri...")
        result = api.query(query)
        return result
    except OverpassGatewayTimeout:
        print("❌ Error: Temps d'espera excedit. La consulta és massa complexa.")
        return overpy.Result()
    except Exception as e:
        print(f"❌ Ha ocorregut un error en la consulta: {e}")
        return overpy.Result()
    
if __name__ == '__main__':
    
    AMENITY_CERCA = "cafe"
    TAG_CLAU = "amenity"
    
    # Utilitzem un diccionari per agrupar els resultats per nom de barri
    resultats_agrupats = {}
    
    # 1. Execució de la cerca global
    resultat_global = consulta_amenity_amb_barri(TAG_CLAU, AMENITY_CERCA, BB_LA)
    
    elements = list(resultat_global.nodes) + list(resultat_global.ways) + list(resultat_global.relations)
    num_total = len(elements)
    
    print(f"\n✅ Total de {AMENITY_CERCA}s trobats globalment: {num_total}")
    
    if num_total == 0:
        print("No s'ha trobat cap element. Sortint.")
    else:
        # 2. Agrupació dels elements per barri (post-processament)
        
        for element in elements:
            
            # Intentem extreure el nom del barri d'alguna de les etiquetes que 'is_in' adjunta:
            # - 'addr:city' és la ciutat gran
            # - 'addr:neighbourhood' o 'name:ca' és el que busquem
            
            # Prioritzem la cerca de noms de barris més específics:
            barri_name = element.tags.get('addr:neighbourhood') or element.tags.get('neighbourhood')
            
            # Si no troba un barri específic, utilitzem el nom de la ciutat o una clau 'Desconegut'
            if not barri_name:
                barri_name = element.tags.get('addr:city', 'Barri Desconegut')
            
            # Obtenim el nom de la cafeteria
            nom_amenity = element.tags.get('name', f"Sense Nom (ID: {element.id})")
            
            # 3. Guardar el resultat
            if barri_name not in resultats_agrupats:
                resultats_agrupats[barri_name] = []
            
            resultats_agrupats[barri_name].append({
                'nom': nom_amenity,
                'lat': getattr(element, 'lat', getattr(element, 'center_lat', 'N/A')),
                'lon': getattr(element, 'lon', getattr(element, 'center_lon', 'N/A')),
            })
            
        # 4. Resum Final Agrupat
        print("\n--- RESUM DE DISTRIBUCIÓ PER BARRI ---")
        
        for barri, amenities in sorted(resultats_agrupats.items(), key=lambda item: len(item[1]), reverse=True):
            print(f"[{barri}]: {len(amenities)} {AMENITY_CERCA}s")