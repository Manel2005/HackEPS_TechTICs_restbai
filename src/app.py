import pandas as pd
import streamlit as st
import folium
from streamlit_folium import st_folium
import branca.colormap as cm

from shapely.geometry import shape

import queries
import barris
import dic2csv


# -------------------------------------------------------------------
# Configuració bàsica de la pàgina
# -------------------------------------------------------------------
st.set_page_config(page_title="Recomanador de barris de Los Angeles", layout="wide")
st.title("Recomanador de barris de Los Angeles")


# -------------------------------------------------------------------
# BACKEND: obtenció i puntuació de barris amb els teus mòduls
# -------------------------------------------------------------------
def obtenir_puntuacions_barris(preferencies: dict) -> pd.DataFrame:
    """
    Utilitza:
      - barris.dades_barris()   -> polígon dels barris de LA
      - queries.do_query()      -> dades d'Overpass
      - barris.agrupar_barris() -> agrupació d'elements per barri
      - dic2csv.exportar_a_csv  -> exportació de resultats a CSV

    Retorna un DataFrame amb columnes: name, lat, lon, score
    on score ∈ [0, 1] és una puntuació normalitzada per barri.
    """

    # 1) Descarregar la geometria dels barris
    dades_barris = barris.dades_barris("https://services5.arcgis.com/7nsPwEMP38bSkCjy/arcgis/rest/services/LA_Times_Neighborhoods/FeatureServer/0/query?where=1%3D1&outFields=*&outSR=4326&f=json")
    if not dades_barris or "features" not in dades_barris:
        return pd.DataFrame(columns=["name", "lat", "lon", "score"])

    # 2) Construir llista de filtres Overpass segons preferències
    filtres = []

    # Oferta cultural / gastronòmica -> restaurants, bars, cafès, etc.
    if preferencies["oferta_cultural"] > 1:
        filtres.extend([
            '["amenity"="restaurant"]',
            '["amenity"="cafe"]',
            '["amenity"="bar"]',
            '["amenity"="fast_food"]',
            '["amenity"="library"]',
            '["tourism"="museum"]',
            '["tourism"="gallery"]',
            '["tourism"="information"]',
        ])

    # Proximitat a zones verdes -> parcs, jardins
    if preferencies["prox_zones_verdes"] > 1:
        filtres.extend([
            '["leisure"="park"]',
            '["leisure"="garden"]',
            '["leisure"="recreation_ground"]',
            '["leisure"="nature-reserve"]'
        ])

    # Proximitat a gimnassos i equipaments esportius
    if preferencies["prox_gimnas"] > 1:
        filtres.extend([
            '["amenity"="gym"]',
            '["leisure"="sports_centre"]',
            '["leisure"="pitch"]',
            '["leisure"="stadium"]',
        ])

    # Connexions amb transport públic
    if preferencies["transport_public"] > 1:
        filtres.extend([
            '["highway"="bus_stop"]',
            '["amenity"="bus_station"]',
            '["railway"="station"]',
            '["railway"="halt"]',
            '["public_transport"="stop_position"]',
            '["public_transport"="platform"]',
        ])

    if preferencies["seguretat"] > 1:
        filtres.extend([
            '["amenity"="police"]',
            '["amenity"="fire_station"]',
            '["emergency"]',
            '["amenity"="hospital"]',
            '["amenity"="clinic"]',
            ])

    if preferencies["educacio"] > 1:
        filtres.extend([
            '["amenity"="kindergarten"]',
            '["amenity"="school"]',
            '["amenity"="university"]',
            '["amenity"="college"]',
            '["amenity"="research_institute"]',
        ])

    # Si no hi ha cap filtre actiu, per defecte demanem restaurants (per tenir alguna cosa)
    if not filtres:
        filtres = ['["building"="supermarket"]']

    # Accessibilitat universal: si és imprescindible, fem servir la query amb wheelchair=yes
    access_flag = 1 if preferencies["accessibilitat"] else 0

    # 3) Crida a Overpass amb els filtres construïts
    llocs = queries.do_query(filtres, access=access_flag)

    # 4) Agrupar punts d'interès per barri
    grupats = barris.agrupar_barris(llocs, dades_barris)  # {barri: [elements]}

    if not grupats:
        return pd.DataFrame(columns=["name", "lat", "lon", "score"])

    # 5) Calcular centroid de cada barri per tenir lat/lon
    centroids = {}
    for feature in dades_barris["features"]:
        geom = feature.get("geometry", {})
        if "rings" not in geom:
            continue
        geo_adaptat = {
            "type": "Polygon",
            "coordinates": geom["rings"],
        }
        poly = shape(geo_adaptat)
        c = poly.centroid
        nom_barri = feature["attributes"]["name"]
        centroids[nom_barri] = (c.y, c.x)  # (lat, lon)

    # 6) Comptar per categoria a cada barri
    estadistiques = {}
    for nom_barri, elements in grupats.items():
        if nom_barri == "Desconegut":
            continue

        compt_cultura = 0
        compt_verda = 0
        compt_esport = 0
        compt_transport = 0
        compt_seguretat = 0
        compt_educacio = 0

        for e in elements:
            tags = e.get("tags", {})
            amenity = tags.get("amenity", "")
            leisure = tags.get("leisure", "")
            highway = tags.get("highway", "")
            railway = tags.get("railway", "")
            public_transport = tags.get("public_transport", "")
            tourism = tags.get("tourism", "")

            # Cultural / gastronòmic
            if (
                amenity in ("restaurant", "cafe", "bar", "fast_food", "food_court")
                or tourism in ("museum", "theatre", "cinema", "arts_centre")
            ):
                compt_cultura += 1

            # Zones verdes
            if leisure in ("park", "garden", "recreation_ground", "nature_reserve"):
                compt_verda += 1

            # Esport
            if (
                amenity in ("gym", "fitness_centre")
                or leisure in ("sports_centre", "pitch", "stadium", "track")
            ):
                compt_esport += 1

            # Transport públic
            if (
                highway in ("bus_stop",)
                or amenity in ("bus_station", "ferry_terminal")
                or railway in ("station", "halt", "stop")
                or public_transport in ("stop_position", "platform", "station")
            ):
                compt_transport += 1

            # Seguretat
            if (
                amenity in ("police", "fire_station", "hospital", "clinic")
            ):
                compt_transport += 1

            # Educacio
            if (
                    amenity in ("kindergarten", "school", "university", "college", "research_institute")
            ):
                compt_educacio += 1

        estadistiques[nom_barri] = {
            "cultura": compt_cultura,
            "verda": compt_verda,
            "esport": compt_esport,
            "transport": compt_transport,
            "seguretat": compt_seguretat,
            "educacio": compt_educacio,
        }

    if not estadistiques:
        return pd.DataFrame(columns=["name", "lat", "lon", "score"])

    # 7) Calcular màxims per normalitzar per categoria
    max_cultura = max(v["cultura"] for v in estadistiques.values()) or 0
    max_verda = max(v["verda"] for v in estadistiques.values()) or 0
    max_esport = max(v["esport"] for v in estadistiques.values()) or 0
    max_transport = max(v["transport"] for v in estadistiques.values()) or 0
    max_seguretat = max(v["seguretat"] for v in estadistiques.values()) or 0
    max_seguretat = max(v["educacio"] for v in estadistiques.values()) or 0

    # 8) Construir puntuació ponderada per barri
    puntuacions_brutes = {}
    for nom_barri, counts in estadistiques.items():
        # Normalitzacions per categoria
        norm_cultura = counts["cultura"] / max_cultura if max_cultura > 0 else 0.0
        norm_verda = counts["verda"] / max_verda if max_verda > 0 else 0.0
        norm_esport = counts["esport"] / max_esport if max_esport > 0 else 0.0
        norm_transport = counts["transport"] / max_transport if max_transport > 0 else 0.0
        norm_seguretat = counts["seguretat"] / max_seguretat if max_seguretat > 0 else 0.0
        norm_educacio = counts["educacio"] / max_seguretat if max_seguretat > 0 else 0.0


        # Pesos a partir del qüestionari (0–5 → 0–1)
        w_cultura = preferencies["oferta_cultural"] / 5.0
        w_verda = preferencies["prox_zones_verdes"] / 5.0
        w_esport = preferencies["prox_gimnas"] / 5.0
        w_comunitat = preferencies["comunitat"] / 5.0
        w_transport = preferencies["transport_public"] / 5.0
        w_seguretat = preferencies["seguretat"] / 5.0
        w_educacio = preferencies["educacio"] / 5.0
        # bloc_residencial no es implementat;
        # ara mateix no afecten la puntuació, però es recullen al qüestionari.

        puntuacio = 0.0

        # Components principals
        puntuacio += w_cultura * norm_cultura
        puntuacio += w_verda * norm_verda
        puntuacio += w_esport * norm_esport
        puntuacio += w_transport * norm_transport
        puntuacio += w_seguretat * norm_seguretat
        puntuacio += w_educacio * norm_educacio

        # Comunitat: afegim una part com a mitjana de cultura+zones verdes+esport
        if w_comunitat > 1:
            base_comunitat = (norm_cultura + norm_verda + norm_esport + norm_educacio) / 4.0
            puntuacio += w_comunitat * base_comunitat * 0.5  # factor suau

        puntuacions_brutes[nom_barri] = puntuacio

    # 9) Normalitzar puntuacions a [0,1] per facilitar la visualització
    max_puntuacio = max(puntuacions_brutes.values()) if puntuacions_brutes else 0.0

    files = []
    for nom_barri, puntuacio in puntuacions_brutes.items():
        lat, lon = centroids.get(nom_barri, (None, None))
        if lat is None or lon is None:
            continue
        score_norm = puntuacio / max_puntuacio if max_puntuacio > 0 else 0.0
        files.append(
            {
                "name": nom_barri,
                "lat": lat,
                "lon": lon,
                "score": score_norm,
            }
        )

    df = pd.DataFrame(files)

    # 10) Exportar a CSV amb el teu mòdul (puntuació bruta, no normalitzada)
    dic2csv.exportar_a_csv(
        puntuacions_brutes,
        nom_fitxer="puntuacions_barris_brutes.csv",
    )

    return df


