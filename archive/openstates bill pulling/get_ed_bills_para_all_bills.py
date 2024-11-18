
# %% 
import os, sys, json, datetime, re # Provides OS-dependent functionality, system-specific parameters, JSON handling, and date/time manipulation
import pandas as pd             # Provides data structures and data analysis tools
import numpy as np              # Supports large, multi-dimensional arrays and matrices
import ast
import requests
import urllib3
from tqdm import tqdm
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


from bs4 import BeautifulSoup
# %% NC abstract definition


def get_nc_abstract(df, session_param):
    

    base_url = "https://lrs.sog.unc.edu/billsum/"
    


    df['abstract'] = ""
    df['summary'] = ""
    df['url'] = ''
    for i,bill in enumerate(df['number']):

        bill_num = bill.replace(" ","-").replace("B", "").lower().strip()
        
        url = base_url + bill_num + "-" +session_param

        response = requests.get(url, verify = False)
        soup = BeautifulSoup(response.content, 'html.parser')
        abs = soup.find_all('blockquote')
        if len(abs) == 0:
            print("no summary for " + str(bill))
            print(url)
            continue
        elif len(abs) > 1:
            print('more than one summary for ' + str(bill))
            print(url)
            continue

            
        abstracts = []
        # print(len(sums))+ str(bill)
        for ab in abs:
            # print(sum)
            abstracts.append(ab)
        # print(type(abstracts))
        abstract = abstracts[0]
        abstract = str(abstract).replace('<blockquote>', '').replace('</blockquote>', '')
        df.loc[i,'abstract'] = str(abstract).lower()

        sums = soup.findAll('div', class_='field-item even')
        # print("###############SUMS##########")
        # print('LENGTH: ' + str(len(sums)))
        the_sum = []
        for sum in sums:
            if 'date-display-single' not in str(sum):
                the_sum.append(sum)
            # print('%%%%%%%%%%%%%%%%%%%%%%')
            # print(sum)
        summary = the_sum[0]

        # return df
        # continue
        # Get the text within the div, stripping out HTML tags
        sum_text = summary.get_text(separator="\n", strip=True)
        # print(type(sum_text))
        df.loc[i,"summary"] = str(sum_text)

        df.loc[i,'url'] = url
    return df
        # print(bill_num)
# %% Function to find context around the match
def find_context(text, pattern, num_words=10, only_after=False):
    matches = re.finditer(pattern, text)
    results = []
    
    for match in matches:
        start = match.start()
        end = match.end()
        
        # Get the context
        if only_after == False:
            context = text[max(0, start - num_words * 7): min(len(text), end + num_words * 7)]  # 7 chars per word approx
        else:
            context = text[0:min(len(text), end + num_words * 7)]
        results.append(context)
    
    return results


# %%% look in abstracts for more keywords

# ec_subs =  ["child care", 'preschool'
#             ]
# ec_pat = "|".join(ec_subs)
# print(type(ec_pat))

# ec_ed_bills = ec_ed_bills[ec_ed_bills.abstract.str.contains(ec_pat, regex = True, case=False)]
# ec_ed_bills.reset_index(inplace=True, drop=True)

# unique_ec_ed_bills = ec_ed_bills.drop_duplicates(subset='abstract')
# unique_ec_ed_bills.to_csv('ec_ed_bills_unique.csv', index=False)

# %%North Carolina

file = r"C:\Users\clutz\OneDrive - THE HUNT INSTITUTE\Documents\Data\NC\api results\nc_bills_10_16_24.csv"
all_bills_nc = pd.read_csv(file)

# %% early ed bills
ec_subs =  [
    "Child Care Comn",
    "Day Care",
    "Early Childhood Education",
    "Newborns & Infants",
    "Partnership For Children",
    "Social Services"
]
ec_pat = "|".join(ec_subs)
print(ec_pat)
ec_ed_bills = all

ec_ed_bills = all_bills_nc[all_bills_nc.subjects.str.contains(ec_pat, regex = True, case=False)]
ec_ed_bills.reset_index(inplace=True, drop=True)


