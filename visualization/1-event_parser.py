# -*- coding: utf-8 -*-
"""
Created on Fri May 17 13:06:14 2024

@author: naqavi
"""

import gzip
import xml.etree.ElementTree as ET
import csv
from collections import defaultdict
import os
import shutil

#%% create directories and read files


folder = r"C:\Users\naqavi\OneDrive - KTH\!MATSim\Sthlm-try1\OUTPUTS"

#run = r"output_new_pop_2040"
#run = r"22July"
run = r"output_with_experienced_plans"

# create the output event folder to seperate the created files from the main outputs
new_folder_path = os.path.join(folder, run, "output\output_events")
source_file_path = os.path.join(folder, run,"output\output_events.xml.gz") 
destination_file_path = os.path.join(new_folder_path, os.path.basename(source_file_path))
os.makedirs(new_folder_path, exist_ok=True)
shutil.copy(source_file_path, destination_file_path)


relative_path_output_events = r"output\output_events\output_events.xml.gz"
relative_path_csv1 = r"output\output_events\events_output1.csv"
relative_path_csv2 = r"output\output_events\events_output2.csv"


output_events = os.path.join(folder, run, relative_path_output_events)




#%%

def extract_event_info(event):
    """
    Extracts information from an event element in the XML.

    Parameters:
    - event: The event XML element.

    Returns:
    A dictionary containing the extracted information.
    """
    return event.attrib

def parse_events(xml_file):
    """
    Parses events from the given XML file.

    Parameters:
    - xml_file: Path to the input XML file.

    Returns:
    A generator yielding event dictionaries.
    """
    context = ET.iterparse(xml_file, events=('end',))
    for event, element in context:
        if element.tag == 'event':
            yield extract_event_info(element)
        element.clear()

def main(xml_file, csv_file1, csv_file2):
    """
    Main function to extract event information from XML and write to CSV files.

    Parameters:
    - xml_file: Path to the input XML file.
    - csv_file1: Path to the first output CSV file.
    - csv_file2: Path to the second output CSV file.
    """
    excluded_types = {'left link', 'entered link', 'stuckAndAbort', #'vehicle aborts',
                      'vehicle enters traffic', 'vehicle leaves traffic','personMoney', 
                      'PersonEntersVehicle'}#, 'PersonLeavesVehicle'}
    
    unique_keys = set()
    unique_type_values = set()
    link_counts = defaultdict(int)

    with gzip.open(xml_file, 'rb') as f_xml, \
         open(csv_file1, 'w', newline='') as f_csv1, \
         open(csv_file2, 'w', newline='') as f_csv2:
        
        # Initialize CSV writers with initial fieldnames
        fieldnames1 = ['time', 'type', 'person', 'link', 'vehicle', 'networkMode', 'relativePosition', 'distance', 'mode', 'legMode', 'x', 'y', 'actType']
        fieldnames2 = ['person', 'leg_info']
        
        writer1 = csv.DictWriter(f_csv1, fieldnames=fieldnames1)
        writer1.writeheader()
        
        writer2 = csv.DictWriter(f_csv2, fieldnames=fieldnames2)
        writer2.writeheader()

        # Parse events and collect unique keys and types
        context = ET.iterparse(f_xml, events=('end',))
        for event, element in context:
            if element.tag == 'event':
                event_info = extract_event_info(element)
                event_type = event_info['type']
                
                if event_type not in excluded_types:
                    unique_keys.update(event_info.keys())
                    unique_type_values.add(event_type)
    
                    if event_type == 'entered link':
                        link_counts[event_info['link']] += 1
                    
                    # Dynamically update fieldnames if new keys are found
                    for key in event_info.keys():
                        if key not in fieldnames1:
                            fieldnames1.append(key)
                            writer1 = csv.DictWriter(f_csv1, fieldnames=fieldnames1)
                            f_csv1.seek(0)
                            writer1.writeheader()
                    
                    # Write event information to CSV1
                    writer1.writerow(event_info)
    
                    # Write leg information to CSV2 (if applicable)
                    if 'legMode' in event_info:
                        writer2.writerow({'person': event_info['person'], 'leg_info': event_info})
            
                element.clear()
    
    # Print unique keys and types
    print(f"Unique Keys: {unique_keys}")
    print(f"Unique Type Values: {unique_type_values}")

if __name__ == "__main__":
    xml_file = output_events  # Path to your XML file
    csv_file1 = os.path.join(folder, run, relative_path_csv1)
    csv_file2 = os.path.join(folder, run, relative_path_csv2)
    main(xml_file, csv_file1, csv_file2)

