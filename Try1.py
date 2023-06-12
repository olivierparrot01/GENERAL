# -*- coding: utf-8 -*-
"""
Created on Fri May 26 15:04:41 2023

@author: olivier.parrot
"""


import streamlit as st
import pandas as pd
import geopandas as gpd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px

st.title('ICPE sites-multiple')

def load_data():
    data = pd.read_csv('https://raw.githubusercontent.com/olivierparrot01/ICPE/main/2022_GUN_extraction_geocoded.csv')
    return data

data = load_data()
data[["Code_AIOT", "Code_posta", "insee", "result_c_1"]] = data[["Code_AIOT", "Code_posta", "insee", "result_c_1"]].fillna(0).astype(int).astype(str)
data = data.dropna(subset=['latitude', 'longitude'])

data['nb_points'] = data.groupby(['latitude', 'longitude'])['longitude'].transform('size')
data['groupe'] = data.groupby(['latitude', 'longitude']).ngroup() + 1


st.sidebar.markdown("<span style='font-size: 14pt;'>Select ICPE groupées par :</span>", unsafe_allow_html=True)

# Sélectionner le nombre de points dans la barre latérale
# select_nb_points = st.sidebar.selectbox("Select ICPE groupées par :", data['nb_points'].unique())
select_nb_points = st.sidebar.selectbox('', data['nb_points'].unique())




# select_nb_points = st.sidebar.selectbox(
#     "<span style='font-size: 14pt;'>Select nb d'ICPE groupées</span>",
#     data['nb_points'].unique(),
#     format_func=lambda x: )

# select_nb_points = st.sidebar.selectbox( data['nb_points'].unique())
# st.sidebar.markdown(f"<span style='font-size: 14pt;'g</span>", unsafe_allow_html=True)

# 
# Filtrer les données en fonction du nombre de points sélectionné
filtered_data = data[data['nb_points'] == select_nb_points]

commune_count = filtered_data['Commune_si'].nunique()



# st.sidebar.write(f"Résultat {commune_count} communes")
# st.sidebar.markdown(f"<span style='font-size: 14pt;'>Résultat : {commune_count} communes</span>", unsafe_allow_html=True)
# st.sidebar.markdown(f"<span style='font-size: 14pt;'>Liste de ces communes :</span>", unsafe_allow_html=True)

# st.sidebar.markdown("<span style='font-size: 14pt;'>Liste de ces communes :</span>", unsafe_allow_html=True)
# Obtenir les options possibles pour la colonne 'Commune_si' du sous-ensemble de données filtrées

# st.sidebar.write(f"Résultat : {commune_count} communes")
st.sidebar.markdown(f"<span style='font-size: 14pt;'>Résultat : {commune_count} communes</span>", unsafe_allow_html=True)
st.sidebar.markdown("<span style='font-size: 14pt;'>Liste de ces communes :</span>", unsafe_allow_html=True)








commune_options = filtered_data['Commune_si'].unique()




# Sélectionner une commune dans la barre latérale
select_commune = st.sidebar.selectbox('', commune_options)
# st.sidebar.markdown(f"<span style='font-size: 14pt;'>Liste de ces communes : {commune_options}", unsafe_allow_html=True)
# st.write(f"Il y a {len(filtered_data)} communes")

# Filtrer davantage les données en fonction de la commune sélectionnée
filtered_data1 = filtered_data[filtered_data['Commune_si'] == select_commune]
group_counts = filtered_data1 ['groupe'].nunique()
# st.sidebar.write(f"Nombre de groupes : {group_counts}", font_size=18)
st.sidebar.markdown(f"<span style='font-size: 14pt;'>{group_counts} site(s) distinct(s) compt(ent) {select_nb_points} ICPE pour {select_commune}</span>", unsafe_allow_html=True)


# Afficher la carte des sites ICPE sur la commune sélectionnée
if st.sidebar.checkbox("Show data", True, key=1):
    # st.markdown("## **State level analysis**")
    st.markdown("### ICPE sur site-multiple à " +" %s"% (select_commune))
    # st.sidebar.markdown(f"<span style='font-size: 16pt;'>Nombre de sites comptant {select_nb_points} ICPE pour {select_commune}</span>", unsafe_allow_html=True)
    
    st.write(select_commune)
    # if not st.checkbox('Hide Graph', False, key=3):
    fig = px.scatter_mapbox(filtered_data1, lat="latitude", lon="longitude", hover_data=['Nom_usuel', 'Code_AIOT'], size=filtered_data1['nb_points'] / 15, zoom=7)
    center_lat = 43.7102  # Approximate latitude center of PACA region
    center_lon = 6.2570  # Approximate longitude center of PACA region
    fig.update_layout(mapbox_center={"lat": center_lat, "lon": center_lon})
    fig.update_traces(marker=dict(color='red'))
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r":0, "t":0, "l":0, "b":0})
    st.plotly_chart(fig)
