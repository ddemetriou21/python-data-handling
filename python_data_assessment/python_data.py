import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
import os
import openpyxl

'''
# returns the directory in which the script is located at 

script_directory = os.path.dirname(os.path.realpath(__file__))

folder_path = script_directory

# dictionary taking existing columns in the .xlsx files as keys and the value as the renamed columns
column_mapping = {
    'Model Year': 'Model Year',
    'Mfr Name': 'Mfr Name',
    'Division': 'Car Brand',
    'Carline': 'Model',
    'Eng Displ': 'Engine Displacement',
    '# Cyl': '# Cylinders',
    'Transmission': 'Transmission',
    'City FE (Guide) - Conventional Fuel': 'City FE',
    'Hwy FE (Guide) - Conventional Fuel': 'Highway FE',
    'Comb FE (Guide) - Conventional Fuel': 'Combined FE',
    'Air Aspiration Method Desc': 'Air Aspiration Method',
    'Trans Desc': 'Transmission Description',
    '# Gears': '# Gears',
    'Drive Desc': 'Drive Desc',
    'Carline Class Desc': 'Carline Class Desc',
    'Release Date': 'Release Date',
    'City CO2 Rounded Adjusted': 'City CO2',
    'Hwy CO2 Rounded Adjusted': 'Highway CO2',
    'Comb CO2 Rounded Adjusted (as shown on FE Label)': 'Combined CO2',
    'Fuel Usage Desc - Conventional Fuel': 'Fuel Usage',
    'MFR Calculated Gas Guzzler MPG ': 'Gas Guzzler MPG',
    'FE Rating (1-10 rating on Label)': 'FE Rating',
    'Stop/Start System (Engine Management System) Code': 'Stop/Start System',
    'Annual Fuel1 Cost - Conventional Fuel': 'Annual Fuel Cost'
}

# initializing 
cleaned_data_frames = []

for filename in os.listdir(folder_path):
    if filename.endswith('.xlsx'):
        file_path = os.path.join(folder_path, filename)

        columns_to_extract = list(column_mapping.keys())
        df = pd.read_excel(file_path, usecols=columns_to_extract)

        df.rename(columns=column_mapping, inplace=True)

        cleaned_data_frames.append(df)

consolidated_cleaned_data = pd.concat(cleaned_data_frames, ignore_index=True)

consolidated_cleaned_data.to_csv('2015-2024_cleaned_data.csv', index=False)
'''

data = pd.read_csv('2015-2024_cleaned_data.csv')

pivot0 = pd.pivot_table(data,
                        values='Combined FE',
                        index = 'Car Brand',
                        aggfunc = 'mean')

print(pivot0)

# finding the average Combined fuel efficiency of each car brand 
manufacturer_avg_fe = data.groupby('Car Brand')['Combined FE'].mean()

# Find the car brand with the highest average combined fuel economy
most_efficient_manufacturer = manufacturer_avg_fe.idxmax()

manufacturer_avg_fe = manufacturer_avg_fe.sort_values(ascending=False)

plt.figure(figsize=(10,6))
plt.plot(manufacturer_avg_fe.index, manufacturer_avg_fe.values, marker='.')
plt.xticks(rotation=90)
plt.xlabel('Car Brand')
plt.ylabel('Average Combined Fuel Economy')
plt.title('Average Combined Fuel Economy by Car Brand')
plt.grid(True)

plt.tight_layout()
plt.show()

pivot1 = pd.pivot_table(data,
                        values = 'Combined CO2',
                        index = 'Car Brand',
                        aggfunc = 'mean'
                        )

print(pivot1)

# finding the average combined CO2 emissions for each car brand
min_co2_by_brand = data.groupby('Car Brand')['Combined CO2'].mean()

# finding the car brand with the minimum average CO2 emissions
least_co2_brand = min_co2_by_brand.idxmin()

min_co2_by_brand = min_co2_by_brand.sort_values()

plt.figure(figsize=(10,6))

plt.plot(min_co2_by_brand.index, min_co2_by_brand.values, marker='.')

plt.xticks(rotation=90)
plt.xlabel('Car Brand')
plt.ylabel('Average Combined CO2 Emissions')
plt.title('Average Combined CO2 Emissions by Car Brand')
plt.grid(True)

plt.tight_layout()
plt.show()


avg_fe_by_brand = data.groupby('Car Brand')['Combined FE'].mean()
avg_displacement_by_brand = data.groupby('Car Brand')['Engine Displacement'].mean()

# Create a figure and a single subplot
fig, ax1 = plt.subplots(figsize=(10, 6))

# Plot Combined FE on the first y-axis (left)
ax1.bar(avg_fe_by_brand.index, avg_fe_by_brand.values, color='b', width=0.4, label='Combined FE')
ax1.set_ylabel('Combined FE')

# Create a second y-axis (right) sharing the same x-axis
ax2 = ax1.twinx()

# Plot Engine Displacement on the second y-axis (right)
ax2.plot(avg_displacement_by_brand.index, avg_displacement_by_brand.values, color='g', marker='o', label='Engine Displacement')
ax2.set_ylabel('Engine Displacement')

