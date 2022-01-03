import multiprocessing as mp
from functools import partial
from itertools import repeat
import tqdm
#import istarmap
#from observationPoint import *
#from b_induced_single_point import *

from numpy import dot, subtract, add, divide, multiply
from math import sin, cos, sqrt, pi, ceil
from observationGrid import observationGrid
from observationPoint import observationPoint
from dipoleClass import dipoleClass
from constants import *
from shape_constants_file_io import *

#from pathos.multiprocessing import ProcessingPool as Pool
def b_induced_single_point(pointVec, *inputList):
    #pointAndFieldVec, *inputList = arg

    # r_vec is observation location
    r_vec = pointVec#.getLocation()
    B_induced = ['x', 'x', 'x']#pointAndFieldVec.getBfield()

    #check if observation point is inside of the material. If so, skip it
    inside = False
    obsPoint = observationPoint(pointVec, B_induced)

    if TREAT_AS_WHOLE == True:
        if len(inputList) == 1:
            for wholeShape in inputList:
                objects = [wholeShape]
                if obsPoint.checkIfInsideWhole(wholeShape):
                    inside = True
            if inside:
                return obsPoint

        else:
            objects = inputList.shapeList
            for obj in objects:
                if obsPoint.checkIfInsideWhole(obj):
                    inside = True
            if inside:
                return obsPoint

    else:
        objects = inputList
        for obj in objects:
            if obsPoint.checkIfInside(obj):
                inside = True
        if inside:
            return obsPoint

    B_induced = [0, 0, 0]
    for obj in objects:

        #
        # for j in range(len(obj.dipoles)):
            ##Define dipole position vector
            # ro_vec = [obj.dipoles[j].loc]
#
            ##Define magnetic field at dipole
            # mag_b = sqrt(obj.dipoles[j].b[0]**2 + obj.dipoles[j].b[1]**2 + obj.dipoles[j].b[2]**2)
            # b_hat = [obj.dipoles[j].b[0]/mag_b, obj.dipoles[j].b[1]/mag_b, obj.dipoles[j].b[2]/mag_b]
#
            ##Define vector from  dipole to observation location
            # r_to_ro = subtract(r_vec, ro_vec)
            # mag_r_to_ro = sqrt((r_vec[0] - obj.dipoles[j].loc[0]) ** 2 + (r_vec[1] - obj.dipoles[j].loc[1]) ** 2 + (r_vec[2] - obj.dipoles[j].loc[2]) ** 2)
            # r_to_ro_hat = divide(r_to_ro, mag_r_to_ro)
#
            #calculate B field from dipole
            # scalar_part = ((mag_b*obj.dipoles[j].v/(4*pi)) * (obj.dipoles[j].s))/((mag_r_to_ro**3)) #(1+obj.dipoles[j].s)
            # vector_part = subtract((3*dot(r_to_ro_hat,b_hat)*r_to_ro_hat),b_hat)
            # B_dipole = multiply(vector_part, scalar_part) #field at obs. point from a single given dipole
#
            #adding contributions
            # B_induced = add(B_induced, B_dipole) #iterative sum from all dipoles

        for dipole in (obj.dipoles):
            # Define dipole position vector
            ro_vec = [dipole.loc]

            # Define magnetic field at dipole
            mag_b = sqrt(dipole.b[0]**2 + dipole.b[1]**2 + dipole.b[2]**2)
            b_hat = [dipole.b[0]/mag_b, dipole.b[1]/mag_b, dipole.b[2]/mag_b]

            # Define vector from  dipole to observation location
            r_to_ro = subtract(r_vec, ro_vec)
            mag_r_to_ro = sqrt((r_vec[0] - dipole.loc[0]) ** 2 + (r_vec[1] - dipole.loc[1]) ** 2 + (r_vec[2] - dipole.loc[2]) ** 2)
            r_to_ro_hat = divide(r_to_ro, mag_r_to_ro)

            #calculate B field from dipole
            scalar_part = ((mag_b*dipole.v/(4*pi)) * (dipole.s))/((mag_r_to_ro**3)) #(1+dipole.s)
            vector_part = subtract((3*dot(r_to_ro_hat,b_hat)*r_to_ro_hat),b_hat)
            B_dipole = multiply(vector_part, scalar_part) #field at obs. point from a single given dipole

            #adding contributions
            B_induced = add(B_induced, B_dipole) #iterative sum from all dipoles


    B_induced = B_induced.ravel()
    finalObsPoint = observationPoint(r_vec, B_induced)

    return (finalObsPoint)


def calculate_program_induced(grid, *inputList):
    #if __name__ == '__calculate_program_induced__':
    #pool = mp.Pool(processes=mp.cpu_count())
    with mp.Pool(mp.cpu_count()) as pool:
        #results = pool.starmap(my_function, tqdm.tqdm(inputs, total=len(inputs)))
        pointField = pool.starmap(b_induced_single_point, tqdm.tqdm( zip(grid.pointsList, repeat(*inputList)), total = len(grid.pointsList)))

    for vec in pointField:
        if vec.bField[0] != 'x':
            grid.addPoint(vec)

    return grid


    #old for loop
        #for i, pointAndFieldVec in enumerate(grid.pointAndFieldVecs):
            #arg = pointAndFieldVec, *inputList
            #b_field[i] = b_induced_single_point(arg)
                ##pointAndFieldVec.assignBfield(b_induced_single_point(arg))
