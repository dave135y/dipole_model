import numpy as np
chi_1 = 0.000022 #aluminum sus
chi_2 = -0.000005 #plastic sus
a = 1 #both radii
zList = np.arange(0, 10, 1)
B_applied = 1.47
L_2 = 1 #plastic height = 1
z_2 = +L_2/2 #plastic is shifted down



L_1_List = np.arange(0, 10 * L_2, 0.01) #thickness of aluminum

plotList = []
for z  in zList:
    B_2 = -chi_2 * B_applied/2 * ( (z - (z_2 + L_2/2))/np.sqrt(a**2 + (z - (z_2 + L_2/2)) ** 2)
                           -   (z + (z_2 + L_2/2))/np.sqrt(a**2 + (z + (z_2 + L_2/2)) ** 2) )
    bList =[]
    for L_1 in L_1_List:

        z_1 = -L_1/2 #aluminum shift

        B_1 = -chi_1 * B_applied/2 * ( (z - (z_1 + L_1/2))/np.sqrt(a**2 + (z - (z_1 + L_1/2)) ** 2)
                               -   (z + (z_1 + L_1/2))/np.sqrt(a**2 + (z + (z_1 + L_1/2)) ** 2) )

        bList.append(B_1+B_2)
    plotList.append(bList)

import matplotlib.pyplot as plt
x = L_1_List
y = plotList
plt.xlabel("aluminum thickness")
plt.ylabel("B-field")
plt.title("B vs aluminum thickness")
for i in range(len(plotList)):
    plt.plot(x,plotList[i],label = 'z = %s'%zList[i])
plt.vlines( 0.227, 0, np.max(plotList[1]), label = 'susceptibility ratio')
plt.vlines( L_2, 0, np.max(plotList[1]), label = 'plastic thickness')


plt.legend()
plt.show()
