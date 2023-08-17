import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
from folium.raster_layers import ImageOverlay
import json
from folium import plugins
from folium.plugins import Fullscreen

import requests
import base64

# URL du GeoJSON
geojson_url = 'https://raw.githubusercontent.com/olivierparrot01/ICPE/main/line_json_wgs84.geojson'

# Charger le contenu du GeoJSON depuis l'URL
lines_geojson_data = requests.get(geojson_url).json()


# Convertir la colonne "Distance" en nombre entier
for feature in lines_geojson_data['features']:
    if 'properties' in feature and 'Distance' in feature['properties']:
        feature['properties']['Distance'] = int(feature['properties']['Distance'])



# Créer une couche GeoJSON pour les lignes
lines_geojson_layer = folium.GeoJson(
    lines_geojson_data,
    name="Lignes entre points",
    style_function=lambda feature: {
        'color': 'black',  # Utilisez la couleur de votre choix
        'opacity': 1,
        'weight': 2  # Épaisseur constante
    },
    tooltip=folium.GeoJsonTooltip(
        fields=[ "Distance"],
        aliases=[ "Distance"],
        style="font-size: 12px; text-align: center;",
        sticky=True,  # Rend l'étiquette collante (reste affichée lors du survol)
        delay=0  # Aucun délai d'affichage
    )
)



# Chargement des données

df = pd.read_csv('https://raw.githubusercontent.com/olivierparrot01/ICPE/main/0208_gun.csv')
dg = pd.read_csv('https://raw.githubusercontent.com/olivierparrot01/ICPE/main/2geocodage.csv')
# Conversion des données
dg = dg[dg['Distance'] >= 0]
dg['Distance'] = dg['Distance'].astype(int)
dg['Code_AIOT'] = dg['Code_AIOT'].astype(str)
df['Code_AIOT'] = df['Code_AIOT'].astype(str)
df['Nom_usuel'] = df['Nom_usuel'].astype(str)
df["Code_AIOT_liste"] = df.groupby(["latitude", "longitude"])["Code_AIOT"].transform(lambda x: ", ".join(x))
df['Adresse_concat'] = df['Adresse 1'].str.cat([df['Adresse 2'], df['Adresse 3']], sep=' ', na_rep='')
dg["Code_AIOT_liste"] = dg.groupby(["latitude", "longitude"])["Code_AIOT"].transform(lambda x: ", ".join(x))


df= df.drop("Courriel d'échange avec l'administration", axis=1)
df= df.drop("Région", axis=1)


not_in_dg = df[~df['Code_AIOT'].isin(dg['Code_AIOT'])]
not_in_dg = not_in_dg.drop("Unnamed: 0", axis=1)
df = df.drop("Unnamed: 0", axis=1)




# Fonction pour ajouter des marqueurs à la carte
def add_markers(data, color):
    for _, row in data.iterrows():
        popup_content = f"Nom usuel : {row['Nom_usuel']}<br>Code AIOT : {row['Code_AIOT_liste']}"
        tooltip_content = f"Nom usuel : {row['Nom_usuel']}<br>Code AIOT : {row['Code_AIOT_liste']}"
        
        folium.CircleMarker(
            location=[row['latitude'], row['longitude']],
            radius=5,
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=1,
            popup=popup_content,
            tooltip=tooltip_content,
        ).add_to(m)

# Fonction pour ajouter des marqueurs à la carte avec effet de clignotement
def add_blinking_markers(data):
    marker_cluster = plugins.MarkerCluster()
    for _, row in data.iterrows():
        tooltip_content = f"Nom usuel : {row['Nom_usuel']}<br>Code AIOT : {row['Code_AIOT_liste']}"
        
        marker = folium.Marker(
            location=[row['latitude'], row['longitude']],
            tooltip=tooltip_content,
            icon=None  # No default icon, to use custom CSS animation
        )
        marker_cluster.add_child(marker)

    m.add_child(marker_cluster)


st.markdown("<h2 style='font-size:28px;'>Appareillement Gun (bleu)-Geocodage (rouge) </h2>", unsafe_allow_html=True)




#st.write("Afficher/Masquer")
#st.dataframe(df)

# Sidebar pour les options et l'affichage des données
st.sidebar.title("Options")

# Afficher le titre dans le sidebar
st.sidebar.markdown("<h2 style='font-size:18px;'>Afficher la table Gun</h2>", unsafe_allow_html=True)

# Afficher la table dans le sidebar
with st.sidebar.expander("Afficher/Masquer"):
    # Afficher la table à l'intérieur de la section expansible dans le sidebar
    st.dataframe(df)






# Calcul des coordonnées du centre de la carte
center_lat = (df['latitude'].mean() + dg['latitude'].mean()) / 2
center_lon = (df['longitude'].mean() + dg['longitude'].mean()) / 2

# Création de la carte avec Folium
m = folium.Map(location=[center_lat, center_lon], zoom_start=8, control_scale=True)