# Set labels, title, and customize x-axis tick labels rotation
plt.xlabel('Car Brand')
plt.title('Combined FE and Engine Displacement by Car Brand')
plt.xticks(rotation=90)

# Show the legend for both y-axes
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax2.legend(lines1 + lines2, labels1 + labels2, loc='upper left')

plt.tight_layout()
plt.grid(axis='y')
plt.show()


# Find the car brand with the highest average FE Rating
data['FE Rating'] = pd.to_numeric(data['FE Rating'], errors='coerce')

avg_fe_rating_by_car = data.groupby('Car Brand')['FE Rating'].mean()

best_car = avg_fe_rating_by_car.idxmax()
highest_avg_fe_rating = avg_fe_rating_by_car.max()

print(best_car)
print(f"The highest average FE Rating is: {highest_avg_fe_rating:.2f}")

avg_fe_rating_by_car = avg_fe_rating_by_car.sort_values(ascending=False)

plt.figure(figsize=(10,6))
plt.plot(avg_fe_rating_by_car.index, avg_fe_rating_by_car.values, marker='x')
plt.xticks(rotation=90)
plt.xlabel('Car Brand')
plt.ylabel('FE Rating')
plt.title('Average FE Rating by Car Brand')
plt.grid(True)

plt.tight_layout()
plt.show()


# displaying combined FE based on Drive Desc column, grouped by car brand
avg_fe_by_brand_drive = data.groupby(['Car Brand', 'Drive Desc'])['Combined FE'].mean().unstack()

ax = avg_fe_by_brand_drive.plot(kind='bar', figsize=(12, 6))

plt.xlabel('Car Brand')
plt.ylabel('Average Combined FE')
plt.title('Average Combined FE by Car Brand and Drive Desc')
plt.xticks(rotation=90)

plt.tight_layout()
plt.show()


avg_annual_fuel_cost_by_car = data.groupby('Car Brand')['Annual Fuel Cost'].mean()

# Find the car brand with the lowest average annual fuel cost
lowest_cost_brand = avg_annual_fuel_cost_by_car.idxmin()
lowest_avg_annual_fuel_cost = avg_annual_fuel_cost_by_car.min()

# Create a bar chart to visualize the results
plt.figure(figsize=(10, 6))
plt.bar(avg_annual_fuel_cost_by_car.index, avg_annual_fuel_cost_by_car.values, color='b')
plt.xlabel('Car Brand')
plt.ylabel('Average Annual Fuel Cost')
plt.title('Average Annual Fuel Cost by Car Brand')

# Highlight the car brand with the lowest annual fuel cost
plt.bar(lowest_cost_brand, lowest_avg_annual_fuel_cost, color='g', label=f'Lowest: {lowest_cost_brand}')

plt.legend()
plt.xticks(rotation=90)

plt.tight_layout()
plt.show()


avg_mpg_by_car = data.groupby('Car Brand')['Combined FE'].mean()

# Find the car brand with the best average MPG
best_mpg_brand = avg_mpg_by_car.idxmax()
best_avg_mpg = avg_mpg_by_car.max()

# Create a bar chart to visualize the results
plt.figure(figsize=(10, 6))
plt.bar(avg_mpg_by_car.index, avg_mpg_by_car.values, color='b')
plt.xlabel('Car Brand')
plt.ylabel('Average MPG (Combined FE)')
plt.title('Average MPG by Car Brand')

# Highlight the car brand with the best MPG
plt.bar(best_mpg_brand, best_avg_mpg, color='g', label=f'Best MPG: {best_mpg_brand}')

plt.legend()
plt.xticks(rotation=90)

plt.tight_layout()
plt.show()


data['Stop/Start System'] = data['Stop/Start System'].map({'N': 0, 'Y': 1})

# Calculate the average Combined FE for each car brand based on the Start/Stop System
avg_fe_by_start_stop = data.groupby(['Car Brand', 'Stop/Start System'])['Combined FE'].mean().unstack()

# Find the car brand with the best and worst average Combined FE based on Start/Stop System
best_start_stop_brand = avg_fe_by_start_stop[1].idxmax()  # 1 represents 'Y' (Yes)
worst_start_stop_brand = avg_fe_by_start_stop[1].idxmin()  # 1 represents 'Y' (Yes)

# Create a bar chart to visualize the results
plt.figure(figsize=(12, 6))
avg_fe_by_start_stop.plot(kind='bar', ax=plt.gca())
plt.xlabel('Car Brand')
plt.ylabel('Average Combined FE')
plt.title('Average Combined FE by Car Brand and Start/Stop System')
plt.xticks(rotation=90)

plt.legend()
plt.tight_layout()
plt.show()


avg_fe_by_gears = data.groupby(['Car Brand', '# Gears'])['Combined FE'].mean().unstack()

# Create a bar chart to visualize the results
plt.figure(figsize=(12, 6))
avg_fe_by_gears.plot(kind='bar', ax=plt.gca())
plt.xlabel('Car Brand')
plt.ylabel('Average Combined FE')
plt.title('Average Combined FE by Car Brand and Number of Gears')
plt.xticks(rotation=45)

plt.tight_layout()
plt.show()