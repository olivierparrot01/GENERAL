import geopandas as gpd
import pandas as pd
import streamlit as st
import folium
from streamlit_folium import folium_static
import plotly.express as px


# Charger le GeoDataFrame à partir du fichier shapefile
gdf = gpd.read_file('https://raw.githubusercontent.com/olivierparrot01/ICPE/main/i_83_topage.shp')
st.dataframe(gdf["ID_PCE"])
#st.dataframe(gdf["geometry"])

# Convertir en WGS 84 (EPSG 4326)
gdf= gdf.to_crs(epsg=4326)

gdf= gdf.__geo_interface__
# Maintenant, gdf_wgs84 contient les coordonnées en WGS 84


# Calcul des coordonnées du centre de la carte
center_lat = (df['latitude'].mean() + dg['latitude'].mean()) / 2
center_lon = (df['longitude'].mean() + dg['longitude'].mean()) / 2

# Création de la carte avec Folium
m = folium.Map(location=[center_lat, center_lon], zoom_start=8, control_scale=True)



Créer une couche GeoJSON pour les lignes
lines_geojson_layer = folium.GeoJson(
    gdf,
    name="Lignes entre points",
    style_function=lambda feature: {
        'color': 'black',  # Utilisez la couleur de votre choix
        'opacity': 1,
        'weight': 2  # Épaisseur constante
    },
    tooltip=folium.GeoJsonTooltip(
        fields=[ "ID_PCE"],
        aliases=[ "Distance"],
        style="font-size: 12px; text-align: center;",
        sticky=True,  # Rend l'étiquette collante (reste affichée lors du survol)
        delay=0  # Aucun délai d'affichage
    )
)


lines_geojson_layer.add_to(m)
# Convertir le GeoDataFrame en GeoJSON au format Python (dictionnaire)
#geojson_dict = gdf.to_dict()

# Créer une carte Folium centrée sur la zone d'intérêt
#m = folium.Map(location=[gdf['geometry'].total_bounds[1], gdf['geometry'].total_bounds[0]], zoom_start=10)

# Ajouter le GeoJSON directement à la carte Folium
#folium.GeoJson(geojson_dict, name='GeoJSON Layer').add_to(m)

# Afficher la carte 

folium_static(m)


# # Créer la carte choroplèthe centrée sur les données filtrées
geojson_data = gdf.__geo_interface__
center = {"lat": 43.9333, "lon": 6.0679}  # Coordonnées approximatives du centre de la région PACA
fig = px.choropleth_mapbox(gdf, geojson=geojson_data, locations=gdf.index,

                            color_continuous_scale='Viridis', range_color=(0, 20),

                            mapbox_style="open-street-map",

                           hover_data={"ID_PCE": True, "ID_PCE": True},

                            opacity=0.4,

                            zoom=7, center=center)

# # Afficher la carte

# # Mettre à jour le style et la mise en page

fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

fig.update_layout(mapbox_center={"lat": gdf.geometry.centroid.y.mean(), "lon": gdf.geometry.centroid.x.mean()})

# # Afficher la figure dans Streamlit

st.plotly_chart(fig)





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

c1=c[columns_to_display1].reset_index()
d1=d[columns_to_display1].reset_index()
st.dataframe(c1)
st.dataframe(d1)

    
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
parties_communes = pd.merge(c1,d1,left_index=True, right_index=True, how='inner').reset_index(drop=True)




# Afficher les parties communes
st.write('en commun',parties_communes)
#st.dataframe   ( parties_communes[columns_to_display1])
        
        

