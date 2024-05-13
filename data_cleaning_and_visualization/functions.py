# -*- coding: utf-8 -*-
"""
Created on Thu Apr 25 12:11:48 2024

@author: naqavi
"""


import pandas as pd
import datetime
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import os


import warnings
warnings.filterwarnings("ignore")
warnings.resetwarnings()
pd.options.mode.chained_assignment = None  # default='warn'



def get_files(isItInput,file_suffix):
    if isItInput:
        folder = 'input'
        current_directory = r"C:\Users\naqavi\OneDrive - KTH\!MATSim\Sthlm-try1\visualizations\output_vis\outputPlansToCSV"
        plans_df = pd.read_csv(os.path.join(current_directory, fr'{folder}\plans.csv'))
        legs_df = pd.read_csv(os.path.join(current_directory, fr'{folder}\legs.csv'))
        legs_df.drop(columns=['attributes.mode'] ,inplace = True)
    
    else:
        folder = 'output'
        current_directory = os.getcwd()
        plans_df = pd.read_csv(os.path.join(current_directory, fr'{folder}\plans_{file_suffix}.csv'))
        legs_df = pd.read_csv(os.path.join(current_directory, fr'{folder}\legs_{file_suffix}.csv'))
        attributes = pd.DataFrame(columns=['mode','routingMode','route_type','start_link', 'end_link', 'links'], 
                                  data = legs_df[['attributes.mode','attributes.routingMode', 'attributes.route_type',
                                                  'attributes.start_link', 'attributes.end_link', 'attributes.links']])
        legs_df.drop(columns=['attributes.mode','attributes.routingMode', 'attributes.route_type',
                        'attributes.start_link', 'attributes.end_link', 'attributes.links'], inplace = True)
        
    legs_df.drop(columns=['Unnamed: 0'], axis=1, inplace=True)
    plans_df.drop(columns=['Unnamed: 0'], axis=1, inplace=True)
    
    legs_df.sort_values(by = ['person_id','departure_time'], inplace = True)
    plans_df.sort_values(by = ['person_id','end_time'], inplace = True)
    legs_df.reset_index(drop = True, inplace = True)
    plans_df.reset_index(drop = True, inplace = True)    
    ind = plans_df[plans_df.duplicated(subset=['person_id'])].index[0:]
    # indices_not_in_ind = plans_df[~plans_df.index.isin(ind)].index
    # start = plans_df.loc[indices_not_in_ind]
    plans_df = plans_df.loc[ind]
    plans_df.reset_index(drop = True, inplace = True)
    df = plans_df 
    legs_df.sort_values(by = ['person_id','departure_time'])
    df['departure_time'] = legs_df['departure_time']
    df['travel_time'] = legs_df['travel_time']
    df = df[['person_id', 'leg_modes', 'departure_time', 'travel_time', 'end_time']]
    df = df.rename(columns={'leg_modes': 'activity_type', 'end_time': 'end_activity_time'})
   
    if isItInput:    
        return folder, current_directory, df #legs_df, plans_df, start

    else:    
        return folder, current_directory, df, attributes # legs_df, plans_df, attributes, start
 
    
def time_to_numeric(df, time_column):

    # Convert 'time_column' column to timedelta format
    df[time_column] = pd.to_timedelta(df[time_column])
    df['days'] = df[time_column].dt.days
    # df = df[df['days'] == 0]

    # Filter out rows where 'end_time' is larger than 23:59:59
    df['seconds'] = df[time_column].dt.seconds
    df[time_column] = df['seconds'] / 3600
    df.drop(columns=['seconds'], inplace=True)
    
    return df

