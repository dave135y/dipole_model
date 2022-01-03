
import pickle
from math import cos, sin, pi, ceil, sqrt
from numpy import abs
from random import uniform, randint
from dipoleClass import dipoleClass
from constants import *
from voronoi_centroid import voronoi_centroid
from measure_all_distances import *
from voronoi_implementation import voronoi_implementation
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
#%matplotlib inline

#initializes a cylinder whose base lies in the x-y plane
class dipoleRecPrismClass:
    def __init__(self, xlen, ylen, zlen, density, color):
        self.xlen = xlen
        self.ylen = ylen
        self.zlen = zlen
        self.initialDensity = density
        self.actualDensity = density
        self.color = color
        self.volume = xlen * xlen * zlen
        self.dipoles = []
        self.shape = 'recPrism'
        self.isFilled = False
        self.totalXShift = 0
        self.totalYShift = 0
        self.totalZShift = self.zlen/2
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
            print('cyl: cant plot unfilled shape')


    def plot(self):
        if self.isFilled == True:
            pltPoints = []
            for j in range(len(self.dipoles)):
                pltPoints.append(self.dipoles[j].loc)

            plt.figure()
            ax = plt.axes(projection='3d')
            xPlt, yPlt, zPlt = zip(*pltPoints)
            ax.scatter3D(xPlt, yPlt, zPlt, c=zPlt, cmap=self.color);
            title = (self.shape, ': xlen = ', self.xlen, ', ylen = ', self.ylen, ', zlen = ', self.zlen)
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
                #plt.show()


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
                print("invalid plane arg, do: 'xy', 'xz', 'yz'")


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
        xlenBig = self.xlen + PCT_BIGGER * self.xlen
        ylenBig = self.ylen + PCT_BIGGER * self.zlen
        zlenBig = self.zlen + PCT_BIGGER * self.zlen
        largeVolume = xlenBig * ylenBig * zlenBig
        largeShellNumDipoles = ceil(self.initialDensity * largeVolume)

        #define actual values for shape
        numDipoles = ceil(self.initialDensity * self.volume)
        print('goal volume = ', self.volume, 'goal total dipoles = ', numDipoles)

        #initializing first dipole location. Need this since succeeding points need to be based on this
        #pointList is a larger volume than we want
        pointList = [[0, 0, self.zlen/2]]
        #filling in larger volume
        while len(pointList) < int(largeShellNumDipoles):
        #for i in range(0,int(shell_total_dipoles)):
            x = uniform(-(xlenBig/2), xlenBig/2)
            y = uniform(-(ylenBig/2), ylenBig/2)
            z = uniform(-(zlenBig/2 + self.totalZShift) , zlenBig)


            pointList.append([x, y, z])

        #initPoints are within the boundaries of the actual shape
        initPoints = []
        for points in pointList:
            xlen = points[0]
            ylen = points[1]
            zlen = points[2]
            if (abs(points[0]) < self.xlen/2 and  abs(points[1]) < self.ylen/2 and (points[2]) > 0 and points[2] < self.zlen):
                initPoints.append(points)

        #actual density at this point should be very close to specified
        self.actualDensity = (len(initPoints)/self.volume)

        #runs the voronoi method to separate the random points to a minimum distance
        voroPoints = voronoi_implementation(pointList, self) #this fn must be edited for different shapes
        list = []
        #voronoi method might have pushed some points out of bounds
        for points in voroPoints:
            if (abs(points[0]) < self.xlen/2 and  abs(points[1]) < self.ylen/2 and points[2] > 0 and points[2] < self.zlen):
                list.append(points)

        finalPointList = list
        self.actualDensity = (len(finalPointList)/self.volume)

        for i in range(len(finalPointList)):
            self.dipoles.append(dipoleClass(finalPointList[i], [0,0,0], 0))

        self.isFilled = True
        print('finished filling prism')


    def removeExcess(self):
        minDist, maxDist, numLost, goodPoints = measure_all_distances_dipoles(self.dipoles,
                                        self.volume,
                                        mod = False, prints = True)

        self.dipoles = goodPoints
        self.actualDensity = len(goodPoints)/self.volume
        self.minDist = minDist
        self.maxDist = maxDist
