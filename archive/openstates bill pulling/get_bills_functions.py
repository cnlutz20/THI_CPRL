# %%
# Importing basic Python modules

import os, sys, json, datetime  # Provides OS-dependent functionality, system-specific parameters, JSON handling, and date/time manipulation
import pandas as pd             # Provides data structures and data analysis tools
import numpy as np              # Supports large, multi-dimensional arrays and matrices
import requests
import time
from tqdm import tqdm
# %%

# #/

# import requests

# API_KEY = '1d0dc220-f3f3-4f05-b73f-10a7e08f4451'  # Replace with your actual API key
# BASE_URL = 'https://v3.openstates.org/jurisdictions'
# PARAMS = {
#         'classification': 'state',
#         }

# headers = {
#         'X-API-KEY': API_KEY
#     }
# params = PARAMS.copy()
# # year = 2023 #only for troubleshooting; comment out when using it fully as a defined function
# # params['session'] = year

# response = requests.get(BASE_URL, headers=headers, params=params)
# content = response.json()
# states = []
# for juri in content.get('results', []):
#     state = juri.get('division_id').split(':')[-1]
#     states.append(state)


# %%
def get_all_bills(state, *session):


    API_KEY = 'd07ea2eb-e174-46fe-851b-3e5df5eb2fe8'  # Replace with your actual API key
    BASE_URL = 'https://v3.openstates.org/bills'
    PARAMS = {
        'jurisdiction': state,
        'include': ['abstracts', 'other_titles', 'sponsorships','actions'],
        'classification': 'bill',
        'page': 1,
        'per_page': 20
        }
    
    headers = {
        'X-API-KEY': API_KEY
    }

    params = PARAMS.copy()
    # year = 2023 #only for troubleshooting; comment out when using it fully as a defined function
    if session:
        params['session'] = session
    
    response = requests.get(BASE_URL, headers=headers, params=params)
    if response.status_code == 200:
        # Get the JSON content from the response
        content = response.json()

        # Access the 'max_page' value
        max_page = content['pagination']['max_page']
        
        if len(content['results']) == 0:
            print('no data')
            return None
        # Print the 'max_page' value
        print(max_page)
    else:
        print(f"Request failed with status code {response.status_code}")
        return None
    

    #iterate through all the pages
    dfs = []
    for page in tqdm(range(1,max_page,1)):
        # time.sleep(3)
        
        API_KEY = '1d0dc220-f3f3-4f05-b73f-10a7e08f4451'  # Replace with your actual API key
        BASE_URL = 'https://v3.openstates.org/bills'
        PARAMS = {
            'jurisdiction': state,
            'include': ['abstracts', 'other_titles', 'sponsorships','actions'],
            'classification': 'bill',
            'page': page,
            'per_page': 20
            }
        
        headers = {
            'X-API-KEY': API_KEY
        }

        params = PARAMS.copy()
        # year = 2023 #only for troubleshooting; comment out when using it fully as a defined function
        # params['session'] = session
        
        response = requests.get(BASE_URL, headers=headers, params=params)
        content = response.json()
        
        bill_id_ls = []
        session_ls = []
        state_ls = []
        number_ls = []
        title_ls = []
        latest_action_date_ls = []
        latest_action_description_ls = []
        first_action_ls = []
        sponsor_name_ls = []
        subject_ls = []
        sponsor_name_ls = []
        sponsor_id_ls = []
        sponsor_party_ls = []
        p_title_ls = []
        district_ls = []
        # abstracts_ls = []
        # other_titles_ls = []
        
        for bill in content.get('results', []):
            
            
            bill_id = bill.get('id')
            session = bill.get('session')
            state = bill.get('jurisdiction', {}).get('name')
            number = bill.get('identifier')
            title = bill.get('title')
            subjects = bill.get('subject', [])
            subjects = ', '.join(subjects)



            
            # abstracts = bill.get('abstracts', [])
            # print(type(abstracts))
            # print(len(abstracts))

            # abstract = abstracts[0].get('abstract')
            # # abstracts_list = bill.get('abstracts', [])
            # print(abstract)
            
            
            # try:
            #     abstracts = abstracts_list[0].get('abstract')
            # except:
            #     print('moving on')
            # # abstracts = bill.get('abstracts', [])[0].get('abstract')
            # other_titles = bill.get('other_titles', [])[0].get('title')

            # Handle potential empty 'actions' list
            if bill.get('actions'):
                latest_action_date = bill['actions'][0].get('date')
                latest_action_description = bill['actions'][0].get('description')
            else:
                latest_action_date = None
                latest_action_description = None

            first_action = bill.get('first_action_date')
            # Handle potential empty 'sponsorships' list
            if bill.get('sponsorships', []):
                sponsorship = bill['sponsorships'][0]
                # print(sponsorship)
                sponsor_person = sponsorship.get('person', {})
                
                sponsor_name = sponsor_person.get('name')
                sponsor_id = sponsor_person.get('id')
                sponsor_party = sponsor_person.get('party')
                
                current_role = sponsor_person.get('current_role', {})
                p_title = current_role.get('title')
                district = current_role.get('district')
            else:
                sponsor_name = None
                sponsor_id = None
                sponsor_party = None
                p_title = None
                district = None

            bill_id_ls.append(bill_id)
            session_ls.append(session)
            state_ls.append(state)
            number_ls.append(number)
            title_ls.append(title)
            latest_action_date_ls.append(latest_action_date)
            latest_action_description_ls.append(latest_action_description)
            first_action_ls.append(first_action)
            sponsor_name_ls.append(sponsor_name)
            sponsor_id_ls.append(sponsor_id)
            sponsor_party_ls.append(sponsor_party)
            subject_ls.append(subjects)
            p_title_ls.append(p_title)
            district_ls.append(district)
            # abstracts_ls.append(abstracts)
            # other_titles_ls.append(other_titles)
            
            # df = pd.DataFrame(columns=["bill_id", "session", "state", "number", "title", "first_action", "latest_action_date", "latest_action_description", "sponsor_name"])
        
        df = pd.DataFrame({"bill_id": bill_id_ls, 
                           "session": session_ls, 
                           "state": state_ls, 
                           "number": number_ls, 
                           "title": title_ls, 
                           'subjects': subject_ls, 
                           "first_action": first_action_ls, 
                           "latest_action_date": latest_action_date_ls, 
                           "latest_action_description": latest_action_description_ls, 
                           "sponsor_name": sponsor_name_ls,
                           "sponsor_id": sponsor_id_ls,
                           "sponsor_party": sponsor_party_ls,
                           "p_title": p_title_ls,
                           "district": district_ls})

        # print(df)
        dfs.append(df)
    dfs_final = pd.concat(dfs)
    
    

    return dfs_final
    
        # all_dfs.append(dfs_final)

    # full_data = pd.concat(all_dfs)


    # return full_data
