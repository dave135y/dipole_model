#measure distances between all points, print the min distance and desired,
#return a list of good points and the number of bad
from numpy import mean, min, std
from math import sqrt, ceil
from constants import *
import time

def measure_all_distances(points, volume, mod, prints, returnVec, returnMin):


    density = (len(points)/volume)
    if density == 0:
        print('Cant measure distances because there are no points! Returning 0')
        if returnVec == True and returnMin == True:
            return 0, 0, []

        elif returnVec == True and returnMin == False:
            return 0, []

        elif returnMin == True and returnVec == False:
            return 0
    correctCloseness = MINIMUM_SPACING * 1/((density)**(1/3))
    ccSquared = correctCloseness ** 2
    maxFarness =  (2 - MINIMUM_SPACING) * 1/((density)**(1/3))
    mfSquared = maxFarness ** 2
    counter = 0
    goodPoints = []
    allDists = []
    modNum = ceil(VOROID_MOD_NUM * len(points))
    minsAtEachPt = []


    start = time.time()
    for i in range(len(points)):
        singlePointDists = []
        good = True
        if i % modNum != 0 and mod == True:
            continue
        xi = points[i][0]
        yi = points[i][1]
        zi = points[i][2]
        for j in range(len(points)):
            if (i == j):
                continue
            elif (j % VOROID_MOD_NUM != 0 and mod == True):
                continue
            xj = points[j][0]
            yj = points[j][1]
            zj = points[j][2]


            distsq = sqrt((xi - xj)**2 + (yi - yj)**2 + (zi - zj)**2)
            singlePointDists.append(distsq)


            if distsq <= correctCloseness:
                good = False
        #adding each point's closest guy's  distance to a list
        if len(singlePointDists) > 0:
            minsAtEachPt.append((min(singlePointDists)))
        if good == False:
            counter += 1
        if good == True:
            goodPoints.append(points[i])

        if (100 * int(i)/int(len(points)) % UPDATE_PERCENT_MEASURE_ALL_POINTS == 0):
            print('measuring all distances progress: ', 100 * (round((int(i)/int(len(points))), 2)), '%')

    end = time.time()
    minDist = (min(minsAtEachPt))
    maxDist = (max(minsAtEachPt))
    avgClosest = (mean(minsAtEachPt))
    optimalDist = 1/((density)**(1/3))
    progDist = correctCloseness

    if prints == True:
        print('elapsed time for n2 loop: ', end - start)
        print('Min distances: Actual = ', minDist, ', Goal = ', progDist, ', Ideal = ', optimalDist)
        print('Max distances: Actual = ', maxDist, ', Goal = ', maxFarness, ', Ideal = ', optimalDist)
        print('Average closest spacing: ', avgClosest, ', stddev: ', (std(minsAtEachPt)))
        print('Lost ',  counter, ' points out of ', len(points))
        print('Final density = ', len(goodPoints)/volume )

    if returnVec == True and returnMin == True:
        return minDist, counter, goodPoints

    elif returnVec == True and returnMin == False:
        return counter, goodPoints

    elif returnMin == True and returnVec == False:
        return minDist

def measure_all_distances_dipoles(dipoles, volume, mod, prints):
    points = [None] * len(dipoles)
    for i, dipole in enumerate(dipoles):
        points[i] = dipole.loc


    density = (len(points)/volume)
    if density == 0:
        print('Cant measure distances because there are no points! Returning 0')
        return 0, 0,0 , []

    correctCloseness = MINIMUM_SPACING * 1/((density)**(1/3))
    ccSquared = correctCloseness ** 2
    maxFarness =  (2 - MINIMUM_SPACING) * 1/((density)**(1/3))
    mfSquared = maxFarness ** 2
    counter = 0
    goodPoints = []
    allDists = []
    modNum = ceil(VOROID_MOD_NUM * len(points))
    minsAtEachPt = []


    start = time.time()
    for i in range(len(points)):
        singlePointDists = []
        good = True
        if i % modNum != 0 and mod == True:
            continue
        xi = points[i][0]
        yi = points[i][1]
        zi = points[i][2]
        for j in range(len(points)):
            if (i == j):
                continue
            elif (j % VOROID_MOD_NUM != 0 and mod == True):
                continue
            xj = points[j][0]
            yj = points[j][1]
            zj = points[j][2]


            distsq = sqrt((xi - xj)**2 + (yi - yj)**2 + (zi - zj)**2)
            singlePointDists.append(distsq)


            if distsq <= correctCloseness:
                good = False

        #adding each point's closest guy's  distance to a list
        #if len(singlePointDists) > 0:
        minsAtEachPt.append((min(singlePointDists)))
        if good == False:
            counter += 1
        if good == True:
            goodPoints.append(dipoles[i])

        if (100 * int(i)/int(len(points)) % UPDATE_PERCENT_MEASURE_ALL_POINTS == 0):
            print('measuring all distances progress: ', 100 * (round((int(i)/int(len(points))), 2)), '%')

    end = time.time()
    minDist = (min(minsAtEachPt))
    maxDist = (max(minsAtEachPt))
    avgClosest = (mean(minsAtEachPt))
    optimalDist = 1/((density)**(1/3))
    progDist = correctCloseness

    if prints == True:
        print('elapsed time for n2 loop: ', end - start)
        print('Min distances: Actual = ', minDist, ', Goal = ', progDist, ', Ideal = ', optimalDist)
        print('Max distances: Actual = ', maxDist, ', Goal = ', maxFarness, ', Ideal = ', optimalDist)
        print('Average closest spacing: ', avgClosest, ', stddev: ', (std(minsAtEachPt)))
        print('Lost ',  counter, ' points out of ', len(points))
        print('Final density = ', len(goodPoints)/volume )


    return minDist, maxDist, counter, goodPoints
