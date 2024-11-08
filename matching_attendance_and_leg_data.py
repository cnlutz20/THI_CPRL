# %%
import os, sys, json, datetime, re, xlrd  # Provides OS-dependent functionality, system-specific parameters, JSON handling, and date/time manipulation
import pandas as pd             # Provides data structures and data analysis tools
from openpyxl import Workbook
import numpy as np              # Supports large, multi-dimensional arrays and matrices
import requests
import glob
import time
from tqdm import tqdm
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
pd.options.mode.chained_assignment = None  # default='warn'

# %% gathering leg files

os.chdir(r'C:\Users\clutz\OneDrive - THE HUNT INSTITUTE\Documents\Data\legislator data')
legislator_files = glob.glob('**/*.xlsx') 

for i,file in enumerate(legislator_files):
    if '_legislators' not in str(file):
        del legislator_files[i] 


dfs = []
for i,file in enumerate(legislator_files):
    print('working on file:' + str(file))
    # file = legislator_files[0]
    # xls = pd.ExcelFile(file)
    sheets_dict = pd.read_excel(file, engine="openpyxl", sheet_name=None)
    sheet_names = list(sheets_dict.keys())
    for s in sheet_names:
        df = pd.read_excel(file, engine="openpyxl", sheet_name=s)
        dfs.append(df)

    df = pd.concat(dfs)


all_legs = pd.concat(dfs)

os.chdir(r'C:\Users\clutz\OneDrive - THE HUNT INSTITUTE\Documents\Data\attendance data\exports')
all_legs.to_csv('list_of_legislators_11_8_2024.csv')


# %% gathering attendance data

os.chdir(r'C:\Users\clutz\OneDrive - THE HUNT INSTITUTE\Documents\Data\attendance data')
events = glob.glob("*.xlsx")
state_list = [
    "Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", 
    "Connecticut", "Delaware", "Florida", "Georgia", "Hawaii", "Idaho", 
    "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", 
    "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota", 
    "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", 
    "New Hampshire", "New Jersey", "New Mexico", "New York", 
    "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon", 
    "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota", 
    "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington", 
    "West Virginia", "Wisconsin", "Wyoming", "District of Columbia"
]
state_abbreviations = [
    "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA", 
    "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", 
    "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", 
    "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", 
    "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY", "DC"
]


print("a statement")
state_abbreviations_reg = []
for abv in state_abbreviations:
    for_regex = f'^{abv}'
    state_abbreviations_reg.append(for_regex)

state_pat = re.compile("|".join(state_list))

state_abv_pat = re.compile("|".join(state_abbreviations_reg))
print(state_abv_pat)
state_ref = dict(zip(state_list, state_abbreviations))

# %%

