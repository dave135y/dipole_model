from main import *
#print('efgwdfsawef')
#fileMain()

from calculate_program_induced import calculate_program_induced
from calculate_analytical_induced_sphere import calculate_analytical_induced_sphere
from scan_for_file import scan_for_file
from loading_components import loading_cylinder_components
from observationGrid import observationGrid
from observationPoint import observationPoint
from dipoleClass import dipoleClass
from dipoleCylinderClass import dipoleCylinderClass
from dipoleCompositeClass import dipoleCompositeClass
from math import pi, sqrt
from numpy import mean
import pickle
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages


from constants import *
from shape_constants_file_io import *
#comment git

innerGrid = True
outerGrid = True

innerCylBody = loading_cylinder_components(INNER_CYL_BODY_FILE, NEW_CYLS,
                                           RBI1, RBO1, HB1, DENSITY, 'cylinder', 'Blue')

outerCylBody = loading_cylinder_components(OUTER_CYL_BODY_FILE, NEW_CYLS,
                                           RBI2, RBO2, HB2, DENSITY, 'cylinder', 'Blue')


innerCylTop = loading_cylinder_components(INNER_CYL_TOP_FILE, NEW_CYLS,
                                           RTI1, RTO1, HT1, DENSITY, 'cylinder', 'Blue')

innerCylBot = loading_cylinder_components(INNER_CYL_BOTTOM_FILE, NEW_CYLS,
                                           RBMI1, RBMO1, HBM1, DENSITY, 'cylinder', 'Blue')


outerCylTop = loading_cylinder_components(OUTER_CYL_TOP_FILE, NEW_CYLS,
                                           RTI2, RTO2, HT2, DENSITY, 'cylinder', 'Red')

outerCylBot = loading_cylinder_components(OUTER_CYL_BOTTOM_FILE, NEW_CYLS,
                                           RBMI2, RBMO2, HBM2, DENSITY, 'cylinder', 'Red')

outerCylSmallTop = loading_cylinder_components(OUTER_CYL_SMALL_TOP_FILE, NEW_CYLS,
                                           RTI3, RTO3, HT3, DENSITY, 'cylinder', 'Red')

outerCylSmallBot = loading_cylinder_components(OUTER_CYL_SMALL_BOTTOM_FILE, NEW_CYLS,
                                           RBMI3, RBMO3, HBM3, DENSITY, 'cylinder', 'Red')


innerCylBody.magnetize(B_FIELD, SUS1)
innerCylTop.magnetize(B_FIELD, SUS1)
innerCylBot.magnetize(B_FIELD, SUS1)
outerCylBody.magnetize(B_FIELD, SUS2)
outerCylTop.magnetize(B_FIELD, SUS2)
outerCylBot.magnetize(B_FIELD, SUS2)
outerCylSmallTop.magnetize(B_FIELD, SUS2)
outerCylSmallBot.magnetize(B_FIELD, SUS2)

innerCylTop.shift('z', ZSHIFT_TOP1)
innerCylBot.shift('z', ZSHIFT_BOTTOM1)
outerCylBody.shift('z', ZSHIFT_BODY2)
outerCylTop.shift('z', ZSHIFT_TOP2)
outerCylBot.shift('z', ZSHIFT_BOTTOM2)
outerCylSmallTop.shift('z', ZSHIFT_TOP3)
outerCylSmallBot.shift('z', ZSHIFT_BOTTOM3)

list1 = [innerCylBody]
list2 = [outerCylBody]
list3 = [outerCylBody, innerCylBody]
list4 = [innerCylBot, innerCylTop]
list5 = [outerCylBot, outerCylTop]
list6 = [innerCylBot, innerCylTop, outerCylBot, outerCylTop]
list7 = [innerCylBody, innerCylBot, innerCylTop]
list8 = [outerCylBody, outerCylBot, outerCylTop]
list9 = [outerCylBody, innerCylBody,  innerCylBot, outerCylBot, innerCylTop, outerCylTop]
list10 = [innerCylBody, innerCylTop, innerCylBot, outerCylSmallTop, outerCylSmallBot]

