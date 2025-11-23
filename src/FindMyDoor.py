# Developed by Xèn Mata  on 22/11/2025
# Reviewed by  on /11/2025

from users import *

def main():
    Sessio = True
    while Sessio == True:
        nom_u = getName()
        digital_id = nom_u.replace(" ", "_")
        u_self = Usuari(digital_id)
        prioritats_gen = priorities(u_self)
        topPrioritats = caractsUsuari(prioritats_gen)
        whichQueries(topPrioritats)

if __name__ == "__main__":
   main()
    
