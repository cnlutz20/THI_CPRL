# %%
import os, sys, json, datetime  # Provides OS-dependent functionality, system-specific parameters, JSON handling, and date/time manipulation
import pandas as pd             # Provides data structures and data analysis tools
import numpy as np              # Supports large, multi-dimensional arrays and matrices
import requests
import time
from tqdm import tqdm

# %%



API_KEY = '1d0dc220-f3f3-4f05-b73f-10a7e08f4451'  # Replace with your actual API key

URL = "https://v3.openstates.org/people?jurisdiction=North%20Carolina&page=1&per_page=10&apikey=1d0dc220-f3f3-4f05-b73f-10a7e08f4451"
# BASE_URL = 'https://v3.openstates.org/bills'
PARAMS = {
    'jurisdiction': "North Carolina",
    'include': ['abstracts', 'other_titles', 'sponsorships','actions'],
    'page': 1,
    'per_page': 20
    }

headers = {
    'X-API-KEY': API_KEY
}

params = PARAMS.copy()
# year = 2023 #only for troubleshooting; comment out when using it fully as a defined function
# params['session'] = session

response = requests.get(URL)
if response.status_code == 200:
    # Get the JSON content from the response
    content = response.json()

    # Access the 'max_page' value
    max_page = content['pagination']['max_page']
    
    if len(content['results']) == 0:
        print('no data')
        # return None
    # Print the 'max_page' value
    print(max_page)
else:
    print(f"Request failed with status code {response.status_code}")
    # return None


#iterate through all the pages
all_dfs = []
for page in tqdm(range(1,max_page,1)):
    time.sleep(6)
    API_KEY = '1d0dc220-f3f3-4f05-b73f-10a7e08f4451'  # Replace with your actual API key

    URL = "https://v3.openstates.org/people?jurisdiction=North%20Carolina&page=1&per_page=10&apikey=1d0dc220-f3f3-4f05-b73f-10a7e08f4451"
    # BASE_URL = 'https://v3.openstates.org/bills'
    PARAMS = {
        'jurisdiction': "North Carolina",
        'include': ['abstracts', 'other_titles', 'sponsorships','actions'],
        'page': page,
        'per_page': 20
        }

    headers = {
        'X-API-KEY': API_KEY
    }

    params = PARAMS.copy()
    # year = 2023 #only for troubleshooting; comment out when using it fully as a defined function
    # params['session'] = session

    response = requests.get(URL, headers=headers, params=params)
    content = response.json()

    leg_id_ls = []
    name_ls = []
    party_ls = []
    title_ls = []
    org_classification_ls = []
    district_ls = []
    div_id_ls = []
    
    for person in content.get('results', []):
        
        
        leg_id = person.get('id')
        name = person.get('name')
        party = person.get('party')
        current_role = person.get('current_role', {})
        title = current_role.get('title')
        org_classification = current_role.get('org_classification')
        district = current_role.get('district')
        div_id = current_role.get('division_id')


        # # Handle potential empty 'actions' list
        # if bill.get('actions'):
        #     latest_action_date = bill['actions'][0].get('date')
        #     latest_action_description = bill['actions'][0].get('description')
        # else:
        #     latest_action_date = None
        #     latest_action_description = None

        # first_action = bill.get('first_action_date')
        # # Handle potential empty 'sponsorships' list
        # if bill.get('sponsorships'):
        #     sponsor_name = bill['sponsorships'][0].get('name')
        # else:
        #     sponsor_name = None

        leg_id_ls.append(leg_id)
        name_ls.append(name)
        party_ls.append(party)
        title_ls.append(title)
        org_classification_ls.append(org_classification)
        district_ls.append(district)
        div_id_ls.append(div_id)


        # sponsor_name_ls.append(sponsor_name)
        # subject_ls.append(subjects)
        # abstracts_ls.append(abstracts)
        # other_titles_ls.append(other_titles)
        
        # df = pd.DataFrame(columns=["bill_id", "session", "state", "number", "title", "first_action", "latest_action_date", "latest_action_description", "sponsor_name"])
    
    df = pd.DataFrame({
    'leg_id': leg_id_ls,
    'name': name_ls,
    'party': party_ls,
    'title': title_ls,
    'org_classification': org_classification_ls,
    'district': district_ls,
    'div_id': div_id_ls,
    })
    print(df)
    all_dfs.append(df)

export_df = pd.concat(all_dfs)


# %%

os.chdir(r'C:\Users\clutz\OneDrive - THE HUNT INSTITUTE\Documents\Data\ref data')
export_df.to_csv('leg_ref_nc.csv')
# %%