lists = [list1, list2, list3, list4, list5, list6, list7, list8, list9, list10]

fnames = ['Diamagnetic open shell',
            'Paramagnetic open shell',
            'Diamagnetic-paramagnetic layered open shells',
            'Diamagnetic endcaps',
            'Paramagnetic endcaps',
            'Diamagnetic-paramagnetic layered endcaps',
            'Diamagnetic closed shell',
            'Paramagnetic closed shell',
            'Diamagnetic-paramagnetic layered closed shells',
            'Diamagnetic closed shell, paramagnetic endcaps']

lists = [list1]
fnames = ['Diamagnetic open shell']


for i, list in enumerate(lists):
    wholeShape = dipoleCompositeClass(*list)

    wholeShape.removeExcess()
    fig = plt.figure()
    plt.title(fnames[i])
    wholeShape.plotComposite()

    innerCylBody.plot2d('xy')
    innerCylBody.plot2d('yz')
    plt.show()

    if outerGrid:
        programGrid = observationGrid(*OBSERVATION_LIST)
        #innerCylBody.removeExcess()
        #fieldMapProgram = calculate_program_induced(programGrid, innerCylBody)
        fieldMapProgram = calculate_program_induced(programGrid, wholeShape)
        #
        fig2, ax = plt.subplots() # note we must use plt.subplots, not plt.subplot
        ax.quiver(fieldMapProgram.getXVals(), fieldMapProgram.getZVals(),
                   fieldMapProgram.getBXVals(), fieldMapProgram.getBZVals(),
                   fieldMapProgram.getMagVals())
        title1 = ('Inner Cyl: r1 = ' +str(round(RBI1, 4))+ ', r2 = ' +str(round(RBO1, 4))+ ', h = ' +str(round(HB1 + HT1 + HBM1, 4))+ ', Chi = ' +str(SUS1))
        title2 = ('Outer Cyl: r1 = ' +str(round(RBI2, 4))+ ', r2 = ' +str(round(RBO2, 4))+ ', h = ' +str(round(HB2 + HT2 + HBM2, 4))+ ', Chi = ' +str(SUS2))
        til =  (title1 + "\n" + title2 + "\n" + fnames[i])
        plt.title(til)
        wholeShape.plot2dOverlay( ax, 'xz', SLICE_FOR_OVERLAY_PLOTTING, CLOSE_TO_SLICE)


    if innerGrid:
        middleFieldGrid = observationGrid(*OBSERVATION_LIST_MID)
        fieldMapMiddle = calculate_program_induced(middleFieldGrid, wholeShape)#, innerCylTop, innerCylBot, outerCylTop, outerCylBot)
        #
        fig3, ax = plt.subplots() # note we must use plt.subplots, not plt.subplot
        ax.quiver(fieldMapMiddle.getXVals(), fieldMapMiddle.getZVals(),
                   fieldMapMiddle.getBXVals(), fieldMapMiddle.getBZVals(),
                   fieldMapMiddle.getMagVals())
        #
        avgMidStrength = mean(fieldMapMiddle.getMagVals())
        title = 'Avg Field in center = ' + str(round(avgMidStrength * 10**4, 6)) + 'G'
        plt.title(title + '\n' + str(fnames[i]))

    def save_multi_image(filename):
       pp = PdfPages(filename)
       fig_nums = plt.get_fignums()
       figs = [plt.figure(n) for n in fig_nums]
       for fig in figs:
          fig.savefig(pp, format='pdf')
       pp.close()

    if SAVE_OUTPUT == True:
        if os.path.isdir(OUTPUT_FOLDER) == False:
            os.makedirs(OUTPUT_FOLDER)
        filename = (OUTPUT_FOLDER + (fnames[i]) + ".pdf")
        #plt.show()

        save_multi_image(filename)
    else:
        plt.show()
    plt.close(fig)
    if outerGrid:
        plt.close(fig2)
    if innerGrid:
        plt.close(fig3)
