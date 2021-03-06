import pickle
from math import cos, sin, pi, ceil, sqrt
from random import uniform, randint
from dipoleClass import dipoleClass
from constants import *
from voronoi_centroid import voronoi_centroid
from measure_all_distances import *
from voronoi_implementation import voronoi_implementation
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
from random import randint


#%matplotlib inline

#initializes a cylinder whose base lies in the x-y plane
class dipoleCylinderClass:
    def __init__(self, innerRho, outerRho, height, density, rPrecision, thetaPrecision, hPrecision, fillType, color):
        self.innerRho = innerRho
        self.outerRho = outerRho
        self.height = height
        self.initialDensity = density  # thisis still used for random fill
        self.actualDensity = density
        self.color = color
        self.volume = pi * self.height * (self.outerRho ** 2 - self.innerRho ** 2)
        self.dipoles = []
        self.shape = 'cylinder'
        self.isFilled = False
        self.totalXShift = 0
        self.totalYShift = 0
        self.totalZShift = self.height/2
        self.minDist = 0
        self.maxDist = 0
        self.shapeList = [self]
        self.densityRatio = 1

        self.fillType = fillType
        self.rPrecision = rPrecision
        self.thetaPrecision = thetaPrecision
        self.heightPrecision = hPrecision


    #directions  are 'x', 'y', 'z'. Distances are + or - (shift) in cm.

    def getPerimeterInfo(self):

        #perimeters will be listed as: xmin, xmax, ymin, ymax, zmin, zmax for boxes
        #{origin, innerrho, outerrho, height  for cylnders}
        origin = [self.totalXShift, self.totalYShift, self.totalZShift - self.height/2]

        perimeters = {'name':self.shape, 'origin':origin, 'shapeInfo':[self.innerRho, self.outerRho, self.height]}

        return perimeters

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
                    #if j == 1:
                        #print(point)
                    point[2] = point[2] + distance
                    #if j ==1:
                        #print(point)
                    self.dipoles[j].loc = point
                else:
                    print("invalid direction arg: 'x', 'y', 'z'")
            #print('xShift: ', self.totalXShift)
            #print('yShift: ', self.totalYShift)
            #print('zShift: ', self.totalZShift)


    def plotComposite(self, ax):
        if self.isFilled == True:
            pltPoints = []
            for j in range(len(self.dipoles)):
                pltPoints.append(self.dipoles[j].loc)

            xPlt, yPlt, zPlt = zip(*pltPoints)
            ax.scatter3D(xPlt, yPlt, zPlt, c=self.color);

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
            title = (self.shape, ': Inner Radius = ', self.innerRho, ', Outer Radius = ', self.outerRho)
            plt.title(title)
            plt.show()

    def plot2d(self, plane, ax):
        if self.isFilled == True:
            pltPoints = []
            for j in range(len(self.dipoles)):
                pltPoints.append(self.dipoles[j].loc)

            twoDimPoints = []

            if plane == 'xy' or  plane == 'yx':
                for points in pltPoints:
                    if points[2] < self.totalZShift + self.maxDist*self.densityRatio and points[2] > self.totalZShift - self.maxDist*self.densityRatio:
                        twoDimPoints.append(points)

                xPlt, yPlt, zPlt = zip(*twoDimPoints)
                #plt.figure(fig)
                ax.scatter(xPlt, yPlt, s = 0.5)
                ax.hlines(y = self.outerRho + self.totalYShift, xmin = -self.outerRho + self.totalXShift, xmax = self.outerRho +self.totalXShift, linewidth = 0.5)
                ax.hlines(y = -self.outerRho + self.totalYShift,xmin = -self.outerRho + self.totalXShift, xmax = self.outerRho +self.totalXShift, linewidth = 0.5)
                ax.vlines(x = self.outerRho + self.totalXShift, ymin = -self.outerRho + self.totalYShift, ymax = self.outerRho +self.totalYShift, linewidth = 0.5)
                ax.vlines(x = -self.outerRho + self.totalXShift,ymin = -self.outerRho + self.totalYShift, ymax = self.outerRho +self.totalYShift, linewidth = 0.5)

                title = ('xy plane')
                ax.set_title(title)



            elif plane == 'xz' or plane =='zx':
                for points in pltPoints:
                    if points[1] < self.totalYShift + self.maxDist*self.densityRatio and points[1] > self.totalYShift - self.maxDist*self.densityRatio:
                        twoDimPoints.append(points)

                xPlt, yPlt, zPlt = zip(*twoDimPoints)
                #plt.figure(fig)
                ax.scatter(xPlt, zPlt, s = 0.5)
                ax.hlines(y = 0 + self.totalZShift  - self.height/2, xmin = -self.outerRho + self.totalXShift, xmax = self.outerRho + self.totalXShift, linewidth = 0.5)
                ax.hlines(y = self.height + self.totalZShift - self.height/2, xmin = -self.outerRho + self.totalXShift, xmax = self.outerRho + self.totalXShift, linewidth = 0.5)
                title = ('xz plane')
                ax.set_title(title)


            elif plane == 'yz' or plane =='zy':
                for points in pltPoints:
                    if points[0] < self.totalXShift + self.maxDist*self.densityRatio and points[0] > self.totalXShift - self.maxDist*self.densityRatio:
                        twoDimPoints.append(points)

                xPlt, yPlt, zPlt = zip(*twoDimPoints)
                #plt.figure(fig)
                ax.scatter(yPlt, zPlt, s = 0.5)
                ax.hlines(y = 0 + self.totalZShift - self.height/2, xmin = -self.outerRho + self.totalYShift, xmax = self.outerRho + self.totalYShift, linewidth = 0.5)
                ax.hlines(y = self.height + self.totalZShift - self.height/2, xmin = -self.outerRho + self.totalYShift, xmax = self.outerRho + self.totalYShift, linewidth = 0.5)
                title = ('yz plane')
                ax.set_title(title)


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
        if self.fillType == 'random':
            bigOuterRho = self.outerRho + PCT_BIGGER * self.outerRho
            smallInnerRho = self.innerRho - self.innerRho * PCT_SMALLER
            bigHeight = self.height + self.height * PCT_BIGGER
            largeVolume = pi * bigHeight * (bigOuterRho ** 2 - smallInnerRho ** 2)
            largeShellNumDipoles = ceil(self.initialDensity * largeVolume)

            #define actual values for shape
            numDipoles = ceil(self.initialDensity * self.volume)
            print('goal volume = ', self.volume, 'goal total dipoles = ', numDipoles)

            #initializing first dipole location. Need this since succeeding points need to be based on this
            #pointList is a larger volume than we want
            pointList = [[0, 0, (self.outerRho + self.innerRho)/2]]
            #filling in larger volume
            while len(pointList) < round(largeShellNumDipoles):
            #for i in range(0,int(shell_total_dipoles)):
                x = uniform(-(bigOuterRho), bigOuterRho)
                y = uniform(-(bigOuterRho), bigOuterRho)
                z = uniform(-(bigHeight - self.height) , bigHeight)
                pointRho = sqrt(x**2 + y**2)

                validPoint = True
                #make sure point is inside sphere
                if (pointRho <= smallInnerRho) or (pointRho >= bigOuterRho):
                    validPoint = False
                    continue

                pointList.append([x, y, z])

            #initPoints are within the boundaries of the actual shape
            initPoints = []
            for points in pointList:
                radius = sqrt(np.dot([points[0], points[1]], [points[0], points[1]]))
                height = points[2]
                if (radius > self.innerRho and radius < self.outerRho and height < self.height and height > 0):
                    initPoints.append(points)

            #actual density at this point should be very close to specified
            self.actualDensity = (len(initPoints)/self.volume)

            #runs the voronoi method to separate the random points to a minimum distance
            voroPoints = voronoi_implementation(pointList, self)
            list = []
            #voronoi method might have pushed some points out of bounds
            for points in voroPoints:
                radius = sqrt(np.dot([points[0], points[1]], [points[0], points[1]]))
                height = points[2]
                if (radius > self.innerRho and radius < self.outerRho and height < self.height and height > 0):
                    list.append(points)

            finalPointList = list
            self.actualDensity = (len(finalPointList)/self.volume)
            volumeElement = self.volume/len(finalPointsList)

            for i in range(len(finalPointList)):
                self.dipoles.append(dipoleClass(finalPointList[i], [0,0,0], 0, volumeElement))

            spacing = 1/actualDensity**(1/3)
            self.minDist = spacing
            self.maxDist = spacing
            self.isFilled = True
            print('finished filling cylinder')

        elif self.fillType == 'box':

            boxWidth = self.outerRho * 2
            boxHeight = self.height
            spacing = 1/self.initialDensity**(1/3)
            fixedSpacing = 1/(self.initialDensity**(1/3) * self.densityRatio)

            i = round((boxWidth)/self.rPrecision) #number of points, rounded to nearest integer
            wSpacing  = (boxWidth)/i #Make it so that spacing is divisible by an even number. This makes the grid equidistant from boundaries
            wDensity = 1/wSpacing**3
            wlocs = np.arange(-boxWidth/2 + wSpacing/2, boxWidth/2, wSpacing)

            i = round((boxHeight)/self.hPrecision) #number of points, rounded to nearest integer
            hSpacing  = (boxHeight)/i
            hDensity = 1/hSpacing**3
            hlocs = np.arange(hSpacing/2, boxHeight, hSpacing)

            llocs = wlocs
            pointList = np.vstack(np.meshgrid(llocs, wlocs, hlocs)).reshape(3,-1).T
            pointList.ravel()
            #pointList = np.stack((np.ravel(x), np.ravel(y), np.ravel(z)), axis=-1)
            finalPoints = []
            for points in pointList:
                radius = sqrt(np.dot([points[0], points[1]], [points[0], points[1]]))
                height = points[2]
                if (radius > self.innerRho and radius < self.outerRho and height < self.height and height > 0):
                    finalPoints.append(points)

            numPoints = len(finalPoints)

            volumeElement = wSpacing**2 * hSpacing
            self.volume = numPoints * volumeElement
            calculatedDensity = numPoints/self.volume
            self.actualDensity = calculatedDensity


            for i in range(len(finalPoints)):
                self.dipoles.append(dipoleClass(finalPoints[i], [0,0,0], 0, volumeElement))

            self.minDist = np.min([wSpacing, hSpacing])
            self.maxDist = np.max([wSpacing, hSpacing])

            self.isFilled = True
            print('finished filling cylinder')

        else:

            i = round((self.outerRho - self.innerRho)/(self.rPrecision)) #number of points, rounded to nearest integer
            if  i == 0:
                i = 1
            rSpacing  = (self.outerRho - self.innerRho)/i
            rDensity = 1/rSpacing**3
            rlocs = np.arange(self.innerRho  + rSpacing/2, self.outerRho, rSpacing)
            xlocs = []
            ylocs = []
            for j, radius in enumerate(rlocs):
                #s = r*deltatheta ->deltatheta = s/r
                #
                if j % 2 == 1:
                    subber = 1
                elif j % 2 == 0:
                    subber = -1

                i = round(2 * np.pi * radius/self.thetaPrecision) - subber
                if  i == 0:
                    i = 1
                thetaSpacing = 2*np.pi/i

                rand = randint(0, 100)
                #if j % 2 == 0:
                thetalocs = np.arange(0 + (rand * thetaSpacing/2), 2 * np.pi + (rand * thetaSpacing/2), thetaSpacing)
                #else:
                #thetalocs = np.arange(0 + thetaUpdater/3, 2 * np.pi + thetaUpdater/3, thetaSpacing)
                for i, theta in enumerate(thetalocs):
                    xlocs.append(radius * np.cos(theta))
                    ylocs.append(radius * np.sin(theta))
                    if i == 0 and j ==0:
                        rtheta1 = thetaSpacing * radius

            i = round((self.height - 0)/(self.heightPrecision))
            if  i == 0:
                i = 1
            zSpacing  = (self.height - 0)/i
            zDensity  = 1/zSpacing**3
            zlocs = np.arange(0 + zSpacing/2, self.height + 0, zSpacing)


            new  = []
            for i in range(len(xlocs)):
                new.append([xlocs[i], ylocs[i]])
            #why doesnt meshgridwork?
            #I can probably absorb the top loop into the next
            finalPoints = []
            for i in range(len(new)):
                for j in range(len(zlocs)):
                    finalPoints.append([new[i][0], new[i][1], zlocs[j]])


            numPoints = len(finalPoints)
            volumeElement = rtheta1 * zSpacing * rSpacing
            self.volume = numPoints * volumeElement
            #print(self.volume)

            calculatedDensity = numPoints/self.volume
            self.actualDensity = calculatedDensity
            #print(self.actualDensity)

            for i in range(len(finalPoints)):
                self.dipoles.append(dipoleClass(finalPoints[i], [0,0,0], 0, volumeElement))

            self.minDist = np.min([rtheta1, rSpacing, zSpacing])
            self.maxDist = np.max([rtheta1, rSpacing, zSpacing])

            self.isFilled = True
            print('finished filling cylinder')



    def removeExcess(self):

        minDist, maxDist, numLost, goodPoints = measure_all_distances_dipoles(self.dipoles,
                                        self.volume,
                                        mod = False, prints = True)

        self.dipoles = goodPoints
        self.actualDensity = len(goodPoints)/self.volume
        self.minDist = minDist
        self.maxDist = maxDist
