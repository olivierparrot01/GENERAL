import streamlit as st
import pandas as pd
import numpy as np
import base64

# Load data from CSV
df = pd.read_csv('https://raw.githubusercontent.com/olivierparrot01/ICPE/main/1geocodage.csv')

# Filter out negative and non-finite values from the 'Distance' column
df = df[df['Distance'] >= 0]
df = df[np.isfinite(df['Distance'])]

# Convert 'Distance' column to integers
df['Distance'] = df['Distance'].astype(int)

# Define custom distance bins (100 m interval)
distance_bins = np.arange(0, 1100, 100)

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

# Create a function to filter DataFrame based on selected interval
def filter_dataframe_by_interval(interval):
    return df[df['Distance'].between(interval.left, interval.right)]
# Create a function to convert DataFrame to CSV and get the link for download
def get_csv_download_link(df, filename):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}.csv">Download {filename} CSV File</a>'
    return href
# Add download links for the filtered DataFrames
selected_interval = st.slider("Select an Interval:", min_value=0, max_value=len(distance_bins)-2, step=1)
selected_interval_left = distance_bins[selected_interval]
selected_interval_right = distance_bins[selected_interval + 1]

if st.button(f"Download Filtered Data for Interval {selected_interval_left} to {selected_interval_right}"):
    filtered_df_statut_ied = filter_dataframe_by_interval(pd.Interval(selected_interval_left, selected_interval_right))
    st.markdown(get_csv_download_link(filtered_df_statut_ied, f'df_statut_ied_interval_{selected_interval_left}_{selected_interval_right}'), unsafe_allow_html=True)

if st.button(f"Download Filtered Data for Interval {selected_interval_left} to {selected_interval_right}"):
    filtered_df_statut_seveso_haut = filter_dataframe_by_interval(pd.Interval(selected_interval_left, selected_interval_right))
    st.markdown(get_csv_download_link(filtered_df_statut_seveso_haut, f'df_statut_seveso_haut_interval_{selected_interval_left}_{selected_interval_right}'), unsafe_allow_html=True)

if st.button(f"Download Filtered Data for Interval {selected_interval_left} to {selected_interval_right}"):
    filtered_df_statut_seveso_bas = filter_dataframe_by_interval(pd.Interval(selected_interval_left, selected_interval_right))
    st.markdown(get_csv_download_link(filtered_df_statut_seveso_bas, f'df_statut_seveso_bas_interval_{selected_interval_left}_{selected_interval_right}'), unsafe_allow_html=True)
