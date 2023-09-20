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
import plotly.express as px


st.set_option('deprecation.showPyplotGlobalUse', False)

# Chargement du fichier shapefile
gdf = gpd.read_file(r'V:\CONSULTATION\AMENAGEMENT_URBANISME\N_ZONAGES_AMENAGEMENT\AVIS_AE\PROJET\Cas_par_cas_Projet_defrichement.shp')

# Conversion du champ "DATE_AP" en format de date
gdf['DATE_AP'] = pd.to_datetime(gdf['DATE_AP'])

# Création d'une colonne pour extraire l'année
gdf['ANNEE'] = gdf['DATE_AP'].dt.year

gdf['S_DEFRICH'] = gdf['S_DEFRICH'].astype(int)

# Agréger les données par année en calculant la somme de "S_DEFRICH"
donnees_aggregatees = gdf.groupby('ANNEE')['S_DEFRICH'].sum().reset_index()

# Créer un graphique interactif avec Plotly (courbe)


annees_personnalisees = list(range(2014, 2024, 1))

# Création de la liste d'années personnalisée


fig = px.line(donnees_aggregatees, x='ANNEE', y='S_DEFRICH', markers=True)
fig.update_traces(mode='markers+lines', hovertemplate="Année: %{x}<br>Somme: %{y}")
fig.update_layout(xaxis_title="Année", yaxis_title="Somme de S_DEFRICH")

# Définir manuellement les valeurs de l'axe des x (toutes les années)
fig.update_xaxes(tickvals=annees_personnalisees, ticktext=annees_personnalisees)





# Afficher le graphique interactif
st.plotly_chart(fig)






# Créer une application Streamlit
st.title("Évolution de la somme de S_DEFRICH par année et par commune")
# Calculer la somme de S_DEFRICH par commune
somme_defrich_commune = gdf.groupby('LOCALITE')['S_DEFRICH'].sum().reset_index()

# Trier les communes par somme de S_DEFRICH décroissante
somme_defrich_commune = somme_defrich_commune.sort_values(by='S_DEFRICH', ascending=False)

# Sélectionner une commune à partir d'une liste déroulante triée
communes = somme_defrich_commune['LOCALITE'].tolist()

commune_selectionnee = st.selectbox("Sélectionnez une commune", communes)

# Filtrer les données en fonction de la commune sélectionnée
donnees_commune = gdf[gdf['LOCALITE'] == commune_selectionnee]

# Agréger les données par année pour la commune sélectionnée
donnees_aggregatees_commune = donnees_commune.groupby('ANNEE')['S_DEFRICH'].sum().reset_index()

# Créer un graphique interactif avec Plotly (courbe)
fig = px.line(donnees_aggregatees_commune, x='ANNEE', y='S_DEFRICH', markers=True)
fig.update_traces(mode='markers+lines', hovertemplate="Année: %{x}<br>Somme: %{y}")
fig.update_layout(xaxis_title="Année", yaxis_title="Somme de S_DEFRICH")

# Définir manuellement les valeurs de l'axe des x (toutes les années)
fig.update_xaxes(tickvals=annees_personnalisees, ticktext=annees_personnalisees)

# Afficher le graphique interactif
st.plotly_chart(fig)







