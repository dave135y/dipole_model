#200000000 gets a pretty uniform distribution for cyl fill

DENSITY  = 350000000 #dipoles per m^3 # removed a zero350000000
#DENSITIES = [5000000, 10000000, 50000000, 100000000, 150000000, 200000000, 300000000]
CHANGE_RATIO = True

MINIMUM_SPACING = 0.5 #% from 0-1. evenly spaced dipoles are 100% of their correct distance
B_FIELD = [0, 0, 1.45] #[x, y, z]
SUS1 = -0.000005
SUS2 =  0.000022

TREAT_AS_WHOLE = True

#Grd stuff
ROUND_OBS_POINTS = 3
VIEW = 90
DIMENSIONS = 3
OBSERVATION_LIST = [-8/100, 8/100, 0, 0, -5/100, 26/100, 25, 1, 25] #[xmin, xmax, xDENSITY, ymin, ymax, ydensity (points per cm)]
OBSERVATION_LIST_MID = [-0.005, 0.005, 0, 0, 0.095, 0.105, 25, 1, 25]

#EXTRA_SPACE = 3 * 1/((DENSITY)**(1/3)) # sets distance between observation point and the solid
#EXTRA_SPACE_MULTIPLIER= 1 #When basing distance off maxDist, howmuch to multiply maxDist by


#Plotting
COLOR = ['Green', 'Red', 'Blue', 'Grey', 'Purple', 'Orange']
SLICE_FOR_OVERLAY_PLOTTING = 0 #since looking in xz plane, set y = 0. Can probably get this by averaging allshifts
CLOSE_TO_SLICE = 0.5/100 #how to close to the slice we want to get
AVG_SUS = (SUS1 + SUS2)/2


#counters for grid and sphere updating
UPDATE_PERCENT_GRID = 2
UPDATE_PERCENT_SPHERE = 5
UPDATE_PERCENT_MEASURE_ALL_POINTS = 5
COUNT_EVERY_LOOP = 97

#voroid stuff
VOROID_MOD_NUM = 0.05 #sample every 5% of points List
SAFETY_NET = 3
MAX_VORO_TRIES = 3
LOOK_AT_INIT_RAND_PTS = False
PCT_BIGGER = 0.5 #make shape bigger for voronoi method
PCT_SMALLER = 1  #make shape bigger for voronoi method

#object #1 - sphere
NEW_SPHERE = True
SPHERE_FILE = 'sphere_voroid.pickle'
INNER_RADIUS = 3
OUTER_RADIUS = 4
SUSCEPTIBILITY = 0.0001
ROUND_SPHERE_POINTS = 3
#graphing sphere
