# # -*- coding: utf-8 -*-
# """
# Created on Fri Apr 19 08:52:31 2024

# @author: naqavi
# """

import pandas as pd
import os
from parser_funcs import get_directory
from parser_funcs import main, count_person_ids
from parser_funcs import convert_strLists_to_lists, xml_plans_to_df, create_legs_csv_with_links

#%%

# Is this input or output file? (input = 1, output = 0)
isItInput= 0


folder, current_directory, input_file_path = get_directory(isItInput)

#%% check number of distinct agents

num_person_ids = count_person_ids(input_file_path)
print("Number of unique person_ids:", num_person_ids)
                
#%%  extract information from XML file (output_plans)

output_csv_file1 = os.path.join(current_directory, f"{folder}\plans.xml")
output_csv_file2 = os.path.join(current_directory, f"{folder}\legs.xml")

xml_file = input_file_path  # Replace with the path to your XML file
csv_file1 = output_csv_file1
csv_file2 = output_csv_file2
main(xml_file, csv_file1, csv_file2, isItInput)

#%% turn the plan csv file into a dataframe (does not include links)

# Load the CSV file into a DataFrame 
df = pd.read_csv(csv_file1, delimiter=',')
df = convert_strLists_to_lists(df, 'mode_sequence')
df = convert_strLists_to_lists(df, 'leg_modes')
df = convert_strLists_to_lists(df, 'activity_info')
transformed_df = xml_plans_to_df(df)
print('plans look like: ', transformed_df)

# Print the transformed DataFrame
transformed_df.to_csv(os.path.join(current_directory, f'{folder}\plans.csv'))



#%% turn the plan csv file into a dataframe (only includes links)
 
# Load the CSV data into a DataFrame
df = pd.read_csv(csv_file2, delimiter=',')
create_legs_csv_with_links(df)

# Print the final DataFrame
df_final = create_legs_csv_with_links(df)
print('legs look like: ', df_final)
df_final.to_csv(os.path.join(current_directory, f'{folder}\legs.csv'))