dfs = []
vals_changed = 0
for event in events:
    df = pd.read_excel(event)
    # print('######################')
    
    # print(*df.columns)
    event_name = str(event).split('.')[0].strip().replace('_', ' ')
    df = df.iloc[:,:7]
    df.loc[:,'event name'] = event_name
    
    break_all = False
    # #print(df)
    # continue
    for i,state in enumerate(df['state']):
        #print(i)

        # #print(str(state))
        # #print('----------------------------')
        #print(df.loc[i,['first_name', 'last_name', 'title', 'org']])
        #print(str(event_name))
        # #print(df.loc[i, 'event name'])
        # # continue
        # #print('----------------------------')
        if isinstance(state, float):

            if re.search(r'[Rr]epresentative|[Ss]enator|[Ll]egislator',str(df['title'].iloc[i])) or re.search(r'[Ss]enate|[Hh]ouse of ([Rr]epresentatives)?(Delegates)?|[Dd]istrict|[Ss]tate [Hh]ouse', str(df['org'].iloc[i])):
                # continue
                #print("^^^^^^^^^^^")
                #print("found a match")
                # #print(df.loc[i,['first_name', 'last_name']])
                
                testing_string = str(df['title'].iloc[i]) + " " + str(df['org'].iloc[i])
                # #print(testing_string)
                testing_string = testing_string.lstrip('nan').lstrip().strip()
                # #print(re.match(r'[Rr]epresentative|[Ss]enator|[Ll]egislator|[Ss]enate|[Hh]ouse of ([Rr]epresentatives)?(Delegates)?|[Dd]istrict|[Ss]tate [Hh]ouse',str(testing_string)))
                # continue
                # #print('###########')
                # #print(df.loc[i, list(df.columns[:5]) + [df.columns[-1]]])
                # #print('\n')
                state_match_uc = re.findall(state_pat, str(df['org'].iloc[i]))
                state_match = [x for x in state_match_uc if len(x) > 0]
                
                # First match test
                if len(state_match) == 0:
                    #print('no regular state match')
                    #print(state_match_uc)
                    state_abv_match_uc = re.findall(state_abv_pat, str(df['org'].iloc[i]))
                    state_abv_match = [x for x in state_abv_match_uc if len(x) > 0]
                    # Second match test
                    if len(state_abv_match) == 0:
                        #print('no state abbreviation match')
                        #print(state_abv_match_uc)
                        state_abv_event_match_uc = re.findall(state_abv_pat, str(df['event name'].iloc[i]))
                        state_abv_event_match = [x for x in state_abv_event_match_uc if len(x) > 0]
                        # Third match test
                        if len(state_abv_event_match) == 0:
                            #print('no state abv event match')
                            #print(state_abv_event_match_uc)
                            break
                        elif len(state_abv_event_match) > 1:
                            #print('more than one match?')
                            break_all = True
                            break
                        else:
                            #print("abv in event match")
                            state_val = str(state_abv_event_match[0])
                            df.loc[i,'state'] = None
                            df.loc[i,'state'] = state_val
                            #print(state_val)
                            vals_changed += 1
                    elif len(state_abv_match) > 1:
                        #print('more than one match?')
                        #print(state_abv_match)
                        #print(df.loc[i, list(df.columns[:5]) + [df.columns[-1]]])
                        break_all = True
                        break
                    else:
                        #print("regular abreviation match")
                        
                        state_val = str(state_abv_match[0])
                        df.loc[i,'state'] = None
                        df.loc[i,'state'] = state_val
                        #print(state_val)
                        vals_changed += 1


                    # #print('###########')
                    # #print(df.loc[i, list(df.columns[:5]) + [df.columns[-1]]])
                    # #print('\n')
                    # break
                elif len(state_match) > 1:
                    #print("more than one match?")
                    break_all = True
                    break
                else:
                    #print("normal state match")
                    state_val_dirty = str(state_match[0])
                    state_val = state_ref.get(state_val_dirty)
                    df.loc[i,'state'] = None
                    df.loc[i,'state'] = state_val
                    #print(state_val)
                    vals_changed += 1
            else:
                # #print('#########################')
                # #print('NOT A REP OR SEN')
                # #print(df.loc[i,['first_name','last_name','title', 'org']])
                continue
                # #print(df.loc[i, list(df.columns[3:5]) + [df.columns[-1]]])
                # #print('\n')
    if break_all == True:
        break

    dfs.append(df)


event_data = pd.concat(dfs)
event_data.reset_index(inplace=True, drop = True)

# %%
for i,j in enumerate(event_data['state']):
    
    if isinstance(j, float):
        continue
    elif re.search(r'[A-Z]{2}', str(j)):
        continue
    else:
        val = state_ref.get(str(j))
        event_data.loc[i,'state'] = str(val)

# %%
os.chdir(r'C:\Users\clutz\OneDrive - THE HUNT INSTITUTE\Documents\Data\attendance data\exports')
event_data.to_csv("event_data_export_11_7_2024.csv", index=False)


# %%
# Define your regex patterns
title_pattern = r'[Rr]epresentative|[Ss]enator|[Ll]egislator'
org_pattern = r'[Ss]enate|[Hh]ouse of ([Rr]epresentatives)?(Delegates)?|(?<!School )(?:House District|District)|[Ss]tate [Hh]ouse'

# Filter the DataFrame based on the OR condition
filtered_df = event_data[event_data['title'].astype(str).apply(lambda x: bool(re.search(title_pattern, x))) |
                 event_data['org'].astype(str).apply(lambda x: bool(re.search(org_pattern, x)))]


no_districts = filtered_df[~(filtered_df['org'].str.contains(r'[Dd]istrict|[Dd](-|\s)?\d{2,3}', regex=True) | filtered_df['title'].str.contains(r'[Dd]istrict|[Dd](-|\s)?\d{2,3}', regex=True))]
os.chdir(r'C:\Users\clutz\OneDrive - THE HUNT INSTITUTE\Documents\Data\attendance data\exports')
no_districts.to_csv("no_districts_export_11_7_2024.csv", index=False)



# %%


only_legs_event
if re.search(r'[Rr]epresentative|[Ss]enator|[Ll]egislator',str(df['title'].iloc[i])) or re.search(r'[Ss]enate|[Hh]ouse of ([Rr]epresentatives)?(Delegates)?|[Dd]istrict|[Ss]tate [Hh]ouse', str(df['org'].iloc[i])):

only_legs_event = 