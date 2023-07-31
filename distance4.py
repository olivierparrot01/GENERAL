import streamlit as st
import pandas as pd
import numpy as np

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
statut_seveso_haut_counts = df[df['Statut_Sev'] == 'Seveso seuil haut']['Distance'].value_counts(bins=distance_bins, sort=False).sort_index()

# Calculate the count for 'Seveso seuil bas' in each distance category
statut_seveso_bas_counts = df[df['Statut_Sev'] == 'Seveso seuil bas']['Distance'].value_counts(bins=distance_bins, sort=False).sort_index()

# Create a function to convert DataFrame to CSV and get the link for download
def get_csv_download_link(df, filename):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}.csv">Download {filename} CSV File</a>'
    return href

# Show the histogram for distances
plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
plt.bar(hist_data.index.mid, hist_data.values)
plt.xlabel('Distance (m)')
plt.ylabel('Count')
plt.title('Distance Histogram (100 m intervals)')
plt.xticks(rotation=45)

# Plot the counts for 'Statut_IED' in each distance category
plt.subplot(1, 2, 2)
plt.bar(statut_ied_counts.index.mid, statut_ied_counts.values, label='Statut_IED')
plt.bar(statut_seveso_haut_counts.index.mid, statut_seveso_haut_counts.values, label='Seveso seuil haut', alpha=0.7)
plt.bar(statut_seveso_bas_counts.index.mid, statut_seveso_bas_counts.values, label='Seveso seuil bas', alpha=0.7)
plt.xlabel('Distance (m)')
plt.ylabel('Count')
plt.title('Counts in Each Distance Category')
plt.legend()
plt.xticks(rotation=45)

# Show the plot in Streamlit
st.pyplot(plt)

# Add download links for each DataFrame
st.markdown(get_csv_download_link(df[df['Statut_IED'] == 'Oui'], 'df_statut_ied'), unsafe_allow_html=True)
st.markdown(get_csv_download_link(df[df['Statut_Sev'] == 'Seveso seuil haut'], 'df_statut_seveso_haut'), unsafe_allow_html=True)
st.markdown(get_csv_download_link(df[df['Statut_Sev'] == 'Seveso seuil bas'], 'df_statut_seveso_bas'), unsafe_allow_html=True)
