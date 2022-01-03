from calculate_program_induced import calculate_program_induced
from calculate_analytical_induced_sphere import calculate_analytical_induced_sphere
from scan_for_file import scan_for_file
from loading_components import *

from observationGrid import observationGrid
from observationPoint import observationPoint
from dipoleClass import dipoleClass
from dipoleCylinderClass import dipoleCylinderClass
from dipoleRecPrismClass import dipoleRecPrismClass
from dipoleCompositeClass import dipoleCompositeClass
from constants import *
from shape_constants import *

from math import pi, sqrt
from numpy import mean
import pickle
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

#body = loading_recPrism_components(LENGTH, WIDTH, HEIGHT, DENSITY, COLOR[0])
body = loading_recPrism_components('midhatBox.pickle', True, 0.05, 0.05, 0.16, DENSITY, COLOR[0])


body.magnetize(B_FIELD, SUS1)


# outerCylBot.plot('Reds')

fnames = 'midhatBox'


wholeShape = dipoleCompositeClass(body)
wholeShape.removeExcess()
print('1max dist: ', wholeShape.maxDist)
wholeShape.extrudeCylinder(0.02, 0.14, 0.01, 'xy', 0, 0)
wholeShape.plot()
wholeShape.plot2d('xy')


OBSERVATION_LIST = [-0.015, 0.015, 0, 0, 0.015, 0.145, 42, 1, 42] #[xmin, xmax, xDENSITY, ymin, ymax, ydensity (points per cm)]
OBSERVATION_LIST_MID = [-0.004, 0.004, 0, 0, 0.03, 0.06, 40, 1, 40]
#returns points, field data
programGrid = observationGrid(*OBSERVATION_LIST)
print('3max dist: ', wholeShape.maxDist)

fieldMapProgram = calculate_program_induced(programGrid, wholeShape)

fig2, ax = plt.subplots() # note we must use plt.subplots, not plt.subplot
ax.quiver(fieldMapProgram.getXVals(), fieldMapProgram.getZVals(),
           fieldMapProgram.getBXVals(), fieldMapProgram.getBZVals(),
           fieldMapProgram.getMagVals())
title1 = ('Inner Cyl: r1 = ' +str(RBI1)+ ', r2 = ' +str(RBO1)+ ', h = ' +str(HB1 + HT1 + HBM1)+ ', Chi = ' +str(SUS1))
title2 = ('Outer Cyl: r1 = ' +str(RBI2)+ ', r2 = ' +str(RBO2)+ ', h = ' +str(HB2 + HT2 + HBM2)+ ', Chi = ' +str(SUS2))
title3 = (str(DENSITY))
til =  (title3 + title1 + "\n" + title2)
plt.title(til)
wholeShape.plot2dOverlay( ax, 'xz', SLICE_FOR_OVERLAY_PLOTTING, CLOSE_TO_SLICE)
#
#
#
#
middleFieldGrid = observationGrid(*OBSERVATION_LIST_MID)
fieldMapMiddle = calculate_program_induced(middleFieldGrid, wholeShape)#, innerCylTop, innerCylBot, outerCylTop, outerCylBot)
#
fig3, ax = plt.subplots() # note we must use plt.subplots, not plt.subplot
ax.quiver(fieldMapMiddle.getXVals(), fieldMapMiddle.getZVals(),
           fieldMapMiddle.getBXVals(), fieldMapMiddle.getBZVals(),
           fieldMapMiddle.getMagVals())
#
avgMidStrength = mean(fieldMapMiddle.getMagVals())
title = ('Para/Dia Layers: Avg Field in center = ', round(avgMidStrength * 10**4, 6), 'G')
plt.title(title)

def save_multi_image(filename):
   pp = PdfPages(filename)
   fig_nums = plt.get_fignums()
   figs = [plt.figure(n) for n in fig_nums]
   for fig in figs:
      fig.savefig(pp, format='pdf')
   pp.close()
#
filename = ('output_imgs/' + fnames + ".pdf")
save_multi_image(filename)
#plt.close(fig)
#plt.close(fig2)
#plt.close(fig3)

plt.show()
