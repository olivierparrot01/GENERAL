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
import numpy as np

#st.session_state.click_data = None

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
dg["Code_AIOT_liste"] = dg.groupby(["latitude", "longitude"])["Code_AIOT"].transform(lambda x: ", ".join(x))

df['Code_AIOT'] = df['Code_AIOT'].astype(str)
df['Nom_usuel'] = df['Nom_usuel'].astype(str)
df["Code_AIOT_liste"] = df.groupby(["latitude", "longitude"])["Code_AIOT"].transform(lambda x: ", ".join(x))
df['Adresse_concat'] = df['Adresse 1'].str.cat([df['Adresse 2'], df['Adresse 3']], sep=' ', na_rep='')

# Merge df and dg on 'Code_AIOT'
df = df.merge(dg[['Code_AIOT', 'Distance']], on='Code_AIOT', how='left')
#df = df[df['Distance'] >= 0]
#df['Distance'] = df['Distance'].astype(int)



df= df.drop("Courriel d'échange avec l'administration", axis=1)
df= df.drop("Région", axis=1)
df = df.drop("Unnamed: 0", axis=1)




not_in_dg = df[~df['Code_AIOT'].isin(dg['Code_AIOT'])]
#not_in_dg = not_in_dg.drop("Unnamed: 0", axis=1)

# Créer une liste pour enregistrer les coordonnées capturées
#captured_coordinates_list = []


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


import math

# Fonction pour calculer la distance entre deux points en coordonnées géographiques (lat, lon)
def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371000  # Rayon de la Terre en mètres
    phi_1 = math.radians(lat1)
    phi_2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi / 2.0) ** 2 + math.cos(phi_1) * math.cos(phi_2) * math.sin(delta_lambda / 2.0) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = R * c
    return distance

# Créer une liste pour stocker les groupes de points regroupés par distance
grouped_points = []

# Parcourir les points dans filtered_data pour les regrouper
for _, row1 in df.iterrows():
    is_added = False
    for group in grouped_points:
        row2 = group[0]
        distance = haversine_distance(row1['latitude'], row1['longitude'], row2['latitude'], row2['longitude'])
        if distance <= 20000:  # Modifier la distance de regroupement selon vos besoins
            group.append(row1)
            is_added = True
            break
    if not is_added:
        grouped_points.append([row1])

# Créer une liste pour stocker les codes AIOT correspondant à chaque groupe de points
grouped_codes = []

# Parcourir les groupes de points dans grouped_points
for group in grouped_points:
    group_codes = [row['Code_AIOT'] for row in group]  # Extraire les codes AIOT du groupe
    grouped_codes.append(group_codes)  # Ajouter la liste de codes AIOT au groupe correspondant


#grouped_codes
# Créer une colonne 'Secteur' dans le DataFrame df
df['Secteur'] = None
#df['Secteur'] = df['Secteur'].astype(int)
# Parcourir les points dans df et assigner le secteur en fonction des groupes
for group_idx, group in enumerate(grouped_points):
    group_codes = [row['Code_AIOT'] for row in group]  # Extraire les codes AIOT du groupe
    df.loc[df['Code_AIOT'].isin(group_codes), 'Secteur'] = f'{group_idx + 1}'


# Afficher le contenu dans l'expander
with st.sidebar.expander("Informations"):
    st.sidebar.info('''Les temps de réponse sont un peu longs, il faut patienter...
                    À grande échelle, les orthophotos s'affichent.
                    Un clic gauche permet d'afficher les coordonnées géographiques.
                    La virgule dans les grandes valeurs de distance est le séparateur de millier et non la virgule décimale.''')


# Afficher le titre dans le sidebar
st.sidebar.markdown("<h2 style='font-size:18px;'>Afficher la table Gun</h2>", unsafe_allow_html=True)

# Afficher la table dans le sidebar
with st.sidebar.expander("Afficher/Masquer"):
    # Afficher la table à l'intérieur de la section expansible dans le sidebar
    #df['Code_AIOT'] = df['Code_AIOT'].astype(int)
    df['Secteur'] = df['Secteur'].astype(int)
    st.dataframe(df)


st.sidebar.markdown("<h2 style='font-size:18px;'>Filtrer les données Gun par Statut Seveso, Statut IED ou Distance (distance ente les pts homologues Gun-Geocodage)</h2>", unsafe_allow_html=True)
st.sidebar.markdown("")
selected_criteria = st.sidebar.multiselect("", ["Statut Seveso", "Statut IED", "Distance"])                                                                                                           
st.sidebar.markdown("")





