import os
from os.path import isfile, join
from datetime import datetime

#def main(date, specifierID, infoString):
#Does user want to use this script?

def filenamer():

    f = open('fileioConfig.txt','r')
    config = f.read().split('\n')
    print('\n')
    print('parentDir = ', config[0])
    print('date = ', config[1])
    print('NEW_CYLS = ', (config[2]))
    print('SAVE_PARTS = ', (config[3]))
    print('SAVE_OUTPUT = ', (config[4]))
    print('PARTS_FOLDER_NAME = ', config[5])
    print('OUTPUT_FOLDER = ', config[6])
    print('\n')
    f.close()
    dontUseMain = input("Do you want to use this config file (in case the program crashed and nothing was written)? (y/n) ")
    if dontUseMain == 'y':
        return
    elif dontUseMain == 'n':
        print('You will be prompted for i.o.')
    else:
        print('Invalid input')
        quit()
        #return False

    #need some initial info

    os.chdir('../')
    parentDir = os.getcwd() + '/'
    os.chdir('induced_field_model')
    inputDate = datetime.today().strftime('%m-%d')
    #Shape file i/o. Asks if user wants to make new shapes, and where they want to save them
    #If they do, Checks to make sure new shapes don't overwrite old
    #If they don't, asks user which shape-file-folder they want to use. Checks to
    #make sure thre fodler exists
    newShapes = input("Do you want to make new shapes? (y/n): ")
    if newShapes == 'y':
        NEW_PARTS = True
        saveShapes = input("Do you want to save these shapes? (y/n): ")
        if saveShapes == 'y':
            SAVE_PARTS = True

            exitLoop = False
            while exitLoop == False:
                sameName = False
                print("Enter the name of the folder you want to save your shape files to.")
                print("e.g. cyls_10_setups_5e8_density_equal_and_opp_sus")
                infoString = input("Folder name: ")
                qualifier = input("Do you want to add a qualifier to the folder name like 'TEST'? (y/n): ")
                if qualifier == 'y':
                    inputSpecifier = input("Enter qualifier: ")
                elif qualifier == 'n':
                    inputSpecifier = ""
                else:
                    print('invalid input')
                    quit()


                partsFolderName = str(inputDate + '_' + inputSpecifier + infoString + '/')
                mypath = str(parentDir + 'parts/')
                for folder in os.listdir(mypath):
                    if partsFolderName == folder:
                        print(folder, ' already exists.')
                        overwrite = input('Do you want to overwrite? (y/n): ')
                        if overwrite == 'y':
                            sameName = False
                        else:
                            print('Enter new folder name or qualifier')
                            sameName = True

                if sameName == True:
                    exitLoop = False
                else:
                    exitLoop = True
            FULL_PARTS_FOLDER_NAME = str(parentDir + 'parts/' + inputDate + '_' + inputSpecifier + infoString + '/')
            print('Saving shapes to ', FULL_PARTS_FOLDER_NAME)
        elif saveShapes == 'n': #not saving shapes
            SAVE_PARTS = False
            inputSpecifier = ''
            infoString = 'unspecified'
        else:
            print('invalid input')
            quit()

        FULL_PARTS_FOLDER_NAME = str(parentDir + 'parts/' + inputDate + '_' + inputSpecifier + infoString + '/')


    elif newShapes == 'n':
        NEW_PARTS = False
        SAVE_PARTS = False
        mypath = str(parentDir + 'parts/')
        exists = False
        while exists == False:
            folderDict = {}
            for i,folder in enumerate(os.listdir(mypath)):
                folderDict[i] = folder
            for key, value in folderDict.items():
                print(f"{key} : {value}")
            partsFolderNum = input("Enter the folder number (options listed above): ")
            partsFolderName = folderDict[int(partsFolderNum)]
            for folder in os.listdir(mypath):
                if partsFolderName == folder:
                    exists = True
            if exists == False:
                print('specified folder does not exist. Try Entering again.')



        FULL_PARTS_FOLDER_NAME =  str(parentDir + 'parts/' + partsFolderName + '/')
        print('Using parts from ', FULL_PARTS_FOLDER_NAME)
        infoString = partsFolderName[6:]

    else:
        print('invalid input')
        quit()

    output = input("Do you want to save the output of the program? (y/n): ")
    if output == 'y':
        SAVE_OUTPUT = True
        exitLoop = False
        while exitLoop == False:
            sameName = False
            if infoString == 'unspecified':
                infoString = input('A foldername has not been specified yet. Please enter one: ')
            qualifier = input("Do you want to add a qualifier to the folder name like 'TEST'? (y/n): ")
            if qualifier == 'y':
                inputSpecifier = input("Enter qualifier: ")
            else:
                 inputSpecifier = ""

            outputFolder = str(inputSpecifier + infoString + '/')
            mypath = str(parentDir + 'output_files/' + inputDate + '/')
            if os.path.isdir(mypath):
                for folder in os.listdir(mypath):
                    if outputFolder == folder:
                        print(folder, ' already exists.')
                        overwrite = input('Do you want to overwrite? (y/n): ')
                        if overwrite == 'y':
                            sameName = False
                        else:
                            print('Enter new qualifier')
                            sameName = True

            if sameName == True:
                exitLoop = False
            else:
                exitLoop = True

        FULL_OUTPUT_FOLDER = str(parentDir + 'output_files/' + inputDate + '/' + inputSpecifier + infoString + '/')
        print('Writing results to ', FULL_OUTPUT_FOLDER)

    elif output == 'n':
        SAVE_OUTPUT = False
        FULL_OUTPUT_FOLDER = str(parentDir + 'output_files/' + inputDate + '/' + 'nothing' + '/')

    else:
        print('invalid input')
        quit()

    with open('fileioConfig.txt', 'w') as file:
        file.write(str(parentDir))
        file.write('\n')
        file.write(str(inputDate))
        file.write('\n')
        file.write(str(NEW_PARTS))
        file.write('\n')
        file.write(str(SAVE_PARTS))
        file.write('\n')
        file.write(str(SAVE_OUTPUT))
        file.write('\n')
        file.write(str(FULL_PARTS_FOLDER_NAME))
        file.write('\n')
        file.write(str(FULL_OUTPUT_FOLDER))
    file.close()
#
    # print('i.o. parameters:')
    # print('parentDir: ', str(parentDir))
    # print('new parts: ', str(NEW_PARTS))
    # print('save parts: ', str(SAVE_PARTS))
    # print('save output: ', str(SAVE_OUTPUT))
    # print('parts folder: ', str(FULL_PARTS_FOLDER_NAME))
    # print('output folder: ', str(FULL_OUTPUT_FOLDER))
    return
#fileMain()
