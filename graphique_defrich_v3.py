# -*- coding: utf-8 -*-
"""
Created on Wed Oct  9 16:12:02 2024

@author: olivier.parrot
"""

import streamlit as st
import pandas as pd
import geopandas as gpd
import plotly.express as px
import re
import plotly.graph_objs as go

#st.set_option('deprecation.showPyplotGlobalUse', False)

# Chargement du fichier shapefile
gdf = gpd.read_file('https://raw.githubusercontent.com/olivierparrot01/ICPE/main/Cas_par_cas_Projet_defrichement_2024-10-09.geojson')

# gdf = gpd.read_file(r'V:\CONSULTATION\AMENAGEMENT_URBANISME\N_ZONAGES_AMENAGEMENT\AVIS_AE\PROJET\Cas_par_cas_Projet_defrichement.shp')
gdf = gdf.drop_duplicates(subset='id')


def func(x):
    a = re.findall("VITICOLE|VIGNE|VIGNOBLE", x)
    b = re.findall("AGRICULTURE|AGRICOLE|PATURE|PATURAGE|PASTORAL|PRAIRIE|OLIVERAIE|OLIVIER|OLEICOLE|VERGER|FRUITIER|PLANTATION|PRAIRIE|CULTURE|RECONVERSION DES SOLS", x)   
    if a != []:
        return 'VIGNE'   
    elif b != []:
        return 'AGRICULTURE HORS VIGNE (oliveraies, vergers ...)'
    else:
        return 'AMENAGEMENT-CONSTRUCTION (villas, lotissements ...)'

gdf['CATEGORIE'] = gdf['PROJET'].apply(func)



gdf['S_DEFRICH'] = gdf['S_DEFRICH'].astype(float)

gdf = gdf[gdf['S_DEFRICH'].notna()]
# Sélectionner les lignes où 'LOCALITE' contient une virgule ','
condition = gdf['LOCALITE'].str.contains(',')
gdf.loc[condition, 'LOCALITE'] = gdf.loc[condition, 'LOCALITE'].str.split(',').str[0]



gdf1= pd.read_excel ('https://raw.githubusercontent.com/olivierparrot01/ICPE/main/COMMUNE.ods', dtype='str')

gdf1 = gdf1.loc[~((gdf1['NOM_COMM_M'] == 'ASPREMONT') & (gdf1['INSEE_DEP'] != '06')) & 
               ~((gdf1['NOM_COMM_M'] == 'VITROLLES') & (gdf1['INSEE_DEP'] != '13')) &
               ~((gdf1['NOM_COMM_M'] == 'MIRABEAU') & (gdf1['INSEE_DEP'] != '84')) &
               ~((gdf1['NOM_COMM_M'] == 'ROUSSET') & (gdf1['INSEE_DEP'] != '13'))]

#gdf1= Dbf5('https://raw.githubusercontent.com/olivierparrot01/ICPE/main/COMMUNE.dbf')

# Joindre les GeoDataFrames en utilisant la colonne 'NOM_COM'
gdf = gdf.merge(gdf1[['NOM_COMM_M', 'INSEE_DEP']], left_on='LOCALITE',right_on='NOM_COMM_M', how='left')


gdf = gdf[gdf['INSEE_DEP'].notna()]

gdf = gdf[gdf['EI'] != 'ANNULATION']

# Extraire les deux derniers chiffres de 'ID' et les convertir en entier
gdf['ANNEE'] =2000 +  gdf['id'].str.extract(r'F093(\d{2})').astype(int)

# Remplacer 2013 par 2014 dans la colonne 'ANNEE'
gdf['ANNEE'] = gdf['ANNEE'].replace(2013, 2014)



# Agréger les données par année en calculant la somme de "S_DEFRICH"
donnees_aggregatees = gdf.groupby('ANNEE')['S_DEFRICH'].sum().reset_index()


# Création de la liste d'années personnalisée
annees_personnalisees = list(range(2014, 2025, 1))

st.write("\n")
st.header("Évolution du défrichement régional")
#st.subheader('Mise à jour : 2024-09-30')
st.write("  ")
st.markdown('<p style="font-size:24px; font-weight:bold; color:red;">Mise à jour : 2024-09-25</p>', unsafe_allow_html=True)
#st.subheader('''Synchronisée avec la carte interactive "Avis et décisions de l’autorité environnementale"''')
#st.markdown('<p style="font-size:20px;">Synchronisée avec la carte interactive<br>"Avis et décisions de l’autorité environnementale"</p>', unsafe_allow_html=True)
st.write("  ")
st.markdown('<p style="font-size:20px; font-weight:bold; color:red;">Synchronisée avec la couche Cas_par_cas_Projet_defrichement_2014-2024<br>de la carte interactive "Avis et décisions de l’autorité environnementale"</p>', unsafe_allow_html=True)


# Créer un modèle de survol personnalisé
hovertemplate = "Année : %{x}<br>Total : %{y}"

fig = px.line(donnees_aggregatees, x='ANNEE', y='S_DEFRICH', markers=True)
fig.update_traces(mode='markers+lines', hovertemplate=hovertemplate)


# Définir une palette de couleurs personnalisée pour chaque catégorie
couleurs_categories = {
    'VIGNE': 'lightgreen',
    'AGRICULTURE HORS VIGNE (oliveraies, vergers ...)': 'green',
    'AMENAGEMENT-CONSTRUCTION (villas, lotissements ...)': 'gray'
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
#st.write("\n")

st.write("  ")

# Liste déroulante multisélection pour sélectionner les communes (INSEE_DEP)
st.sidebar.subheader("Comparer des départements")
departements_selectionnees = st.sidebar.multiselect("  ", donnees_aggregatees_depart['INSEE_DEP'].unique())

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
