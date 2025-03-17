# %%
import os, sys, json, datetime, re  # Provides OS-dependent functionality, system-specific parameters, JSON handling, and date/time manipulation
import pandas as pd             # Provides data structures and data analysis tools
import numpy as np              # Supports large, multi-dimensional arrays and matrices
import requests
import time
from tqdm import tqdm
import urllib3
import tabula as tb
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


from bs4 import BeautifulSoup





# %%


"""
NEEDS TO BE FIXED

There seems to be issues with the data
 being collected stopping at the
 higher education budget committee

"""
# %%

file = r"C:\Users\clutz\OneDrive - THE HUNT INSTITUTE\Documents\Data\legislator data\committees_data.xlsx"

coms = pd.read_excel(file)

ks_coms = coms[coms['state'] == "KS"]

# %%
ks_coms = ks_coms.drop_duplicates(subset=['committee', 'url'], keep='first')
ks_coms.reset_index(inplace=True, drop=True)
# %%
# url = ks_coms['url'].iloc[1]


site = "https://ndlegis.gov/assembly"

response = requests.get(site, verify = False)
soup = BeautifulSoup(response.content, 'html.parser')


# print(soup.text)
assemb = soup.find_all('a')

for a in assemb:
    print("######################################")
    print(a)

    if 'Current' in str(a):
        base = "https://ndlegis.gov"
        href = a.get('href')
        link = f'{base}{href}'
        print(link)
        break


current_session = f'{link}'

# %%

response = requests.get(current_session, verify = False)
soup = BeautifulSoup(response.content, 'html.parser')

links = soup.find_all('a')

for link in links:
    if 'standing' in str(link):
        print("######################")
        print(link)


file = "C:\Users\clutz\Downloads\2023-ndla-senate-standing-committees.pdf"


# %% loop to get data

ks_com_dict = {}
dfs_to_append = []
for i,url in tqdm(enumerate(ks_coms['url'])):
    response = requests.get(url, verify = False)
    soup = BeautifulSoup(response.content, 'html.parser')

    side_bar = soup.find('div', id='sidebar')
    # print(type(side_bar))
    side_contents = side_bar.find_all("ul")

    print(ks_coms['committee'].iloc[i])
    print(len(side_contents))
    

    for i,s in enumerate(side_contents):
        members = []
        roles = []# print(i)
        # Chair
        
            
        name = s.get_text()
        name = name.split('\n')
        name = [x for x in name if len(x) != 0]
        if not isinstance(name, list):
            name = [name]
                
        if i < 2:
            position = len(name) * ['Chair']

        # Ranking Minority Member
        elif i > 2:
            position = len(name) * ['Member']
            


        elif i > 3:
            break
        
        members.extend(name)
        roles.extend(position)

        append_df = pd.DataFrame({"members": members, "roles": roles})
        print("append_df length: " + str(len(append_df)))
        dfs_to_append.append(append_df)

        print("dfs to append: " + str(len(dfs_to_append)))


        ks_dfs = pd.concat(dfs_to_append)
        ks_com_dict[ks_coms['committee'].iloc[i]] = ks_dfs

# %%

for k,v in ks_com_dict.items():
    print("##################")
    print(k)
    # print(v)
# %%

    print(s.get_text())
    new = s.find("li")
    text = new.get_text(strip=True)
    print(text)
print(type(side_bar))


for s in side_contents:
    print(s)
    
# %%

print(response.text)
# %%
df_list = pd.read_html(response)

print(url)
# %%

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Path to your WebDriver executable (adjust if necessary)
webdriver_path = r"C:\Users\clutz\hunt_env\chrome driver\chromedriver-win64\chromedriver.exe"

# Set up Chrome options
chrome_options = Options()
# chrome_options.add_argument("--headless")  # Run in headless mode (no GUI)

# Set up WebDriver service
service = Service(webdriver_path)

# Initialize WebDriver
driver = webdriver.Chrome(service=service, options=chrome_options)



# %%
# url = in_coms['url'].iloc[0]
# print(in_coms['committee'].iloc[0])

member_dict = {}
for i,url in enumerate(in_coms["url"]):
    driver.get(url)
    time.sleep(5)

    # print(response.text)  # Check the raw HTML
    html_from_page = driver.page_source
    soup = BeautifulSoup(html_from_page, 'html.parser')

    member_cards = soup.find_all(class_='MemberCard_memberCardContent__5CHYi')

    if len(member_cards) == 0:
        print(in_coms['committee'].iloc[i])
        break


    members = []
    role = []
    members_df = []
    for member in member_cards:
        
        name = member.select_one('.MemberCard_memberCardName__AA367 span').text.strip()
        position = member.select_one('.MemberCard_memberCardPosition__3b90Z p').text.strip()
        members.extend([name])
        role.extend([position])

        try:
            df = pd.DataFrame({"member": members, "position": role})
        except:
            print("members list length: " + str(len(members)))
            print(members)
            print("roles list length: " + str(len(role)))
            print(role)
            break

        members_df.append(df)
    in_com_dfs = pd.concat(members_df)
    member_dict[in_coms['committee'].iloc[i]] = in_com_dfs

# %%
for k,v in member_dict.items():
    print('########################')
    print(k)
    print(v)
    print('\n')
