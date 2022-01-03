from dipoleClass import dipoleClass
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
from mpl_toolkits.mplot3d import Axes3D
from constants import *
from measure_all_distances import *
from math import pi
import numpy as np

class dipoleCompositeClass:
    def __init__(self, *shapes):
        #order matters!
        self.shapeList = shapes
        self.density = 0 # this is not used
        self.actualDensity = 0 #self.mergeshapes updates density
        self.fillType = ''
        self.isExtruded  = False

        self.volume = self.getVolume()
        self.dipoles = self.mergeShapes()
        self.shape = 'whole'


        self.minDist = self.getMinDist()
        self.maxDist = self.getMaxDist()


    def getTotalDipoles(self):
        return len(self.dipoles)

    def getVolume(self):
        volume = 0
        for shape in self.shapeList:
            volume += shape.volume

        return volume

    def getMinDist(self):
        minDists = []
        for shape in self.shapeList:
            minDists.append(shape.minDist)

        min = np.min(minDists)
        return min

    def getMaxDist(self):
        maxDists = []
        for shape in self.shapeList:
            maxDists.append(shape.maxDist)

        max = np.max(maxDists)
        return max


    def mergeShapes(self):
        fillingList = []
        fillType = []
        for shape in self.shapeList:
            fillingList.append(shape.dipoles)
            fillType.append(shape.fillType)


        flatList = []
        for sublist in fillingList:
            for item in sublist:
                flatList.append(item)

        self.fillType = 'regular'
        for fill in fillType:
            if fill == 'random':
                self.fillType = 'random'

        self.density = len(flatList)/self.volume
        self.actualDensity = len(flatList)/self.volume

        return flatList


    def removeExcess(self):

        minDist, maxDist, numLost, goodPoints = measure_all_distances_dipoles(self.dipoles,
                                        self.volume,
                                        mod = False, prints = True)

        self.dipoles = goodPoints
        self.density = len(goodPoints)/self.volume
        self.actualDensity = len(goodPoints)/self.volume
        self.minDist = minDist
        self.maxDist = maxDist





    def plot(self):
        #plt.figure()
        ax = plt.axes(projection='3d')
        pltPoints = []
        for j in range(len(self.dipoles)):
            pltPoints.append(self.dipoles[j].loc)

        xPlt, yPlt, zPlt = zip(*pltPoints)
        ax.scatter3D(xPlt, yPlt, zPlt);
        title = ('full shape')
        plt.title(title)


    def plotComposite(self,fig):
        #plt.figure()
        ax = plt.axes(projection='3d')
        ax.set_box_aspect(aspect = (1,1,1))
        #fig = plt.figure()
        ax = Axes3D(fig)
        ax.set_xlim3d(-0.2, 0.2)
        ax.set_ylim3d(-0.2, 0.2)
        ax.set_zlim3d(-0.1, 0.3)

        for shape in self.shapeList:
            shape.plotComposite(ax)

    def plot2d(self, plane, fig):

        pltPoints = []
        for j in range(len(self.dipoles)):
            pltPoints.append(self.dipoles[j].loc)

        twoDimPoints = []

        if plane == 'xy' or  plane == 'yx':


            xPlt, yPlt, zPlt = zip(*pltPoints)
            plt.figure(fig)
            plt.scatter(xPlt, yPlt)
            title = ('xy plane')
            plt.title(title)
            #plt.show()


        elif plane == 'xz' or plane =='zx':


            xPlt, yPlt, zPlt = zip(*pltPoints)
            #plt.figure()
            plt.scatter(xPlt, zPlt)
            title = ('xz plane')
            plt.title(title)
            #plt.show()

        elif plane == 'yz' or plane =='zy':


            xPlt, yPlt, zPlt = zip(*pltPoints)
            #plt.figure()
            plt.scatter(yPlt, zPlt)
            title = ('yz plane')
            plt.title(title)
            #plt.show()

        else:
            print("invalid plane arg: 'xy', 'xz', 'yz'")

    def plot2dOverlay(self, ax, plane, planeSlice):
        colorMap = []
        twoDimPoints = []

        if plane == 'xy' or  plane == 'yx':
            for index, points in enumerate(self.dipoles):
                if points.loc[2] < planeSlice + self.maxDist and points.loc[2] > planeSlice - self.maxDist:
                    twoDimPoints.append(points.loc)
                    if points.s > AVG_SUS:
                        colorMap.append('r')
                    else:
                        colorMap.append('b')

            xPlt, yPlt, zPlt = zip(*twoDimPoints)

            ax.scatter(xPlt, yPlt, c=colorMap, s = 1)

        elif plane == 'xz' or plane == 'zx':
            for index, points in enumerate(self.dipoles):
                if points.loc[1] < planeSlice + self.maxDist and points.loc[1] > planeSlice - self.maxDist:
                    twoDimPoints.append(points.loc)
                    if points.s > AVG_SUS:
                        colorMap.append('r')
                    else:
                        colorMap.append('b')

            xPlt, yPlt, zPlt = zip(*twoDimPoints)

            ax.scatter(xPlt, zPlt, c=colorMap, s = 1)

        elif plane == 'yz' or plane == 'zy':
            for index, points in enumerate(self.dipoles):
                if points.loc[0] < planeSlice + self.maxDist and points.loc[0] > planeSlice - self.maxDist:
                    twoDimPoints.append(points.loc)
                    if points.s > AVG_SUS:
                        colorMap.append('r')
                    else:
                        colorMap.append('b')

            xPlt, yPlt, zPlt = zip(*twoDimPoints)

            ax.scatter(yPlt, zPlt, c=colorMap, s = 1)

        else:
            print("invalid plane arg: 'xy', 'xz', 'yz'")

    def extrudeCylinder(self, bot, top, radius, facePlane, uShift, vShift):
        extrudeVolume = pi * np.abs(top - bot) * (radius ** 2)
        newList = []
        newOrg = [uShift, vShift]

        if facePlane == 'xy' or facePlane == 'yx':

            for dipole in self.dipoles:
                if dipole.loc[2] < bot or dipole.loc[2] > top:
                    newList.append(dipole)
                else:
                    pointToCylCenter = sqrt((dipole.loc[0] - newOrg[0])**2 + (dipole.loc[1] - newOrg[1])**2)
                    if pointToCylCenter > radius:
                        newList.append(dipole)

        elif facePlane == 'xz' or facePlane == 'zx':

            for dipole in self.dipoles:
                if dipole.loc[1] < bot and dipole.loc[1] > top:
                    newList.append(dipole)
                else:
                    pointToCylCenter = sqrt((dipole.loc[0] - newOrg[0])**2 + (dipole.loc[2] - newOrg[2])**2)
                    if pointToCylCenter > radius:
                        newList.append(dipole)

        elif facePlane == 'yz' or facePlane == 'zy':

            for dipole in self.dipoles:
                if dipole.loc[0] < bot and dipole.loc[0] > top:
                    newList.append(dipole)
                else:
                    pointToCylCenter = sqrt((dipole.loc[1] - newOrg[1])**2 + (dipole.loc[2] - newOrg[2])**2)
                    if pointToCylCenter > radius:
                        newList.append(dipole)

        else:
            print('invalid extrude facePlane arg')

        self.dipoles = newList
        self.volume = self.volume - extrudeVolume

        self.density = len(self.dipoles)/self.volume
        self.actualDensity = len(self.dipoles)/self.volume
        self.isExtruded = True

    def getPerimeters(self):
        fillingList = []
        if self.isExtruded == True:
            print('Cant get perimeters of extruded objects')
            quit()
        else:
            for shape in self.shapeList:
                fillingList.append(shape.getPerimeterInfo())

        return fillingList