# %%% get abstract from unc leg summaries
base_url = "https://lrs.sog.unc.edu/billsum/"
session_param = "-2023-2024"


ec_ed_bills['abstract'] = ""
for i,bill in enumerate(ec_ed_bills['number']):

    bill_num = bill.replace(" ","-").replace("B", "").lower().strip()
    
    url = base_url + bill_num + session_param

    response = requests.get(url, verify = False)
    soup = BeautifulSoup(response.content, 'html.parser')
    sums = soup.find_all('blockquote')
    if len(sums) == 0:
        print("no summary for " + str(bill))
        print(url)
        continue
    elif len(sums) > 1:
        print('more than one summary for ' + str(bill))
        print(url)
        continue
        
    abstracts = []
    # print(len(sums))+ str(bill)
    for sum in sums:
        # print(sum)
        abstracts.append(sum)
    # print(type(abstracts))
    abstract = abstracts[0]
    abstract = str(abstract).replace('<blockquote>', '').replace('</blockquote>', '')
    ec_ed_bills.loc[i,'abstract'] = str(abstract).lower()
    # print(bill_num)


# %%% look in abstracts for more keywords

ec_subs =  ["child care", 'preschool'
            ]
ec_pat = "|".join(ec_subs)
print(type(ec_pat))

ec_ed_bills = ec_ed_bills[ec_ed_bills.abstract.str.contains(ec_pat, regex = True, case=False)]
ec_ed_bills.reset_index(inplace=True, drop=True)

unique_ec_ed_bills = ec_ed_bills.drop_duplicates(subset='abstract')
unique_ec_ed_bills.to_csv('ec_ed_bills_unique.csv', index=False)

# %% Higher ed bills

he_subs =  [
    
    "Colleges & Universities",
    "Community College Boards",
    "Community Colleges",
    "Community Colleges Board",
    "Community Colleges Office",
    "Distance Education",
    "Education & Workforce Innovation Comn.",
    "Hbcu Infrastructure Study Comm.",
    "Scholarships & Financial Aid",
    "Secondary Education",
    "Student Athletes",
    "Students",
    "Tuition",
    "Unc/s",
    "Unc Board Of Governors",
    "Unc Boards Of Trustees"
]
he_pat = "|".join(he_subs)


# test_string = "ADMINISTRATIVE CODE| ADMINISTRATIVE RULES| COMMERCE| CONSUMER PROTECTION| CONTINUING CARE FACILITIES| CONTRACTS| CORPORATIONS| COUNCIL OF STATE| FEES| FOR-PROFIT| HEALTH SERVICES| INSURANCE| INSURANCE COMMISSIONER| INSURANCE DEPT.| LICENSES & PERMITS| NOTIFICATION| PUBLIC| PUBLIC OFFICIALS| REPORTING"
# print(re.findall(he_pat, test_string, cas))

he_ed_bills = all_bills_nc[all_bills_nc.subjects.str.contains(he_pat, regex = True, case=False)]
he_ed_bills.reset_index(inplace=True, drop=True)


# os.chdir(r'C:\Users\clutz\OneDrive - THE HUNT INSTITUTE\Documents\Data\NC\testing files')
# he_ed_bills.to_csv('he_all_bills_nc.csv', index=False)

# %% get abstracts 
# test_he_ed_bills = he_ed_bills.iloc[:10,:]
# test_nc_he_ed_bills = get_nc_abstract(test_he_ed_bills, "2023-2024")
# %%
nc_he_ed_bills = get_nc_abstract(he_ed_bills, "2023-2024")


# Get the contexts


# %%
 
keywords = [
"post-{0,1}/s{0,1}secondary",
"vocational",
"graduation",
"attainment",
'higher education institutions'
]

he_pattern = "|".join(keywords)
he_ed_bills = nc_he_ed_bills[nc_he_ed_bills.subjects.str.contains(he_pattern, regex = True, case=False)]

# %%

print(he_ed_bills.columns)
for abs in he_ed_bills['abstract']:
    print(str(abs))


