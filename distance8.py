import streamlit as st
import pandas as pd
import numpy as np
import base64
import plotly.express as px
import folium
from streamlit_folium import folium_static
import json
from folium import plugins




# Load data from CSV
dg = pd.read_csv('https://raw.githubusercontent.com/olivierparrot01/ICPE/main/2geocodage.csv')
df = pd.read_csv('https://raw.githubusercontent.com/olivierparrot01/ICPE/main/0208_gun.csv')
# Filter out negative and non-finite values from the 'Distance' column
dg = dg[dg['Distance'] >= 0]
dg = dg[np.isfinite(dg['Distance'])]

# Convert 'Distance' column to integers
dg['Distance'] = dg['Distance'].astype(int)

dg['Code_AIOT']=dg['Code_AIOT'].astype(str)
df['Code_AIOT']=df['Code_AIOT'].astype(str)
dg['Nom_usuel'] = dg['Nom_usuel'].astype(str)
df['Nom_usuel'] = df['Nom_usuel'].astype(str)
df['Adresse_concat'] = df['Adresse 1'].str.cat([df['Adresse 2'], df['Adresse 3']], sep=' ', na_rep='')

df["Code_AIOT_liste"] = df.groupby(["latitude", "longitude"])["Code_AIOT"].transform(lambda x: ", ".join(x))
dg["Code_AIOT_liste"] = dg.groupby(["latitude", "longitude"])["Code_AIOT"].transform(lambda x: ", ".join(x))
df["Nom_usuel_liste"] = df.groupby(["latitude", "longitude"])["Nom_usuel"].transform(lambda x: ", ".join(x))
dg["Nom_usuel_liste"] = dg.groupby(["latitude", "longitude"])["Nom_usuel"].transform(lambda x: ", ".join(x))



not_in_dg = df[~df['Code_AIOT'].isin(dg['Code_AIOT'])]
not_in_dg = not_in_dg.drop("Unnamed: 0", axis=1)


# ... (autres traitements sur les données)

# Calcul des coordonnées du centre de la carte
center_lat = (df['latitude'].mean() + dg['latitude'].mean()) / 2
center_lon = (df['longitude'].mean() + dg['longitude'].mean()) / 2

# Création de la carte avec Folium
m = folium.Map(location=[center_lat, center_lon], zoom_start=8, control_scale=True)
 
#Fonction pour ajouter des marqueurs à la carte
def add_markers(data, color):
    for index, row in data.iterrows():
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
            #icon=folium.Icon(icon='circle', color=color)
        ).add_to(m)

# Ajouter les marqueurs pour df (en bleu) et dg (en rouge)
add_markers(df, 'blue')
add_markers(dg, 'red')

# Fonction pour ajouter des marqueurs à la carte avec effet de clignotement
def add_blinking_markers(data):
    marker_cluster = plugins.MarkerCluster()
    for index, row in data.iterrows():
        popup_content = f"Nom usuel : {row['Nom_usuel']}<br>Code AIOT : {row['Code_AIOT_liste']}"
        tooltip_content = f"Nom usuel : {row['Nom_usuel']}<br>Code AIOT : {row['Code_AIOT_liste']}<br>nb points : {row['nb_points']}"
        
        marker = folium.Marker(
            location=[row['latitude'], row['longitude']],
            popup=popup_content,
            tooltip=tooltip_content,
            icon=None  # No default icon, to use custom CSS animation
        )
        marker_cluster.add_child(marker)

    m.add_child(marker_cluster)

# Ajouter les marqueurs pour df (en bleu) et dg (en rouge)
add_blinking_markers(df)
add_markers(dg, 'red')

# Afficher la couche GeoJSON des lignes avec une couleur unique
geojson_layer = folium.GeoJson(
    data='https://raw.githubusercontent.com/olivierparrot01/ICPE/main/lines.geojson', 
    name="Lignes entre points",
    style_function=lambda feature: {
        'color': 'black',  # Utilisez la couleur de votre choix
        'opacity': 1,
        'weight': 5  # Épaisseur constante
    },
    tooltip=folium.GeoJsonTooltip(
        fields=["Code_AIOT", "Distance"],
        aliases=["Code AIOT", "Distance"],
        style="font-size: 12px; text-align: center;"
    )
)

geojson_layer.add_to(m)
 #Filtrer les données en fonction des codes AIOT sélectionnés
selected_codes = st.multiselect("Sélectionner par le Code AIOT les points Gun à mettre en évidence", df["Code_AIOT"])


# Zoomer sur les points sélectionnés
if selected_codes:
    selected_data = df[df['Code_AIOT'].isin(selected_codes)]
    if not selected_data.empty:
        bounds = [
            (selected_data['latitude'].min(), selected_data['longitude'].min()),
            (selected_data['latitude'].max(), selected_data['longitude'].max())
        ]
        m.fit_bounds(bounds)

# Afficher la carte dans Streamlit en utilisant folium_static
folium_static(m)

# ... (suite du code)

