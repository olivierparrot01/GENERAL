import streamlit as st
import pandas as pd
import numpy as np
import base64
import plotly.express as px
import plotly.graph_objects as go
import folium



# Load data from  CSV
dg = pd.read_csv('https://raw.githubusercontent.com/olivierparrot01/ICPE/main/2geocodage.csv')
df = pd.read_csv('https://raw.githubusercontent.com/olivierparrot01/ICPE/main/0208_gun.csv')
# Filter out negative and non-finite values from the 'Distance' column
dg = dg[dg['Distance'] >= 0]
dg = dg[np.isfinite(dg['Distance'])]

# Convert 'Distance' column to integers
dg['Distance'] = dg['Distance'].astype(int)

dg['Code_AIOT']=dg['Code_AIOT'].astype(str)
df['Code_AIOT']=df['Code_AIOT'].astype(str)
df['Adresse_concat'] = df['Adresse 1'].str.cat([df['Adresse 2'], df['Adresse 3']], sep=' ', na_rep='')

# Create a function to convert DataFrame to CSV and get the link  for download
def get_csv_download_link(df, filename):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}.csv">Télécharger {filename} CSV File</a>'
    return href


# Create a multiselect to choose multiple criteria to filter the DataFrame
st.markdown("<h2 style='font-size:22px;'>Filtrer le fichier de géocodage par type de réponse de l'API et score</h2>", unsafe_allow_html=True)
st.markdown("<center><h2 style='font-size:18px;'>Le filtre n'est pas obligatoire<br></h2></center>", unsafe_allow_html=True)
st.markdown("<center><h2 style='font-size:18px;'>Il s'applique tout le long</h2></center>", unsafe_allow_html=True)
selected_criteria = st.multiselect("", options=['result_typ', 'result_sco'])

# Apply the selected criteria to filterthe DataFrame
filtered_dg = dg.copy()
for criterion in selected_criteria:
    if criterion == 'result_typ':
        unique_values = filtered_dg['result_typ'].unique()
        selected_value = st.selectbox(f"", options=unique_values)
        filtered_dg = filtered_dg[filtered_dg['result_typ'] == selected_value]
    elif criterion == 'result_sco':
        selected_result_sco = st.slider("Le score est supérieur ou égal à :", min_value=dg['result_sco'].min(), max_value=dg['result_sco'].max(), step=0.01)
        filtered_dg = filtered_dg[filtered_dg['result_sco'] >= selected_result_sco]

#df = filtered_df


dg=filtered_dg

# Créer des intervalles de distance jusqu'à 1000 de 100 en 100
distance_bins_1 = np.arange(0, 1100, 100)

# Créer des intervalles de distance à partir de 1000 de 1000 en 1000 jusqu'au maximum
max_distance = dg['Distance'].max()
distance_bins_2 = np.arange(1000, max_distance , 1000)

# Combinez les deux listes d'intervalles de  distance
distance_bins = np.concatenate((distance_bins_1, distance_bins_2))

# Ajouter l'intervalle global [0, max_distance]
distance_bins = np.append(distance_bins, [0, max_distance])

# Supprimer les doublons des bords des intervalles de distance
distance_bins = np.unique(distance_bins)

# Créer l'histogramme pour les nouvelles intervalles de distance
data = dg['Distance'].value_counts(bins=distance_bins, sort=False)
data.index = [f"[{int(interval.left)}, {int(interval.right)}]" for interval in data.index]

# Calculer le nombre pour chaque catégorie de distance pour 'Statut_IED'
statut_ied_counts = dg[dg['Statut_IED'] == 'Oui']['Distance'].value_counts(bins=distance_bins, sort=False)
statut_ied_counts.index = [f"[{int(interval.left)}, {int(interval.right)}]" for interval in statut_ied_counts.index]

# Calculer le nombre pour chaque catégorie de distance pour 'Seveso seuil haut'
statut_seveso_haut_counts = dg[dg['Statut_Sev'] == 'Seveso seuil haut']['Distance'].value_counts(bins=distance_bins, sort=False)
statut_seveso_haut_counts.index = [f"[{int(interval.left)}, {int(interval.right)}]" for interval in statut_seveso_haut_counts.index]

