import geopandas as gpd
import pandas as pd
import streamlit as st


# Charger le GeoDataFrame à partir du fichier shapefile
gdf = gpd.read_file('https://raw.githubusercontent.com/olivierparrot01/ICPE/main/i.shp')

# Convertir le type de la colonne 'ID_PCE' en entier
#gdf['ID_PCE'] = gdf['ID_PCE'].astype(int)

# Filtrer les lignes pour le département 83
gdf_filtered = gdf.loc[gdf['DEPT'] == '83']

# Grouper les lignes par géométrie et concaténer les 'ID_PCE' dans une liste

grouped = gdf_filtered.groupby('geometry')['ID_PCE'].apply(list).reset_index()

# Filtrer les groupes avec plus d'un ID_PCE
grouped_filtered = grouped[grouped['ID_PCE'].apply(len) > 1]

# Convertir la liste d'ID_PCE en tuple


grouped_filtered['ID_PCE'] = grouped_filtered['ID_PCE'].apply(tuple)
columns_to_display = [col for col in grouped_filtered.columns if col != 'geometry']

# Sélectionner toutes les colonnes sauf 'geometry'
columns_to_display1 = [col for col in gdf.columns if col != 'geometry']

# Afficher le DataFrame sans la colonne 'geometry'
st.dataframe(grouped_filtered[columns_to_display])







# Comparer les paires d'ID_PCE dans grouped_filtered
for id_pair in grouped_filtered['ID_PCE']:
    int_1, int_2 = id_pair
    df_int_1 = gdf[gdf['ID_PCE'] == int_1]
    df_int_2 = gdf[gdf['ID_PCE'] == int_2]

    # Exclure la colonne 'ID_PCE' de la comparaison
    #df_int_1 = df_int_1.drop(columns=['ID_PCE'])
    #df_int_2 = df_int_2.drop(columns=['ID_PCE'])



     # Concaténer df_int_1 et df_int_2 en les passant en tant que liste
    c = pd.concat([df_int_1, df_int_2])

   
st.dataframe(c[columns_to_display1])
    
    # Comparer les DataFrames et afficher les différences colonne par colonne
    #differences = df_int_1.compare(df_int_2)

    #if differences.empty:
       # print(f"Les ID_PCE {int_1} et {int_2} ont toutes les colonnes (sauf 'ID_PCE') égales.")
   # else:
     #   print(f"Différences entre les ID_PCE {int_1} et {int_2} :")
      #  print(differences)
