

# %%
#importing modules
import re  
import pandas as pd             # Provides data structures and data analysis tools
from openpyxl import Workbook

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
pd.options.mode.chained_assignment = None  # default='warn'



# %%
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

state_abbreviations_reg = []
for abv in state_abbreviations:
    for_regex = f'^{abv}'
    state_abbreviations_reg.append(for_regex)

state_pat = re.compile("|".join(state_list))
state_abv_pat = re.compile("|".join(state_abbreviations_reg))
#dictionary creation for future reference in later cells
codes = list(range(10,61,1))

thi_states = ['ND', 'NM', 'OH', 'OK', 'VA', 'WV', 'AL', 'CT', 'IL', 'IN', 'KS', 'MO', 'NC']
state_ref = dict(zip(state_list, state_abbreviations))
state_coding = dict(zip(state_abbreviations, codes))

for k,v in state_coding.items():
    print(k,v)


# save_list = [thi_states,state_ref, state_coding]

# for name in dir():
#     if name not in save_list:
#         del globals()[name]


# for name in dir():
#     if name not in save_list:
#         del locals()[name]