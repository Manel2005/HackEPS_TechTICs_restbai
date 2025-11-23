import csv

def exportar_a_csv(diccionari_dades, nom_fitxer="agrupacio_barris.csv"):
    """
    Exporta un diccionari (clau=barri, valor=recompte) a un fitxer CSV.
    """
    with open(nom_fitxer, mode='w', newline='', encoding='utf-8') as fitxer_csv:
        escriptor = csv.writer(fitxer_csv, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        
        escriptor.writerow(['Barri', 'Puntuació'])
        
        # 3. Escriure les dades de cada fila
        for barri, puntuacio in diccionari_dades.items():
            escriptor.writerow([barri, puntuacio])

            