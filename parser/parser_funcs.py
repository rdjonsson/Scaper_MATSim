# -*- coding: utf-8 -*-
"""
Created on Fri May  3 11:36:21 2024

@author: naqavi
"""


import csv
from lxml import etree
import ast
import pandas as pd
import os

def get_directory(isItInput):
    
    if isItInput:
        folder = 'input'
        current_directory = r"C:\Users\naqavi\OneDrive - KTH\!MATSim\Sthlm-try1\visualizations\visualization"
        input_file_path = r"C:\Users\naqavi\OneDrive - KTH\!MATSim\Sthlm-try1\input_files\large_scale\matsim-plans-2040_25b.xml"
    else: 
        folder = 'output'
        current_directory = os.getcwd()
        input_file_path = os.path.join(current_directory, f'{folder}\output_plans_SpeedyAlt.xml')
        
    return (folder, current_directory, input_file_path)

#%%

def extract_plan_info(person_id, plan):
    """
    Extracts information from a plan element in the XML.
    
    Parameters:
    - person_id: ID of the person the plan belongs to.
    - plan: The plan XML element.
    
    Returns:
    A dictionary containing the extracted information.
    """

    activities = plan.findall('activity')
    mode_sequence = []
    activity_info = []
    for activity in activities:
        #print(activity.attrib.get('end_time',''))
        mode_sequence.append(activity.attrib['type'])
        activity_info.append({
            'type': activity.attrib['type'],
            'end_time': activity.attrib.get('end_time', '')
        })
    
        
    legs = plan.findall('leg')
    leg_modes = []
    leg_info = []
    for leg in legs:
        leg_mode = leg.attrib['mode']
        leg_modes.append(leg_mode)
        leg_attributes = {'mode': leg_mode}
        for attribute in leg.findall('attributes/attribute'):
            leg_attributes[attribute.attrib['name']] = attribute.text
        route = leg.find('route')
        if route is not None:
            leg_attributes['route_type'] = route.attrib.get('type', '')
            leg_attributes['start_link'] = route.attrib.get('start_link', '')
            leg_attributes['end_link'] = route.attrib.get('end_link', '')
            leg_attributes['links'] = route.text.split() if route.text else []
        leg_info.append({
            'mode': leg_mode,
            'departure_time': leg.attrib.get('dep_time', ''),
            'travel_time': leg.attrib.get('trav_time', ''),
            'attributes': leg_attributes
        })
        
    return {
        'person_id': person_id,
        'mode_sequence': mode_sequence,
        'leg_modes': leg_modes,
        'activity_info': activity_info,
        'leg_info': leg_info  # Include leg_info again
    }



#%%
def main(xml_file, csv_file1, csv_file2, isItInput):
    """
    Main function to extract information from XML and write to CSV files.
    
    Parameters:
    - xml_file: Path to the input XML file.
    - csv_file1: Path to the first output CSV file.
    - csv_file2: Path to the second output CSV file.
    """
    with open(xml_file, 'rb') as f_xml, \
          open(csv_file1, 'w', newline='') as f_csv1, \
          open(csv_file2, 'w', newline='') as f_csv2:
        
        # Initialize CSV writers
        writer1 = csv.DictWriter(f_csv1, fieldnames=['person_id', 'mode_sequence', 'leg_modes', 'activity_info'])
        writer1.writeheader()
        
        writer2 = csv.DictWriter(f_csv2, fieldnames=['person_id', 'leg_info'])
        writer2.writeheader()
        
        # Iterate through XML elements
        context = etree.iterparse(f_xml, events=('end',))
        for event, element in context:
            if element.tag == 'person':
                person_id = element.attrib['id']
                if isItInput == 0:
                    plans = element.findall('plan[@selected="yes"]')
                else: plans = element.findall('plan')
                for plan in plans:                                        
                    plan_info = extract_plan_info(person_id, plan)
                    # Write plan information to CSV1
                    writer1.writerow({
                        'person_id': person_id,
                        'mode_sequence': plan_info['mode_sequence'],
                        'leg_modes': plan_info['leg_modes'],
                        'activity_info': plan_info['activity_info']
                    })
                    # Write leg information to CSV2
                    for leg in plan_info['leg_info']:
                        writer2.writerow({'person_id': person_id, 'leg_info': leg})
                element.clear()

#%%

def count_person_ids(xml_file):
    person_ids = set()  # Set to store unique person_ids
    
    # Open the XML file for parsing
    with open(xml_file, 'rb') as f_xml:
        # Iterate through XML elements
        context = etree.iterparse(f_xml, events=('end',))
        for event, element in context:
            if element.tag == 'person':
                person_id = element.attrib.get('id')
                if person_id:
                    person_ids.add(person_id)
                element.clear()
    
    return len(person_ids)

#%% cleaning data to create csv files 

def convert_strLists_to_lists(df, col):
    df[col] = df[col].apply(ast.literal_eval)
    return df

def xml_plans_to_df(df):
    # Initialize an empty list to store the transformed data
    transformed_data = []
    
    # Iterate over each row in the DataFrame
    for index, row in df.iterrows():
        person_id = row['person_id']
        mode_sequence = row['mode_sequence']
        activity_info = row['activity_info']
        
        # Iterate over each leg mode and activity info
        for i in range(len(mode_sequence)):
            leg_mode = mode_sequence[i]
            end_time = activity_info[i]['end_time']
            
            # Append the transformed data to the list
            transformed_data.append({
                'person_id': person_id,
                'leg_modes': leg_mode,
                'end_time': end_time
            })
    
    # Create a new DataFrame from the transformed data
    transformed_df = pd.DataFrame(transformed_data)

    return transformed_df


def create_legs_csv_with_links(df):
    # Remove rows with 'nan' values in the 'leg_info' column
    df = df.dropna(subset=['leg_info'])
    
    # Apply literal_eval to convert string representation of dictionary to actual dictionary
    df['leg_info'] = df['leg_info'].apply(ast.literal_eval)
    
    # Normalize the nested dictionaries into separate columns
    df_normalized = pd.json_normalize(df['leg_info'])
    
    # Create a DataFrame for 'person_id' column
    person_id_df = pd.DataFrame(df['person_id'], columns=['person_id'])
    
    # Concatenate the 'person_id' DataFrame with the normalized DataFrame
    df_final = pd.concat([person_id_df, df_normalized], axis=1)
    return df_final