import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load data from CSV file
df = pd.read_csv('https://raw.githubusercontent.com/olivierparrot01/ICPE/main/1geocodage.csv')              
df=df.loc(df['result_sco']>0.5)
# Define distance bins (up to 1000m in 100m intervals, then >1000m)
distance_bins = list(range(0, 1100, 100)) + [np.inf]

# Categorize distances into bins
df['distance_category'] = pd.cut(df['Distance'], bins=distance_bins, labels=['0-100m', '100-200m', '200-300m', '300-400m', '400-500m', '500-600m', '600-700m', '700-800m', '800-900m', '900-1000m', '>1000m'])

# Create histogram for distance categories
hist_data = df['distance_category'].value_counts().sort_index()

# Calculate proportions for 'Statut_IED' and 'Statut_Seveso' in each distance category
statut_ied_proportions = df[df['Statut_IED'] == 'Oui']['distance_category'].value_counts(normalize=True).sort_index()
statut_seveso_haut_proportions = df[df['Statut_Sev'] == 'Seveso seuil haut']['distance_category'].value_counts(normalize=True).sort_index()
statut_seveso_bas_proportions = df[df['Statut_Sev'] == 'Seveso seuil bas']['distance_category'].value_counts(normalize=True).sort_index()

# Plot the histogram
fig, ax = plt.subplots()
bars = ax.bar(hist_data.index, hist_data.values, label='Total')

# Plot the proportions of 'Statut_IED' in each distance category
bars_statut_ied = ax.bar(statut_ied_proportions.index, statut_ied_proportions.values * hist_data.values,
                        label='Statut_IED', alpha=0.7)

# Plot the proportions of 'Seveso seuil haut' in each distance category
bars_statut_seveso_haut = ax.bar(statut_seveso_haut_proportions.index, statut_seveso_haut_proportions.values * hist_data.values,
                                label='Seveso seuil haut', alpha=0.7)

# Plot the proportions of 'Seveso seuil bas' in each distance category
bars_statut_seveso_bas = ax.bar(statut_seveso_bas_proportions.index, statut_seveso_bas_proportions.values * hist_data.values,
                               label='Seveso seuil bas', alpha=0.7)

# Add labels to the bars
for bar in bars:
    height = bar.get_height()
    ax.annotate('{}'.format(height),
                xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 3),  # 3 points vertical offset
                textcoords="offset points",
                ha='center', va='bottom')

# Customize the plot
plt.xlabel('Distance')
plt.ylabel('Count')
plt.title('Distance Histogram with Statut Proportions')
plt.xticks(rotation=45)
plt.legend()

# Show the plot in Streamlit
st.pyplot(fig)

# Display numerical values below the bars
st.write('Counts:')
st.write(hist_data)
st.write('Proportions of Statut_IED:')
st.write(statut_ied_proportions * 100)
st.write('Proportions of Seveso seuil haut:')
st.write(statut_seveso_haut_proportions * 100)
st.write('Proportions of Seveso seuil bas:')
st.write(statut_seveso_bas_proportions * 100)
