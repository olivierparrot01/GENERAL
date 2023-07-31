import streamlit as st
import pandas as pd
import numpy as np
import base64

# Load data from CSV  

df = pd.read_csv('https://raw.githubusercontent.com/olivierparrot01/ICPE/main/1geocodage.csv')

# Define di stance bins (100 m interval)
distance_bins = list(range(0, 1001, 100))

# Create histogram for distances
hist_data = df['Distance'].value_counts(bins=distance_bins, sort=False)

# Calculate the count for 'Statut_IED' in each distance category
statut_ied_counts = df[df['Statut_IED'] == 'Oui']['Distance'].value_counts(bins=distance_bins, sort=False).sort_index()

# Calculate the count for 'Seveso seuil haut' in each distance category
statut_seveso_haut_counts = df[df['Statut_Sev'] == 'Seveso seuil haut']['Distance'].value_counts(bins=distance_bins, sort=False).sort_index()

# Calculate the count for 'Seveso seuil bas' in each distance category
statut_seveso_bas_counts = df[df['Statut_Sev'] == 'Seveso seuil bas']['Distance'].value_counts(bins=distance_bins, sort=False).sort_index()

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

# Add download buttons for each table
def download_button(df, label):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{label}.csv">Download {label} as CSV</a>'
    return href

st.markdown(download_button(hist_data, 'Distance Histogram'), unsafe_allow_html=True)
st.markdown(download_button(statut_ied_counts, 'Statut_IED Counts'), unsafe_allow_html=True)
st.markdown(download_button(statut_seveso_haut_counts, 'Statut_Seveso_Haut Counts'), unsafe_allow_html=True)
st.markdown(download_button(statut_seveso_bas_counts, 'Statut_Seveso_Bas Counts'), unsafe_allow_html=True)
st.markdown(get_csv_download_link(df[df['Statut_IED'] == 'Oui'], 'df_statut_ied'), unsafe_allow_html=True)
