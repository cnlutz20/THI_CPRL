# %%
# Importing basic Python modules

import os, sys, json, datetime  # Provides OS-dependent functionality, system-specific parameters, JSON handling, and date/time manipulation
import pandas as pd             # Provides data structures and data analysis tools
import numpy as np              # Supports large, multi-dimensional arrays and matrices
import requests
import time
import xlsxwriter
from tqdm import tqdm
# %%


officials_file = r"C:\Users\clutz\OneDrive - THE HUNT INSTITUTE\Documents\Data\legislator data\data_tracking_v2.xlsx"
officials = pd.read_excel(officials_file)

comms_file = r"C:\Users\clutz\OneDrive - THE HUNT INSTITUTE\Documents\Data\legislator data\committees_data.xlsx"
comms = pd.read_excel(comms_file)



print(officials.columns)
print(comms.columns)

# %%get committees def

def get_comms(df, state, chamber):
    result = df[(df['state'] == state) & (df['branch'] == chamber)]
    comms_list = result['committee'].to_list()
    
    return comms_list

# %%

def make_initial_df(df, state, chamber):
    result = df[(df['State Abbreviation'] == state) & (df['Chamber'] == chamber)]

    return result

# %% Get leg details
def calc_leg_details(state_chamber) :
    track_cols = ['State Abbreviation','Chamber','Title', 'First Name',
        'Last Name', 'Party', 'District', 'Date Assumed Office', 'Committee List',
        ]
    state_chamber = state_chamber[track_cols]
    
    # Calculate tenure
    current_year = datetime.date.today().year
    # print(type(current_year))
    state_chamber['tenure'] = current_year - state_chamber['Date Assumed Office']


    #get leaders
    state_chamber['leader'] = "No"
    state_chamber['leader'] = state_chamber['Committee List'].apply(lambda x: str(x).split('|', 1)[0] if len(str(x).split('|', 1)) == 2 else np.nan)

    state_chamber['full title'] = state_chamber['Title'] + " " + state_chamber['First Name'] +" " + state_chamber['Last Name'] 

    state_chamber['district'] = state_chamber.District.str.split(' ').str[-1]
    state_chamber = state_chamber.loc[:,['State Abbreviation','Chamber','full title', 'First Name',
        'Last Name', 'Party', 'district', 'tenure', 'leader'
        ]]

    return state_chamber


# %%

# # house
# nc_house = make_initial_df(officials, "NC", "House")
# nc_house_df = calc_leg_details(nc_house)
# os.chdir(r'C:\Users\clutz\OneDrive - THE HUNT INSTITUTE\Documents\Data\legislator data\nc\cleaned')
# nc_house_df.to_csv('nc_house_officials.csv')
# # senate
# nc_senate = make_initial_df(officials, "NC", "Senate")
# nc_senate_df = calc_leg_details(nc_senate)
# os.chdir(r'C:\Users\clutz\OneDrive - THE HUNT INSTITUTE\Documents\Data\legislator data\nc\cleaned')
# nc_senate_df.to_csv('nc_senate_officials.csv', index=False)

# # %%

# # senate
# il_house = make_initial_df(officials, "IL", "House")
# il_house_df = calc_leg_details(il_house)






# %% NORTH DAKOTA
nd_house = make_initial_df(officials, "ND", "House")
nd_house_df = calc_leg_details(nd_house)

nd_senate = make_initial_df(officials, "ND", "Senate")
nd_senate_df = calc_leg_details(nd_senate)



os.chdir(r'C:\Users\clutz\OneDrive - THE HUNT INSTITUTE\Documents\Data\legislator data\nd')
# Create a Pandas Excel writer using XlsxWriter as the engine.
writer = pd.ExcelWriter('ND_legislators.xlsx', engine='xlsxwriter')
# Write each dataframe to a different worksheet.

nd_house_df.to_excel(writer, sheet_name='nd_house', index=False)
nd_senate_df.to_excel(writer, sheet_name='nd_senate', index=False)
# Close the Pandas Excel writer and output the Excel file.
writer.close()

# %% INDIANNA
nd_house = make_initial_df(officials, "ND", "House")
nd_house_df = calc_leg_details(nd_house)

nd_senate = make_initial_df(officials, "ND", "Senate")
nd_senate_df = calc_leg_details(nd_senate)



os.chdir(f'C:\\Users\\clutz\\OneDrive - THE HUNT INSTITUTE\\Documents\\Data\\legislator data\\{state}')
# Create a Pandas Excel writer using XlsxWriter as the engine.
writer = pd.ExcelWriter('ND_legislators.xlsx', engine='xlsxwriter')
# Write each dataframe to a different worksheet.

nd_house_df.to_excel(writer, sheet_name='nd_house', index=False)
nd_senate_df.to_excel(writer, sheet_name='nd_senate', index=False)
# Close the Pandas Excel writer and output the Excel file.
writer.close()