# Apply the selected criteria to filter the DataFrame
filtered_df = df.copy()
for criterion in selected_criteria:
    if criterion == 'Statut Seveso':
        unique_values = filtered_df['Statut Seveso'].unique()
        selected_value = st.sidebar.selectbox("Statut Seveso", options=unique_values)
        filtered_df = filtered_df[filtered_df['Statut Seveso'] == selected_value]
    if criterion == 'Statut IED':
        unique_values = filtered_df['Statut IED'].unique()
        selected_value = st.sidebar.selectbox("Statut IED", options=unique_values)
        filtered_df = filtered_df[filtered_df['Statut IED'] == selected_value]

    elif criterion == 'Distance':
        df = df[df['Distance'].notna()]
        #df = df[df['Distance'] >= 0]
        #df['Distance'] = df['Distance'].astype(float)
        
        # Calculate the step value for the slider based on the range of distances
        min_distance = df['Distance'].min()
        max_distance = df['Distance'].max()

        selected_distance = st.sidebar.slider("La distance est supérieure ou égale à :", min_value=min_distance, max_value=10000, step=50)

        if st.sidebar.button("Filtrer entre 10000 et max"):
            filtered_df = filtered_df[(filtered_df['Distance'] >= 10000) & (filtered_df['Distance'] <= max_distance)]
        else:
            filtered_df = filtered_df[filtered_df['Distance'] >= selected_distance]

        # Check if the "Filtrer pts Gun non geocodes 'Distance is None'" checkbox is selected
       
        
        
        # Add a button to filter distance none
        if st.sidebar.button("Filtrer pts Gun non geocodes"):
            
            filtered_df = filtered_df[filtered_df['Distance'].isna()]
        else:
            filtered_df = filtered_df[filtered_df['Distance'] >= selected_distance]







# Use an expander to display the filtered DataFrame in the sidebar
with st.sidebar.expander(f"Afficher les {len(filtered_df)} données filtrées"):
    sorted_filtered_df = filtered_df.sort_values(by='Distance', na_position='first')
    
    
    # Afficher les données filtrées dans le sidebar
    
    st.write(sorted_filtered_df)

# Calculer le nombre de valeurs "None" dans la colonne "Distance"
count_none = filtered_df['Distance'].isna().sum()

# Afficher le nombre de valeurs "None" dans le sidebar
st.sidebar.info(f'''Nombre de pts Gun non géocodés parmi les données filtrées (valeurs 'None') dans "Distance" : {count_none}''')




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
#st.sidebar.markdown("<h2 style='font-size:18px;'>Sélectionner parmi les {len(filtered_df)} données filtrées, les points Gun à mettre en évidence (sélection multiple possible)</h2>", unsafe_allow_html=True)
# Triez les codes AIOT dans l'ordre décroissant
sorted_codes = sorted( filtered_df['Code_AIOT'].unique(), reverse=False)
sorted_cat = sorted( filtered_df['Secteur'].unique(), reverse=True)
sorted_cat = [int(category) for category in sorted_cat]

st.sidebar.markdown(f"<h2 style='font-size:18px;'>Sélectionner parmi les {len(filtered_df)} données filtrées, les points Gun à mettre en évidence sur la carte (pts blancs)</h2>", unsafe_allow_html=True)
st.sidebar.markdown("")
selected_codes = st.sidebar.multiselect("", sorted_codes)

filtered_data = df[df['Code_AIOT'].isin(selected_codes)]



st.sidebar.markdown(f"<h2 style='font-size:18px;'>Sélectionner parmi les {len(filtered_df)} données filtrées, les points Gun à mettre en évidence sur la carte (pts blancs) par Secteur</h2>", unsafe_allow_html=True)
st.sidebar.markdown("")
#selected_cat = st.sidebar.multiselect("", sorted_cat)

#filtered_data = df[df['Categorie'].isin(selected_cat)]



selected_cat = st.sidebar.multiselect("Sélectionner un Secteur", sorted_cat)
selected_codes1 = df[df['Secteur'].isin(selected_cat)]['Code_AIOT'].tolist()
# Dans la section où vous filtrez les données
# ...

# Combinez les listes selected_codes et selected_codes1 en une seule liste
selected_codes_combined = selected_codes + selected_codes1
#selected_codes_combined = selected_codes_combined.unique()
# Mise à jour de la variable de session

#st.session_state.selected_codes_combined = selected_codes_combined


# Ajouter les marqueurs blanc pour les points sélectionnés
for index, row in df.iterrows():
    if row['Code_AIOT'] in selected_codes_combined:
        folium.CircleMarker(
            location=[row['latitude'], row['longitude']],
            radius=8,
            color='white',
            fill=True,
            fill_color='white',
            fill_opacity=1,
            popup=f"Nom usuel : {row['Nom_usuel']}<br>Code AIOT : {row['Code_AIOT_liste']}",
            tooltip=f"Nom usuel : {row['Nom_usuel']}<br>Code AIOT : {row['Code_AIOT_liste']}"
        ).add_to(m)

# Zoomer sur les points sélectionnés
if selected_codes_combined:
    selected_data = df[df['Code_AIOT'].isin(selected_codes_combined)]
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


# Récupérer le contenu du popup de coordonnées
#popup_content = popup.html
    
# Ajouter les coordonnées capturées et le contenu du popup à la liste
    #captured_coordinates_list.append(popup_content)



# Ajouter le bouton de plein écran à la carte
fullscreen = Fullscreen(position="topleft", title="Plein écran", title_cancel="Quitter le plein écran")
fullscreen.add_to(m)



# Afficher la carte dans Streamlit en utilisant folium_static
folium_static(m)




# Récupérer les coordonnées du popup si elles sont disponibles

try:
    captured_coords = popup.html.split(",")
    latitude = float(captured_coords[0].split(":")[1])
    longitude = float(captured_coords[1].split(":")[1])
    # Récupérer le contenu du popup
    popup_content = popup.get_name()


    st.write(popup_content)


except AttributeError:
    st.write("")








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
