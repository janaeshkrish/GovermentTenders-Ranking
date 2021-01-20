import requests
import pandas as pd 
#import numpy as np
import string
import time


def table():
    
    #To display entire column in dataframe
    #pd.set_option("display.max_rows", None, "display.max_columns", None)

    #getting data from API tenndors24x7
    url = 'http://tenders_api.tender-247.com/tender/getTenderDetails'

    payload={'EmailID/UserName': 'tenders@mazenettech.com',
    'Password': 'GM6Js3NrBo'}

    headers = {
    'Authorization': 'Bearer  eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJ0ZW5kZXJzQG1hemVuZXR0ZWNoLmNvbSIsImV4cCI6MTYzOTY0ODQzMiwiaWF0IjoxNjA4MTEyNDMyfQ.XHg6-ZkXCfZi0sLoe2eJu3mbab6LZtgB8TuFfIfuQTo_jTdecDcu8TVitOF0E05ki-2dZpXZIOduGj_QZ1UB5w'
    }




    response = requests.request("GET", url, headers=headers, data = payload)

    #json data 
    data = response.json()

    #converting json format to pandas dataframe
    data_frame = pd.DataFrame(data['Data'])

    # Reading data from the text file
    with open('keywords.txt','r') as f:
        
        #Splitting the data at next line
        words = f.read().split('\n')
        #Lower casing 
        words = [x.lower() for x in words]
        
    # Cleaning the string for comparision
    def clean_string(text):
        
        
        #Removeing punctuation marks
        text = ''.join([word for word in text if word not in string.punctuation])
        #Lower casing the words
        text = text.lower()
        
        
        return text

    #Getting the count for the keywords
    count = []
    for i in data_frame.index:
        
        #Retriving row wise data from dataframe
        entry = data_frame.loc[i]

        #Getting the description from single row
        test_str = entry['RequirementWorkBrief']

        #Removing punctuations and lower caseing the descriptions
        clean_string(test_str)

        # Get matching substrings in string 
        res = [sub for sub in words if sub in test_str]
        
        count.append(len(res))
        
    #Creating a new column count
    data_frame['count'] = count

    #south zone with keywords matched(1)
    matched_id = []

    #entire state matched keywords (2)
    entire_state_matched_id = []

    #other states with unmatched keywords(4)
    unmatched_keywords_id = []

    #multilocation tendors (3)
    multi_id = []


    for i in data_frame.index:
        
        #Retriving row wise data from dataframe
        entry = data_frame.loc[i]

        #Getting the description from single row
        test_str = entry['RequirementWorkBrief']

        #Removing punctuations and lower caseing the descriptions
        clean_string(test_str)

        # Get matching substrings in string 
        res = [sub for sub in words if sub in test_str]
        
        
        #getting state location
        state = entry['Sitelocation']
        state = state.replace(" ", "")
        state = state.lower()
        state = state.split(',')
        
        #Matching with KEYWORDS
        if (len(state) >= 3):
            
            state = state[1]
            
            
            if (len(res) >= 1):
                
                if state in ['karnataka', 'tamilnadu', 'kerala' , 'telangana' , 'andhrapradesh']:
                    
                    #matched keywords in south zone
                    matched_id.append(entry['TenderID'])
                
                else:
                
                    # entire state with unmatched keywords
                    entire_state_matched_id.append(entry['TenderID'])
                    
            else:
                
                #unmatched keywords 
                unmatched_keywords_id.append(entry['TenderID'])
                
                    
        else:
                
                #multilocation
                #print(state)
                
                multi_id.append(entry['TenderID'])


    #1
    #matched with keywords
    matched = data_frame[data_frame['TenderID'].isin(matched_id)]
    # Sort the rows of dataframe by 'count' column 
    matched = matched.sort_values(by = 'count', ascending = 0)
    #matched keywords in south side
    matched['Score'] = matched['count'] + 300

    #2
    #entire state matched keywords (2)
    entire_state = data_frame[data_frame['TenderID'].isin(entire_state_matched_id)]
    # Sort the rows of dataframe by 'Name' column 
    entire_state = entire_state.sort_values(by = 'count', ascending = 0)
    #others state matched keywords
    entire_state['Score'] = entire_state['count'] + 200

    #3
    #multilocation tendors (3)

    multi_location = data_frame[data_frame['TenderID'].isin(multi_id)]
    multi_location = multi_location.sort_values(by = 'count', ascending = 0)
    multi_location['Score'] = multi_location['count'] + 100

    #4 
    #other states with unmatched keywords(4)
    other_states_unmatched = data_frame[data_frame['TenderID'].isin(unmatched_keywords_id)]
    other_states_unmatched = other_states_unmatched.sort_values(by = 'count', ascending = 0)
    other_states_unmatched['Score'] = other_states_unmatched['count'] + 100

    table = pd.concat([matched,entire_state,multi_location,other_states_unmatched],ignore_index = True)

    return table

#FINAL = table[['TenderID','Score']]


#data to json file 
#FINAL.to_json('final.json',orient='records')
            

