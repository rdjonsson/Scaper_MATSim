# -*- coding: utf-8 -*-
"""
Created on Tue Jun  4 15:09:19 2024

@author: naqavi
"""

import numpy as np
import pandas as pd
pd.set_option('display.max_columns', None)  # Show all columns
import os
import matplotlib.pyplot as plt
import seaborn as sns

#%%
folder = r"C:\Users\naqavi\OneDrive - KTH\!MATSim\Sthlm-try1\OUTPUTS"

#run = r"output_new_pop_2040"
#run = r"22July"
run = r"output_with_experienced_plans"

relative_path_csv = r"output\output_events\activities.csv"

csv_file = os.path.join(folder, run, relative_path_csv)

#%%

df = pd.read_csv(csv_file)
df['start_time'] = df.time - df.duration

df.time = df.time / (3600)
df.duration = df.duration / (3600)
df.start_time = df.start_time / 3600 
df.dropna(subset=['actType'], inplace=True)


#%%

# Define the mapping dictionary
actType_mapping = {'h': 'home', 'l': 'leisure', 'c': 'visit', 'w': 'work', 'o': 'other', 's': 'shopping'}

# Apply the mapping to the 'actType' column
df['actType'] = df['actType'].map(actType_mapping)

non_start = df[df.person_checker == 0]

#all_time_slots = np.concatenate([np.arange(row['start_time'], row['time']) for idx, row in non_start.iterrows()])

act_types = df['actType'].unique()



#%% boxplot of travel modes 

# Create linspace from 0 to 18 with 0.25 steps
num_steps = int((4.5 - 0) / ((1/60))) + 1
steps = np.linspace(0, 4.5, num=num_steps)

# Assuming your DataFrame is named dff
# Create a column that assigns activity duration to the corresponding step
df['step_duration'] = pd.cut(df['duration'], bins=steps, labels=steps[:-1])

# Display the DataFrame
print(df['step_duration'])

# Convert 'step_duration' to numeric type
df['step_duration'] = pd.to_numeric(df['step_duration'])

# Plotting boxplots for step_duration for each activity type
plt.figure(figsize=(12, 8))
sns.boxplot(x='travel_mode', y='step_duration', data=df, palette='Set3')
plt.xlabel('Travel Mode')
plt.ylabel('Travel Duration (1 minute interval)')
plt.title('Travel Duration by Mode (output)')
plt.grid(True)
plt.show()



#%% boxplot of activity types

# Create linspace from 0 to 18 with 0.25 steps
num_steps = int((15 - 0) / ((1/60))) + 1
steps = np.linspace(0, 15, num=num_steps)


df_activities = df[df['travel_mode'].isna()]

# Assuming your DataFrame is named dff
# Create a column that assigns activity duration to the corresponding step
df_activities['step_duration'] = pd.cut(df_activities['duration'], bins=steps, labels=steps[:-1])

# Display the DataFrame
print(df_activities['step_duration'])

# Convert 'step_duration' to numeric type
df_activities['step_duration'] = pd.to_numeric(df_activities['step_duration'])

# Plotting boxplots for step_duration for each activity type
plt.figure(figsize=(12, 8))
sns.boxplot(x='actType', y='step_duration', data=df_activities, palette='Set3')
plt.xlabel('Activity Type')
plt.ylabel('Activity Duration (1 minute interval)')
plt.title('Activity Duration by Activity Type (output)')
plt.grid(True)
plt.show()

#%% stack bar chart of mode shares for each trip purpose

import seaborn as sns
import matplotlib.pyplot as plt

# Filter out rows where mode is 'N'
#df_travelled = df[df.actstart == 1]
df_travelled = df[df['travel_mode'].notna()]

# Group by 'activity_type' and 'mode', then calculate mode shares
mode_shares = df_travelled.groupby(['actType', 'travel_mode']).size().unstack(fill_value=0)

# Normalize mode shares to get proportions
mode_shares = mode_shares.div(mode_shares.sum(axis=1), axis=0)

# Plot stacked bar plot with Seaborn
plt.figure(figsize=(9, 5))

# Define color palette using Viridis colormap
colors = sns.color_palette('viridis', n_colors=4)

# Iterate over columns and plot each one separately
bottom = None
bar_width = 0.5   # Adjust the width of the bars
for i, column in enumerate(mode_shares.columns):
    # Normalize data for each column so that the stack sums to 1
    normalized_data = mode_shares[column] / mode_shares.sum(axis=1)
    plt.bar(mode_shares.index, normalized_data, label=column, bottom=bottom, color=colors[i], width=bar_width)
    if bottom is None:
        bottom = normalized_data
    else:
        bottom += normalized_data

plt.xlabel('Trip Purpose')
plt.ylabel('Mode Share')
plt.title('Mode Shares for Each Trip Purpose (output)')
plt.legend(title='Mode', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True, axis='y')
plt.tight_layout()
plt.show()

