# HackEPS_TechTICs_restbai

# Recomanador de Barris de Los Angeles (LA)

## Objectiu del Projecte
L'aplicació Streamlit ofereix recomanacions de barris de Los Angeles. La puntuació es basa en l'anàlisi de la densitat de Punts d'Interès (POI) d'OpenStreetMap, ponderada segons les preferències d'un usuari.

---

## 1. Instal·lació i Configuració

### 1.1. Requisits 
* Python 3.8+
* Accés a la xarxa per obtenir dades d'Overpass API i ArcGIS Feature Services.

### 1.2. Instal·lació de Dependències
Navega al directori del projecte i instal·la les llibreries principals:

```bash
pip install streamlit pandas folium streamlit-folium branca shapely requests

## 2. Execució de l'Aplicació (Instrucció Clau)

Per iniciar el servidor local de Streamlit i obrir l'aplicació al teu navegador, utilitza la següent comanda des del directori principal:

```bash
streamlit run app.py