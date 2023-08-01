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

# Create a slider to select rows based on the 'result_sco' column
selected_result_sco = st.slider("Select Result Score:", min_value=df['result_sco'].min(), max_value=df['result_sco'].max(), step=0.01)

# Filter the DataFrame based on the selected 'result_sco' value
df = df[df['result_sco'] >= selected_result_sco]

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


# Create a function to convert DataFrame to CSV and get the link for download
def get_csv_download_link(df, filename):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}.csv">Download {filename} CSV File</a>'
    return href



# Show the table for distances
st.write("Counts of ICPE tout type in Each Distance Category (100 m intervals)")
st.table(hist_data)

# Show the table for 'Statut_IED' counts
st.write("Counts of 'Statut_IED' in Each Distance Category")
st.table(statut_ied_counts)
st.markdown(get_csv_download_link(df[df['Statut_IED'] == 'Oui'], 'df_statut_ied_all'), unsafe_allow_html=True)
# Show the table for 'Seveso seuil haut' counts
st.write("Counts of 'Seveso seuil haut' in Each Distance Category")
st.table(statut_seveso_haut_counts)
st.markdown(get_csv_download_link(df[df['Statut_Sev'] == 'Seveso seuil haut'], 'df_statut_seveso_haut_all'), unsafe_allow_html=True)
# Show the table for 'Seveso seuil bas' counts
st.write("Counts of 'Seveso seuil bas' in Each Distance Category")
st.table(statut_seveso_bas_counts)
st.markdown(get_csv_download_link(df[df['Statut_Sev'] == 'Seveso seuil bas'], 'df_statut_seveso_bas_all'), unsafe_allow_html=True)


# Create a function to filter DataFrame based on selected interval
def filter_dataframe_by_interval(interval, statut):
    if statut == 'Statut_IED':
        return df[df['Distance'].between(interval.left, interval.right) & (df['Statut_IED'] == 'Oui')]
    elif statut == 'Seveso seuil haut':
        return df[df['Distance'].between(interval.left, interval.right) & (df['Statut_Sev'] == 'Seveso seuil haut')]
    elif statut == 'Seveso seuil bas':
        return df[df['Distance'].between(interval.left, interval.right) & (df['Statut_Sev'] == 'Seveso seuil bas')]
# Custom format function for the slider
def format_interval_value(value):
    return f"{value * 100}"

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
selected_interval_index = st.selectbox("Select an Interval:", options=interval_indices, format_func=format_interval_label)

selected_interval_left = distance_bins[selected_interval_index]
selected_interval_right = distance_bins[selected_interval_index + 1]


if st.button(f"Download Filtered Data for Interval {selected_interval_left} to {selected_interval_right} (Statut_IED)"):
    filtered_df_statut_ied = filter_dataframe_by_interval(pd.Interval(selected_interval_left, selected_interval_right), 'Statut_IED')
    st.markdown(get_csv_download_link(filtered_df_statut_ied, f'df_statut_ied_interval_{selected_interval_left}_{selected_interval_right}'), unsafe_allow_html=True)

if st.button(f"Download Filtered Data for Interval {selected_interval_left} to {selected_interval_right} (Seveso seuil haut)"):
    filtered_df_statut_seveso_haut = filter_dataframe_by_interval(pd.Interval(selected_interval_left, selected_interval_right), 'Seveso seuil haut')
    st.markdown(get_csv_download_link(filtered_df_statut_seveso_haut, f'df_statut_seveso_haut_interval_{selected_interval_left}_{selected_interval_right}'), unsafe_allow_html=True)

if st.button(f"Download Filtered Data for Interval {selected_interval_left} to {selected_interval_right} (Seveso seuil bas)"):
    filtered_df_statut_seveso_bas = filter_dataframe_by_interval(pd.Interval(selected_interval_left, selected_interval_right), 'Seveso seuil bas')
    st.markdown(get_csv_download_link(filtered_df_statut_seveso_bas, f'df_statut_seveso_haut_interval_{selected_interval_left}_{selected_interval_right}'), unsafe_allow_html=True)
