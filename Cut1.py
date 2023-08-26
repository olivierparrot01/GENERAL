import streamlit as st
import geopandas as gpd
import networkx as nx
from shapely.geometry import Point, LineString

# Charger le GeoDataFrame des lignes (gdf_lignes) et des points (gdf_pts)
#gdf_lignes = gpd.read_file('chemin_vers_lignes.shp')
#gdf_pts = gpd.read_file('chemin_vers_points.shp')
# Charger le GeoDataFrame des lignes (gdf_lignes) et des points (gdf_pts)
gdf_lignes = gpd.read_file('https://raw.githubusercontent.com/olivierparrot01/ICPE/main/c_selected.shp')
gdf_pts = gpd.read_file('https://raw.githubusercontent.com/olivierparrot01/ICPE/main/g_pt3.shp')


import geopandas as gpd
import pandas as pd

# Charger votre GeoDataFrame de lignes (gdf_lines) et de points (gdf_pts)

# Réduire gdf_lines à 3 éléments
gdf_lignes = gdf_lignes.sample(n=3, random_state=42)

# Filtrer les points qui sont dessus
gdf_pts= gpd.sjoin(gdf_pts, gdf_lignes, op='intersects')

# gdf_pts_on_lines contient maintenant les points qui sont sur les 3 lignes échantillonnées




# Créer un graphe à partir des lignes
G = nx.Graph()

# Ajouter les nœuds au graphe à partir des points
for idx, point in gdf_pts.iterrows():
    G.add_node(idx, geometry=point['geometry'])

# Ajouter les arêtes (lignes) au graphe et connecter les nœuds
for idx, line in gdf_lignes.iterrows():
    line_coords = list(line['geometry'].coords)
    
    # Trouver les nœuds les plus proches dans le graphe
    closest_nodes = []
    for coord in line_coords:
        nearest_node = min(G.nodes, key=lambda node: Point(coord).distance(G.nodes[node]['geometry']))
        closest_nodes.append(nearest_node)
    
    # Ajouter les arêtes (lignes) entre les nœuds les plus proches
    for i in range(len(closest_nodes) - 1):
        G.add_edge(closest_nodes[i], closest_nodes[i + 1])

# Créer un GeoDataFrame pour stocker les nouvelles entités
result_gdf = gpd.GeoDataFrame(columns=['geometry'], crs=gdf_lignes.crs)

# Parcourir les composantes connectées du graphe (chaque composante est une nouvelle entité)
for component in nx.connected_components(G):
    # Extraire les géométries des nœuds de la composante
    component_geometries = [G.nodes[node]['geometry'] for node in component]
    
    # Créer une LineString à partir des géométries des nœuds
    component_line = LineString(component_geometries)
    
    # Ajouter la LineString au GeoDataFrame résultant
    result_gdf = result_gdf.append({'geometry': component_line}, ignore_index=True)

# Enregistrez le GeoDataFrame résultant dans un fichier shapefile
#result_gdf.to_file('chemin_vers_nouvelles_entites.shp')


with st.expander(f"Afficher les {len(result_gdf)} données"):
    # Afficher la table à l'intérieur de la section expansible
    st.dataframe(result_gdf)
    
#import geopandas as gpd
import folium

# Charger le GeoDataFrame contenant vos données géospatiales
#gdf = gpd.read_file('chemin_vers_votre_fichier.shp')

# Créer une carte Folium
m = folium.Map(location=[gdf.geometry.centroid.y.mean(), result_gdf.geometry.centroid.x.mean()], zoom_start=10)

# Ajouter les données géospatiales à la carte
for idx, row in result_gdf.iterrows():
    folium.GeoJson(row.geometry).add_to(m)

# Afficher la carte dans Streamlit
st.write("Carte des données géospatiales")
st.write(m)
