# -*- coding: utf-8 -*-
"""
Created on Thu Apr 27 18:17:50 2023

@author: olivier.parrot
"""
from pyproj import Transformer
import requests
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
from geopy.distance import geodesic
import re
# from simpledbf import Dbf5
# Importation du fichier Excel


# df = pd.read_csv(r'C:\Users\olivier.parrot\Desktop\cartopas\icpe\icpe_3103\2022_GUN_extraction.csv', dtype='str')


df = pd.read_excel(r'C:\Users\olivier.parrot\Desktop\cartopas\icpe\icpe_3103\geoide\carte\20230726_export_recherche_avancee_GUN(1).ods',
                   sheet_name='Infos générales et métier', dtype='str')


# df['Code AIOT'] = df['Code AIOT'].replace("000", '', regex=True)

df['Code AIOT'] = df['Code AIOT'].apply(lambda x: re.sub(r'^0+', '', x))


# , engine='odf'
# df = df.loc[(df["Etat de l'activité"] == 'Avec titre') & (
#     (df['Régime en vigueur'] == 'Autorisation') | (df['Régime en vigueur'] == 'Enregistrement'))]


# 1062230 - 6237817  mer


# df['Ref carto X'] = df['Ref carto X'].replace("-", "1062230", regex=True)
# df['Ref carto Y'] = df['Ref carto Y'].replace("-", "6237817", regex=True)

# df['Ref carto X'] = df['Ref carto X'].astype(float)
# df['Ref carto Y'] = df['Ref carto Y'].astype(float)


# df['longitude'] = df['longitude'].astype(float)
# df['latitude'] = df['latitude'].astype(float)



# df['Coordonnées X'] = df['Coordonnées X'].replace("-", "1062230", regex=True)
# df['Coordonnées Y'] = df['Coordonnées Y'].replace("-", "6237817", regex=True)


# Remplacez ce code par le code EPSG correspondant à votre système de référence
current_crs = 'EPSG:2154'

# Définir le système de référence cible (EPSG 4326 pour WGS 84)
target_crs = 'EPSG:4326'

# Créer une instance de Transformer pour effectuer la transformation
transformer = Transformer.from_crs(current_crs, target_crs, always_xy=True)

# Transformer les coordonnées cartographiques en coordonnées géographiques (latitude et longitude)
# df['longitude'], df['latitude'] = transformer.transform(    df['Coordonnées X'], df['Ref carto Y'])

df['longitude'], df['latitude'] = transformer.transform(
    df['Coordonnées X'], df['Coordonnées Y'])


df['nb_points'] = df.groupby(['longitude', 'latitude'])[
    'latitude'].transform('size')


df['groupe_id'] = (df.groupby(['longitude', 'latitude']).ngroup() + 1)


df_nan = df.loc[df['longitude'].isnull()]

df_nan.to_csv(r'C:\Users\olivier.parrot\Desktop\cartopas\icpe\icpe_3103\geoide\carte\gun_sans_coord.csv')


# df_cleaned = df.loc[df['longitude'].notna()]

df = df.loc[df['longitude'].notna()]
df[['longitude', 'latitude']] = df[['longitude', 'latitude']].apply(abs)

geometry = [Point(lon, lat) for lon, lat in zip(df['longitude'], df['latitude'])]
df_geo = gpd.GeoDataFrame(df, crs=target_crs, geometry=geometry)

# df_not_in_df_geo = df[~df['Code AIOT'].isin(df_geo['Code AIOT'])]
# geometry = [Point(lon, lat) for lon, lat in zip(df_not_in_df_geo['longitude'], df_not_in_df_geo['latitude'])]
# df_not_in_df_geo_geo = gpd.GeoDataFrame(df_not_in_df_geo, crs=target_crs, geometry=geometry)


# df_geo = pd.concat([df_geo, df_not_in_df_geo_geo], axis=0)


# df_not_in_df_geo.to_csv(r'C:\Users\olivier.parrot\Desktop\cartopas\icpe\icpe_3103\geoide\carte\df_not_in_df_geo.csv')


# df_in_df_geo = df[df['Code AIOT'].isin(df_geo['Code AIOT'])]

# geometry = [Point(xy) for xy in zip(df['Ref carto X'], df['Ref carto Y'])]

# df =gpd.GeoDataFrame(df, crs=2154, geometry=geometry)

