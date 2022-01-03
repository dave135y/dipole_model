

#from constants import DENSITY, SUS1, SUS2
#print("name: ", __name__)

def str2bool(v):
    return v.lower() in ("true",) # you can add to the tuple other values that you consider as true if useful
f =  open('fileioConfig.txt','r')
config = f.read().split('\n')
parentDir = config[0]
date = config[1]
NEW_CYLS = str2bool(config[2])
SAVE_PARTS = str2bool(config[3])
SAVE_OUTPUT = str2bool(config[4])
PARTS_FOLDER_NAME = config[5]
OUTPUT_FOLDER = config[6]
f.close()

BODY_R_PRECISION = 0.0002
BODY_THETA_PRECISION = 0.002
BODY_H_PRECISION = 0.004

CAP_R_PRECISION = 0.001
CAP_THETA_PRECISION = 0.001
CAP_H_PRECISION = 0.0002




FILL_TYPE = 'cyl'

def innerCylBodyParams(density, fillType):
    innerRadius = 0.02
    outerRadius = 0.03
    height = .2
    rPrecision = BODY_R_PRECISION
    thetaPrecision = BODY_THETA_PRECISION
    hPrecision = BODY_H_PRECISION
    color = 'Blue'

    name = 'inner_cyl_body'
    fileString = ('_Precision=' + str(rPrecision) + '-' + str(thetaPrecision) + '-' + str(hPrecision) + '_IR=' + str(innerRadius) + '_OR=' + str(outerRadius) + '_H=' + str(height))
    fileName = PARTS_FOLDER_NAME + name + fileString + '.pickle'

    return(fileName, innerRadius, outerRadius, height, density, rPrecision, thetaPrecision, hPrecision, fillType, color)
ZSHIFT_BODY1 = 0
#NEW_INNER_CYL_TOP = True

def innerCylTopParams(density, fillType):
    innerRadius = 0
    outerRadius = 0.03
    height = 0.01
    rPrecision = CAP_R_PRECISION
    thetaPrecision = CAP_THETA_PRECISION
    hPrecision = CAP_H_PRECISION
    color = 'Blue'

    name = 'inner_cyl_top'
    fileString = ('_Precision=' + str(rPrecision) + '-' + str(thetaPrecision) + '-' + str(hPrecision) + '_IR=' + str(innerRadius) + '_OR=' + str(outerRadius) + '_H=' + str(height))
    fileName = PARTS_FOLDER_NAME + name + fileString + '.pickle'

    return(fileName, innerRadius, outerRadius, height, density, rPrecision, thetaPrecision, hPrecision, fillType, color)
ZSHIFT_TOP1 = 0.2
    #NEW_INNER_CYL_BOTTOM = True

def innerCylBottomParams(density, fillType):
    innerRadius = 0
    outerRadius = 0.03
    height = 0.01
    rPrecision = CAP_R_PRECISION
    thetaPrecision = CAP_THETA_PRECISION
    hPrecision = CAP_H_PRECISION
    color = 'Blue'

    name = 'inner_cyl_bottom'
    fileString = ('_Precision=' + str(rPrecision) + '-' + str(thetaPrecision) + '-' + str(hPrecision) + '_IR=' + str(innerRadius) + '_OR=' + str(outerRadius) + '_H=' + str(height))
    fileName = PARTS_FOLDER_NAME + name + fileString + '.pickle'

    return(fileName, innerRadius, outerRadius, height, density, rPrecision, thetaPrecision, hPrecision, fillType, color)
ZSHIFT_BOTTOM1 = -0.01
    #NEW_OUTER_CYL_BODY = True
def outerCylBodyParams(density, fillType, outer):
    innerRadius = 0.03
    outerRadius = 0.04
    outerRadius = innerRadius + outer
    height = 0.22
    rPrecision = BODY_R_PRECISION
    thetaPrecision = BODY_THETA_PRECISION
    hPrecision = BODY_H_PRECISION
    color = 'Red'

    name = 'outer_cyl_body'
    fileString = ('_Precision=' + str(rPrecision) + '-' + str(thetaPrecision) + '-' + str(hPrecision) + '_IR=' + str(innerRadius) + '_OR=' + str(outerRadius) + '_H=' + str(height))
    fileName = PARTS_FOLDER_NAME + name + fileString + '.pickle'

    return(fileName, innerRadius, outerRadius, height, density, rPrecision, thetaPrecision, hPrecision, fillType, color)
ZSHIFT_BODY2 = -0.01

def outerCylTopParams(density, fillType, outer):
    #NEW_OUTER_CYL_TOP = True
    innerRadius = 0
    outerRadius = 0.04
    reference = 0.03
    outerRadius = reference + outer
    height = outer
    rPrecision = CAP_R_PRECISION
    thetaPrecision = CAP_THETA_PRECISION
    hPrecision = CAP_H_PRECISION
    color = 'Red'

    name = 'outer_cyl_top'
    fileString = ('_Precision=' + str(rPrecision) + '-' + str(thetaPrecision) + '-' + str(hPrecision) + '_IR=' + str(innerRadius) + '_OR=' + str(outerRadius) + '_H=' + str(height))
    fileName = PARTS_FOLDER_NAME + name + fileString + '.pickle'

    return(fileName, innerRadius, outerRadius, height, density, rPrecision, thetaPrecision, hPrecision, fillType, color)
