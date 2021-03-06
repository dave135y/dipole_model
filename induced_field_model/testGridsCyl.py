if __name__ == "__main__":
    from filenamer import *
    import multiprocessing as mp
    #print('efgwdfsawef')

    filenamer()

    # for multi
    from numpy import dot, subtract, add, divide, multiply
    from math import sin, cos, sqrt, pi, ceil
    from functools import partial
    from itertools import repeat



    from calculate_program_induced import calculate_program_induced
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
    import time
    from constants import *
    from shape_constants_file_io import *

    innerGrid = False
    outerGrid = False
    fillType = FILL_TYPE
    density = 5000000
    outerRadius = [0.0005, 0.001, 0.00227, 0.005]

    for loopVar in outerRadius:
        loopVarName = ' Outer radius = '
        innerCylBody = loading_cylinder_components(*innerCylBodyParams(density, 
            fillType), NEW_CYLS)

        innerCylTop = loading_cylinder_components(*innerCylTopParams(density,
            fillType), NEW_CYLS)

        innerCylBot = loading_cylinder_components(*innerCylBottomParams(density,
            fillType), NEW_CYLS)

        outerCylBody = loading_cylinder_components(*outerCylBodyParams(density,
            fillType, loopVar), NEW_CYLS)

        outerCylTop = loading_cylinder_components(*outerCylTopParams(density,
            fillType, loopVar), NEW_CYLS)

        outerCylBot = loading_cylinder_components(*outerCylBottomParams(density,
            fillType, loopVar), NEW_CYLS)


        innerCylBody.magnetize(B_FIELD, SUS1)
        innerCylTop.magnetize(B_FIELD, SUS1)
        innerCylBot.magnetize(B_FIELD, SUS1)
        outerCylBody.magnetize(B_FIELD, SUS2)
        outerCylTop.magnetize(B_FIELD, SUS2)
        outerCylBot.magnetize(B_FIELD, SUS2)



        innerCylTop.shift('z', ZSHIFT_TOP1)
        innerCylBot.shift('z', ZSHIFT_BOTTOM1)
        outerCylBody.shift('z', ZSHIFT_BODY2)
        outerCylTop.shift('z', ZSHIFT_TOP2)
        outerCylBot.shift('z', ZSHIFT_BOTTOM2)

        list1 = [innerCylBody]

        list2 = [outerCylBody, innerCylBody]

        list3 = [innerCylBot, innerCylTop, outerCylBot, outerCylTop]

        list4 = [innerCylBot, innerCylTop, outerCylBot, outerCylTop, 
                outerCylBody, innerCylBody]

        lists = [list4]#, list2, list3]

        fnames = ['Layered dia-para shells']
            #['Diamagnetic open shell',
                    #'Diamagnetic-paramagnetic layered open shells',
                    #'Diamagnetic-paramagnetic layered endcaps']




        fig1, ax = plt.subplots(nrows=2, ncols=2)

        innerCylTop.plot2d('xy', ax[0,0])
        innerCylTop.plot2d('yz', ax[0,1])
        innerCylBody.plot2d('xy', ax[1,0])
        innerCylBody.plot2d('yz', ax[1,1])

        for i, list in enumerate(lists):
            wholeShape = dipoleCompositeClass(*list)
            print("total Dipoles: ", wholeShape.getTotalDipoles())
            print('whole dens: ', wholeShape.actualDensity)

            #wholeShape.removeExcess()
            fig = plt.figure()
            plt.title(fnames[i])
            wholeShape.plotComposite(fig)




            fig11= plt.figure()
            wholeShape.plot2d('yz', fig11)


            if outerGrid:
                programGrid = observationGrid(*OBSERVATION_LIST)
                #innerCylBody.removeExcess()
                #fieldMapProgram = calculate_program_induced(programGrid,
                                                            #innerCylBody)
                start = time.time()
                fieldMapProgram = calculate_program_induced(programGrid, 
                        wholeShape)
                end= time.time()
                print('time to compute field: ', end - start)


                fig2, ax = plt.subplots() # note we must use plt.subplots, 
                ax.quiver(fieldMapProgram.getXVals(), 
                           fieldMapProgram.getZVals(),
                           fieldMapProgram.getBXVals(), 
                           fieldMapProgram.getBZVals(),
                           fieldMapProgram.getMagVals())
                innerHeight = (innerCylBody.height + innerCylTop.height +
                        innerCylBot.height)
                outerHeight = (outerCylBody.height + outerCylTop.height +
                        outerCylBot.height)
                title1 = (('Inner Cyl: r1 = ' 
                    + str(round(innerCylBody.innerRho, 4)) 
                    + ', r2 = ' + str(round(innerCylBody.outerRho, 4))
                    + ', h = '  + str(round(innerHeight, 4)) 
                    + ', Chi = ' + str(SUS1)))
                title2 = (('Outer Cyl: r1 = ' 
                    + str(round(outerCylBody.innerRho, 4))
                    + ', r2 = ' + str(round(outerCylBody.outerRho, 4))
                    + ', h = ' + str(round(outerHeight, 4))
                    + ', Chi = ' + str(SUS2)))
                til =  (title1 + "\n" + title2 + "\n" + fnames[i])
                plt.title(til)
                wholeShape.plot2dOverlay( ax, 'xz', SLICE_FOR_OVERLAY_PLOTTING)


            if innerGrid:

                middleFieldGrid = observationGrid(*OBSERVATION_LIST_MID)
                start = time.time()
                fieldMapMiddle = (calculate_program_induced(middleFieldGrid,
                    wholeShape))#, )
                end= time.time()
                print('time to compute field: ', end - start)

                fig3, ax = plt.subplots() # note we must use plt.subplot*s*
                ax.quiver(fieldMapMiddle.getXVals(), fieldMapMiddle.getZVals(),
                           fieldMapMiddle.getBXVals(), 
                           fieldMapMiddle.getBZVals(),
                           fieldMapMiddle.getMagVals())
                
                avgMidStrength = mean(fieldMapMiddle.getMagVals())
                title = ('Avg Field in center = ' 
                        + str(round(avgMidStrength * 10**4, 6)) + 'G')
                plt.title(title + '\n' + str(fnames[i]) + ' Total dipoles = '
                                + str(wholeShape.getTotalDipoles()) 
                                + loopVarName + str(loopVar))

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
                filename = (OUTPUT_FOLDER + (fnames[i]) 
                        + str(loopVar) + ".pdf")
                save_multi_image(filename)

            else:
                plt.show()
            plt.close(fig)
            plt.close(fig1)
            plt.close(fig11)
            if outerGrid:
                plt.close(fig2)
            if innerGrid:
                plt.close(fig3)
