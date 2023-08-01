import streamlit as st
import pandas as pd
import numpy as np
import base64

# Load data from CSV
df = pd.read_csv('https://raw.githubusercontent.com/olivierparrot01/ICPE/main/1geocodage.csv')

# Filter out negative and non-finite values from the 'Distance' column
df = df[df['Distance'] >= 0]
df = df[np.isfinite(df['Distance'])]

# Define custom distance bins (100 m interval)
distance_bins = np.arange(0, 1100, 100)

# Categorize distances into custom bins
df['distance_category'] = pd.cut(df['Distance'], bins=distance_bins)

# Create histogram for distances
hist_data = df['distance_category'].value_counts().sort_index().astype(int)

# Calculate the count for 'Statut_IED' in each distance category
statut_ied_counts = df[df['Statut_IED'] == 'Oui']['distance_category'].value_counts().sort_index().astype(int)

# Calculate the count for 'Seveso seuil haut' in each distance category
statut_seveso_haut_counts = df[df['Statut_Sev'] == 'Seveso seuil haut']['distance_category'].value_counts().sort_index().astype(int)

# Calculate the count for 'Seveso seuil bas' in each distance category
statut_seveso_bas_counts = df[df['Statut_Sev'] == 'Seveso seuil bas']['distance_category'].value_counts().sort_index().astype(int)

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
