# %%
import os, re
import pandas as pd
import glob as glob
from tqdm import tqdm
from tabula.io import read_pdf


import pdfplumber

# %%
os.chdir(r'C:\Users\clutz\THE HUNT INSTITUTE\The Hunt Institute Team Site - Documents\Development (formerly Grants Management)\!Administrative\Christian\State Trends Data\nieer')
files = glob.glob("*")
# %%


# Open the PDF and extract tables from page 16
with pdfplumber.open(files[0]) as pdf:
    page = pdf.pages[15]  # Page 16 (0-indexed)
    im = page.to_image(resolution=150)
    im.show()
    tables = page.extract_tables({"horizontal_strategy": "text"})

    for table in tables:
        print(table)  # Print extracted tables row-by-row


# %%

tables = []
for i,file in enumerate(files):
    
    if i > 0:
        break
    file = files[0]
    print(file)
    with pdfplumber.open(file) as pdf:
        pages = pdf.pages
        for page in tqdm(pages):
            tables_found = page.find_tables() 
            if len(tables_found) == 0:
                continue
            else:
                table = page.extract_tables()
                tables.append(table)
                # print(tb.columns)

# %%

for table in tables:
    print(pd.DataFrame(table).to_string())
        # print(first_page.page_number)
        # print(first_page.find_tables())
        # print(first_page.chars[0])
# %%
