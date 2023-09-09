import geopandas as gpd
import folium

# Charger le GeoDataFrame à partir du fichier shapefile
gdf = gpd.read_file('nom_du_fichier_shapefile.shp')

# Créer une carte Folium
m = folium.Map(location=[48.8566, 2.3522], zoom_start=12)

# Définir la fonction de style
style_function = lambda feature: {
    'color': 'black',
    'opacity': 1,
    'weight': 2
}

# Ajouter les fonctionnalités GeoJSON avec popups personnalisés
for _, row in gdf.iterrows():
    feature = {
        'type': 'Feature',
        'geometry': row['geometry'],
        'properties': {
            'popup': f"Nom usuel : {row['Nom_usuel']}<br>Code AIOT : {row['Code_AIOT_liste']}<br>Secteur : {row['Secteur']}"
        }
    }
    folium.GeoJson(
        feature,
        style_function=style_function,
        tooltip=row['TOPO_PCE']
    ).add_to(m)

# Afficher la carte Folium
m.save('ma_carte.html')  # Enregistrez la carte au format HTML
