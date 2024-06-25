import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import glob
import os
from scipy import stats

# Define the folder path containing the .csv files
folder_path = '/Users/Mingda/Library/Mobile Documents/com~apple~CloudDocs/Documents/UCLA/Research/Github/VRColorTraining/Assets/Data/'

# Get a list of all .csv files in the folder
csv_files = glob.glob(os.path.join(folder_path, '*.csv'))

# Initialize a list to hold all dataframes
all_data = []

# Load and process each .csv file
for file_path in csv_files:
    data = pd.read_csv(file_path)
    
    # Calculate (reaction time - objshowtime) and add it as a new column
    data['RT_minus_ObjShowTime'] = data['ReactionTime'] - data['ObjShowTime']
    
    # Create a trial number column
    data['TrialNumber'] = data.index + 1
    
    # Add a column to indicate the file name (useful for distinguishing data from different files)
    data['FileName'] = os.path.basename(file_path)
    
    # Append the dataframe to the list
    all_data.append(data)

# Concatenate all dataframes into one
combined_data = pd.concat(all_data, ignore_index=True)

# Remove outliers using the Z-score method
z_scores = stats.zscore(combined_data['RT_minus_ObjShowTime'])
abs_z_scores = np.abs(z_scores)
filtered_entries = (abs_z_scores < 3)  # Adjust the threshold as needed
filtered_data = combined_data[filtered_entries]

# Plotting the scatter plot with individual best fit lines for each file
plt.figure(figsize=(12, 6))

# Using seaborn's lmplot to create individual trendlines for each participant
sns.lmplot(x='TrialNumber', y='RT_minus_ObjShowTime', hue='FileName', data=filtered_data, height=6, aspect=2, ci=None, scatter_kws={'s': 50}, line_kws={'lw': 2})

plt.xlim(0, filtered_data['TrialNumber'].max() + 1)
plt.ylim(0, 500)
plt.xlabel('Trial Number')
plt.ylabel('Reaction Time - Object Show Time')
plt.title('Reaction Time Minus Object Show Time by Trial Number with Individual Best Fit Lines (Outliers Removed)')
plt.show()