# df = df.to_crs(epsg=4326)
df_geo.to_file(r'C:\Users\olivier.parrot\Desktop\cartopas\icpe\icpe_3103\geoide\carte\gun.shp', driver='ESRI Shapefile', encoding='utf-8')

df_geo.to_csv(r'C:\Users\olivier.parrot\Desktop\cartopas\icpe\icpe_3103\geoide\carte\gun.csv', encoding='utf-8')

# dbf = Dbf5(r'C:\Users\olivier.parrot\Desktop\cartopas\icpe\icpe_3103\geoide\split_2022_GUN_extraction_analyse_geocoded.dbf')

# # On transforme la base de données dbf en une base de données pandas
# dbf1=dbf.to_dataframe()
# df.columns


dg = pd.read_csv(
    r'C:\Users\olivier.parrot\Desktop\cartopas\icpe\icpe_3103\geoide\carte\icpe_geocoded_dreal_nondreal.csv', dtype='str')

dg = dg.loc[dg['result_status'] == 'ok']


dg_nan = dg.loc[dg['result_status'] == 'not-found']

dg_nan.to_csv(r'C:\Users\olivier.parrot\Desktop\cartopas\icpe\icpe_3103\geoide\carte\geocodage_not-found.csv', encoding='utf-8')


df.columns


dg['longitude'] = dg['longitude'].astype(float)
dg['latitude'] = dg['latitude'].astype(float)

# geometry = [Point(x,y) for x,y in zip(dg['longitude'], dg[ 'latitude'])]

# dg =gpd.GeoDataFrame(df, crs=4326, geometry=geometry)
# dg = dg.to_crs(epsg=2154)

# df['Code AIOT']= dbf1['Code AIOT'].apply(str)
# df['latitude']= dbf1['latitude'].apply(str)

# dg.to_file(r'C:\Users\olivier.parrot\Desktop\cartopas\icpe\icpe_3103\geoide\carte\dg.shp', driver='ESRI Shapefile',  encoding='latin-1')

# ajout d'une colonne avec le nombre de points pour chaque latitude
# df['nb_points'] = df.groupby('Ref carto Y')['Ref carto Y'].transform('size')
# df['nb_points'] = df.groupby(['Ref carto Y', 'Ref carto X'])[    'Ref carto Y'].transform('size')


# df2=df.loc[df['nb_points'] > 1]

# df1=df.loc[df['nb_points'] == 1]

# df1['groupe_id'] = 'groupe ' + (df1.groupby(['Ref carto Y', 'Ref carto X']).ngroup() + 1).astype(str)


# df2['groupe_id'] = (df2.groupby(['Ref carto Y', 'Ref carto X']).ngroup() + 1)

# result.to_excel(r'C:\Users\olivier.parrot\Desktop\cartopas\icpe\icpe_3103\AIOT_global_autorisation_enregistrement_analyse.ods', index=False)

# df.to_csv(r'C:\Users\olivier.parrot\Desktop\cartopas\icpe\icpe_3103\geoide\carte\df.csv')

# dg.to_csv(r'C:\Users\olivier.parrot\Desktop\cartopas\icpe\icpe_3103\geoide\carte\dg.csv')


# df2.to_csv(r'C:\Users\olivier.parrot\Desktop\cartopas\icpe\icpe_3103\2022_GUN_extraction_analyse_nb_points_2.csv')


# import matplotlib.pyplot as plt

# # Supposons que vous ayez déjà le GeoDataFrame df créé précédemment

# # Afficher la carte


# Créer une liste pour stocker les distances pour chaque aiot
distances = []

# Boucler sur les valeurs uniques de 'Code AIOT' dans df
for aiot in df['Code AIOT'].unique():
    # Sélectionner les lignes correspondant à l'aiot spécifique dans df
    df_aiot = df[df['Code AIOT'] == aiot]

    # Sélectionner les lignes correspondant à l'aiot spécifique dans dg
    dg_aiot = dg[dg['Code AIOT'] == aiot]

    # Initialiser une liste pour stocker les distances pour cet aiot spécifique
    distances_aiot = []

    # Itérer sur les lignes de df_aiot
    for index_df, row_df in df_aiot.iterrows():
        # Récupérer les coordonnées géographiques de df pour cette ligne
        lat_df, lon_df = float(row_df['latitude']), float(row_df['longitude'])

        # Itérer sur les lignes de dg_aiot
        for index_dg, row_dg in dg_aiot.iterrows():
            # Récupérer les coordonnées géographiques de dg pour cette ligne
            lat_dg, lon_dg = float(row_dg['latitude']), float(
                row_dg['longitude'])

            # Calculer la distance entre les coordonnées géographiques de df et dg pour cette paire de points
            distance = geodesic((lat_dg, lon_dg), (lat_df, lon_df)).meters

            # Ajouter le code AIOT et la distance à la liste des distances
            distances.append({'Code AIOT': aiot, 'Distance': distance})