# -------------------------------------------------------------------
# ESTAT GLOBAL (clients, dades carregades, etc.)
# -------------------------------------------------------------------
BASE_CLIENTS = [
    "Daenerys",
    "Cersei",
    "Bran",
    "Jon",
    "Arya",
    "Tyrion",
]

if "clients" not in st.session_state:
    st.session_state.clients = BASE_CLIENTS.copy()

if "scores_df" not in st.session_state:
    st.session_state.scores_df = None

if "client_scores" not in st.session_state:
    # nom_client -> DataFrame and punctuation d'aquell client
    st.session_state.client_scores = {}

if "selected_client" not in st.session_state:
    st.session_state.selected_client = st.session_state.clients[0]

if "client_params" not in st.session_state:
    # diccionari: nom_client -> dict de preferències
    st.session_state.client_params = {}


# -------------------------------------------------------------------
# QÜESTIONARI A LA BARRA LATERAL
# -------------------------------------------------------------------
st.sidebar.header("Qüestionari de preferències")

with st.sidebar.form("formulari_preferencies"):

    client_actual = st.session_state.selected_client
    params_guardats = st.session_state.client_params.get(client_actual, {})

    oferta_cultural = st.slider(
        "Importància de l'oferta cultural i gastronòmica",
        1, 5,
        params_guardats.get("oferta_cultural", 1),
    )
    prox_zones_verdes = st.slider(
        "Importància de la proximitat a zones verdes",
        1, 5,
        params_guardats.get("prox_zones_verdes", 1),
    )
    prox_gimnas = st.slider(
        "Importància de la proximitat a gimnasos i equipaments esportius",
        1, 5,
        params_guardats.get("prox_gimnas", 1),
    )
    comunitat = st.slider(
        "Importància del sentiment de comunitat al barri",
        1, 5,
        params_guardats.get("comunitat", 1),
    )
    accessibilitat = st.checkbox(
        "És imprescindible una bona accessibilitat (mobilitat reduïda)?",
        value=params_guardats.get("accessibilitat", False),
    )
    transport_public = st.slider(
        "Importància de les connexions amb transport públic",
        1, 5,
        params_guardats.get("transport_public", 1),
    )
    seguretat = st.slider(
        "Importància d'un bon nivell de seguretat al barri",
        1, 5,
        params_guardats.get("seguretat", 1),
    )
    educacio = st.slider(
        "Importància de l'accés a centres educatius i de recerca",
        1, 5,
        params_guardats.get("educacio", 1),
    )
    bloc_residencial = st.checkbox(
        "Prefereixo que la llar sigui en un bloc residencial",
        value=params_guardats.get("bloc_residencial", False),
    )

    enviat = st.form_submit_button("Obtenir barris recomanats")

    if enviat:
        client_actual = st.session_state.selected_client

        preferencies = {
            "oferta_cultural": oferta_cultural,
            "prox_zones_verdes": prox_zones_verdes,
            "prox_gimnas": prox_gimnas,
            "comunitat": comunitat,
            "accessibilitat": accessibilitat,
            "transport_public": transport_public,
            "seguretat": seguretat,
            "educacio": educacio,
            "bloc_residencial": bloc_residencial,
            "client": st.session_state.selected_client,
        }

        # Guarda preferencies del client
        st.session_state.client_params[client_actual] = preferencies

        try:
            df_resultats = obtenir_puntuacions_barris(preferencies)
        except Exception as e:
            # BARRERA DE SEGURETAT GLOBAL
            print(f"[APP] Error obtenint puntuacions: {e}")
            st.session_state.scores_df = pd.DataFrame()
            st.sidebar.error(
                "S'ha produït un error intern en obtenir les dades. "
                "Torna-ho a intentar més tard."
            )
        else:
            # Desa els resultats per aquest client
            if df_resultats is None or df_resultats.empty:
                # Aquest client NO té dades -> neteja resultats
                st.session_state.client_scores[client_actual] = pd.DataFrame()
                st.session_state.scores_df = pd.DataFrame()
                st.sidebar.warning("No s'han trobat resultats per als criteris seleccionats.")
            else:
                # Desa els resultats per aquest client
                st.session_state.client_scores[client_actual] = df_resultats
                st.session_state.scores_df = df_resultats
                st.sidebar.success("Puntuacions actualitzades amb dades d'Overpass.")