# Calculer le nombre pour chaque catégorie de distance pour 'Seveso seuil bas'
statut_seveso_bas_counts = dg[dg['Statut_Sev'] == 'Seveso seuil bas']['Distance'].value_counts(bins=distance_bins, sort=False)
statut_seveso_bas_counts.index = [f"[{int(interval.left)}, {int(interval.right)}]" for interval in statut_seveso_bas_counts.index]

# Convertir les bords des intervalles en chaînes
data.index = data.index.astype(str)
statut_ied_counts.index = statut_ied_counts.index.astype(str)
statut_seveso_haut_counts.index = statut_seveso_haut_counts.index.astype(str)
statut_seveso_bas_counts.index = statut_seveso_bas_counts.index.astype(str)


# Utiliser le widget expander pour créer une section expansible
st.markdown("<h2 style='font-size:18px;'>Nb ICPE tout type par intervalle de distance (par rapport à GUN)</h2>", unsafe_allow_html=True)
with st.expander("Afficher/Masquer la table"):
    # Afficher la table à l'intérieur de la section expansible
    st.table(data)
st.markdown(get_csv_download_link(dg, f'le fichier de geocodage correspondant'), unsafe_allow_html=True)


# Utiliser le widget expander pour créer une section expansible
st.markdown("<h2 style='font-size:18px;'>Nb ICPE 'IED' par intervalle de distance (par rapport à GUN)</h2>", unsafe_allow_html=True)
with st.expander("Afficher/Masquer la table"):
    # Afficher la table à l'intérieur de la section expansible
    st.table(statut_ied_counts)
st.markdown(get_csv_download_link(dg[dg['Statut_IED'] == 'Oui'], 'le fichier de geocodage correspondant'), unsafe_allow_html=True)



# Utiliser le widget expander pour créer une section expansible
st.markdown("<h2 style='font-size:18px;'>Nb ICPE 'Seveso seuil haut'  par intervalle de distance en m (par rapport à GUN)</h2>", unsafe_allow_html=True)
with st.expander("Afficher/Masquer la table"):
    # Afficher la table à l'intérieur de la section expansible
    st.table(statut_seveso_haut_counts)
st.markdown(get_csv_download_link(dg[dg['Statut_Sev'] == 'Seveso seuil haut'], 'le fichier de geocodage correspondant'), unsafe_allow_html=True)




# Utiliser le widget expander pour créer une section expansible
st.markdown("<h2 style='font-size:18px;'>Nb ICPE 'Seveso seuil bas'  par intervalle de distance en m (par rapport à GUN)</h2>", unsafe_allow_html=True)
with st.expander("Afficher/Masquer la table"):
    # Afficher la table à l'intérieur de la section expansible
    st.table(statut_seveso_bas_counts)
st.markdown(get_csv_download_link(dg[dg['Statut_Sev'] == 'Seveso seuil bas'], 'le fichier de geocodage correspondant'), unsafe_allow_html=True)




# Custom format function for the dropdown menu
def format_interval_label(interval_index):
    if interval_index == 0:
        return f"[0 max]"
    if interval_index == len(interval_indices) - 1:
        return f"[{distance_bins[interval_index]}, max]"
    left = distance_bins[interval_index]
    right = distance_bins[interval_index + 1]
    return f"[{left}, {right}]"

    

# Create a list of formatted interval labels for the dropdown menu
interval_indices = list(range(len(distance_bins) - 1))
dropdown_labels = [format_interval_label(interval_index) for interval_index in interval_indices]

# Add the [0, max_distance] interval label at the beginning of the list
# dropdown_labels.insert(0, "[0, max_distance]")

def filter_dataframe_by_interval(interval, statut):
    column_mapping = {
        'Statut_IED': 'Statut_IED',
        'Seveso seuil haut': 'Statut_Sev',
        'Seveso seuil bas': 'Statut_Sev',
        'Code_AIOT': 'Code_AIOT'
    }
    
    if interval.left == 0 and interval.right == max_distance:
        return dg  # Return the entire DataFrame if the interval is [0 max]
    
    selected_column = column_mapping.get(statut)
    if selected_column:
        if statut == 'Code_AIOT':
            return dg[dg['Distance'].between(interval.left, interval.right) & dg[selected_column].notna()]
        else:
            return dg[dg['Distance'].between(interval.left, interval.right) & (dg[selected_column] == statut)]
    else:
        return pd.DataFrame()  # Return an empty DataFrame if the statut is not recognized

