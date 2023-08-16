import streamlit as st
import folium
import json
from folium import plugins
import requests
import base64

# URL du GeoJSON
geojson_url = 'https://raw.githubusercontent.com/olivierparrot01/ICPE/main/lines.geojson'

# Charger le contenu du GeoJSON depuis l'URL
lines_geojson_data = requests.get(geojson_url).json()

# Créer une couche GeoJSON pour les lignes
lines_geojson_layer = folium.GeoJson(
    lines_geojson_data,
    name="Lignes entre points",
    style_function=lambda feature: {
        'color': 'black',  # Utilisez la couleur de votre choix
        'opacity': 1,
        'weight': 2  # Épaisseur constante
    },
    tooltip=folium.GeoJsonTooltip(
        fields=["Code_AIOT"],
        aliases=["Code AIOT"],
        style="font-size: 12px; text-align: center;"
    )
)

# Fonction pour ajouter des marqueurs à la carte
def add_markers(data, color):
    for _, row in data.iterrows():
        popup_content = f"Nom usuel : {row['Nom_usuel']}<br>Code AIOT : {row['Code_AIOT_liste']}"
        tooltip_content = f"Nom usuel : {row['Nom_usuel']}<br>Code AIOT : {row['Code_AIOT_liste']}"
        
        folium.CircleMarker(
            location=[row['latitude'], row['longitude']],
            radius=5,
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=1,
            popup=popup_content,
            tooltip=tooltip_content,
        ).add_to(m)

# Fonction pour ajouter des marqueurs à la carte avec effet de clignotement
def add_blinking_markers(data):
    marker_cluster = plugins.MarkerCluster()
    for _, row in data.iterrows():
        tooltip_content = f"Nom usuel : {row['Nom_usuel']}<br>Code AIOT : {row['Code_AIOT_liste']}"
        
        marker = folium.Marker(
            location=[row['latitude'], row['longitude']],
            tooltip=tooltip_content,
            icon=None  # No default icon, to use custom CSS animation
        )
        marker_cluster.add_child(marker)

    m.add_child(marker_cluster)

# Chargement des données
dg = pd.read_csv('https://raw.githubusercontent.com/olivierparrot01/ICPE/main/2geocodage.csv')
df = pd.read_csv('https://raw.githubusercontent.com/olivierparrot01/ICPE/main/0208_gun.csv')

# Conversion des données
dg = dg[dg['Distance'] >= 0]
dg['Distance'] = dg['Distance'].astype(int)
dg['Code_AIOT'] = dg['Code_AIOT'].astype(str)
df['Code_AIOT'] = df['Code_AIOT'].astype(str)
df['Nom_usuel'] = df['Nom_usuel'].astype(str)
df["Code_AIOT_liste"] = df.groupby(["latitude", "longitude"])["Code_AIOT"].transform(lambda x: ", ".join(x))
# ...

# Calcul des coordonnées du centre de la carte
center_lat = (df['latitude'].mean() + dg['latitude'].mean()) / 2
center_lon = (df['longitude'].mean() + dg['longitude'].mean()) / 2

# Création de la carte avec Folium
m = folium.Map(location=[center_lat, center_lon], zoom_start=8, control_scale=True)

# Ajouter les marqueurs pour df (en bleu) et dg (en rouge)
add_markers(df, 'blue')
add_markers(dg, 'red')

# Ajouter les marqueurs clignotants pour df
add_blinking_markers(df)

# Ajouter la couche GeoJSON des lignes à la carte
lines_geojson_layer.add_to(m)

# Afficher la carte dans Streamlit en utilisant folium_static
folium_static(m)


# Afficher les adresses Gun des points sélectionnés

st.markdown("<h2 style='font-size:18px;'>Adresses, coordonnées Gun et liens Google Maps des points sélectionnés : </h2>", unsafe_allow_html=True)

#st.write("Adresses et coordonnées Gun des points sélectionnés :")
for _, row in filtered_data.iterrows():
    st.write(f"- Adresse Gun : {row['Adresse_concat']}, Coordonnées Gun : {row['longitude']}, {row['latitude']}")
    formatted_address = row['Adresse_concat'].replace(' ', '-')
    google_maps_link = f"[Ouvrir dans Google Maps à partir de l'adresse Gun](https://www.google.com/maps/search/?api=1&query={formatted_address})"
    st.markdown(google_maps_link, unsafe_allow_html=True)
    google_maps_link = f"[Ouvrir dans Google Maps à partir des coordonnées Gun](https://www.google.com/maps?q={row['latitude']},{row['longitude']})"
    st.markdown(google_maps_link, unsafe_allow_html=True)









#st.write("Table Gun correspondant à la sélection :")
#st.dataframe(filtered_data)
