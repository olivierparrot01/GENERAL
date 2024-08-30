# -*- coding: utf-8 -*-
"""
Created on Wed Aug 28 17:55:20 2024

@author: olivier.parrot
"""



import streamlit as st
import pandas as pd
import plotly.express as px
from simpledbf import Dbf5

# Charger les données à partir du fichier DBF
dbf = Dbf5(r'V:\CONSULTATION\AMENAGEMENT_URBANISME\N_ZONAGES_AMENAGEMENT\AVIS_AE\PROJET\Avis_Projet_point.dbf')
df = dbf.to_dataframe()
df = df.drop_duplicates(subset='id')
# Tri des catégories et définition des couleurs
categories = sorted(df['CATEGORIE'].unique())
colors = [
    "#FFFF00",  # blue
    "#626262",  # orange
    "#E6E6E6",  # green
    "#804040",  # red
    "#FF8000",  # purple
    "#0000FF",  # brown
    "#00FF40",  # pink
    "#21CCD0",  # gray
    "#0000FF",  # yellow
    "#B2B2B2",  # cyan
    "#FF82FF",  # light blue
    "#009B00",  # light orange
    "#828282",  # light orange
    "#C0C0C0",  # light green
    "#FF0000",  # light red risque
    "#CFCFCF",  # light purple route
    "#9595FF",  # light brown
    "#000000",  # light pink
    
]
category_color_map = dict(zip(categories, colors))

# Filtrage des données
df = df[df['DATE_PUBLI'] >= '2015']
df['DATE_PUBLI'] = pd.to_datetime(df['DATE_PUBLI'])

# Interface Streamlit
st.header("Analyse Spatio-Temporelle")

# Sélection des années
min_year = int(df['DATE_PUBLI'].dt.year.min())
max_year = int(df['DATE_PUBLI'].dt.year.max())

st.sidebar.subheader("Sélectionner une période :")
year_range = st.sidebar.slider("", 
                               min_value=min_year, 
                               max_value=max_year, 
                               value=(min_year, max_year), 
                               step=1)

filtered_df = df[(df['DATE_PUBLI'].dt.year >= year_range[0]) & (df['DATE_PUBLI'].dt.year <= year_range[1])]
filtered_df['Année'] = filtered_df['DATE_PUBLI'].dt.year

# Sélection des catégories
st.sidebar.subheader("Sélectionner les catégories :")
selected_CATEGORIEs = st.sidebar.multiselect("", categories, default=categories)
filtered_df = filtered_df[filtered_df['CATEGORIE'].isin(selected_CATEGORIEs)]

# Étape 1 : Créer toutes les combinaisons possibles d'années et de catégories
years = sorted(filtered_df['Année'].unique())
categories = selected_CATEGORIEs
all_combinations = pd.MultiIndex.from_product([years, categories], names=['Année', 'CATEGORIE']).to_frame(index=False)

# Étape 2 : Compter les occurrences par année et par catégorie dans le DataFrame filtré
count_by_year_category = filtered_df.groupby(['Année', 'CATEGORIE']).size().reset_index(name='count')

# Étape 3 : Fusionner avec all_combinations pour ajouter les comptes
all_combinations_with_counts = pd.merge(all_combinations, count_by_year_category, on=['Année', 'CATEGORIE'], how='left')
all_combinations_with_counts['count'].fillna(0, inplace=True)
all_combinations_with_counts['count'] = all_combinations_with_counts['count'].astype(int)


# Extraire les catégories uniques et les trier
sorted_all_combinations_with_counts = sorted(all_combinations_with_counts['CATEGORIE'].unique())

# Réordonner les catégories dans le DataFrame en fonction de cet ordre
all_combinations_with_counts['CATEGORIE'] = pd.Categorical(all_combinations_with_counts['CATEGORIE'], categories=sorted_all_combinations_with_counts, ordered=True)

# Trier le DataFrame selon l'ordre des catégories
all_combinations_with_counts = all_combinations_with_counts.sort_values(by='CATEGORIE')





# Graphique empilé par catégorie et année
st.subheader("Effectif par catégorie et par année")
stacked_bar_chart = px.bar(
    all_combinations_with_counts, 
    x='Année', 
    y='count', 
    color='CATEGORIE',
    color_discrete_map=category_color_map,  
    barmode='stack', 
    labels={'count': 'Nb de projets', 'Année': 'Année', 'CATEGORIE': 'Catégorie'}
)
stacked_bar_chart.update_layout(
    xaxis=dict(
        tickmode='linear',
        tick0=min_year,
        dtick=1
    )
)
st.plotly_chart(stacked_bar_chart)

# Graphique par localité
st.subheader("Répartition des projets par localité et catégorie")
locality_category_counts = filtered_df.groupby(['LOCALITE', 'CATEGORIE']).size().reset_index(name='Nb de projets')
locality_category_counts['LOCALITE'] = locality_category_counts['LOCALITE'].replace({'PORTS MARITIMES DE LA METROPOLE AIX-MARSEILLE PROVENCE, DU CG 13 ET DES COMMUNES DE CARRY-LE-ROUET, MARSEILLE ET SAINT-CHAMAS': 'PORTS MARITIMES DE LA METROPOLE AIX-MARSEILLE PROVENCE, DU CG 13'})


# Extraire les catégories uniques et les trier
sorted_categories = sorted(locality_category_counts['CATEGORIE'].unique())

# Réordonner les catégories dans le DataFrame en fonction de cet ordre
locality_category_counts['CATEGORIE'] = pd.Categorical(locality_category_counts['CATEGORIE'], categories=sorted_categories, ordered=True)

# Trier le DataFrame selon l'ordre des catégories
locality_category_counts = locality_category_counts.sort_values(by='CATEGORIE')




# Créer le graphique par localité avec des couleurs spécifiques pour chaque catégorie sélectionnée
LOCALITE_chart = px.bar(
    locality_category_counts,
    x='LOCALITE',
    y='Nb de projets',
    color='CATEGORIE',
    color_discrete_map=category_color_map
)



LOCALITE_chart.update_layout(
    xaxis=dict(tickfont=dict(size=8)) )# Ajuster la taille des étiquettes de l'axe x


st.plotly_chart(LOCALITE_chart)



from io import BytesIO

# Supposons que `filtered_df` soit votre DataFrame filtré.

# Fonction pour convertir le DataFrame en fichier Excel
def convert_df_to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Données filtrées')
    processed_data = output.getvalue()
    return processed_data

# Convertir le DataFrame filtré en Excel
excel_data = convert_df_to_excel(filtered_df)

# Ajouter un bouton de téléchargement pour les données en format XLSX
st.download_button(
    label="Télécharger les données filtrées au format XLSX",
    data=excel_data,
    file_name="filtered_data.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)
