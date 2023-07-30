import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load data from CSV file
df = pd.read_csv('your_file.csv')

# Define distance bins
distance_bins = list(range(0, 600, 100)) + [np.inf]  # Up to 500m and then >500m

# Categorize distances into bins
df['distance_category'] = pd.cut(df['Distance'], bins=distance_bins, labels=['0-100m', '100-200m', '200-300m', '300-400m', '400-500m', '>500m'])

# Create histogram for distance categories
hist_data = df['distance_category'].value_counts().sort_index()

# Calculate proportions for 'Statut_IED' and 'Statut_Seveso' in each distance category
statut_ied_proportions = df[df['Statut_IED'] == 'Oui']['distance_category'].value_counts(normalize=True).sort_index()
statut_seveso_proportions = df[df['Statut_Seveso'] == 'Seveso']['distance_category'].value_counts(normalize=True).sort_index()

# Plot the histogram
fig, ax = plt.subplots()
bars = ax.bar(hist_data.index, hist_data.values, label='Total')

# Plot the proportions of 'Statut_IED' in each distance category
bars_statut_ied = ax.bar(statut_ied_proportions.index, statut_ied_proportions.values * hist_data.values,
                        label='Statut_IED', alpha=0.7)

# Plot the proportions of 'Statut_Seveso' in each distance category
bars_statut_seveso = ax.bar(statut_seveso_proportions.index, statut_seveso_proportions.values * hist_data.values,
                           label='Statut_Seveso', alpha=0.7)

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