#%%



all_travel_acts = df_travelled.groupby(by = ['actType']).count().iloc[:,1]

# Plot pie chart with higher resolution
fig, ax = plt.subplots(figsize=(10, 10), dpi=300)
wedges, texts, autotexts = ax.pie(
    all_travel_acts,
    autopct='%1.1f%%',
    startangle=140,
    colors=plt.cm.Set3.colors,
    textprops=dict(color="k")
)

    
# Customize font properties
for text in texts + autotexts:
    text.set_fontsize(12)

# Add a title with padding
ax.set_title('Trip Purpose Distribution', fontsize=16, fontweight='bold', pad=20)

# Add a legend with spacing
ax.legend(
    wedges, all_travel_acts.index,
    title="Trip Purpose",
    loc="center left",
    bbox_to_anchor=(1, 0, 0.5, 1),
    fontsize=12,
    title_fontsize='13'
)

# Equal aspect ratio ensures that pie is drawn as a circle
ax.axis('equal')

# Adjust layout to add space
plt.tight_layout()

# Display the plot
plt.show()

#%%
all_travel_modes = df_travelled.groupby(by = ['travel_mode']).count().iloc[:,1]


# Plot pie chart with higher resolution
fig, ax = plt.subplots(figsize=(10, 10), dpi=300)
wedges, texts, autotexts = ax.pie(
    all_travel_modes,
    autopct='%1.1f%%',
    startangle=140,
    colors=plt.cm.Set3.colors,
    textprops=dict(color="k")
)

# Customize font properties
for text in texts + autotexts:
    text.set_fontsize(12)

# Add a title with padding
ax.set_title('Mode Share', fontsize=16, fontweight='bold', pad=20)

# Add a legend with spacing
ax.legend(
    wedges, all_travel_modes.index,
    title="Activity Types",
    loc="center left",
    bbox_to_anchor=(1, 0, 0.5, 1),
    fontsize=12,
    title_fontsize='13'
)

# Equal aspect ratio ensures that pie is drawn as a circle
ax.axis('equal')

# Adjust layout to add space
plt.tight_layout()

# Display the plot
plt.show()

#%%

mode_duration = df_travelled.groupby(by = ['travel_mode']).duration.sum()/sum(df_travelled.groupby(by = ['travel_mode']).duration.sum())

# Plot pie chart with higher resolution
fig, ax = plt.subplots(figsize=(10, 10), dpi=300)
wedges, texts, autotexts = ax.pie(
    mode_duration,
    autopct='%1.1f%%',
    startangle=140,
    colors=plt.cm.Set3.colors,
    textprops=dict(color="k")
)

# Customize font properties
for text in texts + autotexts:
    text.set_fontsize(12)

# Add a title with padding
ax.set_title('Travel Time Duration (Percentage to total TT duration)', fontsize=16, fontweight='bold', pad=20)

# Add a legend with spacing
ax.legend(
    wedges, mode_duration.index,
    title="Activity Types",
    loc="center left",
    bbox_to_anchor=(1, 0, 0.5, 1),
    fontsize=12,
    title_fontsize='13'
)

# Equal aspect ratio ensures that pie is drawn as a circle
ax.axis('equal')

# Adjust layout to add space
plt.tight_layout()

# Display the plot
plt.show()



#%%

plt.figure(figsize=(12, 6))
colors = sns.color_palette('Set2', len(act_types))

for i,act_type in enumerate(act_types):
    # Filter dataframe by actType
    act_df = df[df['actType'] == act_type]
    # Expand the time slots for each activity
    all_time_slots = np.concatenate([np.arange(row['start_time'], row['time']) for idx, row in act_df.iterrows()])
    
    # Plot line histogram with KDE
    #plt.hist(all_time_slots, bins=42, range=(4, 25), edgecolor='black', alpha=0.5, label=act_type, color=colors[i])
    bins = np.linspace(4, 25, 43)  # 42 bins between 4 and 25
    hist, bin_edges = np.histogram(all_time_slots, bins=bins)
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
    plt.plot(bin_centers, hist, label='act_type', color=colors[i])
    
        
# Add titles and labels
plt.title('Activity Time of Day by actType', fontsize=16, fontweight='bold')
plt.xlabel('Time of day (hours)', fontsize=14)
plt.ylabel('Count', fontsize=14)
plt.xticks(np.arange(4, 25, 1), fontsize=12)
plt.yticks(fontsize=12)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.legend(act_types, title='actType', fontsize=12, title_fontsize='13')
plt.gca().spines['right'].set_color('gray')
plt.gca().spines['top'].set_color('gray')
plt.gca().spines['left'].set_color('gray')
plt.gca().spines['bottom'].set_color('gray')

# Show plot
plt.show()

