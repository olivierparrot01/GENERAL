import streamlit as st
import folium
from streamlit_folium import folium_static

# Create a Streamlit app
st.title("Coordinate Capture with Folium in Streamlit")

# Create a map using Folium
m = folium.Map(location=[48.8566, 2.3522], zoom_start=12)

# Add a LatLngPopup to the map
popup = folium.LatLngPopup()
m.add_child(popup)

# Display the map in Streamlit using folium_static
folium_static(m)

# Display the captured coordinates in Streamlit
if popup:
    st.write("Captured Coordinates:")
    st.write("Latitude:", popup.args[0].lat)
    st.write("Longitude:", popup.args[0].lng)
