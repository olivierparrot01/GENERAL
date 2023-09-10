import geopandas as gpd
import folium
from streamlit_folium import folium_static
import streamlit as st


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

# Charger les GeoDataFrames à partir des fichiers shapefile
gdf = gpd.read_file('https://raw.githubusercontent.com/olivierparrot01/ICPE/main/i_83_topage.shp')
gdf1 = gpd.read_file('https://raw.githubusercontent.com/olivierparrot01/ICPE/main/i_83.shp')

# Convertir en WGS 84 (EPSG 4326)
gdf = gdf.to_crs(epsg=4326)
gdf1 = gdf1.to_crs(epsg=4326)

# Créer une carte Folium
map = folium.Map(location=[44, 7], zoom_start=8, control_scale=True)

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

# Afficher la carte Folium
folium_static(map)



# Liste des colonnes de 25 à 59
columns_25_to_59 = gdf.columns[39:58]

# Sélection de la colonne
selected_column = st.selectbox("Sélectionnez une colonne (25-59)", columns_25_to_59)

filtered_gdf = gdf[gdf[selected_column] == 1],



st.dataframe(filteted_gdf)
# Afficher la carte Folium en fonction de la sélection de l'utilisateur
if selected_column:
    # Créer une couche GeoJSON en utilisant la colonne sélectionnée
    geojson_layer = folium.GeoJson(
    filtered_gdf,
        name="Données sélectionnées",
        style_function=lambda feature: {
            'color': 'blue',  # Utilisez la couleur de votre choix
            'opacity': 1,
            'weight': 2
        },
        tooltip=folium.GeoJsonTooltip(
            fields=[selected_column],
            aliases=[selected_column],
            style="font-size: 12px; text-align: center;",
            sticky=True,
            delay=0
        )
    )
    geojson_layer.add_to(map)

# Afficher la carte Folium
#folium_static(map)

