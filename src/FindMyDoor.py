# Developed by Xèn Mata  on 22/11/2025
# Reviewed by  on /11/2025

from users import *

def main():
    Sessio = True
    while Sessio == True:
        nom_u = getName()
        digital_id = nom_u.replace(" ", "_")
        u_self = Usuari(digital_id)
        
        # Obtenir llista de barris amb prioritats
        llista_barris = priorities(u_self)
        
        # Calcular puntuació total per barri
        puntuacions = calcular_puntuacio_barris(llista_barris)

        if "Desconegut" in puntuacions:
            del puntuacions["Desconegut"]
        
        # Mostrar resultats
        print("\n" + "="*60)
        print("BARRIS RECOMANATS (ordenats per puntuació)")
        print("="*60 + "\n")
        
        for barri, punts in sorted(puntuacions.items(), key=lambda x: x[1], reverse=True):
            print(f"{barri}: {punts} punts")
        
        # Mostrar el millor barri
        if puntuacions:
            millor_barri = max(puntuacions.items(), key=lambda x: x[1])
            print(f"\n Barri més recomanat: {millor_barri[0]} ({millor_barri[1]} punts)\n")
        
        # Preguntar si vol continuar
        continuar = input("Vols fer una nova cerca? (s/n): ")
        if continuar.lower() != 's':
            Sessio = False
            print("Gràcies per utilitzar FindMyDoor!")

if __name__ == "__main__":
    main()