# Ajouter les marqueurs pour df (en bleu) et dg (en rouge)
add_markers(df, 'blue')
add_markers(dg, 'red')

# Ajouter les marqueurs clignotants pour df
add_blinking_markers(df)

# Ajouter la couche GeoJSON des lignes à la carte
lines_geojson_layer.add_to(m)


# Filtrer les données en fonction des codes AIOT sélectionnés
st.sidebar.markdown("<h2 style='font-size:18px;'>Sélectionner par le Code AIOT les points Gun à mettre en évidence (sélection multiple)</h2>", unsafe_allow_html=True)
# Triez les codes AIOT dans l'ordre décroissant
sorted_codes = sorted(df['Code_AIOT'].unique(), reverse=True)

selected_codes = st.sidebar.multiselect("", sorted_codes)

filtered_data = df[df['Code_AIOT'].isin(selected_codes)]


# Ajouter les marqueurs verts pour les points sélectionnés
for index, row in df.iterrows():
    if row['Code_AIOT'] in selected_codes:
        folium.CircleMarker(
            location=[row['latitude'], row['longitude']],
            radius=8,
            color='green',
            fill=True,
            fill_color='green',
            fill_opacity=0.7,
            popup=f"Nom usuel : {row['Nom_usuel']}<br>Code AIOT : {row['Code_AIOT_liste']}",
            tooltip=f"Nom usuel : {row['Nom_usuel']}<br>Code AIOT : {row['Code_AIOT_liste']}"
        ).add_to(m)

# Zoomer sur les points sélectionnés
if selected_codes:
    selected_data = df[df['Code_AIOT'].isin(selected_codes)]
    if not selected_data.empty:
        bounds = [
            (selected_data['latitude'].min(), selected_data['longitude'].min()),
            (selected_data['latitude'].max(), selected_data['longitude'].max())
        ]
        m.fit_bounds(bounds)


# URL de l'orthophoto IGN à utiliser comme couche de tuile
orthophoto_url = "https://wxs.ign.fr/choisirgeoportail/geoportail/wmts?" \
                 "SERVICE=WMTS&REQUEST=GetTile&VERSION=1.0.0&LAYER=ORTHOIMAGERY.ORTHOPHOTOS&TILEMATRIXSET=PM&" \
                 "FORMAT=image/jpeg&TILECOL={x}&TILEROW={y}&TILEMATRIX={z}&" \
                 "STYLE=normal"

# Ajout de la couche de tuile de l'orthophoto IGN uniquement aux niveaux de zoom 13 
for zoom_level in range(13, 19):
    folium.TileLayer(
        tiles=orthophoto_url,
        attr="IGN France",
        name=f"Orthophoto IGN (Zoom {zoom_level})",
        overlay=True,
        min_zoom=zoom_level,
        max_zoom=zoom_level,
    ).add_to(m)

# Add a LatLngPopup to the map
popup = folium.LatLngPopup()
m.add_child(popup)

# Ajouter le bouton de plein écran à la carte
fullscreen = Fullscreen(position="topleft", title="Plein écran", title_cancel="Quitter le plein écran")
fullscreen.add_to(m)
captured_coordinates_list = []

# Afficher la carte dans Streamlit en utilisant folium_static
folium_static(m)




# Récupérer les coordonnées du popup si elles sont disponibles

try:
    captured_coords = popup.html.split(",")
    latitude = float(captured_coords[0].split(":")[1])
    longitude = float(captured_coords[1].split(":")[1])
    st.write("Coordonnées capturées :")
    st.write("Latitude :", latitude)
    st.write("Longitude :", longitude)
    
    # Ajouter les coordonnées capturées à la liste
    captured_coordinates_list.append((latitude, longitude))
    
except AttributeError:
    st.write("")
    
# Afficher les coordonnées capturées
st.write("Coordonnées capturées :", captured_coordinates_list)



# Afficher le titre dans le sidebar
st.sidebar.markdown("<h2 style='font-size:18px;'>Adresses, coordonnées Gun et liens Google Maps des points sélectionnés :</h2>", unsafe_allow_html=True)

# Afficher le contenu dans le sidebar
for _, row in filtered_data.iterrows():
    st.sidebar.write(f"- Adresse Gun : {row['Adresse_concat']}, Coordonnées Gun : {row['longitude']}, {row['latitude']}")
    formatted_address = row['Adresse_concat'].replace(' ', '-')
    google_maps_link = f"[Ouvrir dans Google Maps à partir de l'adresse Gun](https://www.google.com/maps/search/?api=1&query={formatted_address})"
    st.sidebar.markdown(google_maps_link, unsafe_allow_html=True)
    google_maps_link = f"[Ouvrir dans Google Maps à partir des coordonnées Gun](https://www.google.com/maps?q={row['latitude']},{row['longitude']})"
    st.sidebar.markdown(google_maps_link, unsafe_allow_html=True)






#st.write("Table Gun correspondant à la sélection :")
#st.dataframe(filtered_data)
