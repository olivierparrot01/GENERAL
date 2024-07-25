# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 16:01:20 2024

@author: olivier.parrot
"""
import streamlit as st
import geopandas as gpd
import pandas as pd
import plotly.express as px

# Charger le fichier Shapefile
shp_file = r"V:\CONSULTATION\AMENAGEMENT_URBANISME\N_ZONAGES_AMENAGEMENT\AVIS_AE\PROJET\Avis_Projet_point.shp"
gdf = gpd.read_file(shp_file)

# Supprimer les lignes contenant des valeurs non valides dans la colonne 'DATE_PUBLI'
gdf = gdf[~gdf['DATE_PUBLI'].str.contains('xxxxxx')]

# Convertir le champ DATE_PUBLI en objet de date
gdf['DATE_PUBLI'] = pd.to_datetime(gdf['DATE_PUBLI'])
# Extraire l'année
gdf['YEAR'] = gdf['DATE_PUBLI'].dt.year

# Filtrer les données à partir de l'année 2015
gdf = gdf[gdf['YEAR'] >= 2015]

# Obtenir toutes les catégories uniques
categories = gdf['CATEGORIE'].unique()

st.sidebar.header("Choisir les années")

# Interface Streamlit
# Interface Streamlit avec les années en ordre inverse
selected_years = st.sidebar.multiselect("", sorted(gdf['YEAR'].unique(), reverse=True))

st.header(f"Répartition des projets par catégorie")
st.header(f"Choisir une (des) année(s) à gauche")

# Filtrer les données par années sélectionnées
for year in selected_years:
    data_year = gdf[gdf['YEAR'] == year]
    
    grouped_data = data_year.groupby('CATEGORIE').size().reset_index(name='COUNT')
    
    total_projects = grouped_data['COUNT'].sum()  # Nombre total de projets pour cette année
    
    # Création du camembert avec Plotly
    fig = px.pie(grouped_data, values='COUNT', names='CATEGORIE', title=f'Répartition des {total_projects} projets par catégorie pour l\'année {year}')
    
    # Afficher uniquement le nombre de projets dans le camembert
    fig.update_traces(text=grouped_data['COUNT'], textposition='inside', insidetextfont=dict(size=16))
    
    # Afficher le camembert
    st.plotly_chart(fig)

    # # Afficher les données correspondant au survol de la souris
    # st.write(data_year)
