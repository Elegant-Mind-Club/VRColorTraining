import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the uploaded CSV file
file_path = '/Users/Mingda/Library/Mobile Documents/com~apple~CloudDocs/Documents/UCLA/Research/Github/VRColorTraining/Data/2 Choice/Anjali-rtData-2024-06-26-12-54-50.csv'
data = pd.read_csv(file_path)

# Filter out the false trials
data = data[data['Correct'] == True]

# Create an array of reaction time - object show time
data['ReactionTime_ObjectShowTime'] = data['ReactionTime'] - data['ObjShowTime']

# Subtract 50 ms from all of the reaction times
data['AdjustedReactionTime_ObjectShowTime'] = data['ReactionTime_ObjectShowTime'] - 50

# Separate the data by stimulus type
red_circle_data = data[data['StimType'] == 'redCircle']
green_circle_data = data[data['StimType'] == 'greenCircle']
yellow_circle_data = data[data['StimType'] == 'yellowCircle']

# Function to remove outliers using the IQR method
def remove_outliers(data):
    Q1 = data.quantile(0.25)
    Q3 = data.quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    return data[(data >= lower_bound) & (data <= upper_bound)]

# Remove outliers for each group
red_circle_data_filtered = remove_outliers(red_circle_data['AdjustedReactionTime_ObjectShowTime'])
green_circle_data_filtered = remove_outliers(green_circle_data['AdjustedReactionTime_ObjectShowTime'])
yellow_circle_data_filtered = remove_outliers(yellow_circle_data['AdjustedReactionTime_ObjectShowTime'])

# Calculate mean and standard deviation for each group
red_mean = red_circle_data_filtered.mean()
red_std = red_circle_data_filtered.std()

green_mean = green_circle_data_filtered.mean()
green_std = green_circle_data_filtered.std()

yellow_mean = yellow_circle_data_filtered.mean()
yellow_std = yellow_circle_data_filtered.std()

# Plot the histogram for all three groups in one graph
plt.figure(figsize=(12, 8))

bin_width = 25
bin_edges_red = range(int(red_circle_data['AdjustedReactionTime_ObjectShowTime'].min()), 
                  int(red_circle_data['AdjustedReactionTime_ObjectShowTime'].max()) + bin_width, 
                  bin_width)
bin_edges_green = range(int(green_circle_data['AdjustedReactionTime_ObjectShowTime'].min()), 
                  int(green_circle_data['AdjustedReactionTime_ObjectShowTime'].max()) + bin_width, 
                  bin_width)
bin_edges_yellow = range(int(yellow_circle_data['AdjustedReactionTime_ObjectShowTime'].min()), 
                  int(yellow_circle_data['AdjustedReactionTime_ObjectShowTime'].max()) + bin_width, 
                  bin_width)
sns.histplot(red_circle_data_filtered, bins=bin_edges_red, kde=True, color='red', label='Red Circle')
sns.histplot(green_circle_data_filtered, bins=bin_edges_green, kde=True, color='green', label='Green Circle')
sns.histplot(yellow_circle_data_filtered, bins=bin_edges_yellow, kde=True, color='yellow', label='Yellow Circle')

# Plot mean and standard deviation for each group
plt.axvline(red_mean, color='darkred', linestyle='solid', linewidth=2, label=f'Red Mean: {red_mean:.2f} ms')
plt.axvline(red_mean + red_std, color='lightcoral', linestyle='dashed', linewidth=1, label=f'Red Std Dev: {red_std:.2f} ms')
plt.axvline(red_mean - red_std, color='lightcoral', linestyle='dashed', linewidth=1)

plt.axvline(green_mean, color='darkgreen', linestyle='solid', linewidth=2, label=f'Green Mean: {green_mean:.2f} ms')
plt.axvline(green_mean + green_std, color='lightgreen', linestyle='dashed', linewidth=1, label=f'Green Std Dev: {green_std:.2f} ms')
plt.axvline(green_mean - green_std, color='lightgreen', linestyle='dashed', linewidth=1)

plt.axvline(yellow_mean, color='goldenrod', linestyle='solid', linewidth=2, label=f'Yellow Mean: {yellow_mean:.2f} ms')
plt.axvline(yellow_mean + yellow_std, color='yellow', linestyle='dashed', linewidth=1, label=f'Yellow Std Dev: {yellow_std:.2f} ms')
plt.axvline(yellow_mean - yellow_std, color='yellow', linestyle='dashed', linewidth=1)

# Add labels and title
plt.title('Histogram of Adjusted Reaction Time - Object Show Time by Stimulus Type')
plt.xlabel('Adjusted Reaction Time - Object Show Time (ms)')
plt.ylabel('Frequency')
plt.legend()
plt.grid(True)
plt.xlim(0, 500)
plt.show()

# Output mean and standard deviation for all three groups
(red_mean, red_std), (green_mean, green_std), (yellow_mean, yellow_std)