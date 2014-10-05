from sklearn.naive_bayes import GaussianNB
import numpy as np
from scipy import stats
from sklearn.gaussian_process import GaussianProcess
from matplotlib import pyplot as pl
from matplotlib import cm
from sklearn.datasets import load_iris
from sklearn.cross_validation import cross_val_score
from sklearn.tree import DecisionTreeRegressor
from sklearn.neighbors import KNeighborsClassifier
from sklearn import datasets

# clf = DecisionTreeRegressor(random_state=0)
# iris = load_iris()
# print iris
# a = cross_val_score(clf, iris.data, iris.target, cv=10)
# print "asd"
# print a
#
#
# # IRIS
# print "IRIS"
# iris = datasets.load_iris()
# np.random.seed(0)
# iris_X = iris.data
# iris_y = iris.target
# np.unique(iris_y)
# indices = np.random.permutation(len(iris_X))
# iris_X_train = iris_X[indices[:-10]]
# iris_y_train = iris_y[indices[:-10]]
# iris_X_test  = iris_X[indices[-10:]]
# iris_y_test  = iris_y[indices[-10:]]
#
# print iris_X
# print iris_y
# print iris_X_train
# print iris_y_train
# print iris_X_test
# print iris_y_test
#
# knn = KNeighborsClassifier()
# knn.fit(iris_X_train, iris_y_train)
#
# t = knn.predict(iris_X_test)
# print "PREDICT"
# print t
# print iris_y_test


#http://scikit-learn.org/stable/auto_examples/cluster/plot_color_quantization.html#example-cluster-plot-color-quantization-py
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.metrics import pairwise_distances_argmin
from sklearn.datasets import load_sample_image
from sklearn.utils import shuffle
from time import time


# print "NearestNeighbors!!!"
# from sklearn.neighbors import NearestNeighbors
# import numpy as np
from osgeo import gdal
# src = "/media/vortex/16DE-33641/LORENZO/test_clipped/m1995.tif"
# ds = gdal.Open(src)
# print ds
# myarray = np.array(ds.GetRasterBand(1).ReadAsArray())
# print myarray
#
# # X = np.array([[-1, -1], [-2, -1], [-3, -2], [1, 1], [2, 1], [3, 2]])
# nbrs = NearestNeighbors(n_neighbors=2, algorithm='ball_tree').fit(myarray)
# distances, indices = nbrs.kneighbors(myarray)
# print myarray
# print distances
# print indices
# print nbrs

src = "/media/vortex/16DE-33641/LORENZO/test_clipped/m1995.tif"
ds = gdal.Open(src)
print ds
myarray = np.array(ds.GetRasterBand(1).ReadAsArray())

x, y =  myarray.shape
test = np.random.randint(5, size=(x, y))

#print test
import numpy as np
from scipy import ndimage
input = np.array([[0, 0, 0, 0, 0, 0, 0],
                  [0, 1, 100, 1, 1, 1, 0],
                  [0, 1, 0, 0, 0, 1, 0],
                  [0, 1, 77, 0, 0, 1, 0],
                  [0, 1, 0, 0, 0, 1, 0],
                  [0, 100, 1, 1, 100, 1, 0],
                  [0, 89, 0, 100, 0, 0, 100]], np.uint8)
markers = np.array([[1, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 2, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 3, 0],
                    [0, 0, 0, 0, 0, 0, 3]], np.int8)


#print ndimage.watershed_ift(input, markers)

print ndimage.watershed_ift(myarray, test)