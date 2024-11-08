
# %%
# Importing basic Python modules

import os, sys, json, datetime  # Provides OS-dependent functionality, system-specific parameters, JSON handling, and date/time manipulation
import pandas as pd             # Provides data structures and data analysis tools
import numpy as np              # Supports large, multi-dimensional arrays and matrices
import requests
import time
import glob
import re
from tqdm import tqdm
import shutil

# %%

os.chdir(r'C:\Users\clutz\OneDrive - THE HUNT INSTITUTE\Documents\Data\surveys\survey files to clean up\edited')
edited_files = glob.glob('*.xlsx')



all_surveys = {}
for file in tqdm(edited_files):

    
    # file = edited_files[0]
    df = pd.read_excel(file)
    print("##################")
    print(file)
    print(df.columns[0])
    print("\n")

    dfs = []
    for name, data in df.items():
        if str(name) == 'respondent' or str(name).lower().strip() == 'name':
            index_col = str(name)
            continue
        
        n = len(data)
        
        respondents = df[index_col].to_list()
        # print(respondents)
        quest = [str(name)]*n
        response = data.to_list()
        df_app = pd.DataFrame({'respondent':respondents, 'question': quest, 'response': response})
        dfs.append(df_app)
    survey_data = pd.concat(dfs)
    all_surveys[file] = survey_data


# %%

# List to hold modified DataFrames
modified_dfs = []

# Iterate through the dictionary
for file, df in all_surveys.items():
    df['event'] = str(file).split(".",1)[0].replace("_", " ").replace('eval', "").replace(r'results', '')  # Add new column with the filename
    modified_dfs.append(df)    # Append modified DataFrame to the list

# Concatenate all DataFrames into one
combined_df = pd.concat(modified_dfs, ignore_index=True)


# %%
# for j in survey_data['response']:
#     if 'nan' in str(j):
#         print(str(j))
#         print(len(str(j)))
# %%
# Labeling responses with multiple conditions
def classify_response(j):

    
    if isinstance(j, (int, float)):

        if isinstance(j, float) and str(j) == 'nan':
            return 'missing'         

        elif isinstance(j, (int, float)):
            print(j)
            return 'quantitative'

    elif re.search(r'^yes|^no', str(j).lower().strip()):
        return "bool"
    else:        
        return 'qualitative'

combined_df['data_type'] = combined_df['response'].apply(classify_response)




# %% making a dynamic look up

# replace missing values based on question
lookup = combined_df.loc[:,['question', 'data_type']]
lookup = lookup.drop_duplicates()
lookup = lookup[~lookup['data_type'].str.contains("missing", regex=False)]
mapping = lookup.set_index('question')['data_type'].to_dict()
combined_df['data_type'] =  combined_df['data_type'].replace('missing', np.nan)
combined_df['data_type'] = combined_df['data_type'].fillna(combined_df['question'].map(mapping))

#looking for Net Promoter Questions
combined_df.loc[combined_df['question'].str.contains('recommend ', regex=True), 'data_type'] = 'nps'



# %%

os.chdir(r'C:\Users\clutz\OneDrive - THE HUNT INSTITUTE\Documents\Data\tableau\survey view\data sources')
combined_df.to_csv('master_survey_sheet.csv')


# %%

survey_data_qual = combined_df[combined_df['data_type'] == 'qualitative']
survey_data_quant = combined_df[~(combined_df['data_type'] == 'qualitative')]
# %%
os.chdir(r'C:\Users\clutz\OneDrive - THE HUNT INSTITUTE\Documents\Data\tableau\survey view\data sources')
survey_data_qual.to_excel('survey_data_qual.xlsx', index=False)
survey_data_quant.to_excel('survey_data_quant.xlsx', index=False)





































# %%

survey_data['data_type'] = survey_data['response'].apply(
    lambda x: 'quantitative' if isinstance(x, (int, float)) and str(x) != 'nan' else 'qualitative'
)
# survey_data.loc[isinstance(survey_data['response'], (int, float)), 'data_type'] = 'quantitative'
# survey_data.loc[isinstance(survey_data['response'], str), 'data_type'] = 'qualitative'


# %%

survey_data['data_type'] = ''
for i,j in enumerate(survey_data['response']):
    # print(str(j))
    # if isinstance(j, float):
    #     try:
    #         survey_data.loc[i, "response"] = str(j).astype(int)
            
    
    #     except:
    #         print(survey_data.loc[i,:])
    #         print('not working')
    #         break


    survey_data.loc[isinstance(survey_data['response'], (int, float)), 'data_type'] = 'quantitative'
    survey_data.loc[isinstance(survey_data['response'], str), 'data_type'] = 'qualitative'
    # if isinstance(j,str):
    #     survey_data.loc[i, "data_type"] = 'qualitative'
    # elif isinstance(j, (int, float)):
    #     survey_data.loc[i, "data_type"] = 'quantative'
    # else:
    #     print(str(j) + " isn't either str or int")




# %%
os.chdir(r'C:\Users\clutz\OneDrive - THE HUNT INSTITUTE\Documents\Data\surveys\survey files to clean up')
survey_data.to_excel('survey_data_test.xlsx')


