import pandas as pd
import os
import numpy as np
from zipfile import ZipFile
import camelot
import requests
import string
import time
start = time.time()
import warnings
warnings.filterwarnings("ignore")
from delete import delete_dir
from pdfminer.high_level import extract_text
from ftplib import FTP


path_of_folders = r"C:\Users\USER\Desktop\pdfss\18012021\2021\1\18"
            
#Current working directory
root = os.getcwd()

eligiblity_conditions = []
tender_id_eligiblity = []

for name in os.listdir(path_of_folders):

    print(name)
                    
    path_zip = os.path.join(path_of_folders, name)
            
    print(path_zip)

    tender_id = name.split('.')
    tender_id = tender_id[0]
         
    with ZipFile(path_zip,'r') as zipobj:
                    
        #Extracting the contents to the current Directory
        zipobj.extractall(os.getcwd())
                    
        dir = os.getcwd()

        for filename in os.listdir(dir):

            #print(filename)

            path = os.path.join(dir,filename)
                            
            if filename.endswith('.pdf'):
                            
                try:
                            
                    #To get document required from seller in GEM documents
                            
                    data = camelot.read_pdf(filename)
                            
                    page1 = data[0].df
                            
                    document = page1[page1[0].str.contains('Document required from seller')]
                            
                    result = document.iloc[0,1]
                            
                    eligiblity_conditions.append(result)
                            
                    tender_id_eligiblity.append(tender_id)
                            
                except Exception as e:
                            
                    print(e)
                        
                try:
                            
                    #For GEM tenders
                    text = extract_text(filename)
                            
                    #Getting the terms and conditions For Gem tenders
                    texts = text.split('Special terms and conditions')
                            
                    result = texts[1]
                            
                    eligiblity_conditions.append(result)
                            
                    tender_id_eligiblity.append(tender_id)
                            
                except Exception as e:
                            
                    print(e)
                            
                try:
                            
                    #For IRPS Tenders       
                    texts = text.split('4. ELIGIBILITY CONDITIONS')
                            
                    content = texts[1].split('5. COMPLIANCE')
                            
                    result = content[0].split('Defination  of  Similar  Work')
                            
                    result = result[1].split('.')[0]
                            
                    eligiblity_conditions.append(result)

                    tender_id_eligiblity.append(tender_id)
                            
                except Exception as e:
                            
                    print("not done")
                        
    delete_dir()

Final_eligiblity_conditions = pd.DataFrame(list(zip(eligiblity_conditions,tender_id_eligiblity)),columns =['eligiblity_conditions', 'Tender_Id'])

Final_eligiblity_conditions.drop(Final_eligiblity_conditions[Final_eligiblity_conditions['eligiblity_conditions']=='Series([], )'].index,inplace = True)


def write_file():

    for i in Final_eligiblity_conditions.index:
    
        print(i)
        
        data = Final_eligiblity_conditions.loc[i]
        
        eligiblity_conditions = data['eligiblity_conditions']
        
        tender_id = data['Tender_Id']

        eligiblity_conditions=eligiblity_conditions.rstrip()
        
        name = r'C:\Users\USER\Desktop\text_datas\{}.txt'.format(tender_id)
        
        with open(name, "a") as text_file:
            
            text_file.write(str(eligiblity_conditions))


def send_file():

    #To send the file to FTP server
    ftp_send = FTP('216.10.240.149')

    ftp_send.login(user='meena', passwd = 'Meena@123$%')
    
    #Path to save text files 
    path = r'C:\Users\USER\Desktop\text_datas'

    for name in os.listdir(path):
         
        full_fname = os.path.join(path, name)

        serverdirectorypath='/ec/'

        ftp_send.cwd(serverdirectorypath)
            
        ftp_send.storbinary('STOR ' + name, open(full_fname, 'rb'))
            
        print(full_fname)