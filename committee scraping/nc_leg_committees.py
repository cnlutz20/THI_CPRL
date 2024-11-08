# %%
import os, sys, json, datetime, re  # Provides OS-dependent functionality, system-specific parameters, JSON handling, and date/time manipulation
import pandas as pd             # Provides data structures and data analysis tools
import numpy as np              # Supports large, multi-dimensional arrays and matrices
import requests
import time
from tqdm import tqdm
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#webscraping imports
from bs4 import BeautifulSoup
from lxml import etree, html


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# %%

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager



# %%

# Path to your WebDriver executable (adjust if necessary)
webdriver_path = r"C:\Users\clutz\hunt_env\chrome driver\chromedriver-win64\chromedriver.exe"

# Set up Chrome options
chrome_options = Options()
# chrome_options.add_argument("--headless")  # Run in headless mode (no GUI)

# Set up WebDriver service
service = Service(webdriver_path)

# Initialize WebDriver
# driver = webdriver.Chrome(service=service, )

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)


# %%

file = r"C:\Users\clutz\OneDrive - THE HUNT INSTITUTE\Documents\Data\legislator data\committees_data.xlsx"

coms = pd.read_excel(file)

nc_coms = coms[coms['state'] == "NC"]

[print(x) for x in enumerate(nc_coms['url'])]
nc_coms = nc_coms.drop_duplicates(subset=['committee', 'url'], keep='first')
nc_coms.reset_index(inplace=True, drop=True)

# %%

members_list = []
for i,url in enumerate(nc_coms['url']):
    print("#######################")
    print(url)
    url = nc_coms['url'].iloc[i]
    print(nc_coms['committee'].iloc[i])
    driver.get(url)
    
    
    time.sleep(3)

    # html_from_page = driver.page_source
    
    # Find all matching divs
    xpath_expression = '//*[@id="Membership"]'
    divs = driver.find_elements(By.XPATH, xpath_expression)
    if len(divs) == 1:
        text = divs[0].text
    elif len(divs) > 1:
        print("more than one matching div")
    else:
        print('no matching divs')
    members = text.split('\n')

    members_df = pd.DataFrame({"member": members})
    members_df['roles'] = members_df['member'].apply(lambda x: 'chair' if 'chair' in x.lower() else ('member' if 'member' in x.lower() else np.nan))
    members_df['member'] = members_df['member'].apply(lambda x: np.nan if 'chair' in x.lower() else (np.nan if 'member' in x.lower() else x))
    # members_df['member'] = members_df['roles'].apply(lambda x: x if 'nan' in str(x).lower() else np.nan)
    members_df['committee'] = str(nc_coms['committee'].iloc[i])

    members_df['roles'] = members_df['roles'].ffill()
    members_df = members_df.dropna(subset=['member'])
    members_list.append(members_df)
# %%
nc_coms_members = pd.concat(members_list)
nc_coms_members.reset_index(inplace=True, drop=True)


nc_coms_members = nc_coms_members[nc_coms_members['member'].str.contains('sen.', regex=True, case=False)]
nc_coms_members['member'] = nc_coms_members['member'].fillna('').astype(str).str.replace('Sen.', '').str.strip().str.split(' ').str[-1]
os.chdir(r'C:\Users\clutz\OneDrive - THE HUNT INSTITUTE\Documents\Data\legislator data')
nc_coms_members.to_csv('nc_coms_members.csv', index=False)
# %%
driver.quit()

# %%    
    print(members)
    # roles = []
    for div in divs:
        print('#######')
        print(div.text)
        members.append(div.text)
    len(members)
    members_df = pd.DataFrame({"member": members})
    
    





    for i,j in enumerate(members_df['member']):
        if 'chair' in str(j).lower() or 'member' in str(j).lower():
            
    
    response = requests.get(html_from_page, verify=False)
    
    tree = html.fromstring(response.content)
    
    divs = tree.xpath(xpath_expression)
    for div in divs:
        print(div.text_content())
    
    
    
    driver.get(url)
    time.sleep(5)

    # print(response.text)  # Check the raw HTML
    html_from_page = driver.page_source
        tree = html.fromstring(response.content)
    
    
    soup = BeautifulSoup(html_from_page, 'html.parser')
    print('\n')

    # member_cards = soup.find_all("div",{id:"Memberships"})


    members = etree.HTML(str(soup))

    print(members.xpath('//*[@id="Membership"]')[0].text)
    # for m in member_cards:
    #     print("######################")
    #     print(m)
    #     print("\n")
    # print(member_cards.text)

# %%

soup = BeautifulSoup(r.text, 'html5lib') # If this line causes an error, run 'pip install html5lib' or install html5lib
# %%
links = soup.find_all('a')

commitee_urls = {}
base_url = 'https://www.ncleg.gov'
for link in links:
    href = link.get('href', '')
    full_url = base_url+href
    text = link.get_text(strip=True)
    if 'SenateStanding' in href or 'SenateStanding' in text:
        if 'Education' in text or "Health Care" in text:
            commitee_urls[text] = full_url 
for k,v in commitee_urls.items():
    print(k) 
    print(v)
# %%        
base_url = 'https://www.ncleg.gov'
full_committee_urls = [base_url + url if url.startswith('/') else url for url in committee_urls]

# %%
# Send a GET request to the page
response = requests.get(url)
response.raise_for_status()  # Check that the request was successful

# Parse the page content
soup = BeautifulSoup(response.text, 'html.parser')

# Find all links related to committees
committee_links = soup.find_all('a', href=True)



# Extract URLs and filter out non-committee links
committee_urls = [link['href'] for link in committee_links if 'Committee' in link.text]

# Print the extracted URLs
for url in committee_urls:
    print(url)

# Optional: If you need to get the full URLs, prepend the base URL
base_url = 'https://www.ncleg.gov'
full_committee_urls = [base_url + url if url.startswith('/') else url for url in committee_urls]

print("\nFull Committee URLs:")
for full_url in full_committee_urls:
    print(full_url)