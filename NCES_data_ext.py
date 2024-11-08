
# %%
# For general-purpose operations
import os, sys, datetime, math, random, json, re

# For data manipulation and analysis
import pandas as pd  # Data analysis and manipulation
import numpy as np   # Numerical operations
from bs4 import BeautifulSoup # webscraping
import html5lib

# For web requests and handling
import requests   # Make HTTP requests
from urllib.parse import urlparse  # Parse URLs



# For file handling
import csv  # Read and write CSV files
import sqlite3  # SQLite database operations

# For testing and debugging
import unittest  # Unit testing framework
import logging   # Logging 

# %%

url = "https://nces.ed.gov/programs/digest/current_tables.asp"
response = requests.get(url)
headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"}
r = requests.get(url, headers)
soup = BeautifulSoup(r.text, 'html5lib') # If this line causes an error, run 'pip install html5lib' or install html5lib
# %%
paras = soup.find_all('option')

year = 2021

main_url = "https://nces.ed.gov"

dict = {}
for p in paras:
    
    if re.search(r'\>\d{4}\<', str(p)):
        
        year = re.findall(r'\d{4}', str(p))[0]
        print(year)
        splits = str(p).split('"')
        for split in splits:
            # print('###############')
            # print(split)
            # print('\n')
            if 'menu_tables' in split:
                year_data = main_url+split
                print(year_data)
        

    dict[year] = year_data

# %%

links_233 = {}
for k,v in dict.items():
    print(v)
    k = 2021
    v = dict.get(k)
    excel_r = requests.get(v, headers)
    data_soup = BeautifulSoup(excel_r.text, 'html5lib') # If this line causes an error, run 'pip install html5lib' or install html5lib

    

    find_233_40 = data_soup.find_all('li')


    for f in find_233_40:
        
        print('#####')
        print(f)
        print('\n')
        # if "Percentage of students suspended and expelled" in f:
        #     print('###')
        #     print(f)
        #     print('\n')
    # print('******')
    # print('\n')
    continue

    for ex in find_233_40:
        if "Percentage of students suspended and expelled" in str(ex):
            print(ex)
            partial_link_233 = str(ex).split('"')[1]
            link_233 = main_url + partial_link_233
            break
        else:
            continue
    
    try:
        links_233[k] = link_233
    except:
        print('i guess it wasnt found')



#  "Percentage of students suspended and expelled"
# %%

for k,v in excel_links.items():
    print(v)
    # %%
    

    


# %%
# Send a GET request to the website
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    print("Request successful")
    # Print a snippet of the response to verify content
    print(response.text)  # Print the first 1000 characters of the HTML content
else:
    print(f'Failed to retrieve the webpage. Status code: {response.status_code}')

