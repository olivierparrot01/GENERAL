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

data = data.dropna(subset=['latitude', 'longitude'])

data['nb_points'] = data.groupby(['latitude', 'longitude'])['longitude'].transform('size')

data['groupe'] = data.groupby(['latitude', 'longitude']).ngroup() + 1

# Sélectionner le nombre de points dans la barre latérale

select_nb_points = st.sidebar.selectbox('Select nb_points', data['nb_points'].unique())

# Filtrer les données en fonction du nombre de points sélectionné

filtered_data = data[data['nb_points'] == select_nb_points]

# Obtenir les options possibles pour la colonne 'Commune_si' du sous-ensemble de données filtrées

commune_options = filtered_data['Commune_si'].unique()

# Sélectionner une commune dans la barre latérale

select_commune = st.sidebar.selectbox('Select commune', commune_options)

# Filtrer davantage les données en fonction de la commune sélectionnée

state_data = filtered_data[filtered_data['Commune_si'] == select_commune]

# Afficher la carte des sites ICPE sur la commune sélectionnée

if st.sidebar.checkbox("Show Analysis by State", True, key=2):

    st.markdown("## **State level analysis**")

    st.markdown("### Overall Confirmed, Active, Recovered and " +

                "Deceased cases in %s yet" % (select_commune))

   

    if not st.checkbox('Hide Graph', False, key=3):

        fig = px.scatter_mapbox(state_data, lat="latitude", lon="longitude", hover_data=['Nom_usuel', 'Code_AIOT'], size=filtered_data['nb_points'] / 15, zoom=7)

        center_lat = 43.7102  # Approximate latitude center of PACA region

        center_lon = 6.2570  # Approximate longitude center of PACA region

        fig.update_layout(mapbox_center={"lat": center_lat, "lon": center_lon})

        fig.update_traces(marker=dict(color='red'))

        fig.update_layout(mapbox_style="open-street-map")

        fig.update_layout(margin={"r":0, "t":0, "l":0, "b":0})

        st.plotly_chart(fig)

