# -*- coding: utf-8 -*-
"""
Created on Wed Jun 12 15:01:27 2024

@author: naqavi
"""
import pandas as pd
from pyproj import Proj, transform

# Load the CSV file into a DataFrame
csv_path = r'C:\Users\naqavi\OneDrive - KTH\!MATSim\Sthlm-try1\OUTPUTS\output-innovation-0.6\output_events\activities.csv'

df = pd.read_csv(csv_path)

# Define the source and destination coordinate reference systems (CRS)
crs_source = Proj(init='epsg:3006')
crs_dest = Proj(init='epsg:3857')

# Convert each coordinate pair from EPSG 3006 to EPSG 3857
x_new, y_new = transform(crs_source, crs_dest, df['x'].values, df['y'].values)

# Add the new columns to the DataFrame
df['x_new'] = x_new
df['y_new'] = y_new

# Save the DataFrame to a new CSV file
df.to_csv(r'C:\Users\naqavi\OneDrive - KTH\!MATSim\Sthlm-try1\OUTPUTS\output-innovation-0.6\output_events\converted_coordinates.csv', index=False)