# Add a dropdown menu to select an interval
st.markdown("<h2 style='font-size:18px;'>Afficher ou télécharger les données pour un intervalle particulier :</h2>", unsafe_allow_html=True)
selected_interval_index = st.selectbox("", options=interval_indices, format_func=format_interval_label)

if selected_interval_index == 0:
    selected_interval_left = 0
    selected_interval_right = max_distance
else:
    selected_interval_left = distance_bins[selected_interval_index]
    selected_interval_right = distance_bins[selected_interval_index + 1]

filtered_dg1 = filter_dataframe_by_interval(pd.Interval(selected_interval_left, selected_interval_right), 'Code_AIOT')
filtered_dg_statut_ied = filter_dataframe_by_interval(pd.Interval(selected_interval_left, selected_interval_right), 'Statut_IED')  
filtered_dg_statut_seveso_bas = filter_dataframe_by_interval(pd.Interval(selected_interval_left, selected_interval_right), 'Seveso seuil bas')
filtered_dg_statut_seveso_haut = filter_dataframe_by_interval(pd.Interval(selected_interval_left, selected_interval_right), 'Seveso seuil haut')

with st.expander(f"Afficher les données pour l'intervalle {selected_interval_left} à {selected_interval_right} (ICPE tout type)"):
    # Afficher la table à l'intérieur de la section expansible
    st.dataframe(filtered_dg1)
    


with st.expander(f"Afficher les données pour l'intervalle {selected_interval_left} à {selected_interval_right} (Statut_IED)"):
    # Afficher la table à l'intérieur de la section expansible
    st.dataframe(filtered_dg_statut_ied)


with st.expander(f"Afficher les données pour l'intervalle {selected_interval_left} à {selected_interval_right} (Seveso seuil haut)"):
    # Afficher la table à l'intérieur de la section expansible
    st.dataframe(filtered_dg_statut_seveso_haut)

with st.expander(f"Afficher les données pour l'intervalle {selected_interval_left} à {selected_interval_right} (Seveso seuil bas)"):
    # Afficher la table à l'intérieur de la section expansible
    st.dataframe(filtered_dg_statut_seveso_bas)


if st.button(f"Télécharger les données pour l'intervalle {selected_interval_left} à {selected_interval_right} (ICPE tout type)"):
    #filtered_df0 = filter_dataframe_by_interval(pd.Interval(selected_interval_left, selected_interval_right), 'Code_AIOT')
    st.markdown(get_csv_download_link(filtered_dg1, f'ICPE tout type_interval_{selected_interval_left}_{selected_interval_right}'), unsafe_allow_html=True)


filtered_df = df[df['Code_AIOT'].isin(filtered_dg1['Code_AIOT'])]

# Calculer les coordonnées moyennes des latitudes et longitudes de filtered_df
center_lat = filtered_dg1['latitude'].mean()
center_lon = filtered_dg1['longitude'].mean()

# Créer une seule carte avec filtered_dg en rouge et filtered_df en bleu 
st.markdown(f"<h2 style='font-size:22px;'> Gun en bleu et Geocodage en rouge pour l'intervalle [{selected_interval_left} {selected_interval_right}] (ICPE tout type)</h2>", unsafe_allow_html=True)


fig = px.scatter_mapbox(filtered_dg1, lat="latitude", lon="longitude", hover_data=["Nom_usuel", "Code_AIOT", "Adresse_si","nb_points"], size='nb_points', size_max=15,  zoom=8,color_discrete_sequence=['red'])
fig.add_trace(px.scatter_mapbox(filtered_df, lat="latitude", lon="longitude", hover_data=["Nom_usuel", "Code_AIOT","Adresse_concat","nb_points"], size='nb_points', size_max=10,  zoom=8, color_discrete_sequence=['blue']).data[0])


# Add a scattermapbox trace for the scale bar
scale_bar_trace = px.scatter_mapbox(lat=[center_lat], lon=[center_lon], text=["Scale Bar"]).data[0]
scale_bar_trace.update(textfont=dict(color="black", size=12), hoverinfo="text", mode="text")
fig.add_trace(scale_bar_trace)




fig.update_layout(mapbox_style="open-street-map")
fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
fig.update_layout(mapbox_center={"lat": center_lat, "lon": center_lon})
# Créer une seule carte avec filtered_df en rouge et filtered_df1 en bleu

st.plotly_chart(fig)
                                                                                                                                       



