import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load data from CSV file
df = pd.read_csv('your_file.csv')

# Define distance bins
distance_bins = list(range(0, 600, 100)) + [np.inf]  # Up to 500m and then >500m

# Categorize distances into bins
df['distance_category'] = pd.cut(df['distance'], bins=distance_bins, labels=['0-100m', '100-200m', '200-300m', '300-400m', '400-500m', '>500m'])

# Create histogram
hist_data = df['distance_category'].value_counts().sort_index()

# Plot the histogram
plt.bar(hist_data.index, hist_data.values)
plt.xlabel('Distance')
plt.ylabel('Count')
plt.title('Distance Histogram')
plt.xticks(rotation=45)

# Add labels to the bars
for i in range(len(hist_data)):
    plt.text(i, hist_data[i], str(hist_data[i]), ha='center', va='bottom')

# Show the plot in Streamlit
st.pyplot(plt)
