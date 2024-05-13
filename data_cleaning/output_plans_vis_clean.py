# -*- coding: utf-8 -*-
"""
Created on Fri Apr 26 09:22:34 2024

@author: naqavi
"""

#%% import libraries

import os
import pandas as pd
from functions import get_files
from functions import time_to_numeric
from functions import get_duration
from functions import activity_duration_histogram, box_plot_modes_activities
from functions import mode_by_trip_purpose_new
from functions import activity_duration_freq_hist
from functions import activity_along_day, travel_duration_histogram, travel_along_day
from functions import density_plot_of_travel_time, dist_travel_time_for_each_mode, modes_travel_time_boxPlot, pivot_table_mode_activity
from functions import keep_travel_time_larger_than_2andHalf, mode_percentage

from functions import get_start_time, clean_output, removes_row_with_ids_just_in_one_df, merge_legs_and_plans

#from travel_time_digging import check_long_travel_times

import warnings
warnings.filterwarnings("ignore")
warnings.resetwarnings()


#%% read input

file_suffix = 'innovation'

folder1, current_directory1, df1  = get_files(1,file_suffix)
df1 = time_to_numeric(df1, 'travel_time')
df1 = time_to_numeric(df1, 'end_activity_time')

folder2, current_directory2, df, attributes  = get_files(0,file_suffix)

#%%
df = time_to_numeric(df, 'departure_time')
df = time_to_numeric(df, 'travel_time')
df = time_to_numeric(df, 'end_activity_time')
df['end_travel_time'] = df['departure_time'] + df['travel_time']
df['activity_duration'] = df['end_activity_time'] - df['end_travel_time']

#%% 


df1['id_check'] = (df1['person_id'] == df1['person_id'].shift(1)).astype(int)
df['id_check'] = (df['person_id'] == df['person_id'].shift(1)).astype(int)

