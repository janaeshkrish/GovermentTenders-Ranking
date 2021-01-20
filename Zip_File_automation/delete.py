import os

import shutil


def delete_dir():
    
    directory = os.getcwd()

    for filename in os.listdir(directory):

        path = os.path.join(directory, filename)


        if filename.endswith('.ZIP') or filename.endswith('.zip') or filename.endswith('.html') or filename.endswith('.pdf') or filename.endswith('.jpg') or filename.endswith('.gif') or filename.endswith('.png'):

            os.remove(path)