from numpy import dot, subtract, add, divide, multiply
from math import sin, cos, sqrt, pi, ceil
#from observationGrid import observationGrid
from observationPoint import observationPoint
from dipoleClass import dipoleClass
from constants import *
from shape_constants_file_io import *

def b_induced_single_point(arg):
    pointAndFieldVec, *inputList = arg

    # r_vec is observation location
    r_vec = pointAndFieldVec.getLocation()
    B_induced = pointAndFieldVec.getBfield()

    #check if observation point is inside of the material. If so, skip it
    inside = False
    obsPoint = pointAndFieldVec

    if TREAT_AS_WHOLE == True:
        if len(inputList) == 1:
            for wholeShape in inputList:
                objects = [wholeShape]
                if obsPoint.checkIfInsideWhole(wholeShape):
                    inside = True
            if inside:
                return [0, 0, 0]


        else:
            objects = inputList.shapeList
            for obj in objects:
                if obsPoint.checkIfInsideWhole(obj):
                    inside = True
            if inside:
                return [0, 0, 0]

    else:
        objects = inputList
        for obj in objects:
            if obsPoint.checkIfInside(obj):
                inside = True
        if inside:
            return [0, 0, 0]


    for obj in objects:
        #v = 1/obj.actualDensity
        #print(len(obj))
        division_100 = ceil(len(obj.dipoles)/100)
        keeper = division_100
        counter = 1
        for j in range(len(obj.dipoles)):
            #if  j == 1:
                # print("location: ", obj[j].loc)
                # print("susceptibility: ", obj[j].s)
                # print("B felt: ", obj[j].b)
            # Define dipole position vector
            ro_vec = [obj.dipoles[j].loc]

            # Define magnetic field at dipole
            mag_b = sqrt(obj.dipoles[j].b[0]**2 + obj.dipoles[j].b[1]**2 + obj.dipoles[j].b[2]**2)
            b_hat = [obj.dipoles[j].b[0]/mag_b, obj.dipoles[j].b[1]/mag_b, obj.dipoles[j].b[2]/mag_b]

            # Define vector from  dipole to observation location
            r_to_ro = subtract(r_vec, ro_vec)
            mag_r_to_ro = sqrt((r_vec[0] - obj.dipoles[j].loc[0]) ** 2 + (r_vec[1] - obj.dipoles[j].loc[1]) ** 2 + (r_vec[2] - obj.dipoles[j].loc[2]) ** 2)
            r_to_ro_hat = divide(r_to_ro, mag_r_to_ro)

            #calculate B field from dipole
            scalar_part = ((mag_b*obj.dipoles[j].v/(4*pi)) * (obj.dipoles[j].s))/((mag_r_to_ro**3)) #(1+obj.dipoles[j].s)
            vector_part = subtract((3*dot(r_to_ro_hat,b_hat)*r_to_ro_hat),b_hat)
            B_dipole = multiply(vector_part, scalar_part) #field at obs. point from a single given dipole

            #adding contributions
            B_induced = add(B_induced, B_dipole) #iterative sum from all dipoles
            #B_induced = B_induced.tolist()
            #B_induced = B_induced.ravel()

            if j == keeper:
                counter += 1
                keeper += division_100

    B_induced = B_induced.ravel()
    #print(B_induced)
    return(B_induced)


    #print((grid.pointAndFieldVecs[i].location))
    #print((grid.pointAndFieldVecs[i].bField))
