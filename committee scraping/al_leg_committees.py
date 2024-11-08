# %%
import os, sys, json, datetime, re  # Provides OS-dependent functionality, system-specific parameters, JSON handling, and date/time manipulation
import pandas as pd             # Provides data structures and data analysis tools
import numpy as np              # Supports large, multi-dimensional arrays and matrices
import requests
import time
from tqdm import tqdm

from bs4 import BeautifulSoup

# %%

url = 'https://alison.legislature.state.al.us/committees-senate-standing-current-year'

response = requests.get(url, verify = False).content
df_list = pd.read_html(response)
print(type(df_list[0]))
df = df_list[0]


# %% For AL
'''
This will require committee names 
to match what is on the website.
***double check that this is the case****

'''
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

# %%% senate

dfs = {}
try:
    # Open the target URL
    driver.get('https://alison.legislature.state.al.us/committees-senate-standing-current-year')

    # Wait for the page to load and the tbody to be present
    wait = WebDriverWait(driver, 20)

    # Use a broader selector or additional waits to ensure the page is fully loaded
    tbody = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "tbody")))

    # Debug: Print the HTML of the tbody to verify its presence
    # print(tbody.get_attribute('outerHTML'))

    # Find all rows within the tbody
    rows = wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "tbody tr")))
    #list of committee names (replace with logic to pull from csv and filter by appropriate state)
    coms = ['Education Policy','Finance and Taxation Education','Finance and Taxation General Fund','Children and Youth Health','Healthcare']


    # go through each committee and check if relevant and save table to dict
    for row in rows:
        time.sleep(2)  # Adjust sleep time if necessary to allow the table to load
        ActionChains(driver).move_to_element(row).click().perform()
        time.sleep(2)  # Adjust sleep time if necessary to allow the table to load
        html_from_page = driver.page_source
        soup = BeautifulSoup(html_from_page, 'html.parser')
        modal_div = soup.find_all("div", class_= "ReactModalPortal")
        for m in modal_div:
            # print(m)
            if len(str(m)) > 36:
                div = m
                break

        # print(div)
        header = div.find("h1")
        header = str(header).split('">', 1)[-1].split('</h1', 1)[0].replace('Members','').strip()

        pass_through = False
        for h in coms:
            if str(header) in h:
                pass_through = True
            else:
                continue
        #close if not a relevant committee
        if pass_through != True:
            print(str(header) + ' is not a valid committee')
            close_button_pot = driver.find_element(By.XPATH, "/html/body/div[6]/div/div/div/div[1]/button")
            # time.sleep(5)  # Adjust sleep time if necessary to allow the table to load
            ActionChains(driver).move_to_element(close_button_pot).click().perform()
            # time.sleep(5)  # Adjust sleep time if necessary to allow the table to load

            continue
        
        #fetch table
        df_list = pd.read_html(html_from_page)
        df = df_list[-1]

        
       
        #close popup
        close_button_pot = driver.find_element(By.XPATH, "/html/body/div[6]/div/div/div/div[1]/button")
        ActionChains(driver).move_to_element(close_button_pot).click().perform()
        
        # save table
        dfs[header] = df

finally:
    # Close the WebDriver
    driver.quit()

# %%% house


dfs = {}
try:
    # Open the target URL
    driver.get('https://alison.legislature.state.al.us/committees-house-standing-current')

    # Wait for the page to load and the tbody to be present
    wait = WebDriverWait(driver, 20)

    # Use a broader selector or additional waits to ensure the page is fully loaded
    tbody = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "tbody")))

    # Debug: Print the HTML of the tbody to verify its presence
    # print(tbody.get_attribute('outerHTML'))

    
    coms = ["Education Policy","Ways and Means General Fund","Ways and Means Education","Health","Children and Senior Advocacy"]
    
    
    
    
    # Find all rows within the tbody
    rows = wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "tbody tr")))
    #list of committee names (replace with logic to pull from csv and filter by appropriate state)

    # go through each committee and check if relevant and save table to dict
    for row in rows:
        time.sleep(2)  # Adjust sleep time if necessary to allow the table to load
        ActionChains(driver).move_to_element(row).click().perform()
        time.sleep(2)  # Adjust sleep time if necessary to allow the table to load
        html_from_page = driver.page_source
        soup = BeautifulSoup(html_from_page, 'html.parser')
        modal_div = soup.find_all("div", class_= "ReactModalPortal")
        for m in modal_div:
            # print(m)
            if len(str(m)) > 36:
                div = m
                break

        # print(div)
        header = div.find("h1")
        header = str(header).split('">', 1)[-1].split('</h1', 1)[0].replace('Members','').strip()

        pass_through = False
        for h in coms:
            if str(header) in h:
                pass_through = True
            else:
                continue
        #close if not a relevant committee
        if pass_through != True:
            print(str(header) + ' is not a valid committee')
            close_button_pot = driver.find_element(By.XPATH, "/html/body/div[6]/div/div/div/div[1]/button")
            # time.sleep(5)  # Adjust sleep time if necessary to allow the table to load
            ActionChains(driver).move_to_element(close_button_pot).click().perform()
            # time.sleep(5)  # Adjust sleep time if necessary to allow the table to load

            continue
        
        #fetch table
        df_list = pd.read_html(html_from_page)
        df = df_list[-1]

        
       
        #close popup
        close_button_pot = driver.find_element(By.XPATH, "/html/body/div[6]/div/div/div/div[1]/button")
        ActionChains(driver).move_to_element(close_button_pot).click().perform()
        
        # save table
        dfs[header] = df

finally:
    # Close the WebDriver
    driver.quit()
# %%
for k,v in dfs.items():
    print(k)
    print(v)

# %%

headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"}
r = requests.get(url, headers=headers)

# %%