distance_df_dg = pd.DataFrame(distances)
# Effectuer une jointure entre distance_df et dg en utilisant la colonne 'Code AIOT'
dg_merged = dg.merge(distance_df_dg, on='Code AIOT',  how='left')

dg_merged_nan = dg_merged .loc[dg_merged ['Distance'].isnull()]

values_not_in_df = dg[~dg['Code AIOT'].isin(df['Code AIOT'])]['Code AIOT']

df_geo = df_geo.merge(distance_df_dg, on='Code AIOT', how='outer')

df_geo_distance_nan = df_geo.loc[df_geo['Distance'].isnull()]


dg_merged = dg_merged.merge(df[['Code AIOT','Statut IED', 'Statut Seveso']], on= 'Code AIOT', how='left')

# df.columns

# dg_merged = pd.concat([dg_merged, dg_merged_nan], axis=0)





# Convertir le DataFrame en GeoDataFrame en spécifiant la géométrie comme une colonne de points
geometry = [Point(xy)
            for xy in zip(dg_merged['longitude'], dg_merged['latitude'])]

dg_merged_gdf = gpd.GeoDataFrame(dg_merged, crs='EPSG:4326', geometry=geometry)




dg_merged_gdf['nb_points'] = dg_merged_gdf.groupby(['longitude', 'latitude'])[
    'latitude'].transform('size')


dg_merged_gdf['groupe_id'] = (dg_merged_gdf.groupby(['longitude', 'latitude']).ngroup() + 1)



# dg_merged_gdf.to_file(r'C:\Users\olivier.parrot\Desktop\cartopas\icpe\icpe_3103\geoide\carte\geocodage.shp',
#                       driver='ESRI Shapefile',  encoding='utf-8')

# dg_merged_gdf.to_csv(r'C:\Users\olivier.parrot\Desktop\cartopas\icpe\icpe_3103\geoide\carte\geocodage.csv', encoding='utf-8')



# dg_merged_gdf_sup_500 = dg_merged_gdf.loc[(dg_merged_gdf["Distance"] >= 500)]
# dg_merged_gdf_sup_500.reset_index

# dg_merged_gdf_500 = dg_merged_gdf.loc[(dg_merged_gdf["Distance"] <= 500)]

# dg_merged_gdf_400 = dg_merged_gdf.loc[(dg_merged_gdf["Distance"] <= 400)]

# dg_merged_gdf_300 = dg_merged_gdf.loc[(dg_merged_gdf["Distance"] <= 300)]

# dg_merged_gdf_200 = dg_merged_gdf.loc[(dg_merged_gdf["Distance"] <= 200)]

# dg_merged_gdf_100 = dg_merged_gdf.loc[(dg_merged_gdf["Distance"] <= 100)]


# 



# dg_merged_gdf.columns


# Convertir les valeurs de la colonne "result_score" en nombres flottants (float)
dg_merged_gdf["result_score"] = dg_merged_gdf["result_score"].astype(float)

# Filtrer les lignes avec un score de résultat supérieur ou égal à 0.5
dg_merged_gdf_result_score = dg_merged_gdf.loc[dg_merged_gdf["result_score"] >= 0.5]

# dg_merged_gdf_Statut IED = dg_merged_gdf.loc[dg_merged_gdf["Statut IED"] == 'oui']
dg_merged_gdf_Statut_IED = dg_merged_gdf.loc[dg_merged_gdf['Statut IED'] == 'Oui']

# print(dg_merged_gdf_Statut_IED)

# dg_merged_gdf_result_score.plot()













# import geopandas as gpd
# import pandas as pd
import numpy as np
from shapely.geometry import Point

# Supposons que vous ayez déjà un GeoDataFrame appelé dg_merged_gdf avec la colonne "nb_points"

