import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the uploaded CSV file
file_path = 'c:/Users/metpe/OneDrive/Documents/GitHub/VRColorTraining/Assets/Data/Metztli-rtData-2024-06-26-12-18-00.csv'
data = pd.read_csv(file_path)

# Create an array of reaction time - object show time
data['ReactionTime_ObjectShowTime'] = data['ReactionTime'] - data['ObjShowTime']

# Remove outliers using the IQR method
Q1 = data['ReactionTime_ObjectShowTime'].quantile(0.25)
Q3 = data['ReactionTime_ObjectShowTime'].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

filtered_data = data[(data['ReactionTime_ObjectShowTime'] >= lower_bound) & (data['ReactionTime_ObjectShowTime'] <= upper_bound)]

# Subtract 150 ms
filtered_data['AdjustedReactionTime_ObjectShowTime'] = filtered_data['ReactionTime_ObjectShowTime'] - 50

# Calculate mean and standard deviation
mean_value = filtered_data['AdjustedReactionTime_ObjectShowTime'].mean()
std_deviation = filtered_data['AdjustedReactionTime_ObjectShowTime'].std()

# Plot the histogram with seaborn
plt.figure(figsize=(10, 6))
bin_width = 25
bin_edges = range(int(filtered_data['AdjustedReactionTime_ObjectShowTime'].min()), 
                  int(filtered_data['AdjustedReactionTime_ObjectShowTime'].max()) + bin_width, 
                  bin_width)
sns.histplot(filtered_data['AdjustedReactionTime_ObjectShowTime'], bins=bin_edges, kde=True)
plt.axvline(mean_value, color='r', linestyle='dashed', linewidth=1, label=f'Mean: {mean_value:.2f} ms')
plt.axvline(mean_value + std_deviation, color='g', linestyle='dashed', linewidth=1, label=f'Standard Deviation: {std_deviation:.2f} ms')
plt.axvline(mean_value - std_deviation, color='g', linestyle='dashed', linewidth=1)
plt.title('Histogram of Adjusted Reaction Time - Object Show Time (with Seaborn)')
plt.xlabel('Adjusted Reaction Time - Object Show Time (ms)')
plt.ylabel('Frequency')
plt.legend()
plt.grid(True)
plt.xlim(0, 500)
plt.show()

# Output mean and standard deviation
print(f"Mean: {mean_value:.2f} ms")
print(f"Standard Deviation: {std_deviation:.2f} ms")
