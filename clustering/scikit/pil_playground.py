from  PIL import Image, ImageEnhance, ImageFilter
import gdal
from gdalconst import *

import numpy
import scipy
from scipy import ndimage
from skimage import filter
import gdalnumeric
from skimage.filter import canny
from scipy import ndimage
from skimage.filter import sobel
from skimage.morphology import watershed
import numpy as np






#src = "/home/vortex/Desktop/LAYERS/lorenzo/tiles/1995/Mosaic/test_clipped/normal.tif"
src = "/home/vortex/Desktop/LAYERS/lorenzo/tiles/1995/Mosaic/test_clipped/m1995.tif"

dst = "/home/vortex/Desktop/LAYERS/lorenzo/tiles/1995/Mosaic/test_clipped/enanched3.tif"
dst_sobel = "/home/vortex/Desktop/LAYERS/lorenzo/tiles/1995/Mosaic/test_clipped/enanched_sobel.tif"
dst_sobel2 = "/home/vortex/Desktop/LAYERS/lorenzo/tiles/1995/Mosaic/test_clipped/enanched_sobel2.tif"
dst_segmentation = "/home/vortex/Desktop/LAYERS/lorenzo/tiles/1995/Mosaic/test_clipped/enanched_sobel_seg.tif"


# image = Image.open(src)
#
#
# im = image.convert('L')
# contr = ImageEnhance.Contrast(im)
# im = contr.enhance(2)
# # bright = ImageEnhance.Brightness(im)
# # im = bright.enhance(1)
# im.save(dst, "tiff")


# sobel2

# SEGMENTATION
image_array = gdalnumeric.LoadFile(src)
for a in image_array:
    print ("a %s") % a
    print ("-----------")
    for b in a:
        print ("%s") % b
    break
markers = np.zeros_like(image_array)
markers[image_array < 90] =1
markers[image_array > 90 ] = 2
markers[image_array > 110] = 3

# print image_array
# print markers

segmentation = watershed(image_array, markers)
print segmentation
gdalnumeric.SaveArray(segmentation, dst_segmentation, format="GTiff")







# sobel
# im = scipy.misc.imread(dst)
# im = im.astype('int32')
# dx = ndimage.sobel(im, 0)  # horizontal derivative
# dy = ndimage.sobel(im, 1)  # vertical derivative
# mag = numpy.hypot(dx, dy)  # magnitude
# mag *= 255.0 / numpy.max(mag)  # normalize (Q&D)
# scipy.misc.imsave(dst_sobel, mag)

# get parameters
src_dataset = gdal.Open(src)
geotransform = src_dataset.GetGeoTransform()
spatialreference = src_dataset.GetProjection()
ncol = src_dataset.RasterXSize
nrow = src_dataset.RasterYSize
nband = 1

# create dataset for output
fmt = 'GTiff'
# driver = gdal.GetDriverByName(fmt)
# dst_dataset = gdal.Open(dst, GA_Update)
# dst_dataset.SetGeoTransform(geotransform)
# dst_dataset.SetProjection(spatialreference)
#
# # create dataset for output
# fmt = 'GTiff'
# driver = gdal.GetDriverByName(fmt)
# dst_dataset_sobel = gdal.Open(dst_sobel, GA_Update)
# dst_dataset_sobel.SetGeoTransform(geotransform)
# dst_dataset_sobel.SetProjection(spatialreference)


fmt = 'GTiff'
driver = gdal.GetDriverByName(fmt)
dst_dataset_sobel = gdal.Open(dst_segmentation, GA_Update)
dst_dataset_sobel.SetGeoTransform(geotransform)
dst_dataset_sobel.SetProjection(spatialreference)




