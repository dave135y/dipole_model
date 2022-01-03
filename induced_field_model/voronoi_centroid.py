from scipy.spatial import Voronoi
import scipy as sp
from numpy import mean

def voronoi_centroid(points):
    vor = Voronoi(points = points)
    centroids = []

    for ii in range(len(points)):
        centroid = mean(vor.vertices[vor.regions[vor.point_region[ii]]], axis=0)
        centroids.append(centroid)

    return centroids # points = np.stack([np.random.uniform(lx, ux, n_
