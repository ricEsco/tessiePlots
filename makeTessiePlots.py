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
data = pd.read_csv(file_path, header=None, low_memory=False)

# Assign column names based on the provided format
column_names = ['date', 'T-air', 'RH', 'DP', 'T-water'] + \
               [f'powerState[{i}]' for i in range(8)] + \
               [f'Vset[{i}]' for i in range(8)] + \
               [f'Tset[{i}]' for i in range(8)] + \
               [f'T-module[{i}]' for i in range(8)]
data.columns = column_names

# Parse the date column
data['date'] = pd.to_datetime(data['date'], format='%Y/%m/%d_%H:%M:%S.%f')
data.set_index('date', inplace=True)
time_resolution = '1min'
data_resampled = data.resample(time_resolution).mean()

# Extract the 8 temperature columns
temperature_columns = [f'T-module[{i}]' for i in range(8)]
legend_labels = [f'TEC{i+1}' for i in range(8)]

# Plot the data
plt.figure(figsize=(12, 6))
for temp_col, label in zip(temperature_columns, legend_labels):
    plt.plot(data.index, data[temp_col], label=label)  # Use the original time data for plotting

# x-axis
plt.xlabel('Time')
plt.xticks(rotation=45)

# Format the x-axis for better readability
plt.gca().xaxis.set_major_locator(mdates.MinuteLocator(interval=5))  # Set major ticks at n-minute intervals
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))  # Format the labels as HH:MM

#y-axis
plt.ylabel('Temperature (°C)')
y_min = (int(data[temperature_columns].min().min()) // 5) * 5
y_max = ((int(data[temperature_columns].max().max()) + 4) // 5) * 5  # Add 4 to ensure rounding up
y_interval = 1 if y_max - y_min <= 10 else 5
plt.yticks(range(y_min, y_max + 1, y_interval))

Tset_str = -35
plt.title(f'Temp_Set = {Tset_str}C')
plt.legend()
plt.grid(True)

# Save
output_file = f'plots/T={Tset_str}C_actualmodules.png'
plt.savefig(output_file, dpi=300, bbox_inches='tight')
plt.show()