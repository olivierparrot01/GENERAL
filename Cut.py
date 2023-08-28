import folium
import geopandas as gpd
import streamlit as st
from streamlit_folium import folium_static

# Charger le GeoDataFrame des lignes (gdf_lignes) et des points (gdf_pts)
gdf_lignes = gpd.read_file('https://raw.githubusercontent.com/olivierparrot01/ICPE/main/c_selected.shp')
gdf_i = gpd.read_file('https://raw.githubusercontent.com/olivierparrot01/ICPE/main/i_83.shp')
#gdf_i = gdf_i.to_crs('EPSG:2154')

i_pts = gpd.read_file('https://raw.githubusercontent.com/olivierparrot01/ICPE/main/i_endpoints.shp', crs='EPSG:2154')
i_pts = i_pts.to_crs('EPSG:4326')




# Coordonnées du centre de la région PACA
center_lat = 43.7157
center_lon = 5.0792

# Créer une carte Folium centrée sur la région d'intérêt
m = folium.Map(location=[center_lat, center_lon], zoom_start=8)  # Coordonnées et niveau de zoom pour la région PACA

# Ajouter les lignes à la carte
#folium.GeoJson(gdf_lignes).add_to(m)
folium.GeoJson(gdf_lignes, style_function=lambda x: {'color': 'blue'}).add_to(m)
# Ajouter les lignes à la carte
#µfolium.GeoJson(gdf_i).add_to(m)
folium.GeoJson(gdf_i, style_function=lambda x: {'color': 'red'}).add_to(m)
# Créer une nouvelle carte pour les points
#m_pts = folium.Map(location=[center_lat, center_lon], zoom_start=8)  # Coordonnées et niveau de zoom pour la région PACA

# Ajouter les points à la nouvelle carte avec des marqueurs noirs
for idx, row in i_pts.iterrows():
    # Obtenez les coordonnées du point
    lat, lon = row['geometry'].y, row['geometry'].x
    i_pts.at[idx, 'lat'] = lat
    i_pts.at[idx, 'lon'] = lon
    # Créez un marqueur pour le point avec une couleur noire
    folium.CircleMarker(location=[lat, lon], radius=5, color='black').add_to(m)


# Ajouter les lignes à la carte
#folium.GeoJson(i_pts).add_to(m)

# Ajouter les lignes à la carte
#folium.GeoJson(i_pts).add_to(m)

# Afficher la carte des lignes
folium_static(m)

# Afficher la carte des points
#folium_static(m_pts)
