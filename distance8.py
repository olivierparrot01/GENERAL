# ... (code précédent)

# Ajouter la couche GeoJSON des lignes avec une couleur unique
geojson_layer = folium.GeoJson(
    data='https://raw.githubusercontent.com/olivierparrot01/ICPE/main/lines.geojson', 
    name="Lignes entre points",
    style_function=lambda feature: {
        'color': 'black',  # Utilisez la couleur de votre choix
        'opacity': 1,
        'weight': 5  # Épaisseur constante
    },
    tooltip=folium.GeoJsonTooltip(
        fields=["Code_AIOT", "Distance"],
        aliases=["Code AIOT", "Distance"],
        style="font-size: 12px; text-align: center;"
    )
)

geojson_layer.add_to(m)

# Afficher la carte mise à jour dans Streamlit en utilisant folium_static
folium_static(m)

# Afficher les données tabulaires dans une section expansible
with st.expander(f"Afficher les {len(df)} données"):
    # Afficher la table à l'intérieur de la section expansible
    st.dataframe(df)

st.markdown("<h2 style='font-size:18px;'>Sélectionner par le Code AIOT les points Gun à mettre en évidence (carte, table et liens Google Maps)</h2>", unsafe_allow_html=True)
# Sélection des codes AIOT à mettre en évidence
selected_codes = st.multiselect("", df["Code_AIOT"])

# Filtrer les données en fonction des codes AIOT sélectionnés
filtered_data = df[df['Code_AIOT'].isin(selected_codes)]

# Mettre en évidence les points correspondant aux codes AIOT sélectionnés
for index, row in filtered_data.iterrows():
    folium.CircleMarker(
        location=[row['latitude'], row['longitude']],
        radius=10,
        color='green',
        fill=True,
        fill_color='green',
        fill_opacity=0.6,
        popup=f"Code_AIOT(S): {row['Code_AIOT_liste']}"
    ).add_to(m)

# Afficher la carte mise à jour dans Streamlit en utilisant folium_static
folium_static(m)
