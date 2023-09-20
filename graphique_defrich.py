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

# Charger les données à partir du GeoDataFrame
gdf = gpd.read_file('https://raw.githubusercontent.com/olivierparrot01/ICPE/main/Cas_par_cas_Projet_defrichement.shp')

# Prétraiter les données pour extraire la colonne "DATE_AP" et "S_DEFRICH"
gdf['DATE_AP'] = pd.to_datetime(gdf['DATE_AP'])
gdf['Année'] = gdf['DATE_AP'].dt.year

# Agréger les données par année en calculant la somme de "S_DEFRICH"
donnees_aggregatees = gdf.groupby('Année')['S_DEFRICH'].sum().reset_index()

# Créer une application Streamlit
st.title("Évolution de la somme de S_DEFRICH par année")

# Créer un graphique interactif avec Seaborn (courbe)
plt.figure(figsize=(10, 6))
sns.lineplot(data=donnees_aggregatees, x='Année', y='S_DEFRICH', marker='o')
plt.xlabel("Année")
plt.ylabel("Somme de S_DEFRICH")
plt.title("Somme de S_DEFRICH par année")
plt.xticks(rotation=45)
st.pyplot()
Ce code utilise sns.lineplot de Seaborn pour créer une courbe montrant l'évolution de la somme de "S_DEFRICH" par année. Vous pouvez exécuter votre application Streamlit avec streamlit run nom_de_votre_script.py pour visualiser la courbe interactive.






