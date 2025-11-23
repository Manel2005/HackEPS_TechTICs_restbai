
#### Tipus de barris definits:
#### barris_gastrocult, barris_verd, barris_activitatf, barris_ambient, 
#### barris_privacitat, barris_accessib, barris_transpublic, barris_segurs, 
#### barris_economics, barris_ocompra, barris_pisos, barris_cases, 
#### barris_classeAlta, barris_bonaConnexio)


from queries import *
from barris import *

barris = dades_barris()

class Usuari:
    def __init__(self, name, AccessTransPublic=0, CultGastron=0, SeguretatPriv=0, CLocalComunitat=0, AUniversal = 0, EVerdsNatura=0, InfraDigital=0, AmbientDens=0):
        self.name = name
        self.AccessTransPublic = AccessTransPublic
        self.CultGastron = CultGastron
        self.SeguretatPriv = SeguretatPriv
        self.CLocalComunitat = CLocalComunitat
        self.AUniversal = AUniversal
        self.EVerdsNatura = EVerdsNatura
        self.InfraDigital = InfraDigital
        self.AmbientDens = AmbientDens
        
    def set_AccessTransPublic(self, atr1):
        self.AccessTransPublic = atr1

    def set_CultGastron(self, atr2):
        self.CultGastron = atr2

    def set_SeguretatPriv(self, atr3):
        self.SeguretatPriv = atr3

    def set_CLocalComunitat(self, atr4):
        self.CLocalComunitat = atr4
        
    def set_AUniversal(self, atr5):
        self.AUniversal = atr5

    def set_EVerdsNatura(self, atr6):
        self.EVerdsNatura = atr6

    def set_InfraDigital(self, atr7):
        self.InfraDigital = atr7

    def set_AmbientDens(self, atr8):
        self.AmbientDens = atr8

def printaprioritats(self):
    """Imprimeix les prioritats amb representació visual"""
    print("\n=== PRIORITATS DE L'USUARI ===\n")
    
    prioritats = {
        "Accessibilitat i Transport Públic": self.AccessTransPublic,
        "Cultura i Gastronomia": self.CultGastron,
        "Seguretat i Privacitat": self.SeguretatPriv,
        "Comerç Local i Comunitat": self.CLocalComunitat,
        "Accessibilitat Universal": self.AUniversal,
        "Espais Verds i Natura": self.EVerdsNatura,
        "Infraestructura Digital": self.InfraDigital,
        "Ambient i Densitat": self.AmbientDens
    }
    
    for nom, valor in prioritats.items():
        barra = "█" * valor + "░" * (5 - valor)
        print(f"{nom:40} {barra} ({valor}/5)")
    
    print("\n" + "="*60 + "\n")
        

# Mètode per obtenir el nom al que referir-nos a l'usuari
def getName():
    Username = input("Hola! Com ens podríem referir a tu d'ara en endavant?: \n >>> ")
    print("Gràcies, ", Username,"! Ens plau donar-te la benvinguda a FindMyDoor, som al teu servei per ajudar-te a trobar la teva propera llar.")
    return Username