# Filtrer les points ayant une valeur supérieure à 2 dans la colonne "nb_points"
gdf_filtered = dg_merged_gdf[dg_merged_gdf["nb_points"] >= 2]

df_geo_filtered = df_geo[df_geo["nb_points"] >= 2]

# gdf_filtered.reset_index(drop=True, inplace=True)

gdf_non_filtered = dg_merged_gdf[dg_merged_gdf["nb_points"] < 2]
df_geo_non_filtered =df_geo[df_geo["nb_points"] < 2]

# gdf_non_filtered.reset_index(drop=True, inplace=True)

# Fonction pour déplacer aléatoirement un point dans un disque de rayon 100 mètres
def random_displacement(point):
    lat, lon = point["latitude"], point["longitude"]
    r = 100 / 111300  # Convertir 100 mètres en degrés (environ 111300 mètres par degré)
    theta = 2 * np.pi * np.random.random()  # Angle aléatoire en radians
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    
    # Create a copy of the point to preserve original attributes
    new_point = point.copy()
    new_point["latitude"] = lat + y
    new_point["longitude"] = lon + x
    
    return new_point

# Appliquer la fonction de déplacement aléatoire sur les points filtrés
gdf_filtered_displaced = gdf_filtered.apply(random_displacement, axis=1)

df_geo_filtered_displaced =df_geo_filtered.apply(random_displacement, axis=1)

# df_geo_displaced = df_geo_filtered.apply(random_displacement, axis=1)

# Create the 'geometry' column using latitude and longitude
gdf_filtered_displaced['geometry'] = gdf_filtered_displaced.apply(lambda row: Point(row['longitude'], row['latitude']), axis=1)
df_geo_filtered_displaced['geometry'] = df_geo_filtered_displaced.apply(lambda row: Point(row['longitude'], row['latitude']), axis=1)
# # Convertir la Series en DataFrame
# gdf_filtered_displaced = gdf_filtered_displaced.apply(pd.Series)

# Réinitialiser l'index du DataFrame des points déplacés
# gdf_filtered_displaced.reset_index(drop=True, inplace=True)

# Réinitialiser l'index de gdf_filtered
# gdf_filtered.reset_index(drop=True, inplace=True)

# Merge the displaced points DataFrame with the filtered DataFrame
dg_all_points = pd.concat([gdf_filtered_displaced, gdf_non_filtered], axis=0)

dg_all_points_nan = dg_all_points.loc[dg_all_points ['Distance'].isnull()]

df_geo_all_points = pd.concat([df_geo_filtered_displaced,df_geo_non_filtered], axis=0)

df_geo_all_points_nan = df_geo_all_points.loc[df_geo_all_points ['Distance'].isnull()]

values_not_in_dg_all_points = df_geo_all_points[~df_geo_all_points['Code AIOT'].isin(dg_all_points['Code AIOT'])]['Code AIOT']

values_not_in_df_geo_all_points = dg_all_points[~dg_all_points['Code AIOT'].isin(df_geo_all_points['Code AIOT'])]['Code AIOT']

# dg_all_points.to_file(r'C:\Users\olivier.parrot\Desktop\cartopas\icpe\icpe_3103\geoide\carte\dg_all_points.shp', driver='ESRI Shapefile', encoding='utf-8')

# df_geo_all_points.to_file(r'C:\Users\olivier.parrot\Desktop\cartopas\icpe\icpe_3103\geoide\carte\df_geo_all_points.shp', driver='ESRI Shapefile', encoding='utf-8')


# import pandas as pd
# from unidecode import unidecode

# Supposons que df est votre DataFrame contenant des noms de colonnes avec des espaces et des accents.

# Utilisez la méthode rename() en spécifiant un dictionnaire pour renommer les colonnes sans espace ni accent
df_geo_all_points = df_geo_all_points.rename(columns=lambda x: unidecode(x.replace(' ', '_')))
dg_all_points = dg_all_points.rename(columns=lambda x: unidecode(x.replace(' ', '_')))

import pandas as pd
from unidecode import unidecode

# Supposons que df est votre DataFrame contenant des données avec des caractères Unicode.

# Créez une fonction pour appliquer unidecode uniquement sur les éléments de type str
def unidecode_str(element):
    if isinstance(element, str):
        return unidecode(element)
    return element