# %%

file = r"C:\Users\clutz\OneDrive - THE HUNT INSTITUTE\Documents\Data\surveys\survey data\survey_data_monday_export_9_16.xlsx"
survey_update = pd.read_excel(file)

file_paths_surveys = survey_update['file_path'].to_list()


zero_files = []
path_error = []
files_list = {}
for i,f in enumerate(file_paths_surveys):
    # path = survey_update['file_path'].iloc[1]
    # print(path)
    path = f
    
    # print('###############')
    # print(survey_update['event'].iloc[i])
    # print(path)
    try:
        os.chdir(path)
    except:
        print('no')
        path_error.append(path)
        continue

    files = glob.glob('*.xlsx')

   
    if len(files) == 0:
        zero_files.append(path)
    elif len(files) == 2:
        for option in files:
            if 'data' in str(option):
                files_list[path] = option
    else:
        files_list[path] = files[0]
    # data = pd.read_excel(file)

# %%

# Destination folder where you want to copy the files
destination_folder = r'C:\Users\clutz\OneDrive - THE HUNT INSTITUTE\Documents\Data\surveys\survey files to clean up'

# Create the destination folder if it doesn't exist
os.makedirs(destination_folder, exist_ok=True)

didnt_work = []
# Loop through each file path
for k,v in files_list.items():
    
    file_path = os.path.join(k,v)
    print(file_path)
    try:
        # Copy the file to the destination folder
        shutil.copy(file_path, destination_folder)
        print(f'Copied: {file_path} to {destination_folder}')
    except Exception as e:
        print(f'Error copying {file_path}: {e}')
        didnt_work.append(file_path)

# %%

file = r"C:\Users\clutz\OneDrive - THE HUNT INSTITUTE\Documents\Data\surveys\survey files to clean up\edited\HLR_2024_eval_results.xlsx"
df = pd.read_excel(file)
print(df.columns)

# %%



dfs = []
for col_name,col_data in df.items():
    
    res_list = []
    quest_list = []
    response_list = []

    if col_name == df.columns[0]:
        continue
    n = len(df[df.columns[0]])
    res_list.extend(df[df.columns[0]])
    quest_list.extend([str(col_name)]*n)
    response_list.extend(col_data.to_list())

    df_to_append = pd.DataFrame({"responder":res_list, "question": quest_list , "response": response_list})
    dfs.append(df_to_append)

all_dfs = pd.concat(dfs)




# %%

    print('################')
    print(k)
    print(v)
    print('\n')



# %%

for m in multiple_files:
    os.chdir(m)


# %%

# %%

from nameparser import HumanName

def is_name(value):
    try:
        name = HumanName(value)
        # If name parsing did not fail, it might be a name
        return True
    except:
        return False
# %%


