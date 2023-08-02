import streamlit as st
import pandas as pd
import numpy as np
import base64

# Load data from CSV
df = pd.read_csv('https://raw.githubusercontent.com/olivierparrot01/ICPE/main/2geocodage.csv')

# Filter out negative and non-finite values from the 'Distance' column
df = df[df['Distance'] >= 0]
df = df[np.isfinite(df['Distance'])]

# Convert 'Distance' column to integers
df['Distance'] = df['Distance'].astype(int)

# Create a function to convert DataFrame to CSV and get the  link for download
def get_csv_download_link(df, filename):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}.csv">Télécharger {filename} CSV File</a>'
    return href


# Custom format function for the dropdown menu
def format_interval_label(interval_index):
    if interval_index == len(interval_indices) - 1:
        return f"[{distance_bins[interval_index]}, max]"
    left = distance_bins[interval_index]
    right = distance_bins[interval_index + 1]
    return f"[{left}, {right}]"

# Create a multiselect to choose multiple criteria to filter the DataFrame
#selected_criteria = st.multiselect("##Filtrer le fichier de geocodage:", options=['result_typ', 'result_sco'])

# Create a multiselect to choose multiple criteria to filter the DataFrame
st.markdown("<h2 style='font-size:22px;'>Filtrer le fichier de géocodage selon le type de réponse de l'API et le score</h2>", unsafe_allow_html=True)
st.markdown("<h2 style='font-size:10px;'>(le filtre n'est pas obligatoire) 
selected_criteria = st.multiselect("", options=['result_typ', 'result_sco'])

# Apply the selected criteria to filter the DataFrame
filtered_df = df.copy()
for criterion in selected_criteria:
    if criterion == 'result_typ':
        unique_values = filtered_df['result_typ'].unique()
        selected_value = st.selectbox(f"", options=unique_values)
        filtered_df = filtered_df[filtered_df['result_typ'] == selected_value]
    elif criterion == 'result_sco':
        selected_result_sco = st.slider("", min_value=df['result_sco'].min(), max_value=df['result_sco'].max(), step=0.01)
        filtered_df = filtered_df[filtered_df['result_sco'] >= selected_result_sco]


# Show the table for filtered DataFrame
#st.write("Filtered DataFrame")
#st.table(filtered_df)

# Create a slider to select rows based on the 'result_sco' column
#selected_result_sco = st.slider("Select Result Score:", min_value=df['result_sco'].min(), max_value=df['result_sco'].max(), step=0.01)

# Filter the DataFrame based on the selected 'result_sco' value
#df = df[df['result_sco'] >= selected_result_sco]

df=filtered_df


distance_bins = np.arange(0, 1100, 100)

# Add a final interval for [1000, max]
distance_bins = np.append(distance_bins, df['Distance'].max())

# Create histogram for distances
hist_data = df['Distance'].value_counts(bins=distance_bins, sort=False)

# Calculate the count for 'Statut_IED' in each distance category
statut_ied_counts = df[df['Statut_IED'] == 'Oui']['Distance'].value_counts(bins=distance_bins, sort=False).sort_index()

# Calculate the count for 'Seveso seuil haut' in each distance category
statut_seveso_haut_counts = df[df['Statut_Sev'] == 'Seveso seuil haut']['Distance'].value_counts(bins=distance_bins, sort=False).sort_index()

# Calculate the count for 'Seveso seuil bas' in each distance category
statut_seveso_bas_counts = df[df['Statut_Sev'] == 'Seveso seuil bas']['Distance'].value_counts(bins=distance_bins, sort=False).sort_index()

# Convert interval edges to strings
hist_data.index = hist_data.index.astype(str)
statut_ied_counts.index = statut_ied_counts.index.astype(str)
statut_seveso_haut_counts.index = statut_seveso_haut_counts.index.astype(str)
statut_seveso_bas_counts.index = statut_seveso_bas_counts.index.astype(str)




# Show the table for distances
# st.write("Nb ICPE tout type par intervalle de distance (par rapport à GUN)")

st.markdown("<h2 style='font-size:18px;'>Nb ICPE de tout type par intervalle de distance en m (par rapport à GUN)</h2>", unsafe_allow_html=True)
#selected_criteria = st.multiselect("", options=['result_typ', 'result_sco'])

st.table(hist_data)
# Add download link for the filtered DataFrame
st.markdown(get_csv_download_link(filtered_df, f'le fichier de geocodage correspondant'), unsafe_allow_html=True)

# Show the table for 'Statut_IED' counts
st.markdown("<h2 style='font-size:18px;'>Nb ICPE 'IED' par intervalle de distance en m (par rapport à GUN)</h2>", unsafe_allow_html=True)

#st.write("Nb ICPE 'IED' par intervalle de distance (par rapport à GUN)")
st.table(statut_ied_counts)
st.markdown(get_csv_download_link(df[df['Statut_IED'] == 'Oui'], 'le fichier de geocodage correspondant'), unsafe_allow_html=True)
# Show the table for 'Seveso seuil haut' counts
st.markdown("<h2 style='font-size:18px;'>Nb ICPE 'Seveso seuil haut'  par intervalle de distance en m (par rapport à GUN)</h2>", unsafe_allow_html=True)
#st.write("Nb ICPE 'Seveso seuil' haut par intervalle de distance (par rapport à GUN)")
st.table(statut_seveso_haut_counts)
st.markdown(get_csv_download_link(df[df['Statut_Sev'] == 'Seveso seuil haut'], 'le fichier de geocodage correspondant'), unsafe_allow_html=True)
# Show the table for 'Seveso seuil bas' counts
st.markdown("<h2 style='font-size:18px;'>Nb ICPE 'Seveso seuil bas'  par intervalle de distance en m (par rapport à GUN)</h2>", unsafe_allow_html=True)

#st.write("Nb ICPE 'Seveso seuil bas' par intervalle de distance (par rapport à GUN)")
st.table(statut_seveso_bas_counts)
st.markdown(get_csv_download_link(df[df['Statut_Sev'] == 'Seveso seuil bas'], 'le fichier de geocodage correspondant'), unsafe_allow_html=True)


# Create a function to filter DataFrame based on selected interval
def filter_dataframe_by_interval(interval, statut):
    if statut == 'Statut_IED':
        return df[df['Distance'].between(interval.left, interval.right) & (df['Statut_IED'] == 'Oui')]
    elif statut == 'Seveso seuil haut':
        return df[df['Distance'].between(interval.left, interval.right) & (df['Statut_Sev'] == 'Seveso seuil haut')]
    elif statut == 'Seveso seuil bas':
        return df[df['Distance'].between(interval.left, interval.right) & (df['Statut_Sev'] == 'Seveso seuil bas')]
    if statut == 'Code_AIOT':
        return df[df['Distance'].between(interval.left, interval.right) & (df['Code_AIOT'].notna())]

# Custom format function for the dropdown menu
def format_interval_label(interval_index):
    if interval_index == len(interval_indices) - 1:
        return f"[{distance_bins[interval_index]}, max]"
    left = distance_bins[interval_index]
    right = distance_bins[interval_index + 1]
    return f"[{left}, {right}]"
    

# Create a list of formatted interval labels for the dropdown menu
interval_indices = list(range(len(distance_bins) - 1))
dropdown_labels = [format_interval_label(interval_index) for interval_index in interval_indices]

# Add a dropdown menu to select an interval
st.markdown("<h2 style='font-size:18px;'>Télécharger les données pour un intervalle particulier :</h2>", unsafe_allow_html=True)
selected_interval_index = st.selectbox("", options=interval_indices, format_func=format_interval_label)


selected_interval_left = distance_bins[selected_interval_index]
selected_interval_right = distance_bins[selected_interval_index + 1]


if st.button(f"Télécharger les données pour l'intervalle {selected_interval_left} to {selected_interval_right} (Statut_IED)"):
    filtered_df_statut_ied = filter_dataframe_by_interval(pd.Interval(selected_interval_left, selected_interval_right), 'Statut_IED')
    st.markdown(get_csv_download_link(filtered_df_statut_ied, f'df_statut_ied_interval_{selected_interval_left}_{selected_interval_right}'), unsafe_allow_html=True)

if st.button(f"Télécharger les données pour l'intervalle {selected_interval_left} to {selected_interval_right} (Seveso seuil haut)"):
    filtered_df_statut_seveso_haut = filter_dataframe_by_interval(pd.Interval(selected_interval_left, selected_interval_right), 'Seveso seuil haut')
    st.markdown(get_csv_download_link(filtered_df_statut_seveso_haut, f'df_statut_seveso_haut_interval_{selected_interval_left}_{selected_interval_right}'), unsafe_allow_html=True)

if st.button(f"Télécharger les données pour l'intervalle {selected_interval_left} to {selected_interval_right} (Seveso seuil bas)"):
    filtered_df_statut_seveso_bas = filter_dataframe_by_interval(pd.Interval(selected_interval_left, selected_interval_right), 'Seveso seuil bas')
    st.markdown(get_csv_download_link(filtered_df_statut_seveso_bas, f'df_statut_seveso_haut_interval_{selected_interval_left}_{selected_interval_right}'), unsafe_allow_html=True)

if st.button(f"Télécharger les données pour l'intervalle {selected_interval_left} to {selected_interval_right} (ICPE tout type)"):
    filtered_df = filter_dataframe_by_interval(pd.Interval(selected_interval_left, selected_interval_right), 'Code_AIOT')
    st.markdown(get_csv_download_link(filtered_df, f'ICPE tout type_interval_{selected_interval_left}_{selected_interval_right}'), unsafe_allow_html=True)
