import streamlit as st
from streamlit_folium import folium_static
import pandas as pd
import geopandas as gpd
import plotly.express as px



df = gpd.read_file('https://raw.githubusercontent.com/olivierparrot01/GENERAL/main/Avis_Projet_point.geojson')

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

#dict(zip(categories, colors))
category_color_map = {"AGRICULTURE": "orange",    # Proche de jaune#     
    "AMENAGEMENT-CONSTRUCTION": "gray",# Gris foncé
    "AUTORISATION-REGULARISATION-RECONVERSION": "lightgray", # Gris clair
    "CARRIERE": "darkred",                   # Marron foncé
    "DECHETS": "orange",                     # Orange
    "EAU-CAPTAGE-RETENUE-BARRAGE": "darkblue",  # Bleu foncé
    "EOLIENNES": "green",                    # Vert
    "GEOTHERMIE": "lightblue",               # Proche de cyan
    "HYDROELECTRICITE": "blue",              # Bleu
    "LOGISTIQUE": "beige",                   # Gris clair
    "MONTAGNE-LOISIR": "pink",               # Rose
    "PHOTOVOLTAIQUE": "darkgreen",           # Vert foncé
    "PORT-AMENAGEMENT-ACTIVITES": "cadetblue", # Proche de gris
    "RESEAU-ELECTRICITE-GAZ": "lightgray",   # Argent (Gris clair)
    "RISQUES NATURELS-PROTECTION": "red",    # Rouge
    "ROUTE-VOIERIE": "lightgray",            # Gris clair
    "STEP": "purple",                        # Violet clair
    "ZAC": "black",                          # Noir
}


# Filtrage des données
df = df[df['DATE_PUBLI'] >= '2015']
df['DATE_PUBLI'] = pd.to_datetime(df['DATE_PUBLI'])
# Convertir la colonne 'DATE_PUBLI' pour ne garder que la date (année-mois-jour)
# df['DATE_PUBLI'] = pd.to_datetime(df['DATE_PUBLI']).dt.date

# Définir ou extraire la date de mise à jour
#date_mise_a_jour = filtered_df['DATE_PUBLI'].max()  # Par exemple, la dernière date de mise à jour
#date_mise_a_jour_str = date_mise_a_jour.strftime("%Y %B %d") 

# Afficher la date de mise à jour en haut de la page
st.subheader('Mise à jour : 2024-09-30')


# df['DATE_PUBLI'] = pd.to_datetime(df['DATE_PUBLI'])
# Interface Streamlit
#st.header("Analyse Spatio-Temporelle")
st.header("Analyse par Catégorie des Projets MRAe ")

# Sélection des années

# min_year = int(df['DATE_PUBLI'].dt.year.min())
# max_year = int(df['DATE_PUBLI'].dt.year.max())


min_year = df['DATE_PUBLI'].dt.year.min()
max_year = df['DATE_PUBLI'].dt.year.max()






#st.sidebar.subheader("Sélectionner une période :'')
#year_range = st.sidebar.slider("", 
                               #min_value=min_year, 
                               #max_value=max_year, 
                               #value=(min_year, max_year), 
                               #step=1, label_visibility="collapsed")



#filtered_df = df[(df['DATE_PUBLI'].dt.year >= year_range[0]) & (df['DATE_PUBLI'].dt.year <= year_range[1])]














#filtered_df['Année'] = filtered_df['DATE_PUBLI'].dt.year

# Sélection des catégories

# Liste des catégories par défaut
default_categories = ['PHOTOVOLTAIQUE', 'HYDROELECTRICITE','EOLIENNES','GEOTHERMIE']


st.sidebar.subheader("Sélectionner des catégories :")
selected_CATEGORIEs = st.sidebar.multiselect(
    " ", 
    categories, 
    default=default_categories  # Spécifier les catégories par défaut, label_visibility="collapsed"
)

# Filtrer le DataFrame selon les catégories sélectionnées
#filtered_df = filtered_df[filtered_df['CATEGORIE'].isin(selected_CATEGORIEs)]
filtered_df = df[df['CATEGORIE'].isin(selected_CATEGORIEs)]

#st.sidebar.subheader(" ")
st.sidebar.write(" ")
#st.sidebar.write("\n")

st.sidebar.subheader("Sélectionner une période :")
#st.sidebar.subheader(" ", )
st.sidebar.write(" ")
#st.sidebar.write("\n")

year_range = st.sidebar.slider(" ", 
                               min_value=min_year, 
                               max_value=max_year, 
                               value=(min_year, max_year), 
                               step=1, label_visibility="collapsed")



filtered_df = filtered_df[(filtered_df['DATE_PUBLI'].dt.year >= year_range[0]) & (filtered_df['DATE_PUBLI'].dt.year <= year_range[1])]
filtered_df['Année'] = filtered_df['DATE_PUBLI'].dt.year














#st.sidebar.subheader("Sélectionner les catégories :")
#selected_CATEGORIEs = st.sidebar.multiselect("", categories, default=categories)
#filtered_df = filtered_df[filtered_df['CATEGORIE'].isin(selected_CATEGORIEs)]

# Étape 1 : Créer toutes les combinaisons possibles d'années et de catégories
years = sorted(filtered_df['Année'].unique())
categories = selected_CATEGORIEs
all_combinations = pd.MultiIndex.from_product([years, categories], names=['Année', 'CATEGORIE']).to_frame(index=False)

