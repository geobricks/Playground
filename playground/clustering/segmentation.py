# from rsgislib.segmentation import segutils
#
# inputImage = '../Data/naip_newhogansouth_2012_sub.tif'
# clumpsFile = 'naip_newhogansouth_2012_clumps_elim_final.kea'
#
# # Run segmentation
# segutils.runShepherdSegmentation(inputImage, clumpsFile,
#                                  numClusters=60, minPxls=100,
#                                  distThres=100, bands=None,
#                                  sampling=100, kmMaxIter=200)


from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage
import gdal
from gdalconst import *

from skimage.morphology import watershed
from skimage.feature import peak_local_max
from matplotlib import pyplot as plt

from skimage import data
from skimage.feature import corner_harris, corner_subpix, corner_peaks
from skimage.transform import warp, AffineTransform
from skimage.draw import ellipse
import scipy
from skimage.segmentation import random_walker
from skimage.segmentation import felzenszwalb, slic, quickshift
from skimage.segmentation import mark_boundaries




def microstructure(l=256):
    """
    Synthetic binary data: binary microstructure with blobs.

    Parameters
    ----------

    l: int, optional
        linear size of the returned image
    """
    n = 5
    x, y = np.ogrid[0:l, 0:l]
    mask = np.zeros((l, l))
    generator = np.random.RandomState(1)
    points = l * generator.rand(2, n ** 2)
    mask[(points[0]).astype(np.int), (points[1]).astype(np.int)] = 1
    mask = ndimage.gaussian_filter(mask, sigma=l / (4. * n))
    return (mask > mask.mean()).astype(np.float)

def start():
    # Generate noisy synthetic data
    data = microstructure(l=128)
    data += 0.35 * np.random.randn(*data.shape)
    markers = np.zeros(data.shape, dtype=np.uint)
    markers[data < -0.3] = 1
    markers[data > 1.3] = 2

    # Run random walker algorithm
    labels = random_walker(data, markers, beta=10, mode='bf')

    # Plot results
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(8, 3.2))
    ax1.imshow(data, cmap='gray', interpolation='nearest')
    ax1.axis('off')
    ax1.set_title('Noisy data')
    ax2.imshow(markers, cmap='hot', interpolation='nearest')
    ax2.axis('off')
    ax2.set_title('Markers')
    ax3.imshow(labels, cmap='gray', interpolation='nearest')
    ax3.axis('off')
    ax3.set_title('Segmentation')

    fig.subplots_adjust(hspace=0.01, wspace=0.01, top=1, bottom=0, left=0,
                        right=1)
    plt.show()

def modis_ndvi(path):
    ds = gdal.Open(path, GA_ReadOnly )
    data = np.array(ds.GetRasterBand(1).ReadAsArray())
    markers = np.zeros(data.shape, dtype=np.uint)
    markers[data < 2001] = 1
    markers[data > 2000] = 2

    # Run random walker algorithm
    labels = random_walker(data, markers, beta=10, mode='bf')
    # Plot results
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(8, 3.2))
    ax1.imshow(data, cmap='gray', interpolation='nearest')
    ax1.axis('off')
    ax1.set_title('Noisy data')
    ax2.imshow(markers, cmap='hot', interpolation='nearest')
    ax2.axis('off')
    ax2.set_title('Markers')
    ax3.imshow(labels, cmap='gray', interpolation='nearest')
    ax3.axis('off')
    ax3.set_title('Segmentation')

    fig.subplots_adjust(hspace=0.01, wspace=0.01, top=1, bottom=0, left=0,
                        right=1)
    plt.show()

def segmentations(path):
    ds = gdal.Open(path, GA_ReadOnly )
    data = np.array(ds.GetRasterBand(1).ReadAsArray())
    markers = np.zeros(data.shape, dtype=np.uint)
    markers[data < 2001] = 1
    markers[data > 2000] = 2

    # Run random walker algorithm
    labels = random_walker(data, markers, beta=10, mode='bf')
    # Plot results
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(8, 3.2))
    ax1.imshow(data, cmap='gray', interpolation='nearest')
    ax1.axis('off')
    ax1.set_title('Noisy data')
    ax2.imshow(markers, cmap='hot', interpolation='nearest')
    ax2.axis('off')
    ax2.set_title('Markers')
    ax3.imshow(labels, cmap='gray', interpolation='nearest')
    ax3.axis('off')
    ax3.set_title('Segmentation')

    fig.subplots_adjust(hspace=0.01, wspace=0.01, top=1, bottom=0, left=0,
                        right=1)
    plt.show()


def segmentation(path):
    ds = gdal.Open(path, GA_ReadOnly )
    img = np.array(ds.GetRasterBand(1).ReadAsArray())
    segments_fz = felzenszwalb(img, scale=100, sigma=0.5, min_size=50)
    #segments_slic = slic(img, n_segments=250, compactness=10, sigma=1)
    #segments_quick = quickshift(img, kernel_size=3, max_dist=6, ratio=0.5)

    print("Felzenszwalb's number of segments: %d" % len(np.unique(segments_fz)))

    fig, ax = plt.subplots(1, 3)
    fig.set_size_inches(8, 3, forward=True)
    fig.subplots_adjust(0.05, 0.05, 0.95, 0.95, 0.05, 0.05)

    ax[0].imshow(mark_boundaries(img, segments_fz))
    ax[0].set_title("Felzenszwalbs's method")
    # ax[1].imshow(mark_boundaries(img, segments_slic))
    # ax[1].set_title("SLIC")
    # ax[2].imshow(mark_boundaries(img, segments_quick))
    # ax[2].set_title("Quickshift")
    for a in ax:
        a.set_xticks(())
        a.set_yticks(())
    plt.show()


segmentation("/home/vortex/Desktop/LAYERS/MODIS/AB_NDVI_2_4326.geotiff")
