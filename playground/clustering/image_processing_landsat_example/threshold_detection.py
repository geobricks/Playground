from PIL import Image, ImageFilter
import scipy
from scipy import ndimage
import numpy
from skimage import filter
import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage
import gdalnumeric
from skimage.io import imread
from skimage.segmentation import quickshift, slic, felzenszwalb
from skimage.filter.rank import entropy
from PIL import Image, ImageEnhance
from osgeo import gdal
from gdalconst import *


basepath = "/home/vortex/Desktop/LAYERS/lorenzo/tiles/2003_02/LE71690612003035SGS00/rgb/"
file = "projected_5.tif"
image = Image.open(basepath + file)

path =  basepath + "contrast_proj5/"

src_dataset = gdal.Open(path + "contrast0.tif")
geotransform = src_dataset.GetGeoTransform()
spatialreference = src_dataset.GetProjection()
ncol = src_dataset.RasterXSize
nrow = src_dataset.RasterYSize
nband = 1






#print "GaussianBlur"
# file = path + 'FIND_EDGES.tif'
# image = image.filter(ImageFilter.GaussianBlur)
# image.save(file)
#
# print "Meadian_files"
#file = path + 'MedianFilter.tif'
# image = image.filter(ImageFilter.MedianFilter)
# image.save(file)

#
# print "SMOOTH"
# file = path + 'SMOOTH.tif'
# image = image.filter(ImageFilter.SMOOTH)
# image.save(file)


# FILTERS
#Brightness and Contrast




# print "Meadian_files"
# file = path + 'MedianFilter.tif'
# image = image.filter(ImageFilter.MedianFilter)
# image.save(file)
#
# print "Meadian_files2"
# image = Image.open(path + 'MedianFilter.tif')
# file = path + 'MedianFilter2.tif'
# image = image.filter(ImageFilter.MedianFilter)
# image.save(file)
#
# print "Meadian_files2"
# image = Image.open(path + 'MedianFilter2.tif')
# file = path + 'MedianFilter3.tif'
# image = image.filter(ImageFilter.MedianFilter)
# image.save(file)

# lastfile = None
# for i in range(14, 15):
#     print "gaussian" + str(i)
#     image = Image.open(path + 'gaussian'+ str(i)+ '.tif')
#     file = path + 'gaussian'+ str(i+1)+ '.tif'
#     image = image.filter(ImageFilter.GaussianBlur)
#     image.save(file)
#     lastfile = file
#
#
#
# # SOBELFILTER
# im = scipy.misc.imread(lastfile)
# im = im.astype('int32')
# #
# dx = ndimage.sobel(im, 0)  # horizontal derivative
# dy = ndimage.sobel(im, 1)  # vertical derivative
# mag = numpy.hypot(dx, dy)  # magnitude
# mag *= 255.0 / numpy.max(mag)  # normalize (Q&D)
# scipy.misc.imsave(path + "sobelfile2_.tif", mag)


lastfile = None
for i in range(0, 3):
    print "contrast" + str(i)
    image = Image.open(path + 'contrast'+ str(i)+ '.tif')
    file = path + 'contrast'+ str(i+1)+ '.tif'
    image = image.convert('L')
    processed_image = ImageEnhance.Contrast(image)
    im = processed_image.enhance(2)
    # bright = ImageEnhance.Brightness(im)
    # im = bright.enhance(1)
    im.save(file, "tiff")
    fmt = 'GTiff'
    driver = gdal.GetDriverByName(fmt)
    dst_dataset_sobel = gdal.Open(file, GA_Update)
    dst_dataset_sobel.SetGeoTransform(geotransform)
    dst_dataset_sobel.SetProjection(spatialreference)
    lastfile = file


# SOBELFILTER
print "SOBEL"
im = scipy.misc.imread(lastfile)
im = im.astype('int32')
#
dx = ndimage.sobel(im, 0)  # horizontal derivative
dy = ndimage.sobel(im, 1)  # vertical derivative
mag = numpy.hypot(dx, dy)  # magnitude
mag *= 255.0 / numpy.max(mag)  # normalize (Q&D)
scipy.misc.imsave(path + "sobelfile32222_.tif", mag)


fmt = 'GTiff'
driver = gdal.GetDriverByName(fmt)
dst_dataset_sobel = gdal.Open(path + "sobelfile32222_.tif", GA_Update)
dst_dataset_sobel.SetGeoTransform(geotransform)
dst_dataset_sobel.SetProjection(spatialreference)


# print "CANNY"
# from osgeo import gdal
# ds = gdal.Open(path + "sobelfile32_.tif")
# im = np.array(ds.GetRasterBand(1).ReadAsArray())
# #im = gdalnumeric.LoadFile(path + "gaussian_filter.tif")
# print "canny"
# print im
#
# #edges = filter.canny(im)
#
# # edges2 = filter.canny(im, sigma=3)
# edges = filter.canny(im, 3.0, 0.1, 0.5)
#
# print edges
#
# print "saving canny"
# scipy.misc.imsave(path + "gaussian_filter_cannys2333.tif", edges)
# # scipy.misc.imsave(path + "gaussian_filter_edges2.tif", edges2)






