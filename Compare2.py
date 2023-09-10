import geopandas as gpd
import folium
from streamlit_folium import folium_static

# Charger le GeoDataFrame à partir du fichier shapefile
#gdf = gpd.read_file('nom_du_fichier_shapefile.shp')
gdf = gpd.read_file('https://raw.githubusercontent.com/olivierparrot01/ICPE/main/i_83_topage.shp')
gdf1 = gpd.read_file('https://raw.githubusercontent.com/olivierparrot01/ICPE/main/i_83.shp')

# Convertir en WGS 84 (EP SG 4326)
gdf= gdf.to_crs(epsg=4326)
gdf1=gdf1.to_crs(epsg=4326)
gdf= gdf.__geo_interface__
gdf1= gdf1.__geo_interface__


# Créer une carte Folium

m = folium.Map(location=[44,7], zoom_start=8, control_scale=True)


#Créer une couche GeoJSON pour les lignes
lines_geojson_layer = folium.GeoJson(
    gdf,
    name="Lignes entre points",
    style_function=lambda feature: {
        'color': 'black',  # Utilisez la couleur de votre choix
        'opacity': 1,
        'weight': 2  # Épaisseur constante
    },
    tooltip=folium.GeoJsonTooltip(
        fields=[ "ID_PCE","TOPO_PCE"],
        aliases=[ "ID_PCE","TOPO_PCE"],
        style="font-size: 12px; text-align: center;",
        sticky=True,  # Rend l'étiquette collante (reste affichée lors du survol)
        delay=0  # Aucun délai d'affichage
    )
)
lines_geojson_layer.add_to(m)


lines_geojson_layer1 = folium.GeoJson(
    gdf1,
    name="Lignes entre points",
    style_function=lambda feature: {
        'color': 'red',  # Utilisez la couleur de votre choix
        'opacity': 0.6,
        'weight': 2  # Épaisseur constante
    },
    tooltip=folium.GeoJsonTooltip(
        fields=[ "ID_PCE","TOPO_PCE"],
        aliases=[ "ID_PCE","TOPO_PCE"],
        style="font-size: 12px; text-align: center;",
        sticky=True,  # Rend l'étiquette collante (reste affichée lors du survol)
        delay=0  # Aucun délai d'affichage
    )
)
lines_geojson_layer1.add_to(m)


# URL de l'orthophoto IGN à utiliser comme couche de tuile
orthophoto_url = "https://wxs.ign.fr/choisirgeoportail/geoportail/wmts?" \
                 "SERVICE=WMTS&REQUEST=GetTile&VERSION=1.0.0&LAYER=ORTHOIMAGERY.ORTHOPHOTOS&TILEMATRIXSET=PM&" \
                 "FORMAT=image/jpeg&TILECOL={x}&TILEROW={y}&TILEMATRIX={z}&" \
                 "STYLE=normal"

# Ajout de la couche de tuile de l'orthophoto IGN uniquement aux niveaux de zoom 13 
for zoom_level in range(13, 19):
    folium.TileLayer(
        tiles=orthophoto_url,
        attr="IGN France",
        name=f"Orthophoto IGN (Zoom {zoom_level})",
        overlay=True,
        min_zoom=zoom_level,
        max_zoom=zoom_level,
    ).add_to(m)

# Add a LatLngPopup to the map
#popup = folium.LatLngPopup()
#m.add_child(popup)
folium_static(m)
