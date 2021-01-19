from ftplib import FTP
from datetime import datetime
import os
from zipfile import ZipFile
import shutil

#To get file from the server
ftp_get = FTP('216.10.240.149')

ftp_get.login(user='tender247', passwd = 'Tender247@123$%')

#printing list of files in the FTP
#list_of_dir = ftp_get.dir()

#To send the file to FTP server
#ftp_send = FTP('216.10.240.149')

#ftp_send.login(user='meena', passwd = 'Meena@123$%')


#printing list of files in the FTP
#list_s = ftp_send.dir()

#date month year
#01122020.zip
#%d%m%Y
date = datetime.now()

#date = date+timedelta(10)

today = date.strftime('%d%m%Y')

day = date.day

year = date.year

month = date.month


#To grab file from FTp server and store it in current directory
def grabfile():
    
    filename = '{0}.zip'.format(today)
    
    localfile = open(filename, 'wb')
    
    ftp_get.retrbinary('RETR ' + filename, localfile.write, 1024)

    ftp_get.quit()
    
    localfile.close()


#Zip file extraction 
def extraction():
    
    # Extracting the path for zip files and pdf files
    directory = os.getcwd()
    
    for filename in os.listdir(directory):
        
        if filename.endswith('.zip'):
            
            #print(os.path.join(directory, filename))

            path = os.path.join(directory, filename)
            
            #print(path)
            
            with ZipFile(path,'r') as zipObj:
                
                
                
                # Extract all the contents of zip file in current directory
                zipObj.extractall()
                  
                
        else:

            continue
            
            
    #Remove file from dir
    #os.remove(path)

def delete():

    directory = os.getcwd()

    for filename in os.listdir(directory):

        path = os.path.join(directory, filename)


        if filename == str(year):

            #print(path)
            shutil.rmtree(path)

        if filename.endswith('.ZIP') or filename.endswith('.zip'):

            os.remove(path)


path = "{}\{}\{}".format(year,month,day)

dirs = os.getcwd()

full_path = dirs+ "\\"+path



if __name__ =="__main__":

    #grabfile()

    extraction()

    #To send the file to FTP server
    ftp_send = FTP('216.10.240.149')

    ftp_send.login(user='meena', passwd = 'Meena@123$%')

    #r'C:\Users\USER\Desktop\zipautomation\2020\12\17'
    for root, dirs, files in os.walk(full_path):
        
        for fname in files:
            
            full_fname = os.path.join(root, fname)
            
            ftp_send.storbinary('STOR ' + fname, open(full_fname, 'rb'))
            
            print(full_fname)

    print('Process Completed.....')

    delete()

    print('deleted Zip file and Folders Sucessfully')