ZSHIFT_TOP2 = 0.21

def outerCylBottomParams(density, fillType, outer):
    #NEW_OUTER_CYL_BOTTOM = True
    innerRadius = 0
    outerRadius = 0.04
    reference = 0.03
    outerRadius = reference + outer
    height = outer
    rPrecision = CAP_R_PRECISION
    thetaPrecision = CAP_THETA_PRECISION
    hPrecision = CAP_H_PRECISION
    color = 'Red'

    name = 'outer_cyl_bottom'
    fileString = ('_Precision=' + str(rPrecision) + '-' + str(thetaPrecision) + '-' + str(hPrecision) + '_IR=' + str(innerRadius) + '_OR=' + str(outerRadius) + '_H=' + str(height))
    fileName = PARTS_FOLDER_NAME + name + fileString + '.pickle'

    return(fileName, innerRadius, outerRadius, height, density, rPrecision, thetaPrecision, hPrecision, fillType, color)
ZSHIFT_BOTTOM2 = -0.02

def shape7(density, fillType):
    #NEW_OUTER_CYL_TOP = True
    innerRadius = 0
    outerRadius = 0.025
    height = 0.01
    rPrecision = CAP_R_PRECISION
    thetaPrecision = CAP_THETA_PRECISION
    hPrecision = CAP_H_PRECISION
    color = 'Blue'

    name = 'outer_cyl_top_matching_inner'
    fileString = ('_Precision=' + str(rPrecision) + '-' + str(thetaPrecision) + '-' + str(hPrecision) + '_IR=' + str(innerRadius) + '_OR=' + str(outerRadius) + '_H=' + str(height))
    fileName = PARTS_FOLDER_NAME + name + fileString + '.pickle'

    return(fileName, innerRadius, outerRadius, height, rPrecision, thetaPrecision, hPrecision, fillType, color)
ZSHIFT_TOP3 = 0.21

def shape8(density, fillType):
    #NEW_OUTER_CYL_BOTTOM = True
    innerRadius = 0
    outerRadius = 0.025
    height = 0.01
    rPrecision = CAP_R_PRECISION
    thetaPrecision = CAP_THETA_PRECISION
    hPrecision = CAP_H_PRECISION
    color = 'Blue'

    name = 'outer_cyl_top_matching_inner'
    fileString = ('_Precision=' + str(rPrecision) + '-' + str(thetaPrecision) + '-' + str(hPrecision) + '_IR=' + str(innerRadius) + '_OR=' + str(outerRadius) + '_H=' + str(height))
    fileName = PARTS_FOLDER_NAME + name + fileString + '.pickle'

    return(fileName, innerRadius, outerRadius, height, density, rPrecision, thetaPrecision, hPrecision, fillType, color)
ZSHIFT_BOTTOM3 = -0.02


#
#
# useConfigFile = True
# if useConfigFile == True:
    # def str2bool(v):
        # return v.lower() in ("true",) # you can add to the tuple other values that you consider as true if useful
    # f =  open('fileioConfig.txt','r')
    # config = f.read().split('\n')
    # parentDir = config[0]
    # date = config[1]
    # NEW_CYLS = str2bool(config[2])
    # SAVE_PARTS = str2bool(config[3])
    # SAVE_OUTPUT = str2bool(config[4])
    # PARTS_FOLDER_NAME = config[5]
    # OUTPUT_FOLDER = config[6]
    # f.close()
#
# else:
    # system = 'Mac'
     #need to addrelevant info to this handle
    # NEW_CYLS = True
    # SAVE_PARTS = True
    # SAVE_OUTPUT = True
    # existingPartFolder = ['11-2', 'cyls_dia_inside_w_para_caps']
#
    # date = '11-10'
    # infoString = 'cyls_10_setups_5e8_density_equal_and_opp_sus'
    # specifierId = 'add main and grid fill'
    # if system == 'Mac':
        # parentDir = '/Users/davidaguillard/Documents/Research/Chupp/Working/mark_II_He3/dipole_cylinder/'
    # elif system == 'Linux':
        # parentDir = '/home/dpaguill/Documents/mark_II/dipole_cylinder/'
    # else:
        # print('invalid system name')
        # quit()
#
    # if NEW_CYLS == True:
        # PARTS_FOLDER_NAME = str(parentDir + 'parts/' + date + '_' + specifierId + infoString + '/')
    # else:
        # PARTS_FOLDER_NAME = str(parentDir + 'parts/' + existingPartFolder[0] + '_' + existingPartFolder[1] + '/')
#
    # OUTPUT_FOLDER =     str(parentDir + 'output_files/' + date + '/' + specifierId + infoString + '/')