st.markdown("<h2 style='font-size:22px;'> Gun en bleu et geocodage en rouge pour nb_points >= 2</h2>", unsafe_allow_html=True)


# Seuil pour filtrer les valeurs de nb_points
seuil_nb_points = 1

# Utiliser applymask pour filtrer les données en fonction de la colonne "nb_points"
filtered_dg2 = dg[dg['nb_points'].apply(lambda x: x > seuil_nb_points)]
filtered_df2 = df[df['nb_points'].apply(lambda x: x > seuil_nb_points)]
filtered_df2["Nom_usuel"] = filtered_df2["Nom_usuel"].astype(str)
# Créer une nouvelle colonne dans le DataFrame dg pour concaténer les valeurs Code_AIOT
filtered_dg2["Code_AIOT_liste"] = filtered_dg2.groupby(["latitude", "longitude"])["Code_AIOT"].transform(lambda x: ", ".join(x))
filtered_dg2["Nom_usuel_liste"] = filtered_dg2.groupby(["latitude", "longitude"])["Nom_usuel"].transform(lambda x: ", ".join(x))

filtered_df2["Code_AIOT_liste"] = filtered_df2.groupby(["latitude", "longitude"])["Code_AIOT"].transform(lambda x: ", ".join(x))
filtered_df2["Nom_usuel_liste"] = filtered_df2.groupby(["latitude", "longitude"])["Nom_usuel"].transform(lambda x: ", ".join(x))

# Calculer les coordonnées moyennes des latitudes et longitudes de filtered_dg2
center_lat = filtered_dg2['latitude'].mean()
center_lon = filtered_dg2['longitude'].mean()

# Créer la carte avec des points rouges (dg) et bleus (df)
fig = px.scatter_mapbox(filtered_dg2, lat="latitude", lon="longitude", hover_data=["Nom_usuel_liste", "Code_AIOT_liste", "Adresse_si", "nb_points"], size='nb_points', size_max=10, zoom=8, color_discrete_sequence=['red'])
fig.add_trace(px.scatter_mapbox(filtered_df2, lat="latitude", lon="longitude", hover_data=["Nom_usuel_liste", "Code_AIOT_liste", "Adresse_concat", "nb_points"], size='nb_points', size_max=10, color_discrete_sequence=['blue']).data[0])

fig.update_layout(mapbox_style="open-street-map")
fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
fig.update_layout(mapbox_center={"lat": center_lat, "lon": center_lon})


with st.expander(f"Afficher les données Gun"):
    # Afficher la table à l'intérieur de la section expansible
    st.dataframe(filtered_df2)

with st.expander(f"Afficher les données Geocodage"):
    # Afficher la table à l'intérieur de la section expansible
    st.dataframe(filtered_dg2)



# Afficher la carte dans Streamlit 
st.plotly_chart(fig)






import streamlit as st
import pandas as pd
import folium

# Create a function to generate HTML for a Folium map with a numeric scale bar
def create_folium_map_with_scale_bar(center_lat, center_lon, data):
    m = folium.Map(location=[center_lat, center_lon], zoom_start=8, control_scale=True)

    folium.TileLayer('openstreetmap').add_to(m)

    # Calculate distances for the scale bar (in kilometers)
    scale_distance_km = 10  # Change this to the desired scale distance in kilometers

    # Add a scale bar to the HTML
    scale_bar_html = f'''
        <div class="leaflet-bottom leaflet-right">
            <div class="leaflet-control-scale leaflet-control">
                <div class="leaflet-control-scale-line" style="width: {scale_distance_km * 100}px;"></div>
                <div class="leaflet-control-scale-text" style="white-space: nowrap;">{scale_distance_km} km</div>
            </div>
        </div>
    '''

    # Add the custom scale bar HTML to the map
    folium.Element(scale_bar_html).add_to(m)
    
    # Add red data points to the map
    for index, row in data.iterrows():
        folium.Marker([row['latitude'], row['longitude']], icon=folium.Icon(color='red')).add_to(m)

    return m.get_root().render()

# Example usage
center_lat = 48.8566
center_lon = 2.3522
filtered_dg1 = None  # Replace with your data (filtered DataFrame)
folium_map_html = create_folium_map_with_scale_bar(center_lat, center_lon, filtered_dg1)
st.components.v1.html(folium_map_html, height=600)
