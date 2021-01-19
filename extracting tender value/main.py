from ftplib import FTP
from datetime import datetime
import os
from zipfile import ZipFile

import camelot

import pandas as pd


#To delete the file and folders in the current dir
from delete import delete_dir


#Returns updated table
from final import table


data = table()

#To get file from the server
ftp_get = FTP('216.10.240.149')

ftp_get.login(user='meena', passwd = 'Meena@123$%')


for id in data['TenderID'][0]:

    #print(id)

    # Getting the zip file from FTP server
    filename = '{0}.zip'.format(id)

    localfile = open(filename, 'wb')

    ftp_get.retrbinary('RETR ' + filename, localfile.write, 1024)

    ftp_get.quit()
        
    localfile.close()

    #Extracting to the current directory
    directory = os.getcwd()

    for filename in os.listdir(directory):
            
        if filename.endswith('.zip'):
                
            path = os.path.join(directory,filename)
                
            with ZipFile(path,'r') as zipobj:
                    
                zipobj.extractall()
                    
        else:
                
            continue


'''
values = []

dir = os.getcwd()

for filename in os.listdir(dir):

    #print(filename)

    path = os.path.join(dir,filename)

    print(path)

    if filename.endswith('.html'):

        datas = pd.read_html(path)

        first_table = datas[0]

        if (first_table[0]== 'Tender Value in â¹').any() == True:

            tender_value = first_table.loc[first_table[0] == 'Tender Value in â¹']

            v = tender_value[1].to_string(index=False)
            
            values.append(v)

        else:

            values.append(str(0.0))


    if filename.endswith('.pdf'):

        data = camelot.read_pdf(filename, pages = "1")

        #Getting first table 
        page1 = data[0].df
        
        #IRPS
        advertised_value = page1[page1[0].str.contains("Advertised Value")]

        #GEM
        emd = page1[page1[0].str.contains("Estimated Bid Value")]

        if(advertised_value[0] == 'Advertised Value').any() == True:

            value = advertised_value[1]

            v = value.to_string(index=False)

            values.append(v)

        if(emd[0] == 'Estimated Bid Value').any() == True:

            value = emd[1]

            v = value.to_string(index=False)

            values.append(v)

        if ((emd[0] == 'Estimated Bid Value').any() == False) & ((advertised_value[0] == 'Advertised Value').any() == False):

            values.append(str(0.0))
            
print(values)
'''

'''
if __name__ == '__main__':

    #delete_dir()

    #table()
'''
