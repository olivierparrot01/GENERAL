# -*- coding: utf-8 -*-
"""
Created on Mon May 22 18:10:52 2023

@author: olivier.parrot
"""
import streamlit as st
import pandas as pd
import geopandas as gpd
import numpy as np
# from simpledbf import Dbf5
import matplotlib.pyplot as plt
import plotly.express as px
# import base64
import requests 



st.title('ICPE sites-multiple')

DATE_COLUMN = 'insee'

# DATA_URL = (r'C:\Users\olivier.parrot\Desktop\cartopas\icpe\icpe_3103\icpe_geocoded_dreal_nondreal.csv')
# dbf = Dbf5(r'C:\Users\olivier.parrot\Desktop\cartopas\icpe\icpe_3103\geoide\carte\2022_GUN_extraction_geocoded.dbf')
# data=dbf.to_dataframe()

# data.to_csv(r'C:\Users\olivier.parrot\Desktop\cartopas\icpe\icpe_3103\geoide\carte\2022_GUN_extraction_geocoded.csv', index=False)

# data["result_c_1"] = data[ "result_c_1"].fillna("")

# data["result_c_1"] = data[ "result_c_1"].fillna(0).astype(int).astype(str)


# data = pd.read_csv(r'C:\Users\olivier.parrot\Desktop\cartopas\icpe\icpe_3103\geoide\carte\2022_GUN_extraction_geocoded.csv')


# data = pd.read_csv('https://github.com/olivierparrot01/ICPE/blob/main/2022_GUN_extraction_geocoded.csv')
data = pd.read_csv('https://raw.githubusercontent.com/olivierparrot01/ICPE/main/2022_GUN_extraction_geocoded.csv')

data = pd.read_csv('https://raw.githubusercontent.com/olivierparrot01/ICPE/main/2022_GUN_extraction_geocoded.csv')
# https://github.com/olivierparrot01/ICPE/blob/main/2022_GUN_extraction_geocoded.csv
# data["result_c_1"] = data["result_c_1"].fillna("").astype(str).str.split(".", expand=True)[0].astype(int)

# data["insee"] = data[ "insee"].astype(str)

# data["result_c_1"] = data[ "result_c_1"].astype(str).fillna("").astype(int)
# data["insee"] = data[ "insee"].astype(str)

data[["Code_AIOT", "Code_posta", "insee", "result_c_1"]] = data[["Code_AIOT", "Code_posta", "insee", "result_c_1"]].fillna(0).astype(int).astype(str)

# 
distinct_count = data["insee"].nunique()
print("Distinct count of 'insee':", distinct_count)
data['nb_points'] = data.groupby(['latitude', 'longitude'])['longitude'].transform('size')
data = data.dropna(subset=['latitude', 'longitude'])

# df1=df.loc[df['nb_points'] > 1]

@st.cache_data
def load_data(nrows):
    # data = pd.read_csv(DATA_URL, nrows=nrows)
    # data=dbf.to_dataframe()
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    # data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data

data_load_state = st.text('Loading data...')
data = load_data(10000)
data_load_state.text("Done!")

# Afficher le bouton de téléchargement si la case est cochée
if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)
    
    import streamlit as st

# Votre code pour charger et prétraiter les données

# Créer le bouton de téléchargement
csv_url = 'https://github.com/olivierparrot01/ICPE/raw/main/2022_GUN_extraction_geocoded.csv'
st.markdown(f'<a href="{csv_url}" download="raw_data.csv">Télécharger les données brutes</a>', unsafe_allow_html=True)



st.subheader('Nombre de site-multiple par commune')
count_by_commune = data['commune_si'].value_counts()
st.bar_chart(count_by_commune)

st.subheader('Filtrer communes par nb de sites-multiple')

st.write("<p style='font-size:30px; color:red'>Sélectionnez un nombre</p>", unsafe_allow_html=True)
# selected_count = st.number_input('', value=int(count_by_commune.min()), min_value=int(count_by_commune.min()), max_value=int(count_by_commune.max()), step=1)
selected_count = st.slider('', int(count_by_commune.min()), int(count_by_commune.max()), step=1, format="%d", key="my-slider")

