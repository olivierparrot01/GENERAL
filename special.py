# -*- coding: utf-8 -*-
"""
Created on Wed Aug 23 19:22:09 2023

@author: olivier.parrot
"""

import geopandas as gpd

import pandas as pd

from shapely.geometry import Point

# Charger la couche f et la couche g en tant que GeoDataFrames
f_path = r'S:\5_TRAVAUX\2023\2023_077\sig\i.shp'
g_path =r'S:\5_TRAVAUX\2023\2023_077\sig\c_selected.shp'

# Charger la couche f et la couche g en tant que GeoDataFrames
gdf_f = gpd.read_file(f_path)
gdf_g = gpd.read_file(g_path)





# Créez des points à partir des coordonnées x1, y1, x2, y2 de df
geometry_points = [Point(xy) for xy in zip(gdf_f ['L93_XAMONT'], gdf_f ['L93_YAMONT'])] + [Point(xy) for xy in zip(gdf_f ['L93_XAVAL'], gdf_f ['L93_YAVAL'])]

# Créez un GeoDataFrame à partir des points de df
gdf_pt = gpd.GeoDataFrame( geometry=geometry_points, crs="EPSG:2154")



# Ajoutez les attributs de gdf_f à gdf_pt
#gdf_pt = gdf_pt.join(gdf_f, rsuffix='_f')

# Ajouter l'attribut "ID_PCE" à gdf_pt en fonction de la valeur de "L93_XAMONT"
gdf_pt['ID_PCE'] = gdf_f['ID_PCE']

# Supprimer la colonne "geometry" du GeoDataFrame temporaire
#gdf_pt = gdf_pt.drop(columns=['geometry_f'])

# Enregistrez le GeoDataFrame au format shapefile
gdf_pt.to_file(r'S:\5_TRAVAUX\2023\2023_077\sig\i_pt4.shp')












import geopandas as gpd
from shapely.geometry import LineString, Point


# Fonction pour calculer le point médian le long d'une ligne
def middle_point_along_line(line):
    coords = line.coords
    total_length = line.length
    midpoint_length = total_length / 2.0

    accumulated_length = 0.0

    for i in range(len(coords) - 1):
        segment_start = Point(coords[i])
        segment_end = Point(coords[i + 1])
        segment_length = segment_start.distance(segment_end)
        accumulated_length += segment_length

        if accumulated_length >= midpoint_length:
            ratio = (midpoint_length - (accumulated_length - segment_length)) / segment_length
            x = segment_start.x + ratio * (segment_end.x - segment_start.x)
            y = segment_start.y + ratio * (segment_end.y - segment_start.y)
            return Point(x, y)

# Créer un GeoDataFrame pour stocker les points médians avec leurs attributs
gdf_midpoints = gpd.GeoDataFrame(columns=['geometry', 'ID_PCE'], crs=gdf_f.crs)

# Parcourir chaque ligne de gdf_f et calculer les points médians
for idx, row in gdf_f.iterrows():
    line = row['geometry']
    midpoint = middle_point_along_line(line)
    
    # Ajouter le point médian au GeoDataFrame avec l'ID_PCE correspondant
    gdf_midpoints = gdf_midpoints.append({'geometry': midpoint, 'ID_PCE': row['ID_PCE']}, ignore_index=True)

# Maintenant, gdf_midpoints contient les points médians le long des lignes de gdf_f
# Vous pouvez les enregistrer dans un fichier shapefile si nécessaire.

gdf_midpoints.to_file(r'S:\5_TRAVAUX\2023\2023_077\sig\midpoints_i2.shp')








import geopandas as gpd
from shapely.geometry import Point, LineString

# Charger les GeoDataFrames de points et de lignes
gdf_pts = gpd.read_file(r'S:\5_TRAVAUX\2023\2023_077\sig\i_pt1.shp')
gdf_lignes = gpd.read_file(r'S:\5_TRAVAUX\2023\2023_077\sig\c_selected.shp')










# Fonction pour calculer la projection orthogonale d'un point sur une ligne
def project_point_on_line(point, line):
    # Calculer la distance entre le point et la ligne
    distance = point.distance(line)
    
    # Vérifier si la distance est inférieure à 100 mètres
    if distance < 100:
        # Trouver le point le plus proche sur la ligne
        nearest_point = line.interpolate(line.project(point))
        return nearest_point
    else:
        return point

# Créer un GeoDataFrame vide pour stocker les résultats
result_gdf_pt = gpd.GeoDataFrame(columns=['geometry'], crs=gdf_pts.crs)

# Parcourir chaque point dans gdf_pts
for idx, point_row in gdf_pts.iterrows():
    point = point_row['geometry']
    attributs = point_row.drop('geometry')  # Exclure la colonne de géométrie

    # Trouver la ligne la plus proche en utilisant la distance minimale
    nearest_line = None
    min_distance = float('inf')

    for _, line_row in gdf_lignes.iterrows():
        line = line_row['geometry']
        distance = point.distance(line)

        if distance < min_distance:
            min_distance = distance
            nearest_line = line

    # Calculer la projection orthogonale du point sur la ligne
    projected_point = project_point_on_line(point, nearest_line)

    # Ajouter le point projeté avec les attributs appropriés au résultat_gdf
    result_gdf_pt = result_gdf_pt.append({'geometry': projected_point, **attributs}, ignore_index=True)

# Enregistrez le résultat dans un fichier shapefile
result_gdf_pt.to_file(r'S:\5_TRAVAUX\2023\2023_077\sig\g_pt3.shp')









import geopandas as gpd
from shapely.geometry import Point

# Charger la couche g en tant que GeoDataFrame
g_path = r'S:\5_TRAVAUX\2023\2023_077\sig\i.shp'
gdf_g = gpd.read_file(g_path)

# Créer une liste pour stocker les points d'extrémité
endpoints = []

# Parcourir chaque ligne de gdf_g
for idx, row in gdf_g.iterrows():
    line = row['geometry']
    
    # Obtenir les points d'extrémité de la ligne
    start_point = Point(line.coords[0])
    end_point = Point(line.coords[-1])
    
    # Ajouter les points d'extrémité à la liste
    endpoints.extend([start_point, end_point])

# Créer un GeoDataFrame à partir des points d'extrémité
gdf_endpoints = gpd.GeoDataFrame(geometry=endpoints, crs=gdf_g.crs)

# Enregistrer le GeoDataFrame au format shapefile
gdf_endpoints.to_file(r'S:\5_TRAVAUX\2023\2023_077\sig\i_endpoints.shp')