# -------------------------------------------------------------------
# SELECCIÓ DE CLIENT A LA ZONA PRINCIPAL
# -------------------------------------------------------------------
st.markdown("### Selecció de client")

col_client, col_nou_nom, col_boto = st.columns([2, 2, 1])

with col_nou_nom:
    st.markdown("**Nou client**")
    nou_client = st.text_input(
        "Nou client",
        key="nou_client_main",
        label_visibility="collapsed",
        placeholder="Nom del nou client",
    )

with col_boto:
    st.markdown("&nbsp;")  # espaiador vertical
    if st.button("Afegeix", key="afegir_client_main"):
        if not nou_client:
            st.error("El nom del client no pot estar buit.")
        elif nou_client in st.session_state.clients:
            st.warning("Aquest client ja existeix.")
        else:
            # 1) Afegim el client a la llista
            st.session_state.clients.append(nou_client)
            # 2) El marquem com a seleccionat
            st.session_state.selected_client_widget = nou_client
            # 3) Missatge
            st.success(f"S'ha afegit el client '{nou_client}'.")
            # 4) Forcem un rerun perquè el selectbox es torni a dibuixar amb la nova llista
            st.rerun()

with col_client:
    st.markdown("**Client**")
    client = st.selectbox(
        "Client",
        st.session_state.clients,
        label_visibility="collapsed",
        key="selected_client_widget", # Streamlit controla directament aquest estat
    )
    # Sincronitza clau d'app
    st.session_state.selected_client = client

