# -*- coding: utf-8 -*-
"""
Created on Wed Jul 24 09:40:47 2024

@author: naqavi
"""
import gzip
import xml.etree.ElementTree as ET
import csv
import pandas as pd
import ast
import matplotlib.pyplot as plt
import os

#%%

folder = r"C:\Users\naqavi\OneDrive - KTH\!MATSim\Sthlm-try1\OUTPUTS"

run = r"output_with_experienced_plans"
#run = r"22July"

relative_path_input = r"output\output_experienced_plans.xml.gz"
relative_path_output = r"output\output_experienced_plans.csv"
relative_path_output_path = r"output\output_experienced_plans_clean.csv"

path = os.path.join(folder, run, relative_path_input)
output = os.path.join(folder, run, relative_path_output)
output_path = os.path.join(folder, run, relative_path_output_path)

#%%
# Function to read and parse the compressed XML file iteratively and get the root and its children
def iterparse_gzipped_xml(file_path):
    with gzip.open(file_path, 'rb') as f:
        context = ET.iterparse(f, events=('start', 'end'))
        context = iter(context)
        root = None
        children = []

        for event, elem in context:
            if event == 'start' and root is None:
                root = elem  # First start event is the root
            elif event == 'end' and root is not None:
                if elem.tag == root.tag:
                    break  # Stop once the root's end event is encountered
                children.append(elem)
                root.clear()  # Clear the root to free memory

        return root, children

# Function to write the root and children to a CSV file
def write_to_csv(output_file_path, root, children):
    with open(output_file_path, mode='w', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        
        # Write header
        csvwriter.writerow(['tag', 'attrib'])

        # Write root information
        csvwriter.writerow([root.tag, root.attrib])

        # Write children information
        for child in children:
            csvwriter.writerow([child.tag, child.attrib])

# Get the root and its immediate children
root, children = iterparse_gzipped_xml(path)

# Write to CSV
if root is not None:
    write_to_csv(output, root, children)
else:
    print("Root not found")
    
    
#%%
    


# Read the CSV file
input_file_path = output

df = pd.read_csv(input_file_path)

# Parse the 'attrib' column which contains dictionaries
def parse_attrib(attrib_str):
    try:
        return ast.literal_eval(attrib_str)
    except (ValueError, SyntaxError):
        return {}

# Apply the function to the 'attrib' column
attrib_dicts = df['attrib'].apply(parse_attrib)

# Create a DataFrame from the list of dictionaries
attrib_df = pd.json_normalize(attrib_dicts)

# Concatenate the original 'tag' column with the new DataFrame
result_df = pd.concat([df['tag'], attrib_df], axis=1)

# Display the result
print(result_df.head())
result_df = result_df[result_df.tag != "population"]
result_df = result_df[result_df.tag != "attribute"]
result_df = result_df[result_df.tag != "attributes"]
result_df = result_df.drop(['class', 'name', 'vehicleRefId',], axis=1)

result_df.to_csv(output_path, index=False)

#%%

df = pd.read_csv(output_path)

modes = df['mode'].value_counts().reset_index()

types = df['type'].value_counts().reset_index()
