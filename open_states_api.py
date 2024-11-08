# %%
# Importing basic Python modules

import os, sys, json, datetime  # Provides OS-dependent functionality, system-specific parameters, JSON handling, and date/time manipulation
import pandas as pd             # Provides data structures and data analysis tools
import numpy as np              # Supports large, multi-dimensional arrays and matrices
import requests
import time
from tqdm import tqdm



# %%

API_KEY = 'd07ea2eb-e174-46fe-851b-3e5df5eb2fe8'  # Replace with your actual API key
BASE_URL = 'https://v3.openstates.org/people'



headers = {
    'X-API-KEY': API_KEY
}

PARAMS = {
    'jurisdiction': 'nc', 
    'per_page': 50,
    }

params = PARAMS.copy()
# %%

#Intial API call for pagination
response = requests.get(BASE_URL,params=params, headers=headers)#
print(response.status_code)

# # %%
#get max page
legislators = response.json()
max_page = legislators['pagination'].get('max_page')



# %%
states = pd.read_excel(r"C:\Users\clutz\OneDrive - THE HUNT INSTITUTE\Documents\Data\state_intitlas.xlsx")
print(states)

states_sub = states.iloc[[6,7,10],:]
print(states_sub)
# %%
all_states = []
for i,state in enumerate(states_sub['state']):
    print("working on state: " + str(state))
    if i != 0:
        time.sleep(5)
    state = "nc"
        
    
    legislators_dfs = []

    PARAMS = {
            'jurisdiction': state,
            'per_page': 50,
            }

    params = PARAMS.copy()
    response = requests.get(BASE_URL,params=params, headers=headers)
    legislators = response.json()
    max_page = legislators['pagination'].get('max_page')
    for ik in tqdm(range(1,max_page)):
        time.sleep(7)

        PARAMS = {
            'jurisdiction': state,
            'per_page': 50,
            'page': ik
            }

        params = PARAMS.copy()
        response = requests.get(BASE_URL,params=params, headers=headers)
        if response.status_code != 200:
            print(f"Error: {response.status_code} - {response.text}")
            break
        
        legislators = response.json()


    
        max_page = legislators['pagination'].get('max_page')

        # try:
        #     legislators['results']:
        #         # print(legislators['results'])
        #         # print(params)
        #         print('continuing')
        # except:
        #     print("issue with " + str(j))
        #     break

        # legis
        for j in legislators['results']:

            # print(type(j))
            juri_inner_dict = j.get('jurisdiction')
            state = juri_inner_dict.get('name')
            name = j.get('name')
            fname = j.get('given_name')
            lname = j.get('family_name')
            # title = j.get('title')
            cur_role_dict = j.get('current_role')
            title = cur_role_dict.get('title')
            # to_append = [id, name, classification]
            df = pd.DataFrame({"juri": [state], "name":[name], "fname":[fname],"lname":[lname], "title": [title]})
            # print(df)
            legislators_dfs.append(df)


    leg_df = pd.concat(legislators_dfs)
    leg_df.reset_index(inplace=True, drop=True)
    all_states.append(leg_df)

all_data = pd.concat(all_states)
# %%

quorum_file = r"C:\Users\clutz\OneDrive - THE HUNT INSTITUTE\Documents\Data\imports\quorum\leadership downloads\leadership_nc_ok_nd.xlsx"
quorum_data = pd.read_excel(quorum_file)

all_data['leadership'] = all_data['lname'].isin(quorum_data['Last Name'])



# %%

merged_df = pd.merge(df1, df2, on='id', how='inner')  # Options: 'inner', 'outer', 'left', 'right'


# %%
for l in legislators_dfs:
    print(l)


# %% get list of jurisdictions
API_KEY = 'd07ea2eb-e174-46fe-851b-3e5df5eb2fe8'  # Replace with your actual API key
BASE_URL = 'https://v3.openstates.org/jurisdictions'


headers = {
    'X-API-KEY': API_KEY
}

PARAMS = {
    'classification': 'state',
    }

params = PARAMS.copy()
# params['session'] = year



#Intial API call for pagination
response = requests.get(BASE_URL,params=params, headers=headers)
juris = response.json()

juris_dfs = []
for j in juris['results']:
    print(j.get('id'))
    print(j.get('name'))


#     id = j.get('id')
#     name = j.get('name')
#     # classification = j.get('classification').get('name')
#     to_append = [id, name]
#     juris_dfs.append(to_append)

# all_juris = pd.concat(juris_dfs)
    


# %%

