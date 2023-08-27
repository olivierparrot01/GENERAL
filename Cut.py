import folium
import geopandas as gpd
from shapely.geometry import Point, LineString
import streamlit as st
from streamlit_folium import folium_static

# Charger le GeoDataFrame des lignes (gdf_lignes) et des points (gdf_pts)
gdf_lignes = gpd.read_file('https://raw.githubusercontent.com/olivierparrot01/ICPE/main/c_selected.shp')
gdf_i = gpd.read_file('https://raw.githubusercontent.com/olivierparrot01/ICPE/main/i_83.shp')
gdf_i = gdf_i.to_crs('EPSG:2154')

gdf_pts = gpd.read_file('https://raw.githubusercontent.com/olivierparrot01/ICPE/main/i_endpoints.shp', crs='EPSG:2154')
gdf_pts=gdf_pts.to_crs('EPSG:2154')
#st.dataframe(gdf_pts)

# Coordonnées du centre de la région PACA
center_lat = 43.7157
center_lon = 5.0792

# Créer une carte Folium centrée sur la région d'intérêt
m = folium.Map(location=[center_lat, center_lon], zoom_start=8)  # Coordonnées et niveau de zoom pour la région PACA

# Ajouter les points 
#folium.GeoJson(gdf_pts,style_function=lambda x: {'color': 'black'}).add_to(m)
# Ajouter une couche de points à la carte
for idx, row in gdf_pts.iterrows():
    # Obtenez les coordonnées du point
    lat, lon = row['geometry'].y, row['geometry'].x
    st.write(lon)
    # Créez un marqueur pour le point et ajoutez-le à la carte
folium.CircleMarker(location=[lat, lon], radius=16, color='black').add_to(m)



# Ajouter les lignes rouges à la carte
folium.GeoJson(gdf_lignes, style_function=lambda x: {'color': 'red'}).add_to(m)

# Ajouter les lignes bleues à la carte
folium.GeoJson(gdf_i, style_function=lambda x: {'color': 'blue'}).add_to(m)

# Afficher la carte
folium_static(m)