# -------------------------------------------------------------------
# DADES PER AL MAPA I RÀNQUING
# -------------------------------------------------------------------
client_actual = st.session_state.selected_client

# Carreguem les dades associades a aquest client (si n'hi ha)
df = st.session_state.client_scores.get(client, None)
st.session_state.scores_df = df # mantenim sincronitzat l'estat global

# Si aquest client no té dades, NO MOSTREM EL MAPA NI EL RÀNQUING
if df is None or df.empty:
    st.info(
        f"El client <<{client}>> encara no té cap recomanació. "
        "Omple el formulari de l'esquerra i prem <<Obtenir barris recomanats>>."
    )
    st.stop()

score_col = "score"
for col in [score_col, "lat", "lon"]:
    if col not in df.columns:
        st.error(f"No s'ha trobat la columna requerida '{col}' a les dades.")
        st.stop()

df = df.dropna(subset=[score_col, "lat", "lon"])
df = df.sort_values(score_col, ascending=False)
scores = df[score_col].astype(float)

min_score = float(scores.min())
max_score = float(scores.max())

if min_score == max_score:
    colormap = cm.linear.YlOrRd_09.scale(min_score - 1, max_score + 1)
else:
    colormap = cm.linear.YlOrRd_09.scale(min_score, max_score)

