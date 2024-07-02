import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.optimize import curve_fit
import numpy as np

# Load the uploaded CSV file
file_path = '/Users/Mingda/Library/Mobile Documents/com~apple~CloudDocs/Documents/UCLA/Research/Github/VRColorTraining/Data/Reflex/deborah-rtData-2024-06-24-11-57-49.csv'
data = pd.read_csv(file_path)

# Remove any false trials (where the correct column is False)
data = data[data['Correct'] != False]

# Create an array of reaction time - object show time
data['ReactionTime_ObjectShowTime'] = data['ReactionTime'] - data['ObjShowTime']

# Remove outliers using the IQR method
Q1 = data['ReactionTime_ObjectShowTime'].quantile(0.25)
Q3 = data['ReactionTime_ObjectShowTime'].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

filtered_data = data[(data['ReactionTime_ObjectShowTime'] >= lower_bound) & (data['ReactionTime_ObjectShowTime'] <= upper_bound)].copy()

# Subtract 50 ms
filtered_data['AdjustedReactionTime_ObjectShowTime'] = filtered_data['ReactionTime_ObjectShowTime'] - 50

# Calculate mean and standard deviation
mean_value = filtered_data['AdjustedReactionTime_ObjectShowTime'].mean()
std_deviation = filtered_data['AdjustedReactionTime_ObjectShowTime'].std()

# Define Gaussian function
def gaussian(x, amp, mu, sigma):
    return amp * np.exp(- (x - mu) ** 2 / (2 * sigma ** 2))

# Histogram data
hist, bin_edges = np.histogram(filtered_data['AdjustedReactionTime_ObjectShowTime'], bins=range(int(filtered_data['AdjustedReactionTime_ObjectShowTime'].min()), 
                  int(filtered_data['AdjustedReactionTime_ObjectShowTime'].max()) + 25, 25), density=True)

bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2

# Fit Gaussian
popt, pcov = curve_fit(gaussian, bin_centers, hist, p0=[1, mean_value, std_deviation])

# Extract the mean and standard deviation of the fitted Gaussian
fitted_amp, fitted_mean, fitted_std = popt

# Output mean and standard deviation
print(f"Mean: {mean_value:.2f} ms")
print(f"Standard Deviation: {std_deviation:.2f} ms")

# Output mean and standard deviation of the fitted Gaussian
print(f"Fitted Gaussian Mean: {fitted_mean:.2f} ms")
print(f"Fitted Gaussian Standard Deviation: {fitted_std:.2f} ms")

# Plot the histogram and the fitted Gaussian
plt.figure(figsize=(10, 6))
sns.histplot(filtered_data['AdjustedReactionTime_ObjectShowTime'], bins=bin_edges, kde=False, color='#FF8080', stat='density')
plt.axvline(mean_value, color='#800000', linestyle='solid', linewidth=1, label=f'Mean: {mean_value:.2f} ms')
plt.axvline(mean_value + std_deviation, color='#FF0000', linestyle='dashed', linewidth=1, label=f'Standard Deviation: {std_deviation:.2f} ms')
plt.axvline(mean_value - std_deviation, color='#FF0000', linestyle='dashed', linewidth=1)

# Plot Gaussian fit
x_fit = np.linspace(mean_value - 4*std_deviation, mean_value + 4*std_deviation, 1000)
y_fit = gaussian(x_fit, *popt)
plt.plot(x_fit, y_fit, color='#FF0000', linewidth=2, label=f'Gaussian Fit: μ = {fitted_mean:.2f} ms, σ = {fitted_std:.2f} ms')

plt.title('Histogram for Red Stimulus Reaction Time with Gaussian Fit')
plt.xlabel('Reaction Time (ms)')
plt.ylabel('Frequency Density')
plt.legend()
plt.grid(False)
plt.xlim(0, 600)
plt.show()
