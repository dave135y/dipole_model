#from dipoleCylinderClass import dipoleCylinderClass
#from dipoleSphereClass import dipoleSphereClass
from voronoi_centroid import voronoi_centroid
from constants import *
from measure_all_distances import measure_all_distances
from math import cos, sin, pi, ceil, sqrt
import numpy as np

#if 2, we get the 2nd to last update to pointList
nToLastVoro = 2

def voronoi_implementation(pointList, object):
    update = [pointList]
    voroTryCounter = 0
    while len(update) <= nToLastVoro:
        if voroTryCounter > 0:
            print('Voronoi method failed. Trying Again.')
        elif voroTryCounter > MAX_VORO_TRIES:
            quit()

        counter = 0
        higherDens = 0
        destroy = False
        update = [pointList]
        densityList = []
        voroTryCounter += 1

        while destroy == False:
            #safety net to  prevent running too long if loop doesnt break
            if counter >= SAFETY_NET:
                break

            test = voronoi_centroid(update[counter])
            print('Voronoi runs: ', counter + 1)
            update.append(test)

            list = []
            #Look in test for all points in volume, don't update. Use this in measure_all_distances
            for points in test:
                if object.shape == 'cylinder':
                    radius = sqrt(np.dot([points[0], points[1]], [points[0], points[1]]))
                    height = points[2]
                    if (radius > object.innerRho and radius < object.outerRho and height < object.height and height > 0):
                        list.append(points)
                elif object.shape == 'sphere':
                    mag = sqrt(np.dot(points, points))
                    if (mag > object.innerRadius and mag < object.outerRadius):
                        list.append(points)

                elif object.shape == 'recPrism':
                    if (abs(points[0]) < object.xlen/2 and  abs(points[1]) < object.ylen/2 and points[2] > 0 and points[2] < object.zlen):
                        list.append(points)

            #Voronoi method will fail in  a few cases. one of them is that
            #all the points leave the shape
            if len(list) == 0:
                print('additional voronois would leave you with no points!')


            #Another  is that density starts to rise
            densityList.append(len(list)/object.volume)
            if densityList[counter] > densityList[counter - 1]:
                higherDens += 1
            elif (densityList[counter] <= densityList[counter - 1] and higherDens > 0):
                higherDens -= 1

            #Another occurs when points converge somehow. when  minDist = 0, need to stop voronoi
            minDist = measure_all_distances(list, object.volume, mod = True, prints = False, returnVec = False, returnMin = True)
            #if minDist != 0, we  can run 'update' thorugh voroid algorithm again

            if (minDist > 0 and higherDens < 2 and len(list) > 0):
                print('density = ', len(list)/object.volume)
                #update.append(test)
                counter += 1
            else:
                print('destroy density = ', len(list)/object.volume)
                destroy = True

    #[-2] gives the pointList from before the failure. Maybe need to make this -3
    print('final density = ', len(update[-nToLastVoro])/object.volume)
    return update[-nToLastVoro]