#lastfile = None
# for i in range(30,30):
#     print "Meadian_files" + str(i)
#     image = Image.open(path + 'MedianFilter'+ str(i)+ '.tif')
#     file = path + 'MedianFilter'+ str(i+1)+ '.tif'
#     image = image.filter(ImageFilter.MedianFilter)
#     image.save(file)
#     lastfile = file


# for i in range(32, 50):
#     print "Meadian_files" + str(i)
#     image = Image.open(path + 'MedianFilter'+ str(i)+ '.tif')
#     file = path + 'MedianFilter'+ str(i+1)+ '.tif'
#     image = image.filter(ImageFilter.MaxFilter)
#     image.save(file)
#     lastfile = file


# for i in range(33,34):
#     print "Meadian_files" + str(i)
#     image = Image.open(path + 'MedianFilter'+ str(i)+ '.tif')
#     file = path + 'MedianFilter'+ str(i+1)+ '.tif'
#     image = image.filter(ImageFilter.MedianFilter)
#     image.save(file)
#     lastfile = file


# im = scipy.misc.imread(lastfile)
# im = im.astype('int32')
# #
# im = ndimage.gaussian_filter(im, 4)
# #
# scipy.misc.imsave(path + "gaussian_filter_test.tif", im)

# im = scipy.misc.imread(file)
# im = im.astype('int32')
#
# im = ndimage.gaussian_filter(im, 4)
#
# scipy.misc.imsave(path + "gaussian_filter.tif", im)






# from osgeo import gdal
# ds = gdal.Open(path + "gaussian_filter.tif")
# im = np.array(ds.GetRasterBand(1).ReadAsArray())
# #im = gdalnumeric.LoadFile(path + "gaussian_filter.tif")
# print "canny"
# print im




# #edges = filter.canny(im)
#
# # edges2 = filter.canny(im, sigma=3)
# edges = filter.canny(im, 3.0, 0.1, 0.5)
#
# print edges
#
# print "saving canny"
# scipy.misc.imsave(path + "gaussian_filter_cannys23.tif", edges)
# # scipy.misc.imsave(path + "gaussian_filter_edges2.tif", edges2)
#
# print "DONE!"

# SOBELFILTER
# dx = ndimage.sobel(im, 0)  # horizontal derivative
# dy = ndimage.sobel(im, 1)  # vertical derivative
# mag = numpy.hypot(dx, dy)  # magnitude
# mag *= 255.0 / numpy.max(mag)  # normalize (Q&D)
# scipy.misc.imsave(path + "sobelfile_SMOOTH.tif", mag)




# print "canny filter"
# # Compute the Canny filter for two values of sigma
# edges1 = filter.canny(im)
# edges2 = filter.canny(im, sigma=3)
#
# # display results
# fig, (ax1, ax2, ax3) = plt.subplots(nrows=1, ncols=3, figsize=(8, 3))
#
# ax1.imshow(im, cmap=plt.cm.jet)
# ax1.axis('off')
# ax1.set_title('noisy image', fontsize=20)
#
# ax2.imshow(edges1, cmap=plt.cm.gray)
# ax2.axis('off')
# ax2.set_title('Canny filter, $\sigma=1$', fontsize=20)
#
# ax3.imshow(edges2, cmap=plt.cm.gray)
# ax3.axis('off')
# ax3.set_title('Canny filter, $\sigma=3$', fontsize=20)
#
# fig.subplots_adjust(wspace=0.02, hspace=0.02, top=0.9,
#                     bottom=0.02, left=0.02, right=0.98)
#
# plt.show()

print "DONE!"

#
#
# print "GaussianBlur"
# image = image.filter(ImageFilter.FIND_EDGES)
# image.save(path + 'FIND_EDGES.tif')
#
# # print "GaussianBlur"
# # image = image.filter(ImageFilter.GaussianBlur)
# # image.save(path + 'projected_5_GaussianBlur.tif')
#
# # print "EDGE_ENHANCE_MORE"
# # image = image.filter(ImageFilter.EDGE_ENHANCE_MORE)
# # image.save(path + 'rgb_true_color.tif')
# #
# # print "EDGE_ENHANCE"
# # image = image.filter(ImageFilter.EDGE_ENHANCE)
# # image.save(path + 'EDGE_ENHANCE.tif')
# #
# # print "DETAIL"
# # image = image.filter(ImageFilter.DETAIL)
# # image.save(path + 'DETAIL.tif')
# #
# # print "RANK"
# # image = image.filter(ImageFilter.RankFilter)
# # image.save(path + 'RANK.tif')
#
#
# # print "SHARPEN"
# # image = Image.open(basepath + 'projected_5.tif')
# # image = image.filter(ImageFilter.SHARPEN)
# # image.save(path + 'SHARPEN.tif')
# #
# # image = Image.open(path + 'SHARPEN.tif')
# # image = image.filter(ImageFilter.SMOOTH_MORE)
# # image.save(path + 'SMOOTH_MORE.tif')