if response.status_code == 200:
        content = response.json()
        max_page = content['pagination']['max-page']

for j in range(1,max_page):


juris = response.json()
juris_dict = juris.get('results')




# %%



juris_df = []
for bill in juris['results']:
    # Extract attributes from each bill
    
    
    bill_id = bill.get('id')
    session = bill.get('session')
    state = bill.get('jurisdiction', {}).get('name', 'Unknown')
    number = bill.get('identifier')
    title = bill.get('title')
    latest_action_date = bill.get('actions', [{}])[0].get('date', 'Unknown')
    latest_action_description = bill.get('actions', [{}])[0].get('description', 'Unknown')
    first_action = bill.get('first_action_date')

    try:
        sponsor_name = bill.get('sponsorships', [{}])[0].get('name', 'None')
        sponsor_id = bill.get('sponsorships', [{}])[0].get('person', {}).get('id', 'None')
    except IndexError:
        sponsor_name = 'None'
        sponsor_id = 'None'

    to_append = [state, session, number, title, first_action, latest_action_date, latest_action_description, sponsor_name, bill_id, sponsor_id]
    print(to_append)
    # Append to the data list
    df.append(to_append)

# %%





def get_nc_bills():
    #set up
    API_KEY = '1d0dc220-f3f3-4f05-b73f-10a7e08f4451'  # Replace with your actual API key
    BASE_URL = 'https://v3.openstates.org/bills'
    PARAMS = {
    'jurisdiction': 'nc',
    'include': ['sponsorships','actions'],
    'classification': 'bill',
    'page': 1,
    'per_page': 20
    }
    
    headers = {
        'X-API-KEY': API_KEY
    }

    params = PARAMS.copy()
    # params['session'] = year


    #Intial API call for pagination
    response = requests.get(BASE_URL, headers=headers, params=params)


    
    if response.status_code == 200:
        content = response.json()
        max_page = content['pagination']['max-page']
    else:
        print('intial request failed')
        break
    

    
    print(max_page)
    
    """Fetch a list of bills for a specific state."""
    
    

    for page in range()

    response = requests.get(BASE_URL, headers=headers, params=params)
    
    if response.status_code == 200:
        data = response.json()
        print('got data')
        return data
    else:
        print(f"Error: {response.status_code}")
        print(f"Response status code: {response.status_code}")
        print(f"Response text: {response.text}")

        return None

    data



# %%

data = get_nc_bills()

# results = data.get('results')
df = []
for bill in data['results']:
    # Extract attributes from each bill
    bill_id = bill.get('id')
    session = bill.get('session')
    state = bill.get('jurisdiction', {}).get('name', 'Unknown')
    number = bill.get('identifier')
    title = bill.get('title')
    latest_action_date = bill.get('actions', [{}])[0].get('date', 'Unknown')
    latest_action_description = bill.get('actions', [{}])[0].get('description', 'Unknown')
    first_action = bill.get('first_action_date')

    try:
        sponsor_name = bill.get('sponsorships', [{}])[0].get('name', 'None')
        sponsor_id = bill.get('sponsorships', [{}])[0].get('person', {}).get('id', 'None')
    except IndexError:
        sponsor_name = 'None'
        sponsor_id = 'None'

    to_append = [state, session, number, title, first_action, latest_action_date, latest_action_description, sponsor_name, bill_id, sponsor_id]
    print(to_append)
    # Append to the data list
    df.append(to_append)

df2 = pd.DataFrame(df[0:])
try:
    df2.columns = ['state', 'session', 'number', 'title', 'first_action', 'latest_action_date', 'latest_action_description', 'sponsor_name', 'bill_id', 'sponsor_id']
except:
    print(df2)
# %%
for k,v in data.items():
    print('################')
    print(k)
    print(v)
    print('/n')
# %%
print(type(data))
print(list(data))
print(data)
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



# %%

# Function to make API call and retrieve all legislators
def get_legislators(params):
    all_legislators = []
    while True:
        response = requests.get(BASE_URL, params=params, headers=headers)
        if response.status_code != 200:
            print(f"Error: {response.status_code} - {response.text}")
            break
        
        data = response.json()
        all_legislators.extend(data)  # Add the results to the list
        
        # Check for pagination
        if len(data) < params['per_page']:  # If fewer results than per_page, we are done
            break
        
        # Increment the page number
        if 'page' in params:
            params['page'] += 1
        else:
            params['page'] = 2  # Start with page 2 if not set
    
    return all_legislators

# Call the function to get all legislators
legislators = get_legislators(PARAMS)