review = he_ed_bills.loc[:,['number', 'title','abstract', 'summary', 'url']]
os.chdir(r'C:\Users\clutz\OneDrive - THE HUNT INSTITUTE\Documents\Data\NC\testing files')
review.to_excel('review_he_data.xlsx', index=False)
# %%
for i,bill in enumerate(nc_he_ed_bills['summary']):
    # if re.search(r'post-{0,1}\s{0,1}secondary', str(bill)):
    #     print(re.findall(r'post-{0,1}\s{0,1}secondary', str(bill)))

    # print(len(bill.split('\n')))
    if re.search(he_pattern, str(bill).lower()):
        
        
        print('#######################')
        print(nc_he_ed_bills['number'].iloc[i])
        print(nc_he_ed_bills['title'].iloc[i])
        print('$$$$$$')
        print(nc_he_ed_bills['subjects'].iloc[i])
        print('$$$$$$')
        print(nc_he_ed_bills['abstract'].iloc[i])
        context = find_context(bill, f"r'{he_pattern}'", num_words=10)
        print(context)
        # print(str(bill))
        print('\n')
# %%
    
keywords = [
"post-{0,1}\s{0,1}secondary",
"vocational",
"graduation",
"attainment",
'higher education institutions'
]


        
        


phrases = [
    "Post-secondary transition",
    "Equity gaps",
    "College-going rates",
    "Workforce readiness",
    "Certificate programs",
    "Wraparound services",
    "Stackable credentials",
    "Student persistence",
    "Retention strategies",
    "Lifelong learning",
    "Postsecondary barriers",
    "Alternative pathways",
    "Higher education institutions (IHEs)",
    "Legislative support for education",
    "Student success metrics",
    "High quality credential",
    "Vocational training",
    "Attainment",
    "Persistence",
    "Resistance",
    "Graduation"
]


























# %%





pattern = r'\b(?:Post-secondary transition|Equity gaps|College-going rates|Workforce readiness|Certificate programs|Wraparound services|Stackable credentials|Student persistence|Retention strategies|Lifelong learning|Postsecondary barriers|Alternative pathways|Higher education institutions \(IHEs\)|Legislative support for education|Student success metrics|High quality credential|Vocational training|Attainment|Persistence|Resistance|Graduation)\b'



nc_he_ed_bills = nc_he_ed_bills[nc_he_ed_bills.abstract.str.contains(pattern, regex = True, case=False)]
nc_he_ed_bills.reset_index(inplace=True, drop=True)

unique_nc_he_ed_bills = ec_ed_bills.drop_duplicates(subset='abstract')
unique_nc_he_ed_bills.to_csv('ec_ed_bills_unique.csv', index=False)















# %% North Dakota

# %%

file = r"C:\Users\clutz\OneDrive - THE HUNT INSTITUTE\Documents\Data\ND\api results\nd_bills_10_18_24.csv"
all_bills_nd = pd.read_csv(file)

# %% early ed bills
ec_subs =  [
    "child care",
    "day care",
    "early childhood",
    "newborns",
    "infants",
    "preschool"
    ]
ec_pat = "|".join(ec_subs)
print(ec_pat)

#%%



ec_ed_bills_nd = all_bills_nd[all_bills_nd.title.str.contains(ec_pat, regex = True, case=False)]
ec_ed_bills_nd.reset_index(inplace=True, drop=True)


# %%

bill_nums = []
for i,title in enumerate(ec_ed_bills_nd['title']):

    
    intro_statement = title.split('relating', 1)[-1].split('.',1)[0]
    if re.search(ec_pat, str(intro_statement)):
        
        print('##########################')
        print(all_bills_nd['number'].iloc[i])
        print('\n')
        bill_nums.append(all_bills_nd['number'].iloc[i])
        ec_ed_bills_nd.loc[i,'title'] = str(intro_statement)

    elif re.search(ec_pat, str(title)):
        print("not in intro")
        # not_in_keywords.append(intro_statement)
# %%
'''
Take data ec_ed_bills df's and combine them 
'''


# for j in not_in_keywords:
#     print(j)


# %%

ec_subs =  ["child care", 'preschool'
            ]
ec_pat = "|".join(ec_subs)
print(type(ec_pat))

