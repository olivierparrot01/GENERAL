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



# Load GeoJSON data
geojson_url = 'https://raw.githubusercontent.com/olivierparrot01/ICPE/main/line_json_wgs84.geojson'
lines_geojson_data = requests.get(geojson_url).json()

# Convert 'Distance' column to integer
for feature in lines_geojson_data['features']:
    if 'properties' in feature and 'Distance' in feature['properties']:
        feature['properties']['Distance'] = int(feature['properties']['Distance'])

# Load data
df = pd.read_csv('https://raw.githubusercontent.com/olivierparrot01/ICPE/main/0208_gun.csv')
dg = pd.read_csv('https://raw.githubusercontent.com/olivierparrot01/ICPE/main/2geocodage.csv')

# Data conversions
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
df = df[df['Distance'] >= 0]
df['Distance'] = df['Distance'].astype(int)

# Data cleanup
df = df.drop(["Courriel d'échange avec l'administration", "Région", "Unnamed: 0"], axis=1)

# Create a list to store captured coordinates
captured_coordinates_list = []

# Function to add markers to the map
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

# Function to add blinking markers to the map
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

# Sidebar options
st.sidebar.title("Options")

# Sidebar section to filter the DataFrame based on selected criteria
selected_criteria = st.sidebar.multiselect("Critères de sélection", ["Statut Seveso", "Statut IED", "Distance"])

# Apply the selected criteria to filter the DataFrame
filtered_df = df.copy()
for criterion in selected_criteria:
    if criterion == 'Statut Seveso':
        unique_values = filtered_df['Statut Seveso'].unique()
        selected_value = st.sidebar.selectbox("Statut Seveso", options=unique_values)
        filtered_df = filtered_df[filtered_df['Statut Seveso'] == selected_value]
    elif criterion == 'Statut IED':
        unique_values = filtered_df['Statut IED'].unique()
        selected_value = st.sidebar.selectbox("Statut IED", options=unique_values)
        filtered_df = filtered_df[filtered_df['Statut IED'] == selected_value]
    elif criterion == 'Distance':
        min_distance = df['Distance'].min()
        max_distance = df['Distance'].max()
        selected_distance = st.sidebar.slider("La distance est supérieure ou égale à :", min_value=min_distance, max_value=max_distance, step=50)
        filtered_df = filtered_df[filtered_df['Distance'] >= selected_distance]
        if st.sidebar.button("Filtrer entre 10000 et max"):
            filtered_df = filtered_df[(filtered_df['Distance'] >= 10000) & (filtered_df['Distance'] <= max_distance)]
        else:
            filtered_df = filtered_df[filtered_df['Distance'] >= selected_distance]

# Display filtered DataFrame in an expander
with st.sidebar.expander("Afficher les données filtrées"):
    st.write("Données filtrées :", filtered_df)

# Map center coordinates
center_lat = (df['latitude'].mean() + dg['latitude'].mean()) / 2
center_lon = (df['longitude'].mean() + dg['longitude'].mean()) / 2

# Create a Folium map
m = folium.Map(location=[center_lat, center_lon], zoom_start=8, control_scale=True)

# Add markers for df (blue) and dg (red)
add_markers(df, 'blue')
add_markers(dg, 'red')

# Add blinking markers for df
add_blinking_markers(df)

# Add GeoJSON layer of lines to the map
lines_geojson_layer.add_to(m)

# Add full screen button to the map
fullscreen = Fullscreen(position="topleft", title="Plein écran", title_cancel="Quitter le plein écran")
fullscreen.add_to(m)

# Display the map using folium_static
folium_static(m)

# Retrieve coordinates from the popup if available
try:
    captured_coords = popup.html.split(",")
    latitude = float(captured_coords[0].split(":")[1])
    longitude = float(captured_coords[1].split(":")[1])
    popup_content = popup.get_name()
    st.write(popup_content)
except AttributeError:
    st.write("")

# Display information in the sidebar
st.sidebar.markdown("<h2 style='font-size:18px;'>Adresses, coordonnées Gun et liens Google Maps des points sélectionnés :</h2>", unsafe_allow_html=True)
for _, row in filtered_data.iterrows():
    st.sidebar.write(f"- Adresse Gun : {row['Adresse_concat']}, Coordonnées Gun : {row['longitude']}, {row['latitude']}")
    formatted_address = row['Adresse_concat'].replace(' ', '-')
    google_maps_link_address = f"[Ouvrir dans Google Maps à partir de l'adresse Gun](https://www.google.com/maps/search/?api=1&query={formatted_address})"
    st.sidebar.markdown(google_maps_link_address, unsafe_allow_html=True)
    google_maps_link_coords = f"[Ouvrir dans Google Maps à partir des coordonnées Gun](https://www.google.com/maps?q={row['latitude']},{row['longitude']})"
    st.sidebar.markdown(google_maps_link_coords, unsafe_allow_html=True)