def priorities(self): # retorna llista amb llistes de barris amb el nombre de serveis coincidents
    llista_barris =[]
    print("Si us plau, indiqui en una escala de l'1, significant gens, al 5, significant molt, quina és la importància que li atribueix a les següents carecterístiques associades a zones residencials:")
    p_gastrocult = int(input("Tenir una àmplia oferta cultural i gastronòmica = "))
    if p_gastrocult >= 3:
        looking4 = whichQueries('p_gastrocult')
        coincidencies = do_query(looking4) # lat i long de les coincidencies trobades
        barris_gastrocult = agrupar_barris(coincidencies,barris)
        llista_barris.append(barris_gastrocult)
        self.set_CultGastron(p_gastrocult)
    else:
        self.set_CultGastron(p_gastrocult)
    p_verd = int(input("Proximitat a zones verdes = "))
    if p_verd >= 3:
        looking4 = whichQueries('p_verd')
        coincidencies = do_query(looking4) 
        barris_verd = agrupar_barris(coincidencies,barris)
        llista_barris.append(barris_verd)
        self.set_EVerdsNatura(p_verd)
    else:
        self.set_EVerdsNatura(p_verd)
    p_activitatf = int(input("Proximitat a gimnassos i complexos esportius = "))
    if p_activitatf >= 3:
        looking4 = whichQueries('p_activitatf')
        coincidencies = do_query(looking4)
        barris_activitatf = agrupar_barris(coincidencies,barris)
        llista_barris.append(barris_activitatf)
        self.set_CLocalComunitat((int(self.CLocalComunitat) + 1))
    else:
        self.set_CLocalComunitat(p_activitatf)
    """  
    p_ambient = int(input("Tenir un fort sentiment de comunitat o una comunitat de veïns propera = "))
    if p_ambient >= 3:
        looking4 = whichQueries('p_ambient')
        coincidencies = do_query(looking4)
        barris_ambient = agrupar_barris(coincidencies,barris)
        llista_barris.append(barris_ambient)
        self.set_AmbientDens(p_ambient)    
    else:
        looking4 = whichQueries('p_privacitat')
        coincidencies = do_query(looking4)
        barris_privacitat = agrupar_barris(coincidencies,barris)
        llista_barris.append(barris_privacitat)
        self.set_SeguretatPriv( 6 - p_ambient)
   p_accessib = int(input("Acessibilitat Universal i fàcilitat per a persones amb mobilitat reduïda = "))
    if p_accessib >= 3:
        looking4 = whichQueries('p_accessib')
        coincidencies = do_query(looking4)
        barris_accessib = agrupar_barris(coincidencies,barris)
        llista_barris.append(barris_accessib)
        self.set_AUniversal( p_accessib)
    else:
        self.set_AUniversal( p_accessib)
    p_transpublic = int(input("Connexions amb mitjans de transport públic = "))
    if p_transpublic >= 3:
        looking4 = whichQueries('p_transpublic')
        coincidencies = do_query(looking4)
        barris_transpublic = agrupar_barris(coincidencies,barris)
        llista_barris.append(barris_transpublic)
        self.set_AccessTransPublic( p_transpublic)
    else:
        self.set_AccessTransPublic( p_transpublic)
    p_seguretat = int(input("Índex de seguretat ciutadana a la zona = "))
    if p_seguretat >= 3:
        looking4 = whichQueries('p_seguretat')
        coincidencies = do_query(looking4)
        barris_segurs = agrupar_barris(coincidencies,barris)
        llista_barris.append(barris_segurs)
        self.set_SeguretatPriv(((self.SeguretatPriv + p_seguretat)%5))
    else:
        self.set_SeguretatPriv(p_seguretat)
    p_preus = int(input("Preus de l'habitatge per sota de la mitjana general = "))
    if p_preus >= 3:
        looking4 = whichQueries('p_preus')
        coincidencies = do_query(looking4)
        barris_economics = agrupar_barris(coincidencies,barris)
        llista_barris.append(barris_economics)
    p_opcompra = int(input("Opció de compra de l'habitatge = "))
    if p_ocompra >= 3: # opció de compra
        looking4 = whichQueries('p_ocompra')
        coincidencies = do_query(looking4)
        barris_ocompra = agrupar_barris(coincidencies,barris)
        llista_barris.append(
        self.set_SeguretatPriv(((self.SeguretatPriv + p_ocompra)%5))
    p_tipushabit = int(input("Que la meva llar es trobi en un bloc residencial = "))
    if p_tipushabit >= 3:
        looking4 = whichQueries('p_tipushabit')
        coincidencies = do_query(looking4)
        barris_pisos = agrupar_barris(coincidencies,barris)
        llista_barris.append(barris_pisos)
        self.set_CLocalComunitat(p_tipushabit)
    else:
        looking4 = whichQueries('p_tipushabit')
        coincidencies = do_query('["building"="house"]')
        barris_cases = agrupar_barris(coincidencies,barris)
        llista_barris.append(
        self.set_CLocalComunitat((self.CLocalComunitat - 1)%5)
    p_nivelldevida = int(input("Que el poder adquisitiu mitjà del barri sigui alt = "))
    if p_nivelldevida >= 3:
        looking4 = whichQueries('p_nivelldevida')
        coincidencies = do_query(looking4)
        barris_classeAlta = agrupar_barris(coincidencies,barris)
        llista_barris.append(barris_classeAlta)
        self.set_CLocalComunitat((self.CLocalComunitat - p_nivelldevida)%5)
    else:
        self.set_AmbientDens((self.AmbientDens + p_nivelldevida)%5)
    p_infraestdigit = int(input("Tenir una bona connexió a internet i cobertura de fibra òptica = "))
    if p_infraestdigit >= 3:
        looking4 = whichQueries('p_infraestdigit')
        coincidencies = do_query(looking4)
        barris_bonaConnexio = agrupar_barris(coincidencies,barris)
        llista_barris.append(barris_bonaConnexio)
        self.set_InfraDigital((self.InfraDigital))
    else:
        self.set_InfraDigital((self.InfraDigital))
   """
    return llista_barris


    
