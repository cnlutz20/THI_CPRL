# %%
import os, sys, json, datetime, re  # Provides OS-dependent functionality, system-specific parameters, JSON handling, and date/time manipulation
import pandas as pd             # Provides data structures and data analysis tools
import numpy as np              # Supports large, multi-dimensional arrays and matrices
import requests
import time
from tqdm import tqdm
# %%
os.chdir(r'C:\Users\clutz\OneDrive - THE HUNT INSTITUTE\Documents\Data\data imports')


df = pd.read_excel("nc_senators.xlsx")


senate = df.iloc[:, 1:13]
print(list(senate))


col_names = ['full_title', 'first_name', 'last_name', 'title', 'primary_organization', 'state', 'district', 'party', 'email', 'phone_number', 'website', 'on_committees']
senate.columns = col_names
senate["Appropriations on Education / Higher Education"] = np.nan
senate["Education / Higher Education"] = np.nan
senate["Health Care"] = np.nan



# print(list(df))
# %%
#making regex pattern
com_names =["Appropriations on Education / Higher Education","Education / Higher Education","Health Care"] 
regex_pat = "|".join(com_names)
print(regex_pat)
# %%
senate['ed_coms'] = ""
for i,j in enumerate(senate['on_committees']):
    committees = str(j).split(",")
    committees = [str(c).strip() for c in committees]
    
    # print(committees)

    try:
        matches = [re.findall(regex_pat, str(c)) for c in committees]
        matches = [m for m in matches if len(m) > 0]
        if len(matches) == 0:
            continue

        matches_flat = [match for sublist in matches for match in sublist]
        print(matches_flat)

        senate.loc[i,matches_flat] = "member"
        
            # match = matches_flat[0]
            # if 'Appropriations' in str(match):
            #         senate["Appropriations on Education/Higher Education"].iloc[i] = "member"
            # if 'Appropriations' not in str(match):

        # print(type(matches_flat))
        # for m in matches_flat:
        #     if "appropriations" in str(m).lower():
        #         senate["Appropriations on Education/Higher Education"].iloc[i] = "member"

        #     if "higher education" in str(m).lower() and "appropriation" not in str(m).lower():
        #         senate["Education/Higher Education"].iloc[i] = "member"
            
        #     if 'health care' in str(m).lower():
        #         senate['Health Care'].iloc[i] = "member"
        
        # print("############")
        # print(senate['Full Name'].iloc[i])
        # print(matches_flat)
        # print("\n")
        senate['ed_coms'].iloc[i] = matches_flat

    except:
        # print('no committee matches')
        senate['on_committees'].iloc[i] = ""
        continue

# %%member or chair

'''
Finds and matches where chair proceeds the committee they serve on. 
Then matches and changes value from member to chair for that legislator
'''

for i,j in enumerate(senate['on_committees']):
    if len(senate.loc[i,'ed_coms']) == 0:
        continue

    regex = '^(.*?)(?:,\s*)?\((?:Vice\s+|Co\s+)?Chair\)'
    chairs = re.findall(regex, str(j))
    chairs = [str(c).strip() for c in chairs]

    if len(chairs) == 0:
        continue
    else:
        chair = chairs[0]
    try:
        in_columns = False
        for l in list(senate):
            if str(chair) in l:
                in_columns = True
                break
            else:
                continue

        if in_columns == True:                
            senate.loc[i,chair] = 'chair'
        else:
            continue
    except:
        print('assignment not made')
        continue
       
    # %%
    print('##########################')
    print(senate.loc[i,'full_title'])
    print(chairs)
    print('##########################')
    print('\n')
    # for ch in chairs:
    #     if str(ch) in com_names:
    #         print("found one")
# %%
    if len(chairs) == 1:
        chairs[0]
        senate.loc[i,matches_flat] = "member"



#     for com in com_names:
#         if 
# # %%

#     for c in chair:
#         if 'education' in str(c).lower() or 'health care' in str(c).lower():

#     print("##############")
#     print(chair)
#     print("##############")
#     print('\n')


