import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Directory containing the CSV files
directory = '/Users/Mingda/Library/Mobile Documents/com~apple~CloudDocs/Documents/UCLA/Research/Github/VRColorTraining/Assets/Data/'

# Output directory for histograms
output_directory = os.path.join(directory, 'histograms')
os.makedirs(output_directory, exist_ok=True)

# Loop through each file in the directory
for filename in os.listdir(directory):
    if filename.endswith('.csv'):
        file_path = os.path.join(directory, filename)
        
        # Load the CSV file
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

        # Subtract 140 ms
        filtered_data['AdjustedReactionTime_ObjectShowTime'] = filtered_data['ReactionTime_ObjectShowTime'] - 140

        # Calculate mean and standard deviation
        mean_value = filtered_data['AdjustedReactionTime_ObjectShowTime'].mean()
        std_deviation = filtered_data['AdjustedReactionTime_ObjectShowTime'].std()

        # Calculate the bin width and the number of bins
        bin_width = 25
        min_value = filtered_data['AdjustedReactionTime_ObjectShowTime'].min()
        max_value = filtered_data['AdjustedReactionTime_ObjectShowTime'].max()
        num_bins = int((max_value - min_value) / bin_width) + 1

        # Plot the histogram with seaborn
        plt.figure(figsize=(10, 6))
        sns.histplot(filtered_data['AdjustedReactionTime_ObjectShowTime'], bins=num_bins, kde=True)
        plt.axvline(mean_value, color='r', linestyle='dashed', linewidth=1, label=f'Mean: {mean_value:.2f} ms')
        plt.axvline(mean_value + std_deviation, color='g', linestyle='dashed', linewidth=1, label=f'Standard Deviation: {std_deviation:.2f} ms')
        plt.axvline(mean_value - std_deviation, color='g', linestyle='dashed', linewidth=1)
        plt.title(f'Histogram of Adjusted Reaction Time - Object Show Time (with Seaborn) for {filename}')
        plt.xlabel('Adjusted Reaction Time - Object Show Time (ms)')
        plt.ylabel('Frequency')
        plt.legend()
        plt.grid(True)
        plt.xlim(0, 500)
        
        # Save the plot as an image file
        plot_file_path = os.path.join(output_directory, f'{filename[:-4]}_histogram.png')
        plt.savefig(plot_file_path)
        plt.close()

        # Output mean and standard deviation
        print(f"File: {filename}")
        print(f"Mean: {mean_value:.2f} ms")
        print(f"Standard Deviation: {std_deviation:.2f} ms")