def whichQueries(prioritat):
    d_priorities = {
        'p_gastrocult': ['["amenity"="restaurant"]', '["amenity"="cafe"]', '["amenity"="bar"]', 
                         '["amenity"="pub"]', '["amenity"="theatre"]', '["amenity"="cinema"]', 
                         '["amenity"="arts_centre"]', '["amenity"="nightclub"]', 
                         '["amenity"="music_venue"]', '["tourism"="museum"]', 
                         '["tourism"="gallery"]', '["amenity"="community_centre"]'],
        'p_verd': ['["leisure"="park"]', '["leisure"="garden"]', '["landuse"="forest"]', 
                   '["natural"="wood"]', '["leisure"="nature_reserve"]', 
                   '["landuse"="meadow"]', '["leisure"="playground"]'],
        'p_activitatf': ['["leisure"="sports_centre"]', '["leisure"="fitness_centre"]', 
                         '["leisure"="swimming_pool"]', '["leisure"="stadium"]', 
                         '["leisure"="pitch"]', '["sport"]'],
        'p_ambient': ['["amenity"="community_centre"]', '["amenity"="social_centre"]', 
                      '["amenity"="marketplace"]', '["shop"="convenience"]', 
                      '["amenity"="library"]'],
        'p_accessib': ['["wheelchair"="yes"]', '["tactile_paving"="yes"]',
                       '["highway"="elevator"]','["ramp"="yes"]', '["handrail"="yes"]',
                       '["kerb"="lowered"]', '["kerb"="flush"]', '["automatic_door"="yes"]',
                       '["highway"="crossing"]["tactile_paving"="yes"]',
                       '["crossing"="traffic_signals"]["sound"="yes"]',
                       '["public_transport"="platform"]["wheelchair"="yes"]',
                       '["railway"="station"]["wheelchair"="yes"]',
                       '["amenity"="bus_station"]["wheelchair"="yes"]'],
        'p_transpublic': ['["public_transport"="station"]', '["public_transport"="stop_position"]',
                          '["highway"="footway"]', '["highway"="cycleway"]',
                          '["amenity"="bus_station"]', '["railway"="station"]',
                          '["railway"="subway_entrance"]', '["railway"="tram_stop"]',
                          '["amenity"="taxi"]', '["amenity"="bicycle_rental"]'],
        'p_seguretat': ['["amenity"="police"]', '["amenity"="fire_station"]',
                        '["emergency"]', '["amenity"="hospital"]', 
                        '["amenity"="clinic"]'],
        'p_preus': ['["landuse"="residential"]', '["building"="apartments"]', 
                    '["building"="residential"]'],
        'p_ocompra': ['["landuse"="residential"]', '["building"="house"]', 
                       '["building"="apartments"]'],
        'p_tipushabit': ['["building"="apartments"]', '["building"="residential"]', 
                         '["building"="terrace"]'],
        'p_nivelldevida': ['["shop"="department_store"]', '["shop"="boutique"]', 
                           '["amenity"="restaurant"]', '["tourism"="hotel"]', 
                           '["shop"="jewelry"]', '["amenity"="bank"]'],
        'p_infraestdigit': ['["amenity"="internet_cafe"]', '["internet_access"="yes"]', 
                            '["internet_access"="wlan"]', '["office"="telecommunication"]'],
        'p_privacitat': [
            '["access"="private"]',           # Private access areas
            '["barrier"="gate"]',             # Gates
            '["barrier"="fence"]',            # Fences
            '["entrance"="yes"]',             # Controlled entrances
            '["landuse"="residential"]["access"="private"]',  # Private residential areas,
            '["building"="detached"]',        # Detached houses (more privacy)
            '["landuse"="residential"]["access"="private"]',
            '["barrier"="wall"]'             # Walls around properties
        ]

    }
    return  d_priorities.get(prioritat)

def calcular_puntuacio_barris(llista_barris):
    """
    Calcula la puntuació total de cada barri a partir d'una llista 
    de diccionaris retornats per agrupar_barris.
    
    Args:
        llista_barris: Llista amb diccionaris on cada clau és el nom del barri
                      i cada valor és una llista d'elements
    
    Returns:
        Dict amb nom_barri: total_punts
    """
    total_per_barri = {}
    
    for dic_barri in llista_barris:
        # Saltar si és None (quan la prioritat < 3)
        if dic_barri is None:
            continue
            
        # Iterar sobre cada barri en el diccionari
        for nom_barri, llista_elements in dic_barri.items():
            # Si el barri ja existeix, sumar els punts
            if nom_barri in total_per_barri:
                total_per_barri[nom_barri] += len(llista_elements)
            else:
                total_per_barri[nom_barri] = len(llista_elements)
    
    return total_per_barri
