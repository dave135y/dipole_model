import os
from shape_constants_file_io import *

def scan_for_file(filename):

    exit = False
    if os.path.isdir(PARTS_FOLDER_NAME) == False:
        os.makedirs(PARTS_FOLDER_NAME)

    for entry in os.scandir(PARTS_FOLDER_NAME):
        #print('############ ', entry, ' ##############')
        if entry.path == filename:
            #print('############ ', entry, ' ##############')
            exit = True

        if exit == True:
            continue

    return(exit)
