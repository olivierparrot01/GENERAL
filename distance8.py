import streamlit as st
import pandas as pd
import base64

# Load data from CSV file
df = pd.read_csv('https://raw.githubusercontent.com/olivierparrot01/ICPE/main/1geocodage.csv')

# Define distance bins (100 m interval)
distance_bins = list(range(0, 1001, 100))

# Create histogram for distances
hist_data = df['Distance'].value_counts(bins=distance_bins, sort=False)

# Calculate the count for 'Statut_IED' in each distance category
statut_ied_counts = df[df['Statut_IED'] == 'Oui']['Distance'].value_counts(bins=distance_bins, sort=False).sort_index()

# Calculate the count for 'Seveso seuil haut' in each distance category
statut_seveso_haut_counts = df[df['Statut_Seveso'] == 'Seveso seuil haut']['Distance'].value_counts(bins=distance_bins, sort=False).sort_index()

# Calculate the count for 'Seveso seuil bas' in each distance category
statut_seveso_bas_counts = df[df['Statut_Seveso'] == 'Seveso seuil bas']['Distance'].value_counts(bins=distance_bins, sort=False).sort_index()

# Create a function to convert DataFrame to CSV and get the link for download
def get_csv_download_link(df, filename):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}.csv">Download {filename} CSV File</a>'
    return href


# Add download links for each DataFrame
st.markdown(get_csv_download_link(df[df['Statut_IED'] == 'Oui'], 'df_statut_ied'), unsafe_allow_html=True)
st.markdown(get_csv_download_link(df[df['Statut_Seveso'] == 'Seveso seuil haut'], 'df_statut_seveso_haut'), unsafe_allow_html=True)
st.markdown(get_csv_download_link(df[df['Statut_Seveso'] == 'Seveso seuil bas'], 'df_statut_seveso_bas'), unsafe_allow_html=True)