# %%

nm_house = make_initial_df(officials, "NM", "House")
nm_house_df = calc_leg_details(nm_house)

nm_senate = make_initial_df(officials, "NM", "Senate")
nm_senate_df = calc_leg_details(nm_senate)


# %%

def create_state_leg_files(df, state_list):
    
    for state in state_list:
        house = make_initial_df(df, str(state), "House")
        house_df = calc_leg_details(house)
        # print(house)
        senate = make_initial_df(df, state, "Senate")
        senate_df = calc_leg_details(senate)

        if len(senate_df) == 0:
            print('zero length')
            print(state)
            return None
        elif len(house_df) == 0 :
            print(state)
            print('zero length')

            return None
        os.chdir(f'C:\\Users\\clutz\\OneDrive - THE HUNT INSTITUTE\\Documents\\Data\\legislator data\\{state}')
        # Create a Pandas Excel writer using XlsxWriter as the engine.
        file_name = f'{state}_legislators.xlsx'
        writer = pd.ExcelWriter(file_name, engine='xlsxwriter')
        # Write each dataframe to a different worksheet.
        house_sheet = f'{state}_house'
        senate_sheet = f'{state}_senate'
        house_df.to_excel(writer, sheet_name=house_sheet, index=False)
        senate_df.to_excel(writer, sheet_name=senate_sheet, index=False)
        # Close the Pandas Excel writer and output the Excel file.
        writer.close()

# %%
states = ['ND', 'NM', 'OH', 'OK', 'VA', 'WV', 'AL', 'CT', 'IL', 'IN', 'KS', 'MO', 'NC']

create_state_leg_files(officials, states)
# %% one off creations
create_state_leg_files(officials, ["NC"])

# %%



##############################

##############################

##############################

##############################

##############################

##############################

##############################














# %% Illinois testing

il_house = make_initial_df(officials, "IL", "House")
il_house_df = calc_leg_details(il_house)
for i,j in enumerate(il_house_df['Committee List']):
    split_comms = str(j).split(',')
    print('########################')
    # print(str(j))

    print(str(il_house_df['First Name'].iloc[i]) + ' ' + str(il_house_df['Last Name'].iloc[i]))
    print('%%%%%%%%%%%%%')
    for s in split_comms:
        print(str(s).strip())
    print('%%%%%%%%%%%%%')
    print('\n')

# %% indianna teting
in_house = make_initial_df(officials, "IN", "House")
in_house_df = calc_leg_details(in_house)

# %%
nc_house = make_initial_df(officials, "NC", "House")
nc_house_df = calc_leg_details(nc_house)
nc_coms = get_comms(comms, "NC", "house")
nc_house_df[nc_coms] = np.nan

# %%Okalhoma
ok_house = make_initial_df(officials, "OK", "House")




# %%
for i,j in enumerate(nc_house_df['Committee List']):
    split_comms = str(j).split(',')
    print('########################')
    # print(str(j))

    print(str(nc_house_df['First Name'].iloc[i]) + ' ' + str(nc_house_df['Last Name'].iloc[i]))
    print('%%%%%%%%%%%%%')
    for s in split_comms:
        print(str(s).strip())
    print('%%%%%%%%%%%%%')
    print('\n')

# %% NC testing

nc_senate_df = calc_leg_details(nc_senate)
# %% Definition testing (old)
# %% NC GA
nc_house = officials[(officials['State Abbreviation'] == "NC") & (officials['Chamber'] == "House")]
nc_senate = officials[(officials['State Abbreviation'] == "NC") & (officials['Chamber'] == "Senate")]

# Calculate tenure
current_year = datetime.date.today().year
print(type(current_year))
nc_senate['tenure'] = current_year - nc_senate['Date Assumed Office']


#get leaders
nc_senate['leader'] = np.nan
nc_senate['leader'] = nc_senate['Committee List'].apply(lambda x: str(x).split('|', 1)[0] if len(str(x).split('|', 1)) == 2 else np.nan)


# %%

for i,j in enumerate(nc_senate['Committee List']):
    leader_split = str(j).split('|', 1)
    print(len(leader_split))
    if len(leader_split) == 2:
        nc_senate['leader'].iloc[i] = str(leader_split[0])
    

nc_senate['leader'] = nc_senate['Committee List'].str.split('|',1)

#  %%

# %%

for i,j in enumerate(nc_senate['Date Assumed Office']):
    current_year = datetime.date.today().year
    tenure = current_year-j
    nc_senate['tenure'].iloc[i] = tenure





    print('#########################')
    print(j)
    print(type(j))
    print('\n')
#export
# os.chdir(r'C:\Users\clutz\OneDrive - THE HUNT INSTITUTE\Documents\Data\legislator data')
# nc_house.to_excel("nc_house.xlsx")





