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






# Créez un DataFrame vide sans colonnes initiales
c= pd.DataFrame()
d= pd.DataFrame()

# Comparer les paires d'ID_PCE dans grouped_filtered
for id_pair in grouped_filtered['ID_PCE']:
    int_1, int_2 = id_pair
    df_int_1 = gdf[gdf['ID_PCE'] == int_1]
    df_int_2 = gdf[gdf['ID_PCE'] == int_2]

    # Exclure la colonne 'ID_PCE' de la comparaison
    #df_int_1 = df_int_1.drop(columns=['ID_PCE'])
    #df_int_2 = df_int_2.drop(columns=['ID_PCE'])



     # Concaténer df_int_1 et df_int_2 en les passant en tant que liste
    c = pd.concat([c,df_int_1])
    d= pd.concat([d,df_int_2])

#d=c.copy()
#d['ID_PCE']='olive'

# Réinitialiser l'index
c= c.reset_index(drop=True)
d=d.reset_index(drop=True)

st.dataframe(c[columns_to_display1])
st.dataframe(d[columns_to_display1])

    
    # Comparer les DataFrames et afficher les différences colonne par colonne

differences = c.compare(d)

#if differences.empty:
       #st.write("toutes les colonnes égales.")
#else:
      #print(f"Différences entre les ID_PCE apppareilles")
  
    
st.write('differences',differences)

# Comparer les deux DataFrames colonne par colonne
#comparaison = df1.compare(df2)

# Afficher les parties communes (valeurs identiques)
#parties_communes = differences[differences['self'].isna() & differences['other'].isna()]


# Effectuer une jointure sur la première colonne des index en utilisant pd.merge
#parties_communes = pd.merge(c,d,left_index=True, right_index=True, how='inner')




# Afficher les parties communes
#st.write('en commun',parties_communes[columns_to_display1])
#st.dataframe   ( parties_communes[columns_to_display1])
        
        

