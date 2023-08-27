import geopandas as gpd
import pandas as pd
from shapely.geometry import Point, LineString
import streamlit as st
from streamlit_folium import folium_static
# Charger le GeoDataFrame des lignes (gdf_lignes) et des points (gdf_pts)
gdf_lignes = gpd.read_file('https://raw.githubusercontent.com/olivierparrot01/ICPE/main/c_selected.shp')
gdf_i = gpd.read_file('https://raw.githubusercontent.com/olivierparrot01/ICPE/main/i_83.shp')
gdf_i = gdf_i.to_crs('EPSG:2154')

gdf_pts = gpd.read_file('https://raw.githubusercontent.com/olivierparrot01/ICPE/main/g_pt3.shp',crs='2154')
gdf_pts.crs="EPSG:2154"
# Créer un GeoDataFrame vide pour stocker les nouvelles entités
result_gdf = gpd.GeoDataFrame(columns=['geometry'], crs=gdf_lignes.crs

import folium

# Coordonnées approximatives du centre de la région PACA
center_lat = 43.7157
center_lon = 5.0792

# Créer une carte centrée sur la région PACA
m = folium.Map(location=[center_lat, center_lon], zoom_start=8, crs='EPSG:2154')


# Créer une carte Folium centrée sur la région d'intérêt
#m = folium.Map(location=[48.8566, 2.3522], zoom_start=10)  # Remplacez les coordonnées et le niveau de zoom par ceux de votre région

# Ajouter les lignes à la carte
folium.GeoJson(result_gdf).add_to(m)


# Ajouter les lignes à la carte

folium.GeoJson(gdf_i).add_to(m)

# Ajouter les pts à la carte

# Ajouter une couche de points à la carte
for idx, row in gdf_pts.iterrows():
    # Obtenez les coordonnées du point
    lat, lon = row['geometry'].y, row['geometry'].x
    
    # Créez un marqueur pour le point et ajoutez-le à la carte
    folium.CircleMarker(location=[lat, lon], radius=5, color='black').add_to(m)


#folium.GeoJson(gdf_i).add_to(m)
# Afficher la carte
folium_static(m)
