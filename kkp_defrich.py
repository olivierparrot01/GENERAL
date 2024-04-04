# -*- coding: utf-8 -*-
"""
Created on Wed Sep 20 14:38:47 2023

@author: olivier.parrot
"""
import streamlit as st
import pandas as pd
import geopandas as gpd
import plotly.express as px
import re
import plotly.graph_objs as go

st.set_option('deprecation.showPyplotGlobalUse', False)

# Chargement du fichier shapefile
# gdf = gpd.read_file('https://raw.githubusercontent.com/olivierparrot01/ICPE/main/Cas_par_cas_Projet_defrichement.shp')

gdf = gpd.read_file('https://raw.githubusercontent.com/olivierparrot01/GENERAL/main/Cas_par_cas_Projet_defrichement.geojson')

# gdf = gpd.read_file(r'V:\CONSULTATION\AMENAGEMENT_URBANISME\N_ZONAGES_AMENAGEMENT\AVIS_AE\PROJET\Cas_par_cas_Projet_defrichement.shp')

# gdf = gpd.read_file('https://raw.githubusercontent.com/olivierparrot01/ICPE/main/Cas_par_cas_Projet_defrichement.shp')



# Agréger les données par année en calculant la somme de "S_DEFRICH"
donnees_aggregatees = gdf.groupby('ANNEE')['S_DEFRICH'].sum().reset_index()


# Création de la liste d'années personnalisée
annees_personnalisees = list(range(2014, 2024, 1))

st.write("\n")
st.header("Évolution du défrichement régional")


# Créer un modèle de survol personnalisé
hovertemplate = "Année : %{x}<br>Total : %{y}"

fig = px.line(donnees_aggregatees, x='ANNEE', y='S_DEFRICH', markers=True)
fig.update_traces(mode='markers+lines', hovertemplate=hovertemplate)

# Remplacer les valeurs dans la colonne "CATEGORIE"
gdf['CATEGORIE'] = gdf['CATEGORIE'].replace('AGRICULTURE HORS VIGNE', 'AGRICULTURE HORS VIGNE (oliveraies, vergers ...)')



# Définir une palette de couleurs personnalisée pour chaque catégorie
couleurs_categories = {
    'VIGNE': 'lightgreen',
    'AGRICULTURE HORS VIGNE (oliveraies, vergers ...)': 'green',
    'AMENAGEMENT-CONSTRUCTION': 'gray'
}





# Ajouter les données personnalisées (total par catégorie) à chaque point de données
for categorie, couleur in couleurs_categories.items():
    donnees_categorie = gdf[gdf['CATEGORIE'] == categorie].groupby('ANNEE')['S_DEFRICH'].sum().reset_index()
    fig.add_trace(go.Scatter(x=donnees_categorie['ANNEE'], y=donnees_categorie['S_DEFRICH'],
                              mode='markers',
                              text=[f"{val} m2" for val in donnees_categorie['S_DEFRICH']],
                              hovertemplate="Année : %{x}<br>%{text}",
                              name=categorie, 
                              # name="",  # Laissez le nom vide pour enlever les numéros de trace
                              marker_color=couleur,
                              showlegend=True))  # Utiliser la couleur définie pour la catégorie







fig.update_layout(xaxis_title="Année", yaxis_title="Défrichement total en m2")

# Définir manuellement les valeurs de l'axe des x (toutes les années)
fig.update_xaxes(tickvals=annees_personnalisees, ticktext=annees_personnalisees)



# Afficher le graphique interactif
st.plotly_chart(fig)







# Agréger les données par année et par département (utilisant INSEE_DEP)
donnees_aggregatees_depart = gdf.groupby(['ANNEE', 'INSEE_DEP'])['S_DEFRICH'].sum().reset_index()

# Créer une application Streamlit
st.header("Évolution du défrichement par département")
st.write("\n")
# Liste déroulante multisélection pour sélectionner les communes (INSEE_DEP)
st.sidebar.subheader("Comparer des départements (sélection multiple)")
departements_selectionnees = st.sidebar.multiselect("", donnees_aggregatees_depart['INSEE_DEP'].unique())

# Filtrer les données en fonction des communes sélectionnées
donnees_filtrees = donnees_aggregatees_depart[donnees_aggregatees_depart['INSEE_DEP'].isin(departements_selectionnees)]

# Créer un graphique interactif avec Plotly (courbe)
fig = px.line(donnees_filtrees, x='ANNEE', y='S_DEFRICH', color='INSEE_DEP', markers=True)
fig.update_traces(mode='markers+lines', hovertemplate="Année : %{x}<br>Total : %{y}")
fig.update_layout(xaxis_title="Année", yaxis_title="Défrichement total en m2",legend_title_text='DÉPARTEMENT')
# Renommer l'axe des couleurs (légende)
#fig.update_layout(legend_title_text='DÉPARTEMENT')
fig.update_xaxes(tickvals=annees_personnalisees, ticktext=annees_personnalisees)
# Afficher le graphique interactif
st.plotly_chart(fig)
