ec_ed_bills_nd = all_bills_nd[all_bills_nd.title.str.contains(ec_pat, regex = True, case=False)]




# %%

os.chdir(r'C:\Users\clutz\OneDrive - THE HUNT INSTITUTE\Documents\Data\content team data\early childhood')
ec_ed_bills.to_csv('ec_ed_bills.csv', index=False)




for i,j in enumerate(ec_ed_bills['subjects']):
    print(ec_ed_bills['title'].iloc[i])
    print('#####################')
    for x in str(j).split(','):
        print(x)
    print('\n')



#'.*[Ee]ducation.*|.*[Cc]hild.*|.*[Ss]chool.*|.*[Cc]harter.*|.*[Mm]ath.*|.*[Rr]ead.*|.*[Tt]each.*|.*[Pp]arent.*|.*[Kk]id.*|.*[Ss]tudent.*|.*[Cc]ollege.*|.*[Uu]niversit.*|.*[Tt]uition.*'
# %% ED

ed_bills = all_bills_nc[all_bills_nc.Title.str.contains('.*[Ee]ducation.*|.*[Cc]hild.*|.*[Ss]chool.*|.*[Cc]harter.*|.*[Mm]ath.*|.*[Rr]ead.*|.*[Tt]each.*|.*[Pp]arent.*|.*[Kk]id.*|.*[Ss]tudent.*|.*[Cc]ollege.*|.*[Uu]niversit.*|.*[Tt]uition.*', regex = True)]


list = ['Eeducation','Cchild','Sschool','Ccharter','Mmath','Rread','Tteach','Pparent','Kkid','Sstudent','Ccollege','Uuniversit','Ttuition']
print(list)

[print(l) for l in list]
# %% Subjects from plural

file = r"C:\Users\clutz\OneDrive - THE HUNT INSTITUTE\Documents\Data\NC_bills_2023_from_plural_bulk.csv"
nc_bills = pd.read_csv(file)
# %%% compiling all subjects
put_here = []
for i,j in enumerate(nc_bills['subject']):
    # print(type(j))
    v = ast.literal_eval(j)
    put_here.append(v)
result = []
[result.extend(el) for el in put_here] 

print(result)

subjects = pd.DataFrame({'subject': result}).sort_values(by=['subject']).drop_duplicates()
subjects.reset_index(drop = True, inplace = True)

subjects['subject'] = subjects.subject.str.title()
subjects['subject'] = subjects.subject.str.strip()


# %% taking out counties
counties_file = r"C:\Users\clutz\OneDrive - THE HUNT INSTITUTE\Documents\Data\ref data\counties_nc.csv"
counties = pd.read_csv(counties_file)
counties['suffix'] = ['County'] * len(counties)
# counties = counties['County'].to_list()

counties = counties['County'] + " " + counties['suffix']
print(counties)

# %% take out counties
subjects['in_list'] = subjects['subject'].isin(counties)
# subjects = subjects[~subjects['subject'] == True]
subjects_filtered = subjects[~subjects['subject'].eq(True)]
subjects = subjects_filtered['subject']

#export
os.chdir(r'C:\Users\clutz\OneDrive - THE HUNT INSTITUTE\Documents\Data\ref data')
subjects.to_csv('subjects.csv')


# %%


ed_subjs = subjects[subjects.str.contains('.*[Hh][Bb][Cc][Uu].*|.*[Ee]ducation.*|.*[Cc]hild.*|.*[Ss]chool.*|.*[Cc]harter.*|.*[Mm]ath.*|.*[Rr]ead.*|.*[Tt]each.*|.*[Pp]arent.*|.*[Kk]id.*|.*[Ss]tudent.*|.*[Cc]ollege.*|.*[Uu]niversit.*|.*[Tt]uition.*', regex = True)]



# %%

for name, values in subjects.items():
    v = values
    print(v)

    put_here.append(v)

all_subjects = pd.concat(put_here)




pattern = '|'.join(['"', "'"])

all_subjects = all_subjects.str.replace(pattern, 'CORP', regex=True)

all_subjects_minus_dupes = all_subjects.drop_duplicates().sort_values()
# %%
