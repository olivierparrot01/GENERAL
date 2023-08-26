import geopandas as gpd
from shapely.geometry import Point, LineString

# Charger le GeoDataFrame des lignes (gdf_lignes) et des points (gdf_pts)
gdf_lignes = gpd.read_file('https://raw.githubusercontent.com/olivierparrot01/ICPE/main/c_selected.shp')
gdf_pts = gpd.read_file('https://raw.githubusercontent.com/olivierparrot01/ICPE/main/g_pt3.shp')

# Créer un GeoDataFrame vide pour stocker les nouvelles entités
result_gdf = gpd.GeoDataFrame(columns=['geometry'], crs=gdf_lignes.crs)

# Parcourir chaque ligne dans gdf_lignes
for line in gdf_lignes['geometry']:
    new_geometries = []
    
    # Parcourir chaque point dans gdf_pts
    for point in gdf_pts['geometry']:
        # Vérifier si le point est sur la ligne
        if point.intersects(line):
            # Découper la ligne en deux parties à l'emplacement du point
            parts = line.difference(Point(point))
            
            # Si les parties sont des MultiLineString, les découper en LineString individuels
            if parts.geom_type == 'MultiLineString':
                new_geometries.extend(list(parts))
            elif parts.geom_type == 'LineString':
                new_geometries.append(parts)
    
    # Si de nouvelles entités ont été créées, les ajouter au résultat
    if new_geometries:
        result_gdf = pd.concat([result_gdf, gpd.GeoDataFrame({'geometry': new_geometries}, crs=gdf_lignes.crs)], ignore_index=True)

# Enregistrez le GeoDataFrame résultant dans un fichier shapefile
#result_gdf.to_file('chemin_vers_nouvelles_entites.shp')