# Étape 2 : Compter les occurrences par année et par catégorie dans le DataFrame filtré
count_by_year_category = filtered_df.groupby(['Année', 'CATEGORIE']).size().reset_index(name='count')

# Étape 3 : Fusionner avec all_combinations pour ajouter les comptes
all_combinations_with_counts = pd.merge(all_combinations, count_by_year_category, on=['Année', 'CATEGORIE'], how='left')
#all_combinations_with_counts['count'].fillna(0, inplace=True)
all_combinations_with_counts['count'] = all_combinations_with_counts['count'].fillna(0)

all_combinations_with_counts['count'] = all_combinations_with_counts['count'].astype(int)


# Extraire les catégories uniques et les trier
sorted_all_combinations_with_counts = sorted(all_combinations_with_counts['CATEGORIE'].unique())

# Réordonner les catégories dans le DataFrame en fonction de cet ordre
all_combinations_with_counts['CATEGORIE'] = pd.Categorical(all_combinations_with_counts['CATEGORIE'], categories=sorted_all_combinations_with_counts, ordered=True)

# Trier le DataFrame selon l'ordre des catégories
all_combinations_with_counts = all_combinations_with_counts.sort_values(by='CATEGORIE')





# Graphique empilé par catégorie et année
st.subheader("Effectifs par catégorie")
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
st.subheader("Localisation à la commune des projets par catégorie")
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
    label="Télécharger les données filtrées au format xlsx",
    data=excel_data,
    file_name="filtered_data.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)






import folium
from folium.plugins import MarkerCluster,Fullscreen
# Assurez-vous que filtered_df est un GeoDataFrame
filtered_df = gpd.GeoDataFrame(filtered_df)

# Reprojection en EPSG:4326 (WGS84)
filtered_df = filtered_df.to_crs(epsg=4326)

# Extraire la latitude et la longitude à partir de la colonne 'geometry'
filtered_df['latitude'] = filtered_df.geometry.y.astype(float)
filtered_df['longitude'] = filtered_df.geometry.x.astype(float)
filtered_df['DATE_PUBLI'] = pd.to_datetime(df['DATE_PUBLI']).dt.date
# Correspondance des catégories avec les couleurs disponibles dans Folium
color_map = {
    "AGRICULTURE": "orange",    # Proche de jaune#     
    "AMENAGEMENT-CONSTRUCTION": "gray",# Gris foncé
    "AUTORISATION-REGULARISATION-RECONVERSION": "lightgray", # Gris clair
    "CARRIERE": "darkred",                   # Marron foncé
    "DECHETS": "orange",                     # Orange
    "EAU-CAPTAGE-RETENUE-BARRAGE": "darkblue",  # Bleu foncé
    "EOLIENNES": "green",                    # Vert
    "GEOTHERMIE": "lightblue",               # Proche de cyan
    "HYDROELECTRICITE": "blue",              # Bleu
    "LOGISTIQUE": "beige",                   # Gris clair
    "MONTAGNE-LOISIR": "pink",               # Rose
    "PHOTOVOLTAIQUE": "darkgreen",           # Vert foncé
    "PORT-AMENAGEMENT-ACTIVITES": "cadetblue", # Proche de gris
    "RESEAU-ELECTRICITE-GAZ": "lightgray",   # Argent (Gris clair)
    "RISQUES NATURELS-PROTECTION": "red",    # Rouge
    "ROUTE-VOIERIE": "lightgray",            # Gris clair
    "STEP": "purple",                        # Violet clair
    "ZAC": "black",                          # Noir
}

# Créer la carte centrée sur le centre des données
#m = folium.Map(location=[filtered_df['latitude'].mean(), filtered_df['longitude'].mean()], zoom_start=5)


# Coordonnées approximatives du centre de la région PACA
latitude_center = 43.5  # Latitude centrale de PACA
longitude_center = 6.5  # Longitude centrale de PACA
# Vérifiez les valeurs moyennes
#mean_latitude = filtered_df['latitude'].mean()
#mean_longitude = filtered_df['longitude'].mean()

# Créer la carte centrée sur le centre des données
m = folium.Map(location=[latitude_center, longitude_center], zoom_start=7)
#m = folium.Map(location=[mean_latitude, mean_longitude], zoom_start=7)


# Ajouter le bouton de plein écran
Fullscreen().add_to(m)
# Ajouter un cluster de points (facultatif)
marker_cluster = MarkerCluster().add_to(m)

# Ajouter les points au cluster avec un style personnalisé selon la catégorie
for idx, row in filtered_df.iterrows():
    category = row['CATEGORIE']
    color = color_map.get(category, "lightblue")  # Par défaut, bleu clair si la catégorie n'est pas trouvée
    
    # Utiliser color pour changer la couleur de l'icône
    folium.Marker(
        location=[row['latitude'], row['longitude']],
        popup= f"{row['CATEGORIE']}<br>{row['DATE_PUBLI']}<br>{row['LOCALITE']}<br>{row['LIEN_AVIS']}",
        #popup=f"{category}<br>{localite}<br>{lien_avis}"
    
        icon=folium.Icon(color=color, icon='info-sign')  # Couleur selon la catégorie
    ).add_to(marker_cluster)

# Afficher la carte dans Streamlit
st.subheader("Géolocalisation des projets par catégorie")
#st.subheader(" ")
#st.write("")


folium_static(m)  # Fonction pour afficher la carte Folium dans Streamlit

