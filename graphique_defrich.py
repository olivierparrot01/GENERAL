# -*- coding: utf-8 -*-
"""
Created on Wed Sep 20 14:38:47 2023

@author: olivier.parrot
"""

import streamlit as st
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import seaborn as sns

# Chargement du fichier shapefile
gdf = gpd.read_file('https://raw.githubusercontent.com/olivierparrot01/ICPE/main/Cas_par_cas_Projet_defrichement.shp')


# Conversion du champ "DATE_AP" en format de date
gdf['DATE_AP'] = pd.to_datetime(gdf['DATE_AP'])

# Création d'une colonne pour extraire l'année
gdf['ANNEE'] = gdf['DATE_AP'].dt.year

# Titre de l'application
st.title("Évolution de la surface défrichée")

# Filtrage des données pour les années depuis 2014 jusqu'à aujourd'hui
annees_disponibles = gdf['ANNEE'].unique()

min_value = int(min(annees_disponibles))
max_value = int(max(annees_disponibles))


annees_selectionnees = st.slider("Sélectionnez les années", min_value=min_value, max_value=max_value)

# Filtrage des données par année
gdf_annee = gdf[gdf['ANNEE'] <= annees_selectionnees]

# Affichage de la somme totale de la surface défrichée pour les années sélectionnées
st.write(f"Surface défrichée de 2014 à {annees_selectionnees} : {gdf_annee['S_DEFRICH'].sum()} m²")

# Création d'un graphique d'évolution de la surface défrichée par année
fig1, ax1 = plt.subplots()
sns.lineplot(data=gdf_annee.groupby('ANNEE')['S_DEFRICH'].sum().reset_index(), x='ANNEE', y='S_DEFRICH', ax=ax1)
ax1.set_title("Évolution de la surface défrichée par année")
st.pyplot(fig1)

# Sélection de l'année pour l'analyse par commune
annee_commune = st.slider("Sélectionnez une année pour l'analyse par commune", min_value=min_value, max_value=max_value)

# Filtrage des données par année
gdf_annee_commune = gdf[(gdf['ANNEE'] == annee_commune)]

# Sélection de la commune pour l'analyse par commune
communes_disponibles = gdf_annee_commune['LOCALITE'].unique()
commune_selectionnee = st.selectbox("Sélectionnez une commune", communes_disponibles)

# Filtrage des données par commune
gdf_commune = gdf_annee_commune[gdf_annee_commune['LOCALITE'] == commune_selectionnee]

# Affichage de la somme de la surface défrichée pour l'année et la commune sélectionnées
st.write(f"Surface défrichée en {annee_commune} à {commune_selectionnee} : {gdf_commune['S_DEFRICH'].sum()} m²")


gdf_commune['S_DEFRICH'] = gdf_commune['S_DEFRICH'].astype(int)
# Création d'un graphique d'évolution de la surface défrichée par commune pour l'année sélectionnée
fig2, ax2 = plt.subplots()
sns.barplot(data=gdf_commune, x='LOCALITE', y='S_DEFRICH', ax=ax2)
ax2.set_title(f"Évolution de la surface défrichée par commune en {annee_commune}")
ax2.set_xticklabels(ax2.get_xticklabels(), rotation=45, horizontalalignment='right')
st.pyplot(fig2)
