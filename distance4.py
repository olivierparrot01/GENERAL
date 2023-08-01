import streamlit as st
import pandas as pd
import numpy as np
import base64

# Load data from  CSV
df = pd.read_csv('https://raw.githubusercontent.com/olivierparrot01/ICPE/main/1geocodage.csv')

# Filter out non-finite values from the 'Distance' column
df = df[df['Distance'] >= 0]
df = df[np.isfinite(df['Distance'])]

df['Distance'] =df['Distance'].astype(int)
# Define distance bins (100 m interval)
distance_bins = list(range(0, 1100, 100))

# Create histogram for distances
hist_data = df['Distance'].value_counts(bins=distance_bins, sort=False)

# Calculate the count for 'Statut_IED' in each distance category
statut_ied_counts = df[df['Statut_IED'] == 'Oui']['Distance'].value_counts(bins=distance_bins, sort=False).sort_index()

# Calculate the count for 'Seveso seuil haut' in each distance category
statut_seveso_haut_counts = df[df['Statut_Sev'] == 'Seveso seuil haut']['Distance'].value_counts(bins=distance_bins, sort=False).sort_index()

# Calculate the count for 'Seveso seuil bas' in each distance category
statut_seveso_bas_counts = df[df['Statut_Sev'] == 'Seveso seuil bas']['Distance'].value_counts(bins=distance_bins, sort=False).sort_index()

# Update interval edges to integers
hist_data.index = hist_data.index
statut_ied_counts.index = statut_ied_counts.index
statut_seveso_haut_counts.index = statut_seveso_haut_counts
statut_seveso_bas_counts.index = statut_seveso_bas_counts
# Show the table for distances
st.write("Distance Histogram (100 m intervals)")
st.table(hist_data)

# Show the table for 'Statut_IED' counts
st.write("Counts of 'Statut_IED' in Each Distance Category")
st.table(statut_ied_counts)

# Show the table for 'Seveso seuil haut' counts
st.write("Counts of 'Seveso seuil haut' in Each Distance Category")
st.table(statut_seveso_haut_counts)

# Show the table for 'Seveso seuil bas' counts
st.write("Counts of 'Seveso seuil bas' in Each Distance Category")
st.table(statut_seveso_bas_counts)

# Create a function to convert DataFrame to CSV and get the link for download
def get_csv_download_link(df, filename):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}.csv">Download {filename} CSV File</a>'
    return href

# Add download links for each DataFrame
st.markdown(get_csv_download_link(df[df['Statut_IED'] == 'Oui'], 'df_statut_ied'), unsafe_allow_html=True)
st.markdown(get_csv_download_link(df[df['Statut_Sev'] == 'Seveso seuil haut'], 'df_statut_seveso_haut'), unsafe_allow_html=True)
st.markdown(get_csv_download_link(df[df['Statut_Sev'] == 'Seveso seuil bas'], 'df_statut_seveso_bas'), unsafe_allow_html=True)
