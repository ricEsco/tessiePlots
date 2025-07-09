import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

'''
This script loads a CSV file containing data from a various coldbox parameters in the following format:
date,T-air,RH,DP,T-water,powerState[8],Vset[8],Tset[8],T-module[8]

T-module[8] corresponds to the 8 temperature readouts of the TECs.
The script then plots the temperature data of each TEC over time on the same plot.

The input CSV file needs to be in the same directory as this script.
'''

# Load the CSV file without headers
fname = input("Enter the filename (without extension): ")
file_path = f'input/{fname}.csv'
data = pd.read_csv(file_path, header=None)

# Assign column names based on the provided format
column_names = ['date', 'T-air', 'RH', 'DP', 'T-water'] + \
               [f'powerState[{i}]' for i in range(8)] + \
               [f'Vset[{i}]' for i in range(8)] + \
               [f'Tset[{i}]' for i in range(8)] + \
               [f'T-module[{i}]' for i in range(8)]
data.columns = column_names

# Parse the date column and set as the index
data['date'] = pd.to_datetime(data['date'], format='%Y/%m/%d_%H:%M:%S.%f')
data.set_index('date', inplace=True)
# Specify the desired time interval (e.g., '1H' for hourly, '30min' for 30 minutes)
time_resolution = '1min'
data_resampled = data.resample(time_resolution).mean()

# Extract the 8 temperature columns
temperature_columns = [f'T-module[{i}]' for i in range(8)]
legend_labels = [f'TEC{i+1}' for i in range(8)]

# Apply a rolling mean to smooth the data
rolling_window = 10  # Adjust the window size as needed
data_smoothed = data[temperature_columns].rolling(window=rolling_window).mean()

# Plot the data
plt.figure(figsize=(12, 6))
for temp_col, label in zip(temperature_columns, legend_labels):
    plt.plot(data.index, data_smoothed[temp_col], label=label)  # Use the smoothed data for plotting

# x-axis
plt.xlabel('Time')
plt.xticks(rotation=45)

# alternative for shorter time intervals
plt.gca().xaxis.set_major_locator(mdates.SecondLocator(interval=60))  # Set major ticks at 30-second intervals
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))  # Format the labels as HH:MM:SS

#y-axis
plt.ylabel('Temperature (°C)')
y_max = -20
y_min = -32
y_interval = 1
plt.yticks(range(y_min, y_max + 1, y_interval))

Tset_str = -30
plt.title(f'Temp_Set = {Tset_str}C')
plt.legend()
plt.grid(True)

# Save
output_file = f'plots/T={Tset_str}C_allLoadedMockups_zoomed4.png'
plt.savefig(output_file, dpi=300, bbox_inches='tight')
plt.show()