import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import KDTree
from scipy import spatial
from scipy.spatial import Voronoi, voronoi_plot_2d
from scipy.spatial import Delaunay
import matplotlib.pyplot as plt
from pyhull.voronoi import VoronoiTess

pts = [[51.81828,-3.02827],
[51.67208,-1.27967],
[52.0325,-0.4932],
[51.2085,-1.48122]]

# pts = [[44.968046,-94.420307],[44.33328,-89.132008],[33.755787,-116.359998],[33.844843,-116.54911],[44.92057,-93.44786],
#        [44.240309,-91.493619],
#        [44.968041,-94.419696],
#        [44.333304,-89.132027],
#        [33.755783,-116.360066],
#        [33.844847,-116.549069],
#        [44.920474,-93.447851],
#        [44.240304,-91.493768]]

pts_reversed = []
for pt in pts:
    pts_reversed.append([pt[1], pt[0]])


import scipy

print scipy.__version__

# make up data points
points = np.random.rand(15,2)

# compute Voronoi tesselation
vor = Voronoi(pts)

print vor.vertices

print vor.points
print vor.ridge_points
print vor.regions

print "chart"
print vor.points[:,0], vor.points[:,1]
print vor.vertices[:,0], vor.vertices[:,1]


print "ridge_vertices"
for simplex in vor.ridge_vertices:
    simplex = np.asarray(simplex)
    if np.all(simplex >= 0):
        print vor.vertices[simplex,0], vor.vertices[simplex,1]

ptp_bound = vor.points.ptp(axis=0)

print "ptp_bound %s " % ptp_bound

center = vor.points.mean(axis=0)
print "center %s " % center
for pointidx, simplex in zip(vor.ridge_points, vor.ridge_vertices):
    # print "pointidx %s, simplex %s" % (pointidx, simplex)
    simplex = np.asarray(simplex)
    if np.any(simplex < 0):
        i = simplex[simplex >= 0][0]  # finite end Voronoi vertex

        t = vor.points[pointidx[1]] - vor.points[pointidx[0]]  # tangent
        t /= np.linalg.norm(t)
        n = np.array([-t[1], t[0]])  # normal

        midpoint = vor.points[pointidx].mean(axis=0)
        direction = np.sign(np.dot(midpoint - center, n)) * n
        far_point = vor.vertices[i] + direction * ptp_bound.max()

        print "[%s, %s]," % ([vor.vertices[i,0], far_point[0]], [vor.vertices[i,1], far_point[1]])

ptp_bound = points.ptp(axis=0)
print "x_lim: %s %s" % (points[:,0].min() - 0.1*ptp_bound[0], points[:,0].max() + 0.1*ptp_bound[0])
print "y_lim: %s %s" % (points[:,1].min() - 0.1*ptp_bound[1], points[:,1].max() + 0.1*ptp_bound[1])

voronoi_plot_2d(vor)
plt.show()

#plt.show()


# d = VoronoiTess (pts_reversed)
# print d.vertices
# print d.ridges.items()
#plt.show()

#
# print "---------------------------"
# vertices = d.vertices
# avg = np.average(points, 0)
# for nn, vind in d.ridges.items():
#     (i1, i2) = sorted(vind)
#     # print i1
#     # print i2
#     if i1 == 0:
#         print "-----------------"
#         c1 = np.array(vertices[i2])
#         midpt = 0.5 * (np.array(points[nn[0]]) + np.array(points[nn[1]]))
#         if np.dot(avg - midpt, c1 - midpt)> 0:
#            c2 = c1 + 10 * (midpt-c1)
#         else:
#            c2 = c1 - 10 * (midpt-c1)
#         print "[%s,%s],[%s,%s]" % (c1[0], c2[0], c1[1], c2[1])
#         p1, = plt.plot([c1[0],c2[0]], [c1[1], c2[1]], 'k--')
#     else:
#         # print "////////////"
#         c1 = vertices[i1]
#         c2 = vertices[i2]
#         print ",[%s,%s],[%s,%s]" % (c1[0], c2[0], c1[1], c2[1])
#         p, = plt.plot([c1[0],c2[0]], [c1[1], c2[1]], 'k-')


# vertices = d.vertices
# avg = np.average(points, 0)
# for nn, vind in d.ridges.items():
#     (i1, i2) = sorted(vind)
#     if i1 == 0:
#         c1 = np.array(vertices[i2])
#         midpt = 0.5 * (np.array(points[nn[0]]) + np.array(points[nn[1]]))
#         if np.dot(avg - midpt, c1 - midpt)> 0:
#             c2 = c1 + 10 * (midpt-c1)
#         else:
#             c2 = c1 - 10 * (midpt-c1)
#         p1, = plt.plot([c1[0],c2[0]], [c1[1], c2[1]], 'k--')
#     else:
#         c1 = vertices[i1]
#         c2 = vertices[i2]
#         p, = plt.plot([c1[0],c2[0]], [c1[1], c2[1]], 'k-')
#
#
# plt.show()



