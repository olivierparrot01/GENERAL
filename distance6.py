import streamlit as st
import folium
from streamlit_folium import folium_static

# Créer une carte avec Folium
m = folium.Map(location=[48.8566, 2.3522], zoom_start=12)

# Utiliser folium_static pour afficher la carte dans Streamlit
folium_static(m)

# Liste pour stocker les coordonnées des clics
click_coordinates = []

# Ajouter une zone de texte pour afficher les coordonnées capturées
st.sidebar.subheader("Coordonnées capturées")
coordinates_text = st.sidebar.empty()

# Fonction pour mettre à jour la liste des coordonnées et le texte
def update_coordinates(lat, lon):
    click_coordinates.append((lat, lon))
    coordinates_text.text(f"Latitude : {lat}, Longitude : {lon}")

# Ajouter l'événement de clic à la carte
m.add_child(folium.ClickForMarker(popup=None, callback=update_coordinates))

# Afficher les coordonnées capturées
st.sidebar.write("Coordonnées capturées :")
for lat, lon in click_coordinates:
    st.sidebar.write(f"Latitude : {lat}, Longitude : {lon}")
