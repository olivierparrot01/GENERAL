import streamlit as st
import geopandas as gpd
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


# Charger le fichier Shapefile
#shp_file = r"V:\CONSULTATION\AMENAGEMENT_URBANISME\N_ZONAGES_AMENAGEMENT\AVIS_AE\PROJET\Avis_Projet_point.shp"
#gdf = gpd.read_file(r"V:\CONSULTATION\AMENAGEMENT_URBANISME\N_ZONAGES_AMENAGEMENT\AVIS_AE\PROJET\Avis_Projet_point.shp")
gdf = gpd.read_file('https://raw.githubusercontent.com/olivierparrot01/GENERAL/main/Avis_Projet_point.geojson')

# Supprimer les lignes contenant des valeurs non valides dans la colonne 'DATE_PUBLI'
#gdf = gdf[~gdf['DATE_PUBLI'].str.contains('xxxxxx')]
# Remplacer les valeurs incorrectes par NaT
gdf['DATE_PUBLI'] = gdf['DATE_PUBLI'].replace('0000-00-00', pd.NaT)
# Convertir le champ DATE_PUBLI en objet de date
gdf['DATE_PUBLI'] = pd.to_datetime(gdf['DATE_PUBLI'])
# Extraire l'année
gdf['YEAR'] = gdf['DATE_PUBLI'].dt.year

# Filtrer les données à partir de l'année 2015
gdf = gdf[gdf['YEAR'] >= 2015]
gdf['YEAR'] = gdf['YEAR'].astype(int)
# Obtenir toutes les catégories uniques
categories = gdf['CATEGORIE'].unique()

# Définir une palette de couleurs pour les catégories
colors = [
    "#1f77b4",  # blue
    "#ff7f0e",  # orange
    "#2ca02c",  # green
    "#d62728",  # red
    "#9467bd",  # purple
    "#8c564b",  # brown
    "#e377c2",  # pink
    "#7f7f7f",  # gray
    "#bcbd22",  # yellow
    "#17becf",  # cyan
    "#aec7e8",  # light blue
    "#ffbb78",  # light orange
    "#98df8a",  # light green
    "#ff9896",  # light red
    "#c5b0d5",  # light purple
    "#c49c94",  # light brown
    "#f7b6d2",  # light pink
    "#c7c7c7"   # light gray
]

# Mapper les catégories aux couleurs
category_color_map = dict(zip(categories, colors))

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
    #fig = px.pie(grouped_data, values='COUNT', names='CATEGORIE', title=f'Répartition des projets par catégorie pour l\'année {year}', color=grouped_data['CATEGORIE'], color_map=category_color_map)

    #fig = px.pie(grouped_data, values='COUNT', names='CATEGORIE', title=f'Répartition des projets par catégorie pour l\'année {year}', color=categories, color_discrete_map=category_colors)

    fig = px.pie(grouped_data, values='COUNT', names='CATEGORIE', title=f'Répartition des {total_projects} projets par catégorie pour l\'année {year}', color='CATEGORIE', hole=0.3)
    #fig = px.pie(grouped_data, values='COUNT', names='CATEGORIE', title=f'Répartition des projets par catégorie pour l\'année {year}', color='CATEGORIE', color_discrete_sequence=colors)
    # Afficher uniquement le nombre de projets dans le camembert
    #fig.update_traces(text=grouped_data['COUNT'], textposition='inside', insidetextfont=dict(size=16))
   
    # Afficher uniquement le nombre de projets dans le camembert
    #fig.update_traces(textinfo='value+percent+label', text=grouped_data['COUNT'], textposition='inside', insidetextfont=dict(size=16), texttemplate='%{value} (%{percent:.0f}%)' ) # Formatage du texte
   
    # Afficher uniquement le nombre de projets dans le camembert
    #fig.update_traces(textinfo='value+percent+label', text=grouped_data['COUNT'], textposition='inside', insidetextfont=dict(size=16))
    fig.update_traces( text=grouped_data['COUNT'], textposition='inside', insidetextfont=dict(size=16))

    # Forcer les pourcentages à être entiers
    fig.update_traces(texttemplate='%{label}<br>%{value} (%{percent:.0%})')

   
    # Afficher le camembert
    st.plotly_chart(fig)








    










    
    if 'zac' in grouped_data['CATEGORIE'].values:
        zac_projects = data_year[data_year['CATEGORIE'] == 'zac']['PROJET'].tolist()
        st.write(f"Projets ZAC : {zac_projects}")
    

