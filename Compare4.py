import geopandas as gpd
import pandas as pd
import folium
from streamlit_folium import folium_static
import streamlit as st
from folium import LayerControl, plugins

# Charger les GeoDataFrames à partir des fichiers shapefile
def load_and_convert(file_url):
    gdf = gpd.read_file(file_url)
    return gdf.to_crs(epsg=4326)

gdf = load_and_convert('https://raw.githubusercontent.com/olivierparrot01/ICPE/main/i_83_topage.shp')
gdf1 = load_and_convert('https://raw.githubusercontent.com/olivierparrot01/ICPE/main/i_83.shp')

# Créer une carte Folium
map = folium.Map(location=[43, 7], zoom_start=8, control_scale=True)

# Fonction pour créer une couche GeoJSON
def create_geojson_layer(data, color, name):
    return folium.GeoJson(
        data,
        name=name,
        style_function=lambda feature: {
            'color': color,
            'opacity': 0.6,
            'weight': 2
        },
        tooltip=folium.GeoJsonTooltip(
            fields=["ID_PCE", "TOPO_PCE"],
            aliases=["ID_PCE", "TOPO_PCE"],
            style="font-size: 12px; text-align: center;",
            sticky=True,
            delay=0
        )
    )

# Ajouter les couches GeoJSON aux deux GeoDataFrames
lines_geojson_layer = create_geojson_layer(gdf, 'black', 'Lignes entre points')
lines_geojson_layer1 = create_geojson_layer(gdf1, 'red', 'Lignes entre points')
lines_geojson_layer1.add_to(map)
lines_geojson_layer.add_to(map)

# URL de l'orthophoto IGN
orthophoto_url = "https://wxs.ign.fr/choisirgeoportail/geoportail/wmts?" \
                 "SERVICE=WMTS&REQUEST=GetTile&VERSION=1.0.0&LAYER=ORTHOIMAGERY.ORTHOPHOTOS&TILEMATRIXSET=PM&" \
                 "FORMAT=image/jpeg&TILECOL={x}&TILEROW={y}&TILEMATRIX={z}&" \
                 "STYLE=normal"

# Ajout de la couche de tuile de l'orthophoto IGN aux niveaux de zoom 13 à 18
for zoom_level in range(13, 19):
    folium.TileLayer(
        tiles=orthophoto_url,
        attr="IGN France",
        name=f"Orthophoto IGN (Zoom {zoom_level})",
        overlay=True,
        min_zoom=zoom_level,
        max_zoom=zoom_level,
    ).add_to(map)

# Liste des colonnes de 25 à 59
columns_25_to_59 = gdf.columns[39:59]

# Créer un DataFrame vide
#selected_column= None

selected_column= st.selectbox("Sélectionnez une colonne (25-59)", [""]+list(columns_25_to_59))

filtered_gdf = gdf[gdf[selected_column] == 1].copy()  # Copiez les données filtrées pour éviter les problèmes de vue

# Exclure la colonne 'geometry'
filtered_gdf1 = filtered_gdf.drop(columns='geometry')

# Créer une couche GeoJSON en utilisant la colonne sélectionnée
if not filtered_gdf.empty:
    geojson_layer = create_geojson_layer(filtered_gdf, 'blue', 'Données sélectionnées')
    geojson_layer.add_to(map)
    plugins.MousePosition().add_to(map)

# Ajouter la couche de contrôle pour activer/désactiver les couches
LayerControl().add_to(map)

# Afficher la carte Folium
folium_static(map)
