import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.optimize import curve_fit
import numpy as np

# Load the uploaded CSV file
file_path = '/Users/Mingda/Library/Mobile Documents/com~apple~CloudDocs/Documents/UCLA/Research/Github/VRColorTraining/Data/2 Choice/Alex-rtData-2024-06-27-14-26-09.csv'
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

# Define Gaussian function
def gaussian(x, amp, mu, sigma):
    return amp * np.exp(- (x - mu) ** 2 / (2 * sigma ** 2))

# Create a figure
plt.figure(figsize=(10, 6))

# Plot for redCircle trials
red_trials = filtered_data[filtered_data['StimType'] == 'redCircle']
mean_red = red_trials['AdjustedReactionTime_ObjectShowTime'].mean()
std_red = red_trials['AdjustedReactionTime_ObjectShowTime'].std()

# Histogram data for redCircle
hist_red, bin_edges_red = np.histogram(red_trials['AdjustedReactionTime_ObjectShowTime'], bins=range(int(red_trials['AdjustedReactionTime_ObjectShowTime'].min()), 
                  int(red_trials['AdjustedReactionTime_ObjectShowTime'].max()) + 25, 25), density=True)

bin_centers_red = (bin_edges_red[:-1] + bin_edges_red[1:]) / 2

# Fit Gaussian for redCircle
popt_red, _ = curve_fit(gaussian, bin_centers_red, hist_red, p0=[1, mean_red, std_red])

# Extract the mean and standard deviation of the fitted Gaussian for redCircle
fitted_amp_red, fitted_mean_red, fitted_std_red = popt_red

# Plot the histogram and the fitted Gaussian for redCircle
sns.histplot(red_trials['AdjustedReactionTime_ObjectShowTime'], bins=bin_edges_red, kde=False, color='#FF8080', stat='density')
plt.axvline(mean_red, color='#800000', linestyle='solid', linewidth=1, label=f'Mean: {mean_red:.2f} ms')
plt.axvline(mean_red + std_red, color='#FF0000', linestyle='dashed', linewidth=1, label=f'Standard Deviation: {std_red:.2f} ms')
plt.axvline(mean_red - std_red, color='#FF0000', linestyle='dashed', linewidth=1)

# Plot Gaussian fit for redCircle
x_fit_red = np.linspace(mean_red - 4*std_red, mean_red + 4*std_red, 1000)
y_fit_red = gaussian(x_fit_red, *popt_red)
plt.plot(x_fit_red, y_fit_red, color='#FF0000', linewidth=2, label=f'Gaussian Fit: μ = {fitted_mean_red:.2f} ms, σ = {fitted_std_red:.2f} ms')

plt.title('Histogram for Red Stimulus Reaction Time with Gaussian Fit')
plt.xlabel('Reaction Time (ms)')
plt.ylabel('Frequency Density')
plt.legend()
plt.grid(False)
plt.xlim(0, 600)

# Plot for greenCircle trials
green_trials = filtered_data[filtered_data['StimType'] == 'greenCircle']
mean_green = green_trials['AdjustedReactionTime_ObjectShowTime'].mean()
std_green = green_trials['AdjustedReactionTime_ObjectShowTime'].std()

# Histogram data for greenCircle
hist_green, bin_edges_green = np.histogram(green_trials['AdjustedReactionTime_ObjectShowTime'], bins=range(int(green_trials['AdjustedReactionTime_ObjectShowTime'].min()), 
                  int(green_trials['AdjustedReactionTime_ObjectShowTime'].max()) + 25, 25), density=True)

bin_centers_green = (bin_edges_green[:-1] + bin_edges_green[1:]) / 2

# Fit Gaussian for greenCircle
popt_green, _ = curve_fit(gaussian, bin_centers_green, hist_green, p0=[1, mean_green, std_green])

# Extract the mean and standard deviation of the fitted Gaussian for greenCircle
fitted_amp_green, fitted_mean_green, fitted_std_green = popt_green

# Plot the histogram and the fitted Gaussian for greenCircle
sns.histplot(green_trials['AdjustedReactionTime_ObjectShowTime'], bins=bin_edges_green, kde=False, color='#80FF80', stat='density')
plt.axvline(mean_green, color='#008000', linestyle='solid', linewidth=1, label=f'Mean: {mean_green:.2f} ms')
plt.axvline(mean_green + std_green, color='#00FF00', linestyle='dashed', linewidth=1, label=f'Standard Deviation: {std_green:.2f} ms')
plt.axvline(mean_green - std_green, color='#00FF00', linestyle='dashed', linewidth=1)

# Plot Gaussian fit for greenCircle
x_fit_green = np.linspace(mean_green - 4*std_green, mean_green + 4*std_green, 1000)
y_fit_green = gaussian(x_fit_green, *popt_green)
plt.plot(x_fit_green, y_fit_green, color='#00FF00', linewidth=2, label=f'Gaussian Fit: μ = {fitted_mean_green:.2f} ms, σ = {fitted_std_green:.2f} ms')

plt.title('Histogram for Red and Green Reaction Time')
plt.xlabel('Reaction Time (ms)')
plt.ylabel('Frequency Density')
plt.legend()
plt.grid(False)
plt.xlim(0, 600)

plt.tight_layout()
plt.show()