multiple_files = []
dfs = []
for i,f in enumerate(survey_update['file_path']):
    # path = survey_update['file_path'].iloc[1]
    # print(path)
    path = f
    break_main_loop = False
    print('###############')
    print(survey_update['event'].iloc[i])
    print(path)
    try:
        os.chdir(path)
    except:
        print('no')
        continue

    files = glob.glob('*.xlsx')

    if len(files) != 1:
        # print(files)
        # for file in files:
        #     file_df = pd.read_excel(file)
        #     print(file_df)
        print("%%%%%")
        print("multiple files")
        print("%%%%%")
        print('\n')
        print('\n')
        print('\n')
        print('\n')
        print('\n')
        multiple_files.append(path)
        continue
    else:
        file = files[0]


    data = pd.read_excel(file)
    data_cl = data.dropna(how = 'all', axis = 1)
    

    ##THIS DOESNT WORK###
    # # Find columns where the substring is found in the column names
    # for name, col_values in data.cl.items():
    #     check_list = col_values.to_list()
    #     name_found = False
    #     for check in check_list:
    #         if is_name(str(check)):
    #             name_column = name
    #             name_found = True
    #             break
    #     if name_found == True:
    #         break
    


    #Looking for Committee member column to get respondents names as first column
    matching_columns = [col for col in data_cl.columns if re.search(r'^[Cc]ommittee [Mm]ember', col)]
    try:
        first_col = matching_columns[0]
    except:
        print("col match method #2")
        # try:
        summary_found = False
        for col_name, col_data in data_cl.items():
            print('***************************************')
            print(col_name)
            print(col_data)
            print('***************************************')

            print(summary_found)
            if summary_found == True:
                first_col = col_name
                print("first column:")
                print(col_name)
                print("______________________________________________________________________________")
                print(col_data)
                print("______________________________________________________________________________")
                break
            col_to_list = col_data.to_list()


            for col_val in col_to_list:
                # print(col_val)
                # if summary_found == True:
                #     name_col = col_name
                #     print("[" + str(name_col) + "]"+ " is what is being matched")
                #     print(col_data)
                #     break
                    
                
                if re.search(r'number of attendees|response rate', str(col_val).lower()):
                    # print(str(col_val))
                    summary_found = True
                    print('col value that matches: ' + str(col_val).lower())
                    # print(col_data)
                    break
            print(data_cl.columns[(len(data_cl.columns)-1)])

            if col == data_cl.columns[(len(data_cl.columns)-1)] and summary_found ==  False:
                print("no summary found")
                break_main_loop = True
    

        for ik, k in enumerate(data_cl[first_col]):
            if 'attendees' in str(k) or 'response rate' in str(k).lower():
                print('THIS ISNT RIGHT') 
                break_main_loop = True

    if break_main_loop == True:
        break

            # print("first column: " + str(start))
            # print(data_cl.loc[:,name_col])
        # except:
        #     print('no matching columns')
        #     # print(data.columns)
        #     # print(data.iloc[:,0])
        #     # print(data.iloc[:,1])
        #     # print(data_cl)
        #     break
    
    if first_col:
        print('CONTINUE')
        print(first_col)
    else:
        print('STOP')
        # break

    data_cl = data_cl.loc[:,first_col:]
    
    #     data_cl = data_cl.loc[:,first_col:]
    #     print("\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\")
    #     print('new data frame')
    #     print(data_cl)
    #     print("\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\")
    # except:
    #     print("\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\")
    #     print("something wrong, df below for reference")
    #     print(data_cl)
    #     print("\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\")
    #     break



    
    for ix,j in enumerate(data_cl[data_cl.columns[0]]):
        # print(j)
        if 'average' in str(j).lower():
            stop = ix-1
            break
    data_cl = data_cl.iloc[:stop,:]
    
    data_cl = data_cl[~data_cl.iloc[:,3].astype(str).str.contains("sessions", case = False, na = False)]


    # data_cl[data_cl.columns[1]] = data_cl[data_cl.columns[1]].astype(int)
    for col, data in data_cl.items():
        # print(col)
        # data  = data_cl["The Financial Reality of NC Community College Students"]
        data_int = data.dropna()
        # print(data)
        # data_int = data_int.astype(int)
        # pd.api.types.is_integer_dtype(data)
        try:
            # Try to convert to int, if successful update the DataFrame
            data_int = data_int.astype(int)
        except ValueError:
            # If conversion fails, convert to string
            data_int = data_int.astype(str)

        data_cl[col] = data_int



    #gathering data to for export file
    
    for col, data in data_cl.items():
        if col == data_cl.columns[0]:
            # print("this worked")
            # print(col)
            # print(data)
            continue
        # if str(col).strip() == "Committee Member":
        #     continue

        # print(data)
        if pd.api.types.is_integer_dtype(data_cl[col]):
            n = len(data)
            data_type = ['quantitative']*n
            event_name = [str(survey_update['event'].iloc[i])]*n
            respondents = data_cl.iloc[0,:].to_list()
            quest = [str(col)]*n
            response = data.to_list()
            
        else:
            n = len(data)
            data_type = ['qualitative']*n
            event_name = [str(survey_update['event'].iloc[i])]*n
            respondents = data_cl.iloc[:,0].to_list()
            quest = [str(col)]*n
            response = data.to_list()

        list_list = [data_type,event_name,respondents,quest,response]
        if all(len(v) == n for v in list_list):
            print('making df')
            df = pd.DataFrame({'event': event_name, 
            'data_type': data_type, 
            'responder_name': respondents,
            'question': quest,
            'response': response})

            dfs.append(df)
            
            # print('%%%%%%%')
            # print('issue with: ' + str(survey_update['event'].iloc[i]))
            # print(path)
            # print('%%%%%%%')
            # print("_______questions________")
            # print(quest)
            # print("_______respondents_______")
            # print(respondents)
            # break_main_loop = True
            # break
        else:
            print('lengths dont match')
            break

        
        
        # event_list.extend(event_name)
        # data_type_list.extend(data_type)
        # responder_list.extend(respondents)
        # question_list.extend(quest)
        # response_list.extend(response)

        # try:
        #     df = pd.DataFrame({'event': event_list, 
        #     'data_type': data_type_list, 
        #     'responder_name': response,
        #     'question': question_list,
        #     'response': response_list})
        # except:
        #     print("event_list" + ": " +str(len(event_list)))
        #     print("data_type_list" + ": " +str(len(data_type_list)))
        #     print("responder_list" + ": " +str(len(responder_list)))
        #     print("question_list" + ": " +str(len(question_list)))
        #     print("response_list" + ": " +str(len(response_list)))

        #     break

        

    if break_main_loop == True:
        break

all_survey_data = pd.concat(dfs)


            
   

        
# %%
    for i,j in enumerate(data_cl['Commitee Member']):
        list = [0,i]
    
    # data_cl.iloc[:,0].to_list()
    print(data_cl.dtypes)
    print(data_cl)
    print('\n')
# print("Columns with missing values:")
# print(data.isnull().sum())
# %%
for d in data.columns:
    print(d)

    
# %%%

   
    print('###################')
    print(survey_update['event'].iloc[i])
    print(path)
    print('\n')
    print('$$$$$')
    print(data.columns[2])
    print('$$$$$')
    print('\n')
# %%
    for d in data.columns:
        print(d)
    print('$$$$$')
    print('\n')

