import streamlit as st
import folium
from streamlit_folium import folium_static
import folium.plugins as plugins

# Créer une carte avec Folium
m = folium.Map(location=[48.8566, 2.3522], zoom_start=12)

# Utiliser folium_static pour afficher la carte dans Streamlit
folium_static(m)

# Fonction pour gérer le clic sur la carte
def handle_click(event, **kwargs):
    lat, lon = event.latlng
    st.write(f"Latitude : {lat}, Longitude : {lon}")

# Ajouter l'événement de clic à la carte
m.add_child(folium.ClickForMarker(callback=handle_click))

# Afficher la carte mise à jour dans Streamlit en utilisant folium_static
folium_static(m)