# Appliquez la fonction à chaque élément du DataFrame en utilisant applymap
df_geo_all_points = df_geo_all_points.applymap(unidecode_str)

# Affichez le DataFrame après avoir appliqué unidecode sur les éléments de type str
print(df)




# df_geo_all_points=df_geo_all_points['Code AIOT','Nom usuel']

df_geo_all_points_500 = df_geo_all_points.loc[(df_geo_all_points["Distance"] <= 500)]

df_geo_all_points_400 =df_geo_all_points.loc[(df_geo_all_points["Distance"] <= 400)]

df_geo_all_points_300 = df_geo_all_points.loc[(df_geo_all_points["Distance"] <= 300)]

df_geo_all_points_200 = df_geo_all_points.loc[(df_geo_all_points["Distance"] <= 200)]

df_geo_all_points_100 = df_geo_all_points.loc[(df_geo_all_points["Distance"] <= 100)]


df_geo_all_points_sup_500 = df_geo_all_points.loc[(df_geo_all_points["Distance"] > 500)]




df_geo_all_points_100.to_file(r'C:\Users\olivier.parrot\Desktop\cartopas\icpe\icpe_3103\geoide\carte\gun_100m.shp', driver='ESRI Shapefile', encoding='utf-8')

df_geo_all_points_200.to_file(r'C:\Users\olivier.parrot\Desktop\cartopas\icpe\icpe_3103\geoide\carte\gun_200m.shp', driver='ESRI Shapefile', encoding='utf-8')

df_geo_all_points_300.to_file(r'C:\Users\olivier.parrot\Desktop\cartopas\icpe\icpe_3103\geoide\carte\gun_300m.shp', driver='ESRI Shapefile', encoding='utf-8')

df_geo_all_points_400.to_file(r'C:\Users\olivier.parrot\Desktop\cartopas\icpe\icpe_3103\geoide\carte\gun_400m.shp', driver='ESRI Shapefile', encoding='utf-8')

df_geo_all_points_500.to_file(r'C:\Users\olivier.parrot\Desktop\cartopas\icpe\icpe_3103\geoide\carte\gun_500m.shp', driver='ESRI Shapefile', encoding='utf-8')


df_geo_all_points_sup_500.to_file(r'C:\Users\olivier.parrot\Desktop\cartopas\icpe\icpe_3103\geoide\carte\gun_sup_500m.shp', driver='ESRI Shapefile', encoding='utf-8')







# dg_all_points["result_score"] = dg_all_points["result_score"].astype(float)

# # Filtrer les lignes avec un score de résultat supérieur ou égal à 0.5
# dg_all_points_result_score = dg_all_points.loc[dg_all_points["result_score"] >= 0.5]

# # dg_merged_gdf_Statut IED = dg_merged_gdf.loc[dg_merged_gdf["Statut IED"] == 'oui']
# dg_merged_gdf_Statut_IED = dg_merged_gdf.loc[dg_merged_gdf['Statut IED'] == 'Oui']






dg_all_points.to_file(r'C:\Users\olivier.parrot\Desktop\cartopas\icpe\icpe_3103\geoide\carte\geocodage.shp', driver='ESRI Shapefile', encoding='utf-8')

df_geo_all_points.to_file(r'C:\Users\olivier.parrot\Desktop\cartopas\icpe\icpe_3103\geoide\carte\gun_clean.shp', driver='ESRI Shapefile', encoding='utf-8')



















# common_values_count = df['Code AIOT'].isin(dg['Code AIOT']).sum()
# print(common_values_count)


# # Values in df['Code AIOT'] that are not in dg['Code AIOT']
# values_not_in_dg = df_geo[~df_geo['Code AIOT'].isin(dg['Code AIOT'])]['Code AIOT']

# # Values in dg['Code AIOT'] that are not in df['Code AIOT']
# values_not_in_df = dg[~dg['Code AIOT'].isin(df['Code AIOT'])]['Code AIOT']

# # Combine both sets of values into a single list
# all_unique_values = pd.concat([values_not_in_dg, values_not_in_df])

# # Print the unique values that are not common between the two columns
# print(all_unique_values)



# # Values in df['Code AIOT'] that are not in dg['Code AIOT']
# values_not_in_dg = df[~df['Code AIOT'].isin(dg['Code AIOT'])]['Code AIOT']

# # Print the unique values in df that are not in dg
# print(values_not_in_dg)



