
#### Tipus de barris definits:

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
        

# Mètode per obtenir el nom al que referir-nos a l'usuari
def getName():
    Username = input("Hola! Com ens podríem referir a tu d'ara en endavant?: \n >>> ")
    print("Gràcies, ", Username,"! Ens plau donar-te la benvinguda a FindMyDoor, som al teu servei per ajudar-te a trobar la teva propera llar.")
    return Username


def priorities(self): # retorna llista amb llistes de barris amb el nombre de serveis coincidents
    print("Si us plau, indiqui en una escala de l'1, significant gens, al 5, significant molt, quina és la importància que li atribueix a les següents carecterístiques associades a zones residencials:")
    p_gastrocult = int(input("Tenir una àmplia oferta cultural i gastronòmica = "))
    if p_gastrocult >= 3:
        looking4 = whichQueries('p_gastrocult')
        coincidencies = do_query(looking4) # lat i long de les coincidencies trobades
        barris_gastrocult = agrupar_barris(coincidencies)
        set_CultGastron(self,p_gastrocult)
    p_verd = int(input("Proximitat a zones verdes = "))
    if p_verd >= 3:
        looking4 = whichQueries('p_verd')
        coincidencies = do_query(looking4) 
        barris_verd = agrupar_barris(coincidencies)
        set_EVerdsNatura(self,p_verd)
    p_activitatf = int(input("Proximitat a gimnassos i complexos esportius = "))
    if p_activitatf >= 3:
        looking4 = whichQueries('p_activitatf')
        coincidencies = do_query(looking4)
        barris_activitatf = agrupar_barris(coincidencies)
        set_CLocalComunitat(self, (self.CLocalComunitat += 1))
    p_ambient = int(input("Tenir un fort sentiment de comunitat o una comunitat de veïns propera = "))
    if p_ambient >= 3:
        looking4 = whichQueries('p_ambient')
        coincidencies = do_query(looking4)
        barris_ambient = agrupar_barris(coincidencies)
        set_AmbientDens(self, p_ambient))        
    else:
        looking4 = whichQueries('p_privacitat')
        coincidencies = do_query(looking4)
        barris_privacitat = agrupar_barris(coincidencies)
        set_SeguretatPriv(self, 6 - p_ambient)
        p_accessib = int(input("Acessibilitat Universal i fàcilitat per a persones amb mobilitat reduïda = "))
    if p_accessib >= 3:
        p_transpublic = int(input("Connexions amb mitjans de transport públic = "))
        
    if p_transpublic >= 3:
    p_seguretat = int(input("Índex de seguretat ciutadana a la zona = "))
    if p_seguretat >= 3:
    p_preus = int(input("Preus de l'habitatge per sota de la mitjana general = "))
    if p_preus >= 3:
    p_opcompra = int(input("Opció de compra de l'habitatge = "))
    if p_ocompra >= 3:
    p_tipushabit = int(input("Que la meva llar es trobi en un bloc residencial = "))
    if p_tipushabit >= 3:
    p_nivelldevida = int(input("Que el poder adquisitiu mitjà del barri sigui alt = "))
    if p_nivelldevida >= 3:
    p_infraestdigit = int(input("Tenir una bona connexió a internet i cobertura de fibra òptica = "))
    if p_infraestdigit >= 3:
        
    
    return (barris_gastrocult, barris_verd, _activitatf, p_ambient, p_accessib, 
            p_transpublic, p_seguretat, p_preus, p_opcompra, p_tipushabit, 
            p_nivelldevida, p_infraestdigit)


def caractsUsuari(prioritats_gen):
    topPrioritats = {k: v for k, v in prioritats_gen.items() if v >= 3}
    topPrioritats = topPrioritats.keys()
    print(topPrioritats)
    return topPrioritats

    
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
        'p_accessib': ['["highway"="footway"]', '["highway"="cycleway"]', 
                       '["wheelchair"="yes"]', '["tactile_paving"="yes"]'],
        'p_transpublic': ['["public_transport"="station"]', '["public_transport"="stop_position"]',
                          '["amenity"="bus_station"]', '["railway"="station"]', 
                          '["railway"="subway_entrance"]', '["railway"="tram_stop"]',
                          '["amenity"="taxi"]', '["amenity"="bicycle_rental"]'],
        'p_seguretat': ['["amenity"="police"]', '["amenity"="fire_station"]',
                        '["emergency"]', '["amenity"="hospital"]', 
                        '["amenity"="clinic"]'],
        'p_preus': ['["landuse"="residential"]', '["building"="apartments"]', 
                    '["building"="residential"]'],
        'p_opcompra': ['["landuse"="residential"]', '["building"="house"]', 
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
    d_priorities.get(prioritat)
    print(q_todo)
