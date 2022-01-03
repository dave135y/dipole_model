import numpy as np
import matplotlib.pyplot as plt
import time



outerRho = 2
innerRho = 0.5
height = 2
boxWidth = outerRho * 2
boxHeight = 2
spacing = 1/10000**(1/3)
i = int((boxWidth)/spacing) #number of points, rounded to nearest integer
wSpacing  = (boxWidth)/i #Make it so that spacing is divisible by an even number. This makes the grid equidistant from boundaries
wDensity = 1/wSpacing**3
wlocs = np.arange(-boxWidth/2 + wSpacing/2, boxWidth/2, wSpacing)

i = int((boxHeight)/spacing) #number of points, rounded to nearest integer
hSpacing  = (boxHeight)/i
hDensity = 1/hSpacing**3
hlocs = np.arange(hSpacing/2, boxHeight, hSpacing)

llocs = wlocs
start = time.time()
pointList = np.vstack(np.meshgrid(llocs, wlocs, hlocs)).reshape(3,-1).T
# pointList = []
# for i in range(len(wlocs)):
    # for j in range(len(llocs)):
        # for k in range(len(hlocs)):
            # pointList.append([wlocs[i], llocs[j], hlocs[k]])

end = time.time()
print('elapsed time: ', end - start)
#pointList.ravel()
finalPoints = []
for points in pointList:
    radius = np.sqrt(np.dot([points[0], points[1]], [points[0], points[1]]))

    zheight = points[2]
    if (radius > innerRho and radius < outerRho and zheight < height and zheight > 0):
        #print('r = ', radius,' x, y = ', points[0], ', ', points[1])
        finalPoints.append(points)


fig, ax = plt.subplots()
xPlt, yPlt, zPlt = zip(*finalPoints)
ax.scatter(xPlt, yPlt)
plt.show()