colormap.caption = f"Puntuació per al client {client}"

st.markdown(f"### Barris recomanats per al client **{client}**")


# -------------------------------------------------------------------
# MAPA + LLEGENDA
# -------------------------------------------------------------------
m = folium.Map(
    location=[34.05, -118.25],  # centre de LA
    zoom_start=11,
    min_zoom=10,
    max_zoom=14,
)

for _, row in df.iterrows():
    score = float(row[score_col])
    color = colormap(score)

    # Radi en píxels, limitat per no descontrolar-se
    base_radius = 5 + score * 10  # score ∈ [0,1]
    radius = max(4, min(base_radius, 15))

    popup_html = f"""
    <b>{row['name']}</b><br>
    Puntuació: {score:.2f}
    """

    folium.CircleMarker(
        location=[row["lat"], row["lon"]],
        radius=radius,
        popup=popup_html,
        color=color,
        fill=True,
        fill_color=color,
        fill_opacity=0.7,
    ).add_to(m)

col_mapa, col_llegenda = st.columns([3, 1])

with col_mapa:
    st_folium(m, width=900, height=600)

with col_llegenda:
    st.subheader("Llegenda de puntuació")
    st.markdown(
        f"""
        <p>El color representa la puntuació del barri per al client
        <b>{client}</b> segons les preferències definides al qüestionari.</p>
        <p><b>Min:</b> {min_score:.2f}<br>
        <b>Max:</b> {max_score:.2f}</p>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<p><b>Escala de colors</b></p>", unsafe_allow_html=True)

    passos = 5
    if max_score == min_score:
        valors = [min_score]
    else:
        valors = [
            min_score + i * (max_score - min_score) / (passos - 1)
            for i in range(passos)
        ]

    for v in valors:
        color = colormap(v)
        st.markdown(
            f"""
            <div style="display:flex; align-items:center; margin-bottom:4px;">
                <div style="
                    width:20px;
                    height:20px;
                    background:{color};
                    margin-right:8px;
                    border:1px solid #333;
                "></div>
                <span>{v:.2f}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )


# -------------------------------------------------------------------
# RÀNQUING I DESCÀRREGA DE CSV
# -------------------------------------------------------------------
st.subheader("Rànquing de barris")

ranking_df = (
    df[["name", score_col]]
    .head(20)
    .reset_index(drop=True)
)

ranking_df.columns = ["Barri", "Puntuació"]
st.dataframe(ranking_df, hide_index=True)

csv_bytes = df.to_csv(index=False).encode("utf-8")
st.download_button(
    label="Descarrega el CSV de puntuacions",
    data=csv_bytes,
    file_name="puntuacions_barris_normalitzades.csv",
    mime="text/csv",
)