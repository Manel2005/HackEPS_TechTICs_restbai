import overpy
from overpy.exception import OverpassGatewayTimeout
from typing import List, Dict, Any, Optional
import sys

# ===================================================================
# CONFIGURACIÓ GLOBAL
# ===================================================================

api = overpy.Overpass()

# Bounding Box de la Gran Los Angeles: (Sud, Oest, Nord, Est)
BB_LA = (33.70, -118.60, 34.30, -117.90) 

# Ordre de cerca de les etiquetes de contenció (de més petit a més gran/general)
ETIQUETES_BARRI = [
    'addr:quarter',       # Més petit (quarter)
    'addr:locality',      # Localitat petita
    'addr:neighbourhood', # Barri estàndard
    'neighbourhood',
    'addr:suburb',        # Suburbi/Districte
    'addr:city',          # Ciutat (com a fallback)
]

# ===================================================================
# FUNCIONS D'AGRUPACIÓ I CONSULTA
# ===================================================================

def agrupar_resultats_per_barri(
    resultats_agrupats: Dict[str, List[Dict[str, Any]]], 
    elements: List[Any], 
    amenity_cerca: str
) -> Dict[str, List[Dict[str, Any]]]:
    """
    Agrupa els elements d'Overpass en un diccionari de resultats per nom de barri.
    """
    
    for element in elements:
        
        barri_name = 'Barri Desconegut'
        
        # 1. Trobar l'etiqueta de barri més específica (prioritzant barris petits)
        for tag_key in ETIQUETES_BARRI:
            if element.tags.get(tag_key):
                if tag_key in ['addr:city', 'addr:suburb']:
                    # Nomenclatura per a nivells més grans
                    barri_name = f"[CIUTAT] {element.tags.get(tag_key)}"
                else:
                    # Nomenclatura per a nivells locals/barris
                    barri_name = element.tags.get(tag_key)
                break
        
        # 2. Obtenir el nom de l'amenity
        nom_amenity = element.tags.get('name', f"Sense Nom (ID: {element.id})")
        
        # 3. Guardar el resultat al diccionari d'entrada
        if barri_name not in resultats_agrupats:
            resultats_agrupats[barri_name] = []
        
        resultats_agrupats[barri_name].append({
            'nom': nom_amenity,
            'amenity': amenity_cerca,
            'lat': getattr(element, 'lat', getattr(element, 'center_lat', 'N/A')),
            'lon': getattr(element, 'lon', getattr(element, 'center_lon', 'N/A')),
        })
            
    return resultats_agrupats


def consulta_amenity_amb_barri(tag_key: str, tag_value: str, bounding_box: tuple, timeout: int = 120):
    """
    Busca totes les amenities (tag_key=tag_value) dins del BB i intenta adjuntar 
    les dades de contenció amb 'is_in'.
    """
    min_lat, min_lon, max_lat, max_lon = bounding_box
    
    # La consulta utilitza tag_key i tag_value (l'amenity) com a variables
    query = f"""
    [out:json][timeout:{timeout}];
    
    // 1. Cerca TOTS els elements amb l'amenity dins del BB
    (
      node[{tag_key}="{tag_value}"]({min_lat},{min_lon},{max_lat},{max_lon});
      way[{tag_key}="{tag_value}"]({min_lat},{min_lon},{max_lat},{max_lon});
      relation[{tag_key}="{tag_value}"]({min_lat},{min_lon},{max_lat},{max_lon});
    )->.amenities;
    
    // 2. Adjunta el nom del barri més proper/contenidor.
    .amenities is_in;
    
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
    
# ===================================================================
# BLOC PRINCIPAL D'EXECUCIÓ
# ===================================================================

if __name__ == '__main__':
    
    print("--- Cerca d'Amenity a l'Àrea Metropolitana de LA ---")
    
    # 🌟🌟🌟 BUCLE DE VALIDACIÓ DE L'ENTRADA 🌟🌟🌟
    AMENITY_CERCA = ""
    while True:
        amenity_input = input("Introdueix l'amenity d'OpenStreetMap que vols cercar (ex: cafe, restaurant, park): ").strip().lower()
        
        if amenity_input:
            AMENITY_CERCA = amenity_input
            break # Surt del bucle si l'entrada és vàlida
        else:
            print("❌ Entrada no vàlida. L'amenity no pot ser buida. Torna-ho a intentar.")
            
    TAG_CLAU = "amenity"
    
    # 0. Inicialitzem el diccionari de resultats
    resultats_agrupats: Dict[str, List[Dict[str, Any]]] = {}
    
    # 1. Execució de la cerca global
    resultat_global = consulta_amenity_amb_barri(TAG_CLAU, AMENITY_CERCA, BB_LA)
    
    elements = list(resultat_global.nodes) + list(resultat_global.ways) + list(resultat_global.relations)
    num_total = len(elements)
    
    print(f"\n✅ Total de {AMENITY_CERCA}s trobats globalment: {num_total}")
    
    if num_total == 0:
        print("No s'ha trobat cap element. Sortint.")
        sys.exit()
    
    # 2. Crida a la funció d'agrupació
    print("\n3. Agrupant i reclassificant resultats...")
    resultats_finals = agrupar_resultats_per_barri(resultats_agrupats, elements, AMENITY_CERCA)
        
    # 4. Resum Final Agrupat
    print("\n--- RESUM DE DISTRIBUCIÓ PER BARRI ---")
    
    # Creació del resum de recompte
    resum_recompte = {
        barri: len(amenities) 
        for barri, amenities in resultats_finals.items()
    }
    
    # Ordenem per nombre de resultats
    for barri, total in sorted(resum_recompte.items(), key=lambda item: item[1], reverse=True):
        # Utilitzem el nom de l'amenity proporcionat per l'usuari
        print(f"[{barri}]: {total} {AMENITY_CERCA}s")

        