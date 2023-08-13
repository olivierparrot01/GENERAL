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


# Load data from CSV
dg = pd.read_csv('https://raw.githubusercontent.com/olivierparrot01/ICPE/main/2geocodage.csv')
df = pd.read_csv('https://raw.githubusercontent.com/olivierparrot01/ICPE/main/0208_gun.csv')

# ... (autres traitements sur les données)

# Calcul des coordonnées du centre de la carte
center_lat = (df['latitude'].mean() + dg['latitude'].mean()) / 2
center_lon = (df['longitude'].mean() + dg['longitude'].mean()) / 2

# Création de la carte avec Folium
m = folium.Map(location=[center_lat, center_lon], zoom_start=8, control_scale=True)

# Fonction pour ajouter des marqueurs à la carte
def add_markers(data, color):
    for index, row in data.iterrows():
        popup_content = f"Nom usuel : {row['Nom_usuel']}<br>Code AIOT : {row['Code_AIOT_liste']}"
        tooltip_content = f"Nom usuel : {row['Nom_usuel']}<br>Code AIOT : {row['Code_AIOT_liste']}<br>nb points : {row['nb_points']}"
        
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

# Ajouter les marqueurs pour df (en bleu) et dg (en rouge)
add_markers(df, 'blue')
add_markers(dg, 'red')

# Ajouter la couche GeoJSON des lignes avec une couleur unique
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

# Afficher la carte mise à jour dans Streamlit en utilisant folium_static
folium_static(m)

# Afficher les données tabulaires dans une section expansible
with st.expander(f"Afficher les {len(df)} données"):
    # Afficher la table à l'intérieur de la section expansible
    st.dataframe(df)

st.markdown("<h2 style='font-size:18px;'>Sélectionner par le Code AIOT les points Gun à mettre en évidence (carte, table et liens Google Maps)</h2>", unsafe_allow_html=True)
# Sélection des codes AIOT à mettre en évidence
selected_codes = st.multiselect("", df["Code_AIOT"])

# Filtrer les données en fonction des codes AIOT sélectionnés
filtered_data = df[df['Code_AIOT'].isin(selected_codes)]

# Mettre en évidence les points correspondant aux codes AIOT sélectionnés
for index, row in filtered_data.iterrows():
    folium.CircleMarker(
        location=[row['latitude'], row['longitude']],
        radius=10,
        color='green',
        fill=True,
        fill_color='green',
        fill_opacity=0.6,
        popup=f"Code_AIOT(S): {row['Code_AIOT_liste']}"
    ).add_to(m)

# Afficher la carte mise à jour dans Streamlit en utilisant folium_static
folium_static(m)
