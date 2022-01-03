import pickle
from math import cos, sin, pi, ceil, sqrt
from random import uniform, randint
from dipoleClass import dipoleClass
from constants import *
from voronoi_centroid import voronoi_centroid
from measure_all_distances import *
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
#%matplotlib inline

#initializes a sphere centered at origin
class dipoleSphereClass:
    def __init__(self, innerRadius, outerRadius, density, color):
        self.innerRadius = innerRadius
        self.outerRadius = outerRadius
        self.initialDensity = density
        self.actualDensity = density
        self.color = color
        self.volume = 4/3 * pi * (outerRadius ** 3 - innerRadius ** 3)
        self.dipoles = []
        self.shape = 'sphere'
        self.isFilled = False
        self.totalXShift = 0
        self.totalYShift = 0
        self.totalZShift = 0
        self.minDist = 0
        self.maxDist = 0
        self.shapeList = [self]

    #directions  are 'x', 'y', 'z'. Distances are + or - (shift) in cm.
    def shift(self, direction, distance):
        if self.isFilled == True:
            locPoints = []
            if direction == 'x':
                self.totalXShift = self.totalXShift + distance
            elif direction == 'y':
                self.totalYShift = self.totalYShift + distance
            elif direction == 'z':
                self.totalZShift = self.totalZShift + distance

            for j in range(len(self.dipoles)):
                if direction == 'x':
                    point = (self.dipoles[j].loc)
                    point[0] = point[0] + distance
                    self.dipoles[j].loc = point

                elif direction == 'y':
                    point = (self.dipoles[j].loc)
                    point[1] = point[1] + distance
                    self.dipoles[j].loc = point

                elif direction == 'z':
                    point = (self.dipoles[j].loc)
                    if j == 1:
                        print(point)
                    point[2] = point[2] + distance
                    if j ==1:
                        print(point)
                    self.dipoles[j].loc = point
                else:
                    print("invalid direction arg: 'x', 'y', 'z'")
            print('xShift: ', self.totalXShift)
            print('yShift: ', self.totalYShift)
            print('zShift: ', self.totalZShift)

    def plotComposite(self, ax):
        if self.isFilled == True:
            pltPoints = []
            for j in range(len(self.dipoles)):
                pltPoints.append(self.dipoles[j].loc)

            xPlt, yPlt, zPlt = zip(*pltPoints)
            ax.scatter3D(xPlt, yPlt, zPlt, c=zPlt, cmap=self.color);

        else:
            print('sphere: cant plot unfilled shape')


    def plot(self):
        if self.isFilled == True:
            pltPoints = []
            for j in range(len(self.dipoles)):
                pltPoints.append(self.dipoles[j].loc)

            plt.figure()
            ax = plt.axes(projection='3d')
            xPlt, yPlt, zPlt = zip(*pltPoints)
            ax.scatter3D(xPlt, yPlt, zPlt, c=zPlt, cmap=self.color);
            title = (self.shape, ': Inner Radius = ', self.innerRadius, ', Outer Radius = ', self.outerRadius)
            plt.title(title)
            plt.show()

    def plot2d(self, plane):
        if self.isFilled == True:
            pltPoints = []
            for j in range(len(self.dipoles)):
                pltPoints.append(self.dipoles[j].loc)

            twoDimPoints = []

            if plane == 'xy' or  plane == 'yx':
                for points in pltPoints:
                    if points[2] < self.totalZShift + CLOSE_TO_SLICE and points[2] > self.totalZShift - CLOSE_TO_SLICE:
                        twoDimPoints.append(points)

                xPlt, yPlt, zPlt = zip(*twoDimPoints)
                plt.figure()
                plt.scatter(xPlt, yPlt)
                title = ('xy plane')
                plt.title(title)
                plt.show()


            elif plane == 'xz' or plane =='zx':
                for points in pltPoints:
                    if points[1] < self.totalYShift + CLOSE_TO_SLICE and points[1] > self.totalYShift - CLOSE_TO_SLICE:
                        twoDimPoints.append(points)

                xPlt, yPlt, zPlt = zip(*twoDimPoints)
                plt.figure()
                plt.scatter(xPlt, zPlt)
                title = ('xz plane')
                plt.title(title)
                plt.show()

            elif plane == 'yz' or plane =='zy':
                for points in pltPoints:
                    if points[0] < self.totalXShift + CLOSE_TO_SLICE and points[0] > self.totalXShift - CLOSE_TO_SLICE:
                        twoDimPoints.append(points)

                xPlt, yPlt, zPlt = zip(*twoDimPoints)
                plt.figure()
                plt.scatter(yPlt, zPlt)
                title = ('yz plane')
                plt.title(title)
                plt.show()

            else:
                print("invalid plane arg: 'xy', 'xz', 'yz'")



    def magnetize(self, field, sus):
        if self.isFilled == True:
            for j in range(len(self.dipoles)):
                self.dipoles[j].magnetizeDipole(field, sus)

        else:
            print('cant magnetize empty object!!')
            quit()


    def save(self, filename):
        with open(filename, "wb") as fp:   #Pickl
            pickle.dump(self, fp)

    def fill(self):
        #define larger volume than necessary for voronoi method to work
        bigOuterRadius = self.outerRadius + PCT_BIGGER * self.outerRadius
        smallOuterRadius = self.innerRadius - self.innerRadius * PCT_SMALLER
        largeVolume = 4/3 * pi * (bigOuterRadius ** 3 - smallOuterRadius ** 3)
        largeShellNumDipoles = ceil(self.initialDensity * largeVolume)

        #define actual values for shape
        numDipoles = ceil(self.initialDensity * self.volume)
        print('goal volume = ', self.volume, 'goal total dipoles = ', numDipoles)

        #initializing first dipole location. Need this since succeeding points need to be based on this
        #pointList is a larger volume than we want
        pointList = [[0, 0, (self.outerRadius + self.innerRadius)/2]]
        #filling in larger volume
        while len(pointList) < int(largeShellNumDipoles):
        #for i in range(0,int(shell_total_dipoles)):
            x = uniform(-(bigOuterRadius), bigOuterRadius)
            y = uniform(-(bigOuterRadius), bigOuterRadius)
            z = uniform(-(bigOuterRadius), bigOuterRadius)
            pointRad = sqrt(x**2 + y**2 + z**2)

            validPoint = True
            #make sure point is inside sphere
            if (pointRad <= smallOuterRadius) or (pointRad >= bigOuterRadius):
                validPoint = False
                continue

            pointList.append([x, y, z])

        #initPoints are within the boundaries of the actual shape
        initPoints = []
        for points in pointList:
            mag = sqrt(np.dot(points, points))
            if (mag > self.innerRadius and mag < self.outerRadius):
                initPoints.append(points)

        #actual density at this point should be very close to specified
        self.actualDensity = (len(initPoints)/self.volume)

        #runs the voronoi method to separate the random points to a minimum distance
        voroPoints = voronoi_implementation(pointList, self)
        list = []
        #voronoi method might have pushed some points out of bounds
        for points in voroPoints:
            mag = sqrt(np.dot(points, points))
            if (mag < self.outerRadius and mag > self.innerRadius):
                list.append(points)

        finalPointList = list
        self.actualDensity = (len(finalPointList)/self.volume)

        for i in range(len(finalPointList)):
            self.dipoles.append(dipoleClass(finalPointList[i], [0,0,0], 0))

        self.isFilled = True
        print('finished filling sphere')

    def removeExcess(self):
        minDist, maxDist, numLost, goodPoints = measure_all_distances_dipoles(self.dipoles,
                                        self.volume,
                                        mod = False, prints = True)

        self.dipoles = goodPoints
        self.actualDensity = len(goodPoints)/self.volume
        self.minDist = minDist
        self.maxDist = maxDist
