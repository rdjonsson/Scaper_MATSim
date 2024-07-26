# -*- coding: utf-8 -*-
"""
Created on Mon Jun  3 09:21:21 2024

@author: naqavi
"""

import numpy as np
import pandas as pd
import warnings
warnings.filterwarnings('ignore')
import os

#%%

folder = r"C:\Users\naqavi\OneDrive - KTH\!MATSim\Sthlm-try1\OUTPUTS"

#run = r"output_new_pop_2040"
#run = r"22July"
run = r"output_with_experienced_plans"

relative_path_csv1 = r"output\output_events\events_output1.csv"
relative_path_output_csv_file = r"output\output_events\activities.csv"
relative_path_output_csv_file1 = r"output\output_events\activities.csv"

#%%
csv_file1 = os.path.join(folder, run, relative_path_csv1)


df1 = pd.read_csv(csv_file1)
#df2 = pd.read_csv(csv_file2)

t = df1[df1.actType != np.nan]
t.drop(columns =['networkMode','relativePosition'], inplace = True)


t = t.join(pd.get_dummies(t['type']).astype(int))
t.drop(columns =['type'], inplace = True)
t = t.dropna(subset=['person'])


#%%

import sqlite3

# Create a SQLite database in memory
conn = sqlite3.connect(':memory:')

# Write the DataFrame to the SQLite database
t.to_sql('events', conn, index=False, if_exists='replace')

# SQL query to perform the aggregation
query = """
    SELECT
        person,
        time,
        MAX(actType) as actType,
        MAX(computationalRoutingMode) as computationalRoutingMode,
        distance,
        x,
        y,
        MAX(departure) as departure,
        MAX(arrival) as arrival,
        MAX(actstart) as actstart,
        MAX(actend) as actend,
        MAX(travelled) as travelled
    FROM
        events
    GROUP BY
        person, time
"""

# Execute the query and fetch the result into a DataFrame
final_result_df = pd.read_sql(query, conn)

# Write the result to a CSV file
output_csv_file = os.path.join(folder, run, relative_path_output_csv_file)
final_result_df.to_csv(output_csv_file, index=False)

# Close the connection
conn.close()

#%%

#activities = r'C:\Users\naqavi\OneDrive - KTH\!MATSim\Sthlm-try1\OUTPUTS\output-innovation-0.6\output_events\activities.csv'    # Path to your first output CSV file

df = pd.read_csv(output_csv_file)

# df['travelled'][(df.actstart == 1) & (df.arrival == 1) & (df.travelled == 0)] = 1
# df['travel_time'] = df['time'].diff(1).fillna(df['time'])
# df['travel_time'][df.travelled == 0] = 0

df['person_checker1'] = df['person'].diff(1).fillna(df['person'])
df['person_checker2'] = df['person'].diff(-1).fillna(df['person'])
df['person_checker'] = (df['person_checker1'] * df['person_checker2']).astype(int)

df['duration'] = df['time'].diff(1).fillna(df['time']).where(df['person_checker1'] == 0)
df['travel_mode'] = df['computationalRoutingMode'].shift(1).where(df['person_checker1'] == 0)


df.drop(['person_checker1','person_checker2'], axis = 1, inplace = True)
df.person_checker[df.person_checker != 0] = 1

df['duration'] = df['duration'].replace('',np.nan).fillna(0)
df['computationalRoutingMode'] = df['computationalRoutingMode'].replace('',np.nan).fillna(df.travel_mode)

#output_csv_file1 = r'C:\Users\naqavi\OneDrive - KTH\!MATSim\Sthlm-try1\OUTPUTS\output_new_pop_2040\output\output_events\activities.csv'
output_csv_file1 = os.path.join(folder, run, relative_path_output_csv_file)
df.to_csv(output_csv_file1, index=False)
