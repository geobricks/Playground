from pyhull.convex_hull import ConvexHull
from pyhull.voronoi import VoronoiTess
#pts = [[-0.5, -0.5], [-0.5, 0.5], [0.5, -0.5], [0.5, 0.5], [0,0]]
pts = [[44.968046,-94.420307],[44.33328,-89.132008],[33.755787,-116.359998],[33.844843,-116.54911],[44.92057,-93.44786],
[44.240309,-91.493619],
[44.968041,-94.419696],
[44.333304,-89.132027],
[33.755783,-116.360066],
[33.844847,-116.549069],
[44.920474,-93.447851],
[44.240304,-91.493768]]
pts_reversed = []
for pt in pts:
    pts_reversed.append([pt[1], pt[0]])



print pts_reversed
hull = VoronoiTess (pts)
print hull.vertices




