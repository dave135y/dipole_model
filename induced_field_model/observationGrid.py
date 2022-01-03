from constants import *
from observationPoint import *
from numpy import linspace

class observationGrid:
    def __init__(self, xBegin, xEnd, yBegin, yEnd, zBegin, zEnd, xPoints, yPoints, zPoints):

        #private
        self.xStart = xBegin
        self.xStop = xEnd
        self.yStart = yBegin
        self.yStop = yEnd
        self.zStart = zBegin
        self.zStop = zEnd
        self.xPoints = xPoints
        self.yPoints = yPoints
        self.zPoints = zPoints
        self.numPoints = self.getNumPoints()
        self.pointsList = self.makePointsList()
        self.PFVcounter = 0 #0
        #public
        self.pointAndFieldVecs = [] #a list of observation_points objects
        #self.pointAndFieldVecs = self.initializeGrid()


    #private

    def getNumPoints(self):
        #xpoints =  ((self.xStop - self.xStart) * self.xPoints) + 1
        #ypoints =  ((self.yStop - self.yStart) * self.yPoints) + 1
        #zpoints =  ((self.zStop - self.zStart) * self.zPoints) + 1
        return int(self.xPoints * self.yPoints * self.zPoints)


    def makePointsList(self):
        fillingList = [None] * self.numPoints

        #xpoints =  ((self.xStop - self.xStart) * self.xPoints) + 1
        #ypoints =  ((self.yStop - self.yStart) * self.yPoints) + 1
        #zpoints =  ((self.zStop - self.zStart) * self.zPoints) + 1

        x = linspace(self.xStart, self.xStop, self.xPoints)
        y = linspace(self.yStart, self.yStop, self.yPoints)
        z = linspace(self.zStart, self.zStop, self.zPoints)

        counter = 0
        for i in range(len(x)):
            for j in range(len(y)):
                for k in range(len(z)):
                    xR = round(x[i], ROUND_OBS_POINTS)
                    yR = round(y[j], ROUND_OBS_POINTS)
                    zR = round(z[k], ROUND_OBS_POINTS)
                    fillingList[counter] = ([xR, yR, zR])
                    counter += 1

        return  fillingList

    def initializeGrid(self):
        fieldVecs = []

        for i in range(self.numPoints):
            B_induced= [0, 0, 0]
            fieldVecs.append(observationPoint(self.pointsList[i], B_induced))

        self.PFVCounter = self.numPoints
        return fieldVecs

    #public
    def addPoint(self, obsPoint):
        self.pointAndFieldVecs.append(obsPoint)

        self.PFVcounter =  self.PFVcounter + 1


    def getXVals(self):
        fillingList = [None] * self.PFVcounter
        for i, points in enumerate(self.pointAndFieldVecs):
            fillingList[i] = points.getX()

        return fillingList


    def getYVals(self):
        fillingList = [None] * self.PFVcounter
        for i, points in enumerate(self.pointAndFieldVecs):
            fillingList[i] = points.getY()

        return fillingList


    def getZVals(self):
        fillingList = [None] * self.PFVcounter
        for i, points in enumerate(self.pointAndFieldVecs):
            fillingList[i] = points.getZ()

        return fillingList


    def getBXVals(self):
        fillingList = [None] * self.PFVcounter
        for i, points in enumerate(self.pointAndFieldVecs):
            fillingList[i] = points.getBX()

        return fillingList


    def getBYVals(self):
        fillingList = [None] * self.PFVcounter
        for i, points in enumerate(self.pointAndFieldVecs):
            fillingList[i] = points.getBY()

        return fillingList


    def getBZVals(self):
        fillingList = [None] * self.PFVcounter
        for i, points in enumerate(self.pointAndFieldVecs):
            fillingList[i] = points.getBZ()

        return fillingList


    def getMagVals(self):
        fillingList = [None] * self.PFVcounter
        for i, points in enumerate(self.pointAndFieldVecs):
            fillingList[i] = points.getFieldMagnitude()

        return fillingList
