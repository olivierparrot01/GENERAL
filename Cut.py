import geopandas as gpd
import pandas as pd
from shapely.geometry import Point, LineString
import streamlit as st
from streamlit_folium import folium_static
# Charger le GeoDataFrame des lignes (gdf_lignes) et des points (gdf_pts)
gdf_lignes = gpd.read_file('https://raw.githubusercontent.com/olivierparrot01/ICPE/main/c_selected.shp')
gdf_pts = gpd.read_file('https://raw.githubusercontent.com/olivierparrot01/ICPE/main/g_pt3.shp',crs='2154')
#st.write(len(gdf_lignes))
# Créer un GeoDataFrame vide pour stocker les nouvelles entités
result_gdf = gpd.GeoDataFrame(columns=['geometry'], crs=gdf_lignes.crs)

# Parcourir chaque ligne dans gdf_lignes
for line in gdf_lignes['geometry']:
    new_geometries = []
    
    # Parcourir chaque point dans gdf_pts
    for point in gdf_pts['geometry']:
        # Vérifier si le point est sur la ligne
        if point.intersects(line):
            # Découper la ligne en deux parties à l'emplacement du point
            parts = line.difference(Point(point))
            
            # Si les parties sont des MultiLineString, les découper en LineString individuels
            if parts.geom_type == 'MultiLineString':
                new_geometries.extend(list(parts))
            elif parts.geom_type == 'LineString':
                new_geometries.append(parts)
    
    # Si de nouvelles entités ont été créées, les ajouter au résultat
    if new_geometries:
        result_gdf = pd.concat([result_gdf, gpd.GeoDataFrame({'geometry': new_geometries}, crs=gdf_lignes.crs)], ignore_index=True)
        #st.write(result_gdf)
# Enregistrez le GeoDataFrame résultant dans un fichier shapefile
#result_gdf.to_file('chemin_vers_nouvelles_entites.shp')

import folium

# Charger le GeoDataFrame des lignes (gdf_lignes)
#gdf_lignes = gpd.read_file('chemin_vers_votre_shapefile.shp')

# Créer une carte Folium centrée sur la région d'intérêt
m = folium.Map(location=[48.8566, 2.3522], zoom_start=10)  # Remplacez les coordonnées et le niveau de zoom par ceux de votre région

# Ajouter les lignes à la carte
folium.GeoJson(result_gdf).add_to(m)

# Ajouter les pts à la carte
folium.GeoJson(gdf_pts).add_to(m)

# Afficher la carte
folium_static(m)
