# %%
import os, sys, json, datetime, re  # Provides OS-dependent functionality, system-specific parameters, JSON handling, and date/time manipulation
import pandas as pd             # Provides data structures and data analysis tools
import numpy as np              # Supports large, multi-dimensional arrays and matrices
import requests
import time
from tqdm import tqdm
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
pd.options.mode.chained_assignment = None  # default='warn'


from bs4 import BeautifulSoup
# %%

def take_away_titles(x) :
    if '|' in str(x):
        parts = x.split('|', 1)
        keep = str(parts[-1])
        print("removing ", parts[0])
        print(keep)
        return keep
    else:
        return x
# %%

def take_out_roles(x) :
    if '(' in str(x) or ')' in str(x):
        new_x = re.sub(r'\(.{,25}\)', "",str(x))
        return str(new_x)
    else:
        return x
        
# %%

def assign_to_list(x) :
    if isinstance(x, float):
        return x
    
    temp_list = []

    parts = x.split(',')
    parts = [f for f in parts if len(f) > 0]
    for part in parts:
        print(part)
        temp_list.append(part)
    return temp_list
        
# %%
file = r"C:\Users\clutz\OneDrive - THE HUNT INSTITUTE\Documents\Data\legislator data\IL\Il_committee_data_from_quorum.xlsx"
il_coms_data = pd.read_excel(file)

# print(il_coms_data)
il_coms_data.columns = ['full_id', 'title', 'party', 'com_list']


il_coms_data.loc[:,'com_list'] = il_coms_data['com_list'].apply(take_away_titles)
il_coms_data.loc[:,'com_list'] = il_coms_data['com_list'].apply(take_out_roles)


# %%

il_coms_data_senate = il_coms_data[il_coms_data["full_id"].str.contains('Sen.')]
il_coms_data_house = il_coms_data[il_coms_data["full_id"].str.contains('Rep.')]

# %%


# committee_names = il_coms_data['com_list'].to_list()
senate_names = il_coms_data_senate['com_list'].apply(assign_to_list)
house_names = il_coms_data_house['com_list'].apply(assign_to_list)




# %%


def create_list(names):

    master = []
    for name in names:
        # print(name)
        if isinstance(name, float):
            continue
        for n in name:
            # print('###########')
            # print(n)
            master.append(str(n).strip())
    master_set = set(master)
    master_list =[item for item in master_set]
    compiled_list = "|".join(master_list)
    print(compiled_list)
# %%

create_list(senate_names)
create_list(house_names)

# %%
master_set = set(master)


master_list =[item for item in master_set]


compiled_list = "|".join(master_list)

















# %%

file = r"C:\Users\clutz\OneDrive - THE HUNT INSTITUTE\Documents\Data\legislator data\committees_data.xlsx"

coms = pd.read_excel(file)

il_coms = coms[coms['state'] == "IL"]

# %%
il_coms = il_coms.drop_duplicates(subset=['committee', 'url'], keep='first')
il_coms.reset_index(inplace=True, drop=True)


# %%
com_dfs = {}
member_urls_list = []
for i,j in tqdm(enumerate(il_coms['url'])):
    # print("________________________________")
    ii = 0
    # j = "https://www.ilga.gov/house/committees/members.asp?CommitteeID=2879&GA=103"
    response = requests.get(j, verify = False).content
    df_list = pd.read_html(response)
    # print(df_list)
    # print(df_list)
    # print(j)
    for df in df_list:
        ii += 1
        # print("######### Item " + str(ii) + " ############")
        # print(df.iat[0,0])
        if str(df.iat[0,0]).strip() == "Role":
            df_extract = df
            df_extract.columns = df_extract.iloc[0]
            df_extract = df_extract[1:]
            break
    
    # print(type(df_extract))
    soup = BeautifulSoup(response, 'html.parser')


    urls = []
    for a in soup.find_all('a', href=True,  class_='notranslate'):
        url = "https://www.ilga.gov" + a['href']
        urls.append(url)



    df_extract.loc[:,'urls'] = urls
    df_extract.loc[:,'district'] = ""
    for iu,url in enumerate(df_extract['urls']):
        response = requests.get(url, verify = False).content
        soup = BeautifulSoup(response, 'html.parser')


        soups = soup.find_all('span')
        # print("soup length: ",len(soups))
        if len(soups) == 0:
            print('soup didnt work')
            break

        
        
        found = False
        for noodle in soups:
            # print(noodle)
            # print(noodle.text)
            if re.search(r'\d{1,2}[rdstndh]{2}', str(noodle)):
                district = re.sub(r'[rdstndh]', "", noodle.text)
                found = True
            
                
        
        if found != True:
            print('no district found for: ', df_extract.iloc[iu, 1])
            print(url)

            #     break
        # print("district is", district)    
        
        df_extract.loc[iu,'district'] = district
    
    
    df_extract = df_extract.loc[:, df_extract.columns != 'url']
    # print(df_extract)
    # print(*urls,"\n")



    # member_urls = soup.find_all('a', href=True, class_='notranslate')

    # for mem in member_urls:
    #     # if "MemberID" in str(mem):
    #     # print(mem)
    #     # print(mem.text)
        
    #     member_urls_list.append(mem)
    
    
    com_dfs[str(il_coms['committee'].iloc[i])] = df_extract 

# %%
for k,v in com_dfs.items():
    print("#############################")      
    print(k)
    print(v)
    print("\n")
    df_temp = v


    





# %%
