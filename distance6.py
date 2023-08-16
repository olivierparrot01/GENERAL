import streamlit as st
import folium
from streamlit_folium import folium_static
import folium.plugins as plugins

# Créer une carte avec Folium
m = folium.Map(location=[48.8566, 2.3522], zoom_start=12)

# Utiliser folium_static pour afficher la carte dans Streamlit
folium_static(m)

# Fonction pour gérer le clic sur la carte
def handle_click(e):
    lat, lon = e.latlng
    st.write(f"Latitude : {lat}, Longitude : {lon}")

# Ajouter l'événement de clic à la carte avec un marqueur personnalisé
click_plugin = plugins.MarkerCluster().add_to(m)
folium.Marker(
    location=[48.8566, 2.3522],
    icon=None,
    popup="Cliquez pour obtenir les coordonnées",
    callback=handle_click
).add_to(click_plugin)

# Afficher la carte mise à jour dans Streamlit en utilisant folium_static
folium_static(m)
