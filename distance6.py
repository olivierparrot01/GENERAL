import streamlit as st
import folium
from streamlit_folium import folium_static

# Create a map using Folium
m = folium.Map(location=[48.8566, 2.3522], zoom_start=12)

# Add a LatLngPopup to the map
folium.LatLngPopup().add_to(m)

# Display the map in Streamlit
folium_static(m)