st.subheader(f"Commune(s) (count = {selected_count})")
filtered_data = data[data['commune_si'].map(count_by_commune) == selected_count]
filtered_count_by_commune = filtered_data['commune_si'].value_counts()
filtered_communes = filtered_count_by_commune.index.tolist()

if len(filtered_communes) > 0:
    communes_text = '\n'.join(filtered_communes)
    # st.markdown(communes_text)
    st.text(communes_text)
else:
    # st.markdown("PAS DE COMMUNES")
    st.markdown("<p style='font-size:18px; color:red'>PAS DE COMMUNES</p>", unsafe_allow_html=True)

if st.checkbox('Show attributes'):
    st.write(filtered_data)

fig = px.scatter_mapbox(data, lat="latitude", lon="longitude", hover_data=["nom_usuel", "code_aiot"],  size=data['nb_points'] / 15, zoom=7)
center_lat = 43.7102  # Approximate latitude center of PACA region
center_lon = 6.2570  # Approximate longitude center of PACA region
fig.update_layout(mapbox_center={"lat": center_lat, "lon": center_lon})


fig.update_traces(marker=dict(color='red'))
# Afficher la figure dans Streamlit

fig.update_layout(mapbox_style="open-street-map")
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
st.plotly_chart(fig)    

insee_list = data['commune_si'].unique().tolist()
insee_to_filter = st.multiselect('Select commune', insee_list)
filtered_data = data[data['commune_si'].isin(insee_to_filter)]

if st.checkbox('Show'):
    st.write(filtered_data)

if len(insee_to_filter) > 0:
    center_lat = filtered_data['latitude'].mean()
    center_lon = filtered_data['longitude'].mean()
else:
    center_lat = 43.2965  # Latitude of Marseille (fallback if no commune is selected)
    center_lon = 5.3698  # Longitude of Marseille (fallback if no commune is selected)

st.subheader('Map of icpe for selected commune')

fig1 = px.scatter_mapbox(filtered_data, lat="latitude", lon="longitude", hover_data=["nom_usuel", "code_aiot"], size='nb_points', zoom=10)
fig1.update_traces(marker=dict(color='red'))

fig1.update_layout(mapbox_style="open-street-map")
fig1.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig1.update_layout(mapbox_center={"lat": center_lat, "lon": center_lon})

st.plotly_chart(fig1)

st.subheader('Map of polygons')
# Load GeoJSON data
data1 = gpd.read_file('https://raw.githubusercontent.com/olivierparrot01/ICPE/main/Avis_Projet_commune.zip')
# data.info()
data1 = data1.to_crs("EPSG:4326")
geojson_data = data1.__geo_interface__
# Créer la carte choroplèthe
fig = px.choropleth_mapbox(data1, geojson=geojson_data, locations=data1.index,
                           color_continuous_scale='Viridis', range_color=(0, 20),                           
                           mapbox_style="open-street-map",
                           hover_data={"PROJET": True, "DATE_PUBLI": True},
                           opacity=0.4,
                           zoom=7, center={"lat": 43.7102, "lon": 6.2570})

# Mettre à jour le style et la mise en page
fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
fig.update_layout(mapbox_center={"lat": data1.geometry.centroid.y.mean(), "lon": data1.geometry.centroid.x.mean()})

# Afficher la figure dans Streamlit
st.plotly_chart(fig)

# Autres éléments interactifs dans la sidebar

# st.sidebar.header("Options")
# selected_project = st.sidebar.selectbox('ICPE sites-multiple', ["Select a project", 'Nombre de site-multiple par commune', 'Map of icpe for selected commune', 'Map of polygons'])
# filtered_data = data1[data1["PROJET"] == selected_project]
# st.sidebar.subheader("Project Details")
# st.sidebar.write("Project Name:", selected_project)
# st.sidebar.write("Number of Polygons:", len(filtered_data))

# Autres éléments du tableau de bord
