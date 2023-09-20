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
gdf = gpd.read_file(r'V:\CONSULTATION\AMENAGEMENT_URBANISME\N_ZONAGES_AMENAGEMENT\AVIS_AE\PROJET\Cas_par_cas_Projet_defrichement.shp')

# Prétraiter les données pour extraire la colonne "DATE_AP" et "S_DEFRICH"
gdf['DATE_AP'] = pd.to_datetime(gdf['DATE_AP'])

# Créer une application Streamlit
st.title("Évolution de S_DEFRICH depuis 2014")

# Créer un graphique interactif avec Seaborn pour toutes les années
plt.figure(figsize=(10, 6))
sns.lineplot(data=gdf, x='DATE_AP', y='S_DEFRICH', estimator=None)
plt.xlabel("Année")
plt.ylabel("S_DEFRICH")
plt.title("Évolution de S_DEFRICH pour toutes les années")
plt.xticks(rotation=45)
st.pyplot()

