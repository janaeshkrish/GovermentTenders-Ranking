import os

import shutil


def delete_dir():
    
    directory = os.getcwd()


    list = os.listdir()

    #print(list)

    for filename in os.listdir(directory):

        path = os.path.join(directory, filename)


        if filename.endswith('.ZIP') or filename.endswith('.zip') or filename.endswith('.html') or filename.endswith('.pdf') or filename.endswith('.jpg') or filename.endswith('.gif') or filename.endswith('.png') or filename.endswith('.JPG') or filename.endswith('.htm') or filename.endswith('.xlsx') or filename.endswith('.docx') or filename.endswith('.doc') or filename.endswith('.PDF'):

            os.remove(path)