# %% 2025 data pull
thi_states = ["OK", "VA", "WV", "AL", "CT", "IL", "IN", "KS", "MO", "NC", "ND", "NM", "OH"]

all_dfs = []
for state in thi_states:
    all_bills = get_all_bills(state)
    all_dfs.append(all_bills)


# %%

test_df = get_all_bills('nc')

# %%    """Fetch a list of bills for a specific state."""
    

    # response = requests.get(BASE_URL, headers=headers, params=params)
    
    # if response.status_code == 200:
    #     data = response.json()
    #     print('got data')
    #     return data
        
    # else:
    #     print(f"Error: {response.status_code}")
    #     print(f"Response status code: {response.status_code}")
    #     print(f"Response text: {response.text}")

    #     return None



# %% North Carolina bills
#last pull: 10/16/24
all_bills_nc = get_all_bills("nc", 2023)

os.chdir(r'C:\Users\clutz\OneDrive - THE HUNT INSTITUTE\Documents\Data\NC\api results')
all_bills_nc.to_csv('nc_bills_10_16_24.csv', index=False)
# %%  North Dakota Bills
# last pull: 10/18/24
all_bills_nd = get_all_bills("nd")
os.chdir(r'C:\Users\clutz\OneDrive - THE HUNT INSTITUTE\Documents\Data\ND\api results')
all_bills_nd.to_csv('nd_bills_10_18_24.csv', index=False)
# %% Oklahoma

all_bills_ok = get_all_bills("ok")
os.chdir(r'C:\Users\clutz\OneDrive - THE HUNT INSTITUTE\Documents\Data\OK\api results')
all_bills_ok.to_csv('ok_bills_10_18_24.csv', index=False)




# %% narrow down to ed bills

ed_bills = all_bills[all_bills.title.str.contains('.*[Ee]ducation.*|.*[Cc]hild.*|.*[Ss]chool.*|.*[Cc]harter.*|.*[Mm]ath.*|.*[Rr]ead.*|.*[Tt]each.*|.*[Pp]arent.*|.*[Kk]id.*|.*[Ss]tudent.*|.*[Cc]ollege.*|.*[Uu]niversit.*|.*[Tt]uition.*', regex = True)]

# %% THI Bill Tracker import
thi_bill_tracker_file = r"C:\Users\clutz\OneDrive - THE HUNT INSTITUTE\Documents\Data\thi_bill_tracker.xlsx"
thi_bill_tracker = pd.ExcelFile(thi_bill_tracker_file)



# %%
if __name__ == "__main__":
    state_code = 'ca'  # California
    legislator_id = 'ocd-person/1234'  # Replace with a valid legislator ID

    # Fetch legislator information
    legislator_info = get_legislator_info(state_code, legislator_id)
    if legislator_info:
        print("Legislator Info:", legislator_info)

    # Fetch bills for the state
    bills_info = get_bills_by_state(state_code)
    if bills_info:
        print("Bills Info:", bills_info)