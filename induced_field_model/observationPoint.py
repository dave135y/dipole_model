from numpy import sqrt, abs
from constants import *
from dipoleSphereClass import dipoleSphereClass
from dipoleCylinderClass import dipoleCylinderClass
RANDOM_EXTRA_SPACE_MULTIPLIER = 3
REGULAR_EXTRA_SPACE_MULTIPLIER = 1

class observationPoint:

    def __init__(self, loc, field):
        self.location = loc
        self.bField = field
        self.isInside = False


    def assignLocation(self, loc):
        self.location = loc


    def assignBfield(self, field):
        self.bField = field


    def getLocation(self):
        return(self.location)


    def getX(self):
        return(self.location[0])


    def getY(self):
        return(self.location[1])


    def getZ(self):
        return(self.location[2])


    def getBfield(self):
        return (self.bField)


    def getBX(self):
        return(self.bField[0])


    def getBY(self):
        return(self.bField[1])


    def getBZ(self):
        return(self.bField[2])


    def getRadius(self):
        x = self.location[0]
        y = self.location[1]
        z = self.location[2]
        return (sqrt(x**2 + y**2 + z**2))


    def getXYRadius(self):
        x = self.location[0]
        y = self.location[1]
        return (sqrt(x**2 + y**2))


    def getFieldMagnitude(self):
        x = self.bField[0]
        y = self.bField[1]
        z = self.bField[2]
        return (sqrt(x**2 + y**2 + z**2))


    def getFieldDirection(self):
        x = self.bField[0]
        y = self.bField[1]
        z = self.bField[2]

        mag = sqrt(x**2 + y**2 + z**2)
        return [(x/mag), (y/mag), (z/mag)]


    def checkIfInside(self, object):
        if (object.shape == 'sphere'):
            x = self.getX()
            y = self.getY()
            z = self.getZ()
            newOrg = [object.totalXShift, object.totalYShift, object.totalZShift]
            #need to get obsPoint radius from new newOrigin
            sphereCenterToObs = sqrt((x - newOrg[0])**2 + (y - newOrg[1])**2 + (z - newOrg[2])**2)

            meetsXYZCriteria = False

            if (sphereCenterToObs > object.innerRadius - EXTRA_SPACE) and (sphereCenterToObs < (object.outerRadius + EXTRA_SPACE)):
                meetsXYCriteria = True

            if meetsXYZCriteria:
                self.isInside = True

        if (object.shape == 'cylinder'):
            x = self.getX()
            y = self.getY()
            z = self.getZ()
            newOrg = [object.totalXShift, object.totalYShift]
            #need to get obsPoint radius from new newOrigin
            cylCenterToObs = sqrt((x - newOrg[0])**2 + (y - newOrg[1])**2)

            meetsZCriteria = False
            meetsXYCriteria = False

            if (cylCenterToObs > object.innerRho - EXTRA_SPACE) and (cylCenterToObs < (object.outerRho + EXTRA_SPACE)):
                meetsXYCriteria = True

            if (z > -object.height/2 + object.totalZShift - EXTRA_SPACE) and (z < object.height/2 + object.totalZShift + EXTRA_SPACE):
                meetsZCriteria = True


            if (meetsZCriteria and meetsXYCriteria):
                self.isInside = True

            return self.isInside

    def checkIfInsideWhole(self, wholeShape):
        distances = []
        passingDists = [10000]
        if wholeShape.isExtruded == True:
            for i, dipole in enumerate(wholeShape.dipoles):
                distance = sqrt((self.location[0] - dipole.loc[0]) ** 2
                                 + (self.location[1] - dipole.loc[1]) ** 2
                                 + (self.location[2] - dipole.loc[2]) ** 2)
                distances.append(distance)

                if wholeShape.fillType == 'regular':
                    minDistance = wholeShape.maxDist
                    extraSpaceMultiplier = REGULAR_EXTRA_SPACE_MULTIPLIER
                elif wholeShape.fillType == 'random':
                    minDistance = wholeShape.maxDist
                    extraSpaceMultiplier = RANDOM_EXTRA_SPACE_MULTIPLIER
                else:
                    print('fill name: ', wholeShape.fillType)
                    print('in observationPoint - invalid fill name')
                    quit()


                if distance < extraSpaceMultiplier* (minDistance):
                    passingDists.append(distance)
                    self.isInside = True
                    break
            #print('max shape dist: ', wholeShape.maxDist, ', min distance between obs and dip: ', min(distances), ', min passing dist: ', min(passingDists))

        else:
            x = self.getX()
            y = self.getY()
            z = self.getZ()
            r = self.getXYRadius()
            perimeterDicts = wholeShape.getPerimeters()
            safeShape = True
            for dict in perimeterDicts:
                if dict['name'] == 'cylinder':
                    newOrigin = dict['origin']
                    inner, outer, height = dict['shapeInfo']

                    rObsShifted = sqrt((x - newOrigin[0])**2 + (y - newOrigin[1])**2)
                    zObsShifted = z - newOrigin[2]
                    #check if not inside
                    if (rObsShifted < outer + (wholeShape.maxDist * REGULAR_EXTRA_SPACE_MULTIPLIER)
                      and rObsShifted > inner - (wholeShape.maxDist * REGULAR_EXTRA_SPACE_MULTIPLIER)
                      and zObsShifted > 0 -  (wholeShape.maxDist * REGULAR_EXTRA_SPACE_MULTIPLIER)
                      and zObsShifted < height + (wholeShape.maxDist * REGULAR_EXTRA_SPACE_MULTIPLIER)):
                      safeShape = False
                      break

                else:
                    print("observation_point: didnt write this code yet")
                    quit()


            if safeShape == False:
                self.isInside = True


        return self.isInside
