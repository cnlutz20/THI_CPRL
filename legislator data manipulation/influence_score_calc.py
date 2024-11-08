# %%
# Importing basic Python modules

import os, sys, json, datetime, re  # Provides OS-dependent functionality, system-specific parameters, JSON handling, and date/time manipulation
import pandas as pd             # Provides data structures and data analysis tools
import numpy as np              # Supports large, multi-dimensional arrays and matrices
import requests
import time
from tqdm import tqdm

# %%

file = r"C:\Users\clutz\OneDrive - THE HUNT INSTITUTE\Documents\Data\legislator data\nc\master_w_coms.xlsx"
nc_senate = pd.read_excel(open(file, 'rb'), sheet_name='NC Senate')
print(nc_senate.columns)


nc_senate_w_inf_scores = calculate_influence_scores(nc_senate)

# %%
def find_majority_party(df):

    republicans = df[df.Party.str.contains('Republican')]
    democrats = df[df.Party.str.contains('Democrat')]

    # print(len(republicans))
    # print(len(democrats))

    if len(republicans) > len(democrats):
        majority_party = "Republican"
    else:
        majority_party = "Democrat"

    return majority_party

# %%

def calculate_influence_scores(df, coms_start_indx = 11, is_house=True):
    majority_party = find_majority_party(df)

    # score_list = []

    for i,j in enumerate(df['leader']):
        influence_score = 1 if is_house else 2
        tenure = df['tenure'].iloc[i]
        leadership = str(j)
        party = df['Party'].iloc[i]
        committees = df.iloc[i, coms_start_indx:].tolist()
        print(committees)

        leader_one_regex = re.compile(r'\[1\]')
        leader_two_regex = re.compile(r'\[2\]')
        vice_regex = re.compile(r'[Vv]ice')
        rank_member_regex = re.compile(r'[Mm]ember')
        chair_regex = re.compile(r'^(?!.*vice).*chair.*$', re.IGNORECASE)

        # Scoring logic
        if leader_one_regex.search(leadership) and majority_party == party:
            influence_score = 20
        elif leader_two_regex.search(leadership) and majority_party == party:
            influence_score = 15
        elif leader_one_regex.search(leadership) and majority_party != party:
            influence_score = 15
        elif any(chair_regex.search(com) for com in committees):
            influence_score = 15
        elif leadership != "No" and majority_party == party:
            influence_score = 10
        elif leader_two_regex.search(leadership) and majority_party != party:
            influence_score = 10
        elif any(vice_regex.search(com) for com in committees):
            influence_score = 10
        elif any(rank_member_regex.search(com) for com in committees):
            influence_score = 10
        elif "Member" in committees:
            influence_score = 5
        elif leadership != "No" and majority_party != party:
            influence_score = 5

        # Tenure bonus
        if tenure > 10:
            influence_score += 3
        elif tenure > 6:
            influence_score += 2
        elif tenure > 2:
            influence_score += 1

        # Ensure max value is 20
        influence_score = min(influence_score, 20)

        df.loc[i,'Influence Score'] = influence_score

    return df
        # score_list.append([influence_score])

    # # Write scores back to the spreadsheet
    # sheet.iloc[2:last_row, 7] = pd.DataFrame(score_list)
    # return sheet
# %%
