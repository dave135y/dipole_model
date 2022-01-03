from scan_for_file import scan_for_file
from dipoleCylinderClass import dipoleCylinderClass
from dipoleSphereClass import dipoleSphereClass
from dipoleRecPrismClass import dipoleRecPrismClass
from shape_constants_file_io import *
import pickle


def loading_cylinder_components(file, inner, outer, height, density, rPrecision, thetaPrecision, hPrecision, fillType, color, new):

    if SAVE_PARTS == True or NEW_CYLS == False:
        isFile = scan_for_file(file)
        if isFile == True:
            with open(file, "rb") as fp:   # Unpickli
                object = pickle.load(fp)

        #the case where I don't want a new sphere, but we can't find the file
        if new == False and isFile == False:
            print('cannot find file: ', file)
            quit()

        if new == True:
            object = dipoleCylinderClass(inner, outer, height, density, rPrecision, thetaPrecision, hPrecision, fillType, color)
            object.fill()

            object.save(file)

    else:
        object = dipoleCylinderClass(inner, outer, height, density, rPrecision, thetaPrecision, hPrecision, fillType, color)
        object.fill()
    return object


def loading_sphere_components(file, new, inner, outer, density, color):

    isFile = scan_for_file(file)
    if isFile == True:
        with open(file, "rb") as fp:   # Unpickli
            object = pickle.load(fp)

    #the case where I don't want a new sphere, but we can't find the file
    if new == False and isFile == False:
        print('in loading_components - cannot find file: ', file)
        quit()

    if new == True:
        object = dipoleSphereClass(inner, outer, density, color)
        object.fill()
        object.save(file)

    return object
#
#
def loading_recPrism_components(file, new, length, width, height, density, color):
#
    isFile = scan_for_file(file)
    if isFile == True:
        with open(file, "rb") as fp:   # Unpickli
            object = pickle.load(fp)
#
    #the case where I don't want a new sphere, but we can't find the file
    if new == False and isFile == False:
        print('cannot find file: ', file)
        quit()
#
    if new == True:
        object = dipoleRecPrismClass(length, width, height, density, color)
        object.fill()
        object.save(file)

    return object
