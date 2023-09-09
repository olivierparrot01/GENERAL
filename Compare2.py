import geopandas as gpd
import folium
from streamlit_folium import folium_static

# Charger le GeoDataFrame à partir du fichier shapefile
#gdf = gpd.read_file('nom_du_fichier_shapefile.shp')
gdf = gpd.read_file('https://raw.githubusercontent.com/olivierparrot01/ICPE/main/i_83_topage.shp')


# Convertir en WGS 84 (EPSG 4326)
gdf= gdf.to_crs(epsg=4326)

gdf= gdf.__geo_interface__
# Maintenant, gdf_wgs84 contient les coordonnées en WGS 84



# Créer une carte Folium
m = folium.Map(location=[48.8566, 2.3522], zoom_s




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
folium_static(m